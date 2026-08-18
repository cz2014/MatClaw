"""Tool definitions for the MatClaw."""

from __future__ import annotations

import json
import os
import signal
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from core._smol import Tool, tool

# Pause controller for wait_for_jobflow polling
_pause_controller = None


def set_pause_controller(controller):
    """Set the pause controller for wait_for_jobflow polling."""
    global _pause_controller
    _pause_controller = controller


def _wait_if_paused(context: str) -> None:
    """Honor harness pause state locally or through the kernel tool socket."""
    if _pause_controller is not None:
        _pause_controller.wait_if_paused(context=context)
        return
    socket_path = os.environ.get("MATCLAW_TOOL_SOCKET")
    if not socket_path:
        return
    from core.toolserver import ToolClient

    client = ToolClient(socket_path)
    try:
        while client.call("pause_status").get("paused"):
            time.sleep(0.25)
    except (ConnectionError, OSError, RuntimeError):
        return


class JobflowWaitTimeout(Exception):
    """wait_for_jobflow returned control after timeout_s without a terminal state.

    Not a crash -- a check-in. The agent decides whether to keep waiting or to
    investigate and fix. Carries ``.jobs`` (a structured per-job snapshot of the
    whole flow) and renders to the human-readable diagnostic message (its ``str``
    form) the LLM reads. Built from the object returned by _collect_job_diagnostics.
    """

    def __init__(self, diagnostics):
        self.jobs = diagnostics.jobs
        super().__init__(diagnostics.render())


# --- Shared helpers for I/O and remote transfer tools ---


def _safe_path(workspace: Path, rel_path: str) -> Path:
    """Resolve rel_path under workspace, reject traversal escapes."""
    p = (workspace / rel_path).resolve()
    if p == workspace or workspace in p.parents:
        return p
    raise ValueError(f"Path outside workspace: {rel_path}")


def _confine_to_roots(roots: list[Path], target: str | Path, default: Path) -> Path:
    """Resolve a read-only search target and confine it to one of the allowed roots.

    Used by the grep/glob helpers, whose allowed roots are the workspace plus the
    read-only corpus (the knowledge base). A relative target resolves under the first
    root (the workspace); ``None`` uses ``default``. Anything resolving outside every
    root is rejected -- the agent can still reach arbitrary paths via native
    subprocess/open in the open runtime; this is the safe default, not a wall.
    """
    if target is None:
        p = Path(default).resolve()
    else:
        p = Path(target)
        p = (p if p.is_absolute() else roots[0] / p).resolve()
    for root in roots:
        root = root.resolve()
        if p == root or root in p.parents:
            return p
    raise ValueError(
        f"Path outside the allowed search roots {[str(r) for r in roots]}: {target}"
    )


def _get_ssh_host(project_name: str, worker_name: str):
    """Get connected SSH host from jobflow-remote config."""
    from jobflow_remote.config.manager import ConfigManager

    cm = ConfigManager()
    project = cm.get_project(project_name)
    worker = project.workers[worker_name]
    host = worker.get_host()
    host.connect()
    return host


# --- wait_for_jobflow timeout diagnostics (the gather) ---
#
# When a bounded wait_for_jobflow times out, we hand the agent everything it would
# otherwise spend several steps gathering by hand. The gather PRESENTS raw evidence;
# it does not classify or guess a cause (only the LLM can reliably tell a quiet job
# from a stuck one). It is deliberately code-agnostic: a directory listing sorted by
# mtime (the heartbeat for any engine), the jobflow standard streams, the newest-file
# tails, and the scheduler/resource numbers -- no per-engine filenames, no grep
# pattern list. See docs/exec-plans/active/2026-06-04_bounded-wait-jobflow-stall-recovery.md.


def _job_field(job, key):
    """Read a top-level field from a JobInfo object or a raw Mongo dict.

    get_jobs_info_by_flow_uuid returns raw find() dicts (where the name is nested
    under job['job']['name']) or, in some versions, JobInfo objects (flat .name).
    """
    if isinstance(job, dict):
        if key == "name":
            return job.get("job", {}).get("name", "unknown")
        return job.get(key)
    return getattr(job, key, None)


def _job_process_id(job):
    """The SLURM process id from remote.process_id (dict or object form)."""
    remote = job.get("remote") if isinstance(job, dict) else getattr(job, "remote", None)
    if remote is None:
        return None
    return remote.get("process_id") if isinstance(remote, dict) else getattr(remote, "process_id", None)


def _state_value(state):
    """Extract .value from a JobState enum, or return a string state as-is."""
    return state.value if hasattr(state, "value") else state


def _to_datetime(val):
    """Best-effort parse of a Mongo datetime field to NAIVE UTC.

    jobflow-remote stores naive UTC datetimes (created_on / start_time), so we
    normalize everything to naive UTC for safe arithmetic against _utcnow().
    """
    from datetime import datetime, timezone

    if val is None:
        return None
    if isinstance(val, datetime):
        dt = val
    else:
        try:
            dt = datetime.fromisoformat(str(val).replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return None
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def _utcnow():
    """Naive UTC now (matches jobflow-remote's stored naive datetimes)."""
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(tzinfo=None)


def _fmt_duration(seconds):
    """Render a duration in s as e.g. '2h46m' / '6m12s' / '8s'; '?' if unknown."""
    if seconds is None:
        return "?"
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h{m:02d}m"
    if m:
        return f"{m}m{s:02d}s"
    return f"{s}s"


@dataclass(frozen=True)
class ToolSpec:
    """Picklable inputs for constructing stateless tools inside a kernel."""

    workspace: Path
    search_roots: tuple[Path, ...]
    site_packages: Path
    experience_path: Path | None = None
    web_search_model: str | None = None
    web_search_api_key: str | None = None
    disabled: tuple[str, ...] = ()


def build_stateless_tools(spec: ToolSpec) -> list[Tool]:
    """Build per-kernel tools whose behavior depends only on config/filesystem."""
    tools: list[Tool] = [
        wait_for_jobflow,
        WriteFileTool(spec.workspace),
        ReadFileTool(spec.workspace),
        EditFileTool(spec.workspace),
        ReadPdfTool(spec.workspace),
        GrepTool(list(spec.search_roots), spec.site_packages),
        GlobTool(list(spec.search_roots), spec.workspace),
        FetchHistoryTool(spec.workspace),
        RemotePutTool(spec.workspace),
        RemoteGetTool(spec.workspace),
        RemoteLsTool(),
        QueryJobstoreTool(),
        web_fetch,
        WebSearchTool(model=spec.web_search_model, api_key=spec.web_search_api_key),
    ]
    if spec.experience_path is not None:
        tools.append(WriteExperienceTool(spec.experience_path))
    disabled = set(spec.disabled)
    return [tool_instance for tool_instance in tools if tool_instance.name not in disabled]


# Fixed, job-agnostic next-steps menu shown on every timeout (S7.3). Deliberately
# generic: a job-specific worker/resources suggestion is guesswork the harness
# cannot get right across tasks and engines -- the agent decides from the evidence.
_NEXT_STEPS = (
    "Next steps:\n"
    "  1. keep waiting -- call wait_for_jobflow(...) again for the still-running job(s)\n"
    "  2. fix         -- use the jf command to cancel the job, then resubmit it\n"
    "                    (adjust the worker or resources as needed)"
)


def _remote_probe_script(probes: list[dict]) -> str:
    """Build ONE batched shell script for a worker host (Sources B+C).

    `probes` is a list of {db_id, run_dir, slurm_id}. Per probe it emits, fenced by
    `===JOB <db_id> <SECTION>===` markers so the combined stdout parses back per job:
      - LS      : `ls -la --time-style=long-iso` (mtime-sorted heartbeat + inventory)
      - STREAMS : tail of the jobflow standard streams (std_err/std_out/queue.err/.out)
      - NEWEST  : tail of the one or two most-recently-written files
      - SCHED   : squeue / sacct / sstat for the SLURM id
    Code-agnostic on purpose: no engine filenames, no grep pattern list.
    """
    import shlex

    parts = ["set +e"]
    for p in probes:
        db_id = p["db_id"]
        rd = shlex.quote(str(p["run_dir"]))
        sid = shlex.quote(str(p["slurm_id"]))
        parts.append(f'echo "===JOB {db_id} LS==="')
        parts.append(f"ls -la --time-style=long-iso {rd} 2>&1")
        parts.append(f'echo "===JOB {db_id} STREAMS==="')
        parts.append(
            f"for f in std_err.txt std_out.txt queue.err queue.out; do "
            f'if [ -f {rd}/$f ]; then echo "--- $f ---"; tail -n 15 {rd}/$f; fi; done'
        )
        parts.append(f'echo "===JOB {db_id} NEWEST==="')
        parts.append(
            f"for f in $(ls -t {rd} 2>/dev/null | head -2); do "
            f'echo "--- $f ---"; tail -n 15 {rd}/$f 2>&1; done'
        )
        parts.append(f'echo "===JOB {db_id} SCHED==="')
        parts.append(
            f"squeue -j {sid} 2>&1; "
            f"sacct -j {sid} --format=State,MaxRSS,ExitCode,Elapsed,Timelimit -P 2>&1; "
            f"sstat -j {sid}.* --format=AveCPU,MaxRSS,NTasks -P 2>&1"
        )
        parts.append(f'echo "===JOB {db_id} END==="')
    return "\n".join(parts)


def _parse_probe_output(stdout: str) -> dict:
    """Parse the batched probe stdout into {db_id: {section: text}} by the markers."""
    import re

    out: dict[str, dict] = {}
    cur_id = cur_sec = None
    buf: list[str] = []
    marker = re.compile(r"^===JOB (\S+) (LS|STREAMS|NEWEST|SCHED|END)===$")

    def _flush():
        if cur_id is not None and cur_sec is not None and cur_sec != "END":
            out.setdefault(cur_id, {})[cur_sec] = "\n".join(buf).strip()

    for line in stdout.splitlines():
        m = marker.match(line.strip())
        if m:
            _flush()
            cur_id, cur_sec = m.group(1), m.group(2)
            buf = []
        else:
            buf.append(line)
    _flush()
    return out


class _JobDiagnostics:
    """Structured + rendered snapshot of a flow at wait_for_jobflow timeout.

    `.jobs` is the structured list (one record per job); `.render()` is the
    human-readable message the LLM reads.
    """

    def __init__(self, jobs: list[dict], flow_uuid: str, timeout_s: int, elapsed_s):
        self.jobs = jobs
        self.flow_uuid = flow_uuid
        self.timeout_s = timeout_s
        self.elapsed_s = elapsed_s

    def render(self) -> str:
        active = [j for j in self.jobs if j["category"] in ("RUNNING", "QUEUED")]
        lines = [
            f"JobflowWaitTimeout after {int(self.timeout_s)}s "
            f"({self.timeout_s / 3600:.1f}h). Flow {self.flow_uuid}: "
            f"{len(active)}/{len(self.jobs)} jobs still active.",
            "",
        ]
        for j in self.jobs:
            cat = j["category"]
            if cat == "DONE":
                lines.append(f"[DONE]    {j['name']}  {j['state']}")
                continue
            tag = "[ACTIVE]" if cat in ("RUNNING", "QUEUED") else "[FAILED]"
            head = f"{tag}  {j['name']}  {j['state']}"
            if j.get("slurm_id"):
                head += f"  slurm={j['slurm_id']}"
            head += f"  run={_fmt_duration(j.get('run_time_s'))}  queue={_fmt_duration(j.get('queue_wait_s'))}"
            lines.append(head)
            if j.get("run_dir"):
                lines.append(f"          run_dir = {j['run_dir']}")
            if j.get("remote_error"):
                lines.append(f"          (remote probe unavailable: {j['remote_error']})")
            if j.get("listing"):
                lines.append("          recent files (newest first):")
                lines += [f"            {ln}" for ln in j["listing"].splitlines()]
            if j.get("sched"):
                lines.append("          scheduler / resources (squeue/sacct/sstat):")
                lines += [f"            {ln}" for ln in j["sched"].splitlines()]
            for label, key in (("streams", "streams"), ("newest files", "newest")):
                if j.get(key):
                    lines.append(f"          {label} (tail):")
                    lines += [f"            {ln}" for ln in j[key].splitlines()]
            if j.get("error"):
                lines.append(f"          error = {j['error']}")
        lines += ["", _NEXT_STEPS]
        return "\n".join(lines)


def _collect_job_diagnostics(jc, flow_uuid, project_name, timeout_s=14400, elapsed_s=None):
    """Snapshot every job in the flow for a timed-out wait_for_jobflow.

    Source A (no remote): per-job state/worker/run_dir/slurm-id/timings from the
    JobController DB. Sources B+C (one batched SSH per worker, only for jobs that
    already have a run_dir AND a process_id): a code-agnostic directory listing,
    the jobflow standard-stream tails, the newest-file tails, and the
    squeue/sacct/sstat numbers. The remote half is best-effort (fail-soft): any
    failure attaches remote_error and falls back to Source A. Returns a
    _JobDiagnostics (carry it into JobflowWaitTimeout).
    """
    from jobflow_remote.jobs.state import JobState

    completed = JobState.COMPLETED.value
    terminal_error = {
        JobState.FAILED.value,
        JobState.REMOTE_ERROR.value,
        JobState.STOPPED.value,
        JobState.USER_STOPPED.value,
    }

    raw_jobs = jc.get_jobs_info_by_flow_uuid(flow_uuid)

    # Source A -- classify and time every job from the DB only.
    records: list[dict] = []
    for job in raw_jobs:
        state = _state_value(_job_field(job, "state"))
        if state == completed:
            category = "DONE"
        elif state in terminal_error:
            category = "FAILED"
        elif state == JobState.RUNNING.value:
            category = "RUNNING"
        else:
            category = "QUEUED"  # submitted/uploaded/checked-out: no node yet

        created = _to_datetime(_job_field(job, "created_on"))
        started = _to_datetime(_job_field(job, "start_time"))
        now = _utcnow()
        queue_wait_s = (started - created).total_seconds() if (started and created) else None
        run_time_s = (now - started).total_seconds() if started else None

        records.append({
            "name": _job_field(job, "name"),
            "uuid": _job_field(job, "uuid"),
            "db_id": _job_field(job, "db_id"),
            "worker": _job_field(job, "worker"),
            "state": state,
            "category": category,
            "run_dir": _job_field(job, "run_dir"),
            "slurm_id": _job_process_id(job),
            "queue_wait_s": queue_wait_s,
            "run_time_s": run_time_s,
            "error": _job_field(job, "error"),
        })

    # Sources B+C -- one batched remote probe per worker, only for jobs that have a
    # run_dir AND a slurm id (RUNNING ones; QUEUED jobs have no node yet -> skip).
    by_worker: dict[str, list[dict]] = {}
    rec_by_id: dict[str, dict] = {}
    for rec in records:
        if rec["category"] in ("RUNNING", "QUEUED") and rec["run_dir"] and rec["slurm_id"]:
            by_worker.setdefault(rec["worker"], []).append({
                "db_id": rec["db_id"],
                "run_dir": rec["run_dir"],
                "slurm_id": rec["slurm_id"],
            })
            rec_by_id[str(rec["db_id"])] = rec

    for worker, probes in by_worker.items():
        # Fail-soft: the SSH call AND the parsing. A gather failure must never
        # suppress the JobflowWaitTimeout -- fall back to Source A for these jobs.
        try:
            host = _get_ssh_host(project_name, worker)
            stdout, _stderr, _rc = host.execute(_remote_probe_script(probes))
            parsed = _parse_probe_output(stdout)
            for db_id, sections in parsed.items():
                rec = rec_by_id.get(str(db_id))
                if rec is None:
                    continue
                rec["listing"] = sections.get("LS")
                rec["streams"] = sections.get("STREAMS")
                rec["newest"] = sections.get("NEWEST")
                rec["sched"] = sections.get("SCHED")
        except Exception as e:  # noqa: BLE001 -- best-effort enrichment
            for probe in probes:
                rec = rec_by_id.get(str(probe["db_id"]))
                if rec is not None:
                    rec["remote_error"] = f"{type(e).__name__}: {e}"

    return _JobDiagnostics(records, flow_uuid, timeout_s, elapsed_s)


@tool
def wait_for_jobflow(
    project_name: str,
    job_uuid: str,
    timeout_s: int = 14400,
) -> dict:
    """Bounded check-in on a jobflow's progress; the jobs themselves are never killed.

    Given any job UUID from a flow, this function:
      1. Finds the parent flow containing that job
      2. Polls all jobs in the flow, printing status updates
      3. Returns the output of the specified job when complete
      4. Raises an exception if any job fails

    This follows the same bounded check-in model as wait_command: long SLURM queue
    waits are handled automatically, but if the flow is still not terminal after
    timeout_s, the call returns control by raising JobflowWaitTimeout. The exception
    carries a diagnostic snapshot of every non-terminal job (recent files,
    scheduler/memory numbers, log tails) plus next-step options. Re-call this tool to
    wait again, or use the diagnostics to investigate and act.

    Interaction with the per-step timeout: the code step itself returns control
    after at most 600 s (the `# timeout:` cap) with `running: true` while this call
    keeps waiting inside its kernel. For long HPC waits, run this call in a
    dedicated kernel (e.g. `# kernel: hpc`) and check in from later steps with
    `wait_command("hpc")`; timeout_s only bounds the wait inside that kernel.

    Args:
        project_name: The jobflow-remote project (as configured in ~/.jfremote).
        job_uuid: Any Job UUID from the flow to monitor.
        timeout_s: Seconds this call waits in its kernel before raising the
            diagnostic snapshot (default 14400 = 4h). You rarely need to change it;
            the step's own `# timeout:` returns control to you far earlier.

    Returns:
        The output dict of the specified job.
    """
    from jobflow_remote.jobs.jobcontroller import JobController
    from jobflow_remote.jobs.state import JobState

    POLL_S = 10
    # Use .value for comparison since state can be string or enum
    TERMINAL_ERROR_VALUES = {
        JobState.FAILED.value,
        JobState.REMOTE_ERROR.value,
        JobState.STOPPED.value,
        JobState.USER_STOPPED.value,
    }

    jc = JobController.from_project_name(project_name)

    # Check runner
    runner_info = jc.get_running_runner()
    if runner_info == "NO_DOCUMENT":
        print("  WARNING: No runner detected. Jobs may not progress.", flush=True)

    # Get flow UUID from the given job
    flow_info = jc.get_flow_info_by_job_uuid(job_uuid)
    if flow_info is None:
        raise ValueError(f"Job {job_uuid} not found in any flow")
    # flow_info can be a dict or an object depending on jobflow-remote version
    flow_uuid = flow_info["uuid"] if isinstance(flow_info, dict) else flow_info.uuid
    print(f"  Tracking flow: {flow_uuid}", flush=True)

    # Helper to access job attributes (handles both dict and object)
    def _get(obj, key):
        if isinstance(obj, dict):
            if key == "name":
                # Name is nested under job['job']['name']
                return obj.get("job", {}).get("name", "unknown")
            return obj[key]
        return getattr(obj, key)

    def _state_val(state):
        """Extract .value from enum or return as-is if string."""
        return state.value if hasattr(state, "value") else state

    t0 = time.monotonic()
    last_states = {}  # job_uuid -> last printed state

    while True:
        # Get all jobs in this flow
        jobs = jc.get_jobs_info_by_flow_uuid(flow_uuid)

        elapsed = time.monotonic() - t0

        # Check for failures
        for job in jobs:
            state = _get(job, "state")
            state_val = _state_val(state)
            if state_val in TERMINAL_ERROR_VALUES:

                raise RuntimeError(
                    f"Job '{_get(job, 'name')}' ({_get(job, 'uuid')}) failed: "
                    f"state={state_val}, error={_get(job, 'error') if isinstance(job, dict) else getattr(job, 'error', None)}"
                )

        # Print state changes
        for job in jobs:
            job_uuid_cur = _get(job, "uuid")
            state = _get(job, "state")
            if job_uuid_cur not in last_states or last_states[job_uuid_cur] != state:
                print(f"  [{int(elapsed)}s] {_get(job, 'name')}: {_state_val(state)}", flush=True)
                last_states[job_uuid_cur] = state

        # Check if target job is complete
        target_job = next((j for j in jobs if _get(j, "uuid") == job_uuid), None)
        if target_job:
            target_state = _get(target_job, "state")
            if _state_val(target_state) == JobState.COMPLETED.value:
                all_done = all(
                    _state_val(_get(j, "state")) == JobState.COMPLETED.value
                    for j in jobs
                )
                status = "all jobs COMPLETED" if all_done else "target job COMPLETED"
                print(f"  {status} after {int(elapsed)}s", flush=True)

                return jc.get_job_output(job_id=job_uuid, load=True)

        # Bounded wait: after timeout_s, hand control back to the agent with a
        # diagnostic snapshot of every non-terminal job (no internal backstop --
        # we trust the agent to re-call wait_for_jobflow as it sees fit).
        if elapsed > timeout_s:
            print(f"  Timeout after {int(elapsed)}s; gathering diagnostics.", flush=True)
            raise JobflowWaitTimeout(
                _collect_job_diagnostics(
                    jc, flow_uuid, project_name, timeout_s=timeout_s, elapsed_s=elapsed
                )
            )

        time.sleep(POLL_S)
        _wait_if_paused(
            context=f"During jobflow polling (flow={flow_uuid}, elapsed={int(elapsed)}s)"
        )


# --- History fetch tool ---


class FetchHistoryTool(Tool):
    name = "fetch_history"
    description = """Retrieve past conversation history that may have been pruned from context.

Two modes:
- mode="index": Returns step number + summary for steps in [start, end] range.
  Use this to scan what happened (like a table of contents).
  Example: fetch_history(mode="index", start=1, end=20)

- mode="detail": Returns full messages for specific step numbers.
  Use this after index mode to retrieve exact content.
  Example: fetch_history(mode="detail", steps=[3, 15])

Recommended workflow:
1. Call with mode="index" to get summaries of pruned steps
2. Identify which steps have the information you need
3. Call with mode="detail" for those specific steps"""

    inputs = {
        "mode": {
            "type": "string",
            "description": "Either 'index' (step summaries) or 'detail' (full messages)",
        },
        "start": {
            "type": "integer",
            "description": "Start step number for index mode (inclusive)",
            "nullable": True,
        },
        "end": {
            "type": "integer",
            "description": "End step number for index mode (inclusive)",
            "nullable": True,
        },
        "steps": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "List of step numbers for detail mode",
            "nullable": True,
        },
    }
    output_type = "string"

    def __init__(self, workspace: Path):
        super().__init__()
        self._history_path = workspace.resolve() / "history.jsonl"

    def _load_history(self) -> list[dict]:
        if not self._history_path.exists():
            return []
        records = []
        with self._history_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return records

    def forward(
        self,
        mode: str,
        start: int | None = None,
        end: int | None = None,
        steps: list[int] | None = None,
    ) -> str:
        records = self._load_history()
        if not records:
            return "No conversation history found."

        if mode == "index":
            return self._index_mode(records, start, end)
        elif mode == "detail":
            if not steps:
                return "Error: 'steps' parameter required for detail mode."
            return self._detail_mode(records, steps)
        else:
            return f"Error: unknown mode '{mode}'. Use 'index' or 'detail'."

    def _index_mode(self, records: list[dict], start: int | None, end: int | None) -> str:
        assistant_recs = [r for r in records if r.get("role") == "assistant"]

        step_summaries: dict[int, dict] = {}
        for rec in assistant_recs:
            sn = rec.get("step", 0)
            if sn not in step_summaries:
                step_summaries[sn] = rec

        if start is not None:
            step_summaries = {k: v for k, v in step_summaries.items() if k >= start}
        if end is not None:
            step_summaries = {k: v for k, v in step_summaries.items() if k <= end}

        if not step_summaries:
            return f"No steps found in range [{start}, {end}]."

        lines = []
        for sn in sorted(step_summaries.keys()):
            rec = step_summaries[sn]
            phase = rec.get("phase", "")
            summary = rec.get("summary", "(no summary)")
            phase_str = f" [{phase}]" if phase else ""
            lines.append(f"Step {sn}{phase_str}: {summary}")

        return "\n".join(lines)

    def _detail_mode(self, records: list[dict], steps: list[int]) -> str:
        step_set = set(steps)
        grouped: dict[int, list[dict]] = {}
        for rec in records:
            sn = rec.get("step", 0)
            if sn in step_set:
                grouped.setdefault(sn, []).append(rec)

        if not grouped:
            return f"No messages found for steps {steps}."

        self._save_history_images(grouped)

        parts = []
        for sn in sorted(grouped.keys()):
            parts.append(f"=== Step {sn} ===")
            for rec in grouped[sn]:
                role = rec.get("role", "unknown")
                content = rec.get("content", "")
                n_images = len(rec.get("images_b64", []))
                if n_images:
                    content += f"\n[{n_images} image(s) saved to workspace -- visible next step]"
                parts.append(f"[{role}]\n{content}")
            parts.append("")

        return "\n".join(parts)

    def _save_history_images(self, grouped: dict[int, list[dict]]):
        import base64
        import io

        import PIL.Image

        img_dir = self._history_path.parent / "_history_images"
        if img_dir.exists():
            for f in img_dir.glob("*.png"):
                f.unlink()
        img_dir.mkdir(exist_ok=True)

        for sn, recs in grouped.items():
            for rec in recs:
                for i, b64 in enumerate(rec.get("images_b64", [])):
                    img = PIL.Image.open(io.BytesIO(base64.b64decode(b64)))
                    img.save(img_dir / f"step{sn}_{i}.png")


# --- Experience log tool ---


class WriteExperienceTool(Tool):
    name = "write_experience"
    description = """Append a new experience note to the persistent experience log.

Use this when you discover an operational lesson that should be remembered
across sessions -- e.g., a constraint, a best practice, or a workaround
that took multiple steps to figure out.

The note is appended to the experience file and will be auto-injected into
future prompts. Do NOT write notes about task-specific details (file paths,
material parameters) -- only universal lessons.

Args:
    summary: One-line description of the lesson (becomes the heading).
    details: Multi-line explanation with context and recommendations."""

    inputs = {
        "summary": {
            "type": "string",
            "description": "One-line summary of the lesson learned",
        },
        "details": {
            "type": "string",
            "description": "Detailed explanation with context and recommendations",
        },
    }
    output_type = "string"

    def __init__(self, experience_path: Path):
        super().__init__()
        self._path = experience_path.resolve()

    def forward(self, summary: str, details: str) -> str:
        import re

        next_id = 1
        if self._path.exists():
            content = self._path.read_text(encoding="utf-8")
            ids = [int(m) for m in re.findall(r"^## (\d+)\.", content, re.MULTILINE)]
            if ids:
                next_id = max(ids) + 1

        entry = f"\n\n## {next_id}. {summary.strip()}\n\n{details.strip()}\n"
        with self._path.open("a", encoding="utf-8") as f:
            f.write(entry)

        return f"Experience note #{next_id} saved: {summary.strip()}"


# --- MongoDB query tool ---


class QueryJobstoreTool(Tool):
    name = "query_jobstore"
    description = (
        "Query jobflow's MongoDB for job/flow status and computation results. "
        "This is a thin wrapper around jobflow_remote's JobController -- "
        "call any read-only method by name with its kwargs. "
        "Use show_source_code=True to see the method signatures. "
        "Key methods: get_jobs_info(flow_ids=[...]), "
        "get_job_doc(job_id=<UUID string>, db_id=<numeric string>) — use db_id (not job_id) when you have the numeric ID from get_jobs_info, "
        "get_job_output(job_id=..., load=True), count_jobs(states=[...])."
    )

    inputs = {
        "project": {
            "type": "string",
            "description": "jobflow-remote project name (e.g., 'perlmutter', 'anvil')",
        },
        "method": {
            "type": "string",
            "description": (
                "JobController method name. Allowed read-only methods: "
                "get_jobs_info, get_jobs_doc, get_job_info, get_job_doc, "
                "get_job_output, get_flows_info, get_flow_info_by_flow_uuid, "
                "get_flow_info_by_job_uuid, get_job_info_by_job_uuid, "
                "count_jobs, count_flows"
            ),
        },
        "kwargs": {
            "type": "object",
            "description": (
                "Keyword arguments passed directly to the JobController method. "
                "See show_source_code=True for method signatures."
            ),
            "nullable": True,
        },
        "show_source_code": {
            "type": "boolean",
            "description": (
                "If True, return the source code of the specified method "
                "(or all whitelisted methods if method='all') instead of "
                "executing a query. Useful for discovering parameters."
            ),
            "nullable": True,
        },
    }
    output_type = "string"

    _ALLOWED_METHODS = frozenset({
        # Job queries
        "get_jobs_info",
        "get_jobs_doc",
        "get_job_info",
        "get_job_doc",
        "get_job_output",
        "get_job_info_by_job_uuid",
        # Flow queries
        "get_flows_info",
        "get_flow_info_by_flow_uuid",
        "get_flow_info_by_job_uuid",
        # Counting
        "count_jobs",
        "count_flows",
    })

    _MAX_RESULT_CHARS = 50_000

    def forward(
        self,
        project: str,
        method: str,
        kwargs: dict | None = None,
        show_source_code: bool | None = None,
    ) -> str:
        if show_source_code:
            import inspect

            from jobflow_remote.jobs.jobcontroller import JobController as JC

            if method == "all":
                lines = []
                for name in sorted(self._ALLOWED_METHODS):
                    fn = getattr(JC, name)
                    sig = inspect.signature(fn)
                    doc = (fn.__doc__ or "").strip().split("\n")[0]
                    lines.append(f"{name}{sig}\n    {doc}")
                return "\n\n".join(lines)
            if method not in self._ALLOWED_METHODS:
                raise ValueError(
                    f"Method {method!r} not allowed. "
                    f"Allowed: {sorted(self._ALLOWED_METHODS)}"
                )
            return inspect.getsource(getattr(JC, method))

        if method not in self._ALLOWED_METHODS:
            raise ValueError(
                f"Method {method!r} not allowed. "
                f"Allowed: {sorted(self._ALLOWED_METHODS)}"
            )

        from jobflow_remote.jobs.jobcontroller import JobController

        jc = JobController.from_project_name(project)
        result = getattr(jc, method)(**(kwargs or {}))
        return self._serialize(result)

    def _serialize(self, result) -> str:
        import json

        if isinstance(result, list):
            items = [
                r.model_dump() if hasattr(r, "model_dump") else r for r in result
            ]
        elif hasattr(result, "model_dump"):
            items = result.model_dump()
        else:
            items = result
        text = json.dumps(items, indent=2, default=str)
        if len(text) > self._MAX_RESULT_CHARS:
            text = (
                text[: self._MAX_RESULT_CHARS]
                + f"\n... [truncated at {self._MAX_RESULT_CHARS} chars]"
            )
        return text


# --- Workspace I/O tools ---


class WriteFileTool(Tool):
    name = "write_file"
    description = """Write text content to a file in the workspace directory (mirrors Claude `Write`).

The path is relative to the workspace root. Parent directories are created
automatically. Existing files are overwritten in full (no append/merge). Paths
that escape the workspace (e.g., '../etc/passwd') are rejected. Maximum content
size is 5 MB per call.

A convenience helper -- native open()/pathlib also work in the open runtime. For
binary output use native open(path, 'wb').

Returns the absolute path of the written file."""

    inputs = {
        "rel_path": {
            "type": "string",
            "description": "File path relative to workspace (e.g., 'output/report.md')",
        },
        "content": {
            "type": "string",
            "description": "Text content to write",
        },
    }
    output_type = "string"

    def __init__(self, workspace: Path):
        super().__init__()
        self._workspace = workspace.resolve()

    def forward(self, rel_path: str, content: str) -> str:
        p = _safe_path(self._workspace, rel_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        if len(content) > 5_000_000:
            raise ValueError("Refusing to write >5MB in one call")
        p.write_text(content, encoding="utf-8")
        return str(p)


class ReadFileTool(Tool):
    name = "read_file"
    description = """Read text from a file in the workspace directory (mirrors Claude `Read`).

The path is relative to the workspace root; escaping paths are rejected.

By default returns the file's RAW text (no line-number prefixes) so the result
composes directly in code, e.g. Structure.from_str(read_file("x.cif")) or
json.loads(read_file("d.json")). Files longer than 2000 lines are truncated with
a notice; use offset/limit to page through the rest.

Pass line_numbers=True for a `cat -n`-style numbered view (handy for planning an
edit_file); in that view, and whenever offset/limit are set, lines longer than
2000 chars are truncated. A convenience helper -- native open()/pathlib also work."""

    inputs = {
        "rel_path": {
            "type": "string",
            "description": "File path relative to workspace (e.g., 'data/input.cif')",
        },
        "offset": {
            "type": "integer",
            "description": "1-based line number to start reading from (default: 1).",
            "nullable": True,
        },
        "limit": {
            "type": "integer",
            "description": "Maximum number of lines to read (default: 2000).",
            "nullable": True,
        },
        "line_numbers": {
            "type": "boolean",
            "description": "Prefix each line with its number (cat -n style). Default False.",
            "nullable": True,
        },
    }
    output_type = "string"

    _DEFAULT_MAX_LINES = 2000
    _MAX_LINE_CHARS = 2000

    def __init__(self, workspace: Path):
        super().__init__()
        self._workspace = workspace.resolve()

    def forward(
        self,
        rel_path: str,
        offset: int | None = None,
        limit: int | None = None,
        line_numbers: bool = False,
    ) -> str:
        p = _safe_path(self._workspace, rel_path)
        if not p.exists():
            raise FileNotFoundError(f"File not found: {rel_path}")
        if p.is_dir():
            raise IsADirectoryError(f"Is a directory, not a file: {rel_path}")
        text = p.read_text(encoding="utf-8")

        lines = text.split("\n")
        if lines and lines[-1] == "":  # drop the trailing element from a final newline
            lines = lines[:-1]
        total = len(lines)

        view_mode = offset is not None or limit is not None or line_numbers
        if not view_mode:
            # Faithful round-trip for the common parse case; only bound very long files.
            if total <= self._DEFAULT_MAX_LINES:
                return text
            body = "\n".join(lines[: self._DEFAULT_MAX_LINES])
            return body + (
                f"\n[truncated: showing lines 1-{self._DEFAULT_MAX_LINES} of {total}; "
                "pass offset/limit to read more]"
            )

        start = max(0, (offset - 1) if offset else 0)
        count = limit if limit is not None else self._DEFAULT_MAX_LINES
        window = lines[start : start + count]
        rendered = []
        for i, ln in enumerate(window):
            if len(ln) > self._MAX_LINE_CHARS:
                ln = ln[: self._MAX_LINE_CHARS] + " ...[line truncated]"
            rendered.append(f"{start + i + 1}\t{ln}" if line_numbers else ln)
        body = "\n".join(rendered)
        end = start + len(window)
        if start > 0 or end < total:
            body += f"\n[showing lines {start + 1}-{end} of {total}; pass offset/limit for the rest]"
        return body


class ReadPdfTool(Tool):
    name = "read_pdf"
    description = """Read text from a PDF file in the workspace directory.

The path is relative to the workspace root (same as read_file).
By default, extracts all pages. Output is truncated to ~80K characters
if the extracted text is very long.
Use the optional pages parameter to target specific sections if needed.

Args:
    rel_path: File path relative to workspace (e.g., 'He2023.pdf').
    pages: Optional page range string, e.g. '1-5', '3', '1,3,5-7'.
        Page numbers are 1-based. If omitted, extracts all pages."""

    inputs = {
        "rel_path": {
            "type": "string",
            "description": "PDF file path relative to workspace (e.g., 'paper.pdf')",
        },
        "pages": {
            "type": "string",
            "description": "Page range, e.g. '1-5', '3', '1,3,5-7'. 1-based.",
            "nullable": True,
        },
    }
    output_type = "string"

    _MAX_CHARS = 80000

    def __init__(self, workspace: Path):
        super().__init__()
        self._workspace = workspace.resolve()

    @staticmethod
    def _parse_pages(pages_str: str, total_pages: int) -> list[int]:
        """Parse page range string into sorted list of 0-based page indices."""
        result = set()
        for part in pages_str.split(","):
            part = part.strip()
            if "-" in part:
                start_s, end_s = part.split("-", 1)
                start, end = int(start_s.strip()), int(end_s.strip())
                for i in range(start, end + 1):
                    if 1 <= i <= total_pages:
                        result.add(i - 1)
            else:
                i = int(part)
                if 1 <= i <= total_pages:
                    result.add(i - 1)
        return sorted(result)

    def forward(self, rel_path: str, pages: str | None = None) -> str:
        try:
            import pymupdf
        except ImportError:
            raise ImportError(
                "pymupdf is required for read_pdf. "
                "Install with: pip install pymupdf"
            )

        pdf_path = _safe_path(self._workspace, rel_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF file: {pdf_path}")

        doc = pymupdf.open(str(pdf_path))
        total_pages = len(doc)

        if pages:
            page_indices = self._parse_pages(pages, total_pages)
        else:
            page_indices = list(range(total_pages))

        header = (
            f"[PDF: {pdf_path.name}, {total_pages} pages total, "
            f"extracting pages {', '.join(str(i+1) for i in page_indices)}]"
        )
        parts = [header]
        for idx in page_indices:
            text = doc[idx].get_text()
            parts.append(f"\n--- Page {idx + 1} ---\n{text}")

        doc.close()
        result = "\n".join(parts)

        if len(result) > self._MAX_CHARS:
            result = result[:self._MAX_CHARS] + (
                "\n\n[... truncated, use pages= to read specific sections ...]"
            )
        return result


# --- Basic agent primitives (P4): code-callable helpers mirroring the mainstream
#     agents (Claude Code Read/Write/Edit/Glob/Grep/Bash). These are convenience,
#     token-bounded defaults -- native open()/pathlib/subprocess remain available. ---


class EditFileTool(Tool):
    name = "edit_file"
    description = """Replace an exact string in a workspace file (mirrors Claude `Edit`).

old_string must match the file content exactly (including whitespace) and must be
unique unless replace_all=True; otherwise the edit is rejected so an ambiguous or
absent target never silently mis-edits. old_string and new_string must differ.

Returns a one-line summary of the replacement."""

    inputs = {
        "rel_path": {"type": "string", "description": "File path relative to workspace."},
        "old_string": {"type": "string", "description": "Exact text to find (must be unique unless replace_all)."},
        "new_string": {"type": "string", "description": "Replacement text (must differ from old_string)."},
        "replace_all": {
            "type": "boolean",
            "description": "Replace every occurrence instead of requiring a unique match. Default False.",
            "nullable": True,
        },
    }
    output_type = "string"

    def __init__(self, workspace: Path):
        super().__init__()
        self._workspace = workspace.resolve()

    def forward(self, rel_path: str, old_string: str, new_string: str, replace_all: bool = False) -> str:
        if old_string == new_string:
            raise ValueError("old_string and new_string are identical; nothing to edit.")
        p = _safe_path(self._workspace, rel_path)
        if not p.exists():
            raise FileNotFoundError(f"File not found: {rel_path}")
        text = p.read_text(encoding="utf-8")
        count = text.count(old_string)
        if count == 0:
            raise ValueError(f"old_string not found in {rel_path}.")
        if count > 1 and not replace_all:
            raise ValueError(
                f"old_string is not unique in {rel_path} ({count} occurrences); add surrounding "
                "context to make it unique, or pass replace_all=True."
            )
        new_text = text.replace(old_string, new_string) if replace_all else text.replace(old_string, new_string, 1)
        p.write_text(new_text, encoding="utf-8")
        n = count if replace_all else 1
        return f"Edited {rel_path}: {n} replacement{'s' if n != 1 else ''}."


class GrepTool(Tool):
    name = "grep"
    description = """Search file contents with ripgrep and return a structured result (mirrors Claude `Grep`).

A general content search (not code-only), powered by ripgrep (Rust-regex syntax,
not POSIX). Searches installed package sources (site-packages) by default; pass path= to search elsewhere, such as the doc corpus directories listed in the system prompt.
Scope to a package with path (e.g. ".../pymatgen") or glob/type. output_mode:
  - "files_with_matches" (default): list[str] of matching file paths.
  - "content": {"matches": [{"file","line","text"}], "truncated": bool}.
  - "count": {file: match_count}.
Scope with glob (e.g. "**/*.py") or type (e.g. "py"); -i via case_insensitive;
-C context lines; multiline matching; head_limit caps the number of entries.
Searches all files including .gitignored paths (the package source lives in a gitignored venv)."""

    inputs = {
        "pattern": {"type": "string", "description": "Ripgrep regex to search for."},
        "path": {"type": "string", "description": "Dir/file to search (default: installed package sources under site-packages).", "nullable": True},
        "glob": {"type": "string", "description": "Glob filter, e.g. '**/*.py'.", "nullable": True},
        "type": {"type": "string", "description": "ripgrep file type, e.g. 'py'.", "nullable": True},
        "output_mode": {
            "type": "string",
            "description": "'files_with_matches' (default), 'content', or 'count'.",
            "nullable": True,
        },
        "case_insensitive": {"type": "boolean", "description": "Case-insensitive (-i). Default False.", "nullable": True},
        "context": {"type": "integer", "description": "Context lines around each match (-C). Default 0.", "nullable": True},
        "multiline": {"type": "boolean", "description": "Match across line boundaries. Default False.", "nullable": True},
        "head_limit": {"type": "integer", "description": "Cap the number of entries returned.", "nullable": True},
    }
    output_type = "any"

    def __init__(self, search_roots: list[Path], default_target: Path):
        super().__init__()
        self._roots = [r.resolve() for r in search_roots]
        self._default_target = default_target.resolve()

    def forward(
        self,
        pattern: str,
        path: str | None = None,
        glob: str | None = None,
        type: str | None = None,
        output_mode: str = "files_with_matches",
        case_insensitive: bool = False,
        context: int = 0,
        multiline: bool = False,
        head_limit: int | None = None,
    ):
        rg = shutil.which("rg")
        if not rg:
            raise RuntimeError("ripgrep (rg) is not installed in this environment.")
        if output_mode not in ("files_with_matches", "content", "count"):
            raise ValueError(f"Unknown output_mode={output_mode!r}.")
        target = _confine_to_roots(self._roots, path, self._default_target)

        # --no-ignore: the agent greps the installed package source under site-packages, which lives
        # in a gitignored venv -- without this, ripgrep would skip the entire venv and return nothing.
        cmd = [rg, "--json", "--no-ignore"]
        if case_insensitive:
            cmd.append("-i")
        if multiline:
            cmd += ["-U", "--multiline-dotall"]
        if glob:
            cmd += ["-g", glob]
        if type:
            cmd += ["-t", type]
        if context and output_mode == "content":
            cmd += ["-C", str(int(context))]
        cmd += ["--", pattern, str(target)]

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode not in (0, 1):  # 1 = no matches (not an error); 2 = real error
            raise RuntimeError(f"ripgrep failed: {proc.stderr.strip()}")

        files: list[str] = []
        seen: set[str] = set()
        matches: list[dict] = []
        counts: dict[str, int] = {}
        for line in proc.stdout.splitlines():
            if not line:
                continue
            evt = json.loads(line)
            etype = evt.get("type")
            data = evt.get("data", {})
            if etype == "match":
                fpath = data["path"]["text"]
                if fpath not in seen:
                    seen.add(fpath)
                    files.append(fpath)
                counts[fpath] = counts.get(fpath, 0) + 1
                if output_mode == "content":
                    matches.append({
                        "file": fpath,
                        "line": data.get("line_number"),
                        "text": data["lines"]["text"].rstrip("\n"),
                    })
            elif etype == "context" and output_mode == "content":
                matches.append({
                    "file": data["path"]["text"],
                    "line": data.get("line_number"),
                    "text": data["lines"]["text"].rstrip("\n"),
                })

        if output_mode == "files_with_matches":
            return files[:head_limit] if head_limit else files
        if output_mode == "count":
            return counts
        truncated = bool(head_limit and len(matches) > head_limit)
        return {"matches": matches[:head_limit] if head_limit else matches, "truncated": truncated}


class GlobTool(Tool):
    name = "glob"
    description = """Find files by name pattern (mirrors Claude `Glob`).

Fast file-name match supporting `**` recursion (e.g. 'src/**/*.py'). Returns up to
100 paths, most-recently-modified first; refine the pattern if you need more. Paths
under the workspace are returned workspace-relative (so they compose with read_file);
others are absolute. Does NOT apply .gitignore (unlike grep). Default search path is
the workspace."""

    inputs = {
        "pattern": {"type": "string", "description": "Glob pattern, e.g. '**/*.cif' or 'inputs/*.json'."},
        "path": {"type": "string", "description": "Directory to search in (default: workspace).", "nullable": True},
    }
    output_type = "array"

    _CAP = 100

    def __init__(self, search_roots: list[Path], default_target: Path):
        super().__init__()
        self._roots = [r.resolve() for r in search_roots]
        self._default_target = default_target.resolve()

    def forward(self, pattern: str, path: str | None = None) -> list[str]:
        base = _confine_to_roots(self._roots, path, self._default_target)
        if not base.is_dir():
            raise NotADirectoryError(f"Not a directory: {path or base}")
        hits = [p for p in base.glob(pattern) if p.is_file()]
        hits.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        hits = hits[: self._CAP]
        ws = self._roots[0]
        out = []
        for p in hits:
            out.append(os.path.relpath(p, ws) if (p == ws or ws in p.parents) else str(p))
        return out


# One process-table scan is shared by every vitals sampler tick in this window;
# each owned process would otherwise walk the whole host table five times a second.
_PROCESS_SCAN_TTL_S = 0.15
_process_scan_lock = threading.Lock()
_process_scan: tuple[float, dict[int, list]] = (0.0, {})


def _process_table_by_group(max_age_s: float = 0.0) -> dict[int, list]:
    """Return the host process table grouped by pgid, reusing a recent scan."""
    import psutil

    global _process_scan
    with _process_scan_lock:
        sampled_at, groups = _process_scan
        if groups and time.monotonic() - sampled_at < max_age_s:
            return groups
        groups = {}
        for proc in psutil.process_iter():
            try:
                groups.setdefault(os.getpgid(proc.pid), []).append(proc)
            except (OSError, psutil.Error):
                continue
        _process_scan = (time.monotonic(), groups)
        return groups


def _process_create_time(pid: int) -> float | None:
    """Identity stamp for a PID, used to detect reuse; None when unreadable."""
    import psutil

    try:
        return psutil.Process(pid).create_time()
    except psutil.Error:
        return None


@dataclass
class _LocalProcess:
    proc: subprocess.Popen
    command: str
    log_path: Path
    started_at: float
    stream: Any = field(repr=False)
    max_output_chars: int = 30_000
    background: bool = False
    create_time: float | None = None
    sample_at: float = 0.0
    sample_cpu_time: float = 0.0
    sample_rss: int = 0
    sample_log_size: int = 0
    latest_vitals: dict = field(default_factory=dict, repr=False)
    sample_ready: threading.Event = field(default_factory=threading.Event, repr=False)
    sample_stop: threading.Event = field(default_factory=threading.Event, repr=False)
    sampler: threading.Thread | None = field(default=None, repr=False)


class _LocalExecState:
    """Harness-owned foreground Bash slot and background process registry."""

    def __init__(self, workspace: Path, pause_controller=None, kill_grace_s: float = 5.0):
        self.workspace = workspace.resolve()
        self.pause_controller = pause_controller
        self.kill_grace_s = kill_grace_s
        self.foreground: _LocalProcess | None = None
        self.background: dict[int, _LocalProcess] = {}
        self.completed: dict[int, _LocalProcess] = {}
        self.completed_foreground_pid: int | None = None
        self._completion_notes: list[str] = []
        self._lock = threading.RLock()

    def _log_path(self, prefix: str) -> Path:
        return self.workspace / f".{prefix}_{os.getpid()}_{time.time_ns()}.log"

    @staticmethod
    def _close_stream(record: _LocalProcess) -> None:
        record.sample_stop.set()
        if record.sampler is not None and record.sampler is not threading.current_thread():
            record.sampler.join(timeout=0.2)
        if not record.stream.closed:
            record.stream.close()

    @staticmethod
    def _output(record: _LocalProcess, cap: int | None = None) -> tuple[str, bool]:
        cap = cap or record.max_output_chars
        try:
            size = record.log_path.stat().st_size
        except FileNotFoundError:
            return "", False
        with record.log_path.open("rb") as stream:
            if size <= cap:
                return stream.read().decode("utf-8", errors="replace"), False
            half = max(1, cap // 2)
            head = stream.read(half).decode("utf-8", errors="replace")
            stream.seek(max(0, size - half))
            tail = stream.read(half).decode("utf-8", errors="replace")
        return (
            head
            + f"\n..._This content has been truncated to stay below {cap} characters_...\n"
            + tail,
            True,
        )

    @staticmethod
    def _group_alive(pgid: int) -> bool:
        try:
            os.killpg(pgid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            return True

    @staticmethod
    def _group_processes(pgid: int, max_age_s: float = 0.0):
        return _process_table_by_group(max_age_s).get(pgid, [])

    @staticmethod
    def _same_process(proc, create_time: float | None) -> bool:
        import psutil

        if create_time is None:
            return True
        try:
            return abs(proc.create_time() - create_time) < 1e-6
        except psutil.Error:
            return False

    @classmethod
    def _record_running(cls, record: _LocalProcess) -> bool:
        """Popen owns the direct child; a surviving group must prove its identity.

        A PID/PGID recycled by an unrelated process would otherwise keep the slot
        busy forever and make the kill ladder signal a stranger.
        """
        if record.proc.poll() is None:
            return True
        if not cls._group_alive(record.proc.pid):
            return False
        members = cls._group_processes(record.proc.pid)
        for proc in members:
            if proc.pid == record.proc.pid and not cls._same_process(proc, record.create_time):
                return False
        return bool(members)

    @classmethod
    def _resource_totals(cls, record: _LocalProcess) -> tuple[float, int, int]:
        import psutil

        members = cls._group_processes(record.proc.pid, _PROCESS_SCAN_TTL_S)
        cpu_time = 0.0
        rss = 0
        live = 0
        for proc in members:
            try:
                cpu_time += sum(proc.cpu_times()[:2])
                rss += proc.memory_info().rss
            except psutil.Error:
                continue
            live += 1
        return cpu_time, rss, max(0, live - 1)

    @classmethod
    def _start_sampler(
        cls, record: _LocalProcess, sample_window_s: float = 1.0, tick_s: float = 0.2
    ) -> None:
        import psutil

        def sample() -> None:
            try:
                cpu_time, _, _ = cls._resource_totals(record)
            except (psutil.Error, OSError):
                cpu_time = 0.0
            history = [(time.monotonic(), cpu_time)]
            while not record.sample_stop.wait(tick_s):
                try:
                    cpu_time, rss, child_count = cls._resource_totals(record)
                    now = time.monotonic()
                    history.append((now, cpu_time))
                    cutoff = now - sample_window_s
                    while len(history) > 2 and history[1][0] <= cutoff:
                        history.pop(0)
                    sampled_at, cpu_before = history[0]
                    log_size = record.log_path.stat().st_size if record.log_path.exists() else 0
                    record.latest_vitals = {
                        "pid": record.proc.pid,
                        "elapsed_s": round(max(0.0, now - record.started_at), 3),
                        "cpu_time_s": round(cpu_time, 3),
                        "cpu_over_wall": round(
                            max(0.0, cpu_time - cpu_before) / max(1e-9, now - sampled_at), 3
                        ),
                        "rss_bytes": rss,
                        "children": child_count,
                        "log_bytes": log_size,
                    }
                    record.sample_at = now
                    record.sample_cpu_time = cpu_time
                    record.sample_ready.set()
                    if not cls._record_running(record):
                        return
                except (psutil.Error, OSError):
                    if not cls._record_running(record):
                        return

        record.sampler = threading.Thread(
            target=sample,
            name=f"matclaw-vitals-{record.proc.pid}",
            daemon=True,
        )
        record.sampler.start()

    @classmethod
    def _vitals(cls, record: _LocalProcess) -> dict:
        import psutil

        record.sample_ready.wait(timeout=0.05)
        if record.latest_vitals:
            result = dict(record.latest_vitals)
            result["elapsed_s"] = round(max(0.0, time.monotonic() - record.started_at), 3)
            result["rss_delta"] = result["rss_bytes"] - record.sample_rss
            result["log_growth_bytes"] = result["log_bytes"] - record.sample_log_size
            record.sample_rss = result["rss_bytes"]
            record.sample_log_size = result["log_bytes"]
            return result
        try:
            cpu_time, rss, child_count = cls._resource_totals(record)
            log_size = record.log_path.stat().st_size if record.log_path.exists() else 0
            return {
                "pid": record.proc.pid,
                "elapsed_s": round(max(0.0, time.monotonic() - record.started_at), 3),
                "cpu_time_s": round(cpu_time, 3),
                "cpu_over_wall": 0.0,
                "rss_bytes": rss,
                "rss_delta": rss,
                "children": child_count,
                "log_bytes": log_size,
                "log_growth_bytes": log_size,
            }
        except (psutil.Error, OSError):
            return {
                "pid": record.proc.pid,
                "elapsed_s": round(max(0.0, time.monotonic() - record.started_at), 3),
                "log_bytes": record.log_path.stat().st_size if record.log_path.exists() else 0,
            }

    def _reap(self) -> None:
        if self.foreground is not None and not self._record_running(self.foreground):
            record = self.foreground
            self._close_stream(record)
            self._completion_notes.append(
                f"bash PID {record.proc.pid} completed with returncode {record.proc.returncode}"
            )
            self.completed[record.proc.pid] = record
            self.completed_foreground_pid = record.proc.pid
            self.foreground = None
        for pid, record in list(self.background.items()):
            if not self._record_running(record):
                self._close_stream(record)
                self._completion_notes.append(
                    f"background PID {pid} completed with returncode {record.proc.returncode}"
                )
                self.completed[pid] = record
                del self.background[pid]

    def _take_notes(self) -> list[str]:
        notes, self._completion_notes = self._completion_notes, []
        return notes

    def take_completion_notes(self) -> list[str]:
        """Reap, then drain the pending bash notes so a code step can carry them."""
        with self._lock:
            self._reap()
            return self._take_notes()

    def is_local_target(self, target: str | int) -> bool:
        """True for the bash aliases and for PIDs this state currently knows."""
        if target in ("bash", "foreground", "bash:foreground"):
            return True
        try:
            pid = int(str(target).removeprefix("bash:"))
        except ValueError:
            return False
        with self._lock:
            return (
                (self.foreground is not None and self.foreground.proc.pid == pid)
                or pid in self.background
                or pid in self.completed
            )

    def status_lines(self) -> str:
        with self._lock:
            self._reap()
            if self.foreground is None:
                foreground = "bash: idle"
            else:
                v = self._vitals(self.foreground)
                foreground = (
                    f"bash: busy {_fmt_duration(v['elapsed_s'])}, "
                    f"cpu {v.get('cpu_over_wall', 0) * 100:.0f}%, "
                    f"rss {v.get('rss_bytes', 0) / (1024 ** 2):.1f}M"
                )
            live = [record for record in self.background.values() if self._record_running(record)]
            if live:
                background = "background: " + " | ".join(
                    f"PID {record.proc.pid} {record.command[:40]} "
                    f"(elapsed {_fmt_duration(time.monotonic() - record.started_at)}, "
                    f"cpu {self._vitals(record).get('cpu_over_wall', 0) * 100:.0f}%)"
                    for record in live
                )
            else:
                background = "background: none"
            return foreground + "\n" + background

    def run_bash(
        self,
        command: str,
        timeout: int = 120,
        max_output_chars: int = 30_000,
        cwd: str | None = None,
        run_in_background: bool = False,
    ) -> dict:
        run_cwd = str(self.workspace if cwd is None else Path(cwd))
        timeout = min(int(timeout or 120), 600)
        cap = int(max_output_chars or 30_000)
        with self._lock:
            self._reap()
            notes = self._take_notes()
            if run_in_background:
                log = self._log_path("bash_bg")
                stream = open(log, "wb")
                proc = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=run_cwd,
                    stdout=stream,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
                record = _LocalProcess(
                    proc,
                    command,
                    log,
                    time.monotonic(),
                    stream,
                    cap,
                    background=True,
                    create_time=_process_create_time(proc.pid),
                )
                self._start_sampler(record)
                self.background[proc.pid] = record
                return {
                    "pid": proc.pid,
                    "background": True,
                    "log_file": os.path.relpath(log, self.workspace),
                    "returncode": None,
                    "completion_notes": notes,
                }

            if self.foreground is not None:
                record = self.foreground
                output, truncated = self._output(record, cap)
                return {
                    "running": True,
                    "bash": "foreground",
                    "pid": record.proc.pid,
                    "elapsed": time.monotonic() - record.started_at,
                    "stdout": output,
                    "tail": output[-4000:],
                    "truncated": truncated,
                    "log_file": os.path.relpath(record.log_path, self.workspace),
                    "vitals": self._vitals(record),
                    "refused": True,
                    "completion_notes": notes,
                }

            log = self._log_path("bash_fg")
            stream = open(log, "wb")
            proc = subprocess.Popen(
                command,
                shell=True,
                cwd=run_cwd,
                stdout=stream,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            record = _LocalProcess(
                proc,
                command,
                log,
                time.monotonic(),
                stream,
                cap,
                create_time=_process_create_time(proc.pid),
            )
            self._start_sampler(record)
            self.completed_foreground_pid = None
            self.foreground = record

        if not self._wait_record(record, timeout):
            with self._lock:
                output, truncated = self._output(record, cap)
                return {
                    "running": True,
                    "bash": "foreground",
                    "pid": proc.pid,
                    "elapsed": time.monotonic() - record.started_at,
                    "stdout": output,
                    "tail": output[-4000:],
                    "truncated": truncated,
                    "log_file": os.path.relpath(log, self.workspace),
                    "vitals": self._vitals(record),
                    "completion_notes": notes,
                }

        with self._lock:
            self._close_stream(record)
            output, truncated = self._output(record, cap)
            if self.foreground is record:
                self.foreground = None
            return {
                "stdout": output,
                "returncode": proc.returncode,
                "truncated": truncated,
                "log_file": os.path.relpath(log, self.workspace),
                "completion_notes": notes,
            }

    def _resolve(self, target: str | int) -> _LocalProcess | None:
        self._reap()
        if target in ("bash", "foreground", "bash:foreground"):
            if self.foreground is not None:
                return self.foreground
            if self.completed_foreground_pid is not None:
                return self.completed.get(self.completed_foreground_pid)
            return None
        try:
            pid = int(str(target).removeprefix("bash:"))
        except ValueError:
            return None
        if self.foreground is not None and self.foreground.proc.pid == pid:
            return self.foreground
        return self.background.get(pid) or self.completed.get(pid)

    def _wait_record(self, record: _LocalProcess, timeout: float) -> bool:
        deadline = time.monotonic() + max(0.0, timeout)
        while self._record_running(record):
            if time.monotonic() >= deadline:
                return False
            time.sleep(min(0.05, max(0.0, deadline - time.monotonic())))
        record.proc.poll()
        return True

    def wait_command(self, target: str | int, timeout: int = 60) -> dict:
        # Same per-call cap as kernel execution: a check-in is always bounded.
        timeout = min(max(0, int(timeout or 60)), 600)
        with self._lock:
            record = self._resolve(target)
            notes = self._take_notes()
            if record is None:
                return {"running": False, "target": str(target), "completion_notes": notes}
        if not self._wait_record(record, timeout):
            with self._lock:
                output, truncated = self._output(record)
                return {
                    "running": True,
                    "bash": str(target),
                    "pid": record.proc.pid,
                    "elapsed": time.monotonic() - record.started_at,
                    "stdout": output,
                    "tail": output[-4000:],
                    "truncated": truncated,
                    "log_file": os.path.relpath(record.log_path, self.workspace),
                    "vitals": self._vitals(record),
                    "completion_notes": notes,
                }
        with self._lock:
            self._close_stream(record)
            output, truncated = self._output(record)
            if self.foreground is record:
                self.foreground = None
            self.background.pop(record.proc.pid, None)
            self.completed.pop(record.proc.pid, None)
            if self.completed_foreground_pid == record.proc.pid:
                self.completed_foreground_pid = None
            return {
                "running": False,
                "bash": str(target),
                "pid": record.proc.pid,
                "stdout": output,
                "returncode": record.proc.returncode,
                "truncated": truncated,
                "log_file": os.path.relpath(record.log_path, self.workspace),
                "completion_notes": notes,
            }

    def kill_command(self, target: str | int) -> dict:
        with self._lock:
            record = self._resolve(target)
            notes = self._take_notes()
            if record is None:
                return {
                    "running": False,
                    "target": str(target),
                    "method": "noop",
                    "completion_notes": notes,
                }
            if not self._record_running(record):
                self._close_stream(record)
                output, truncated = self._output(record)
                self.completed.pop(record.proc.pid, None)
                if self.completed_foreground_pid == record.proc.pid:
                    self.completed_foreground_pid = None
                return {
                    "running": False,
                    "bash": str(target),
                    "pid": record.proc.pid,
                    "method": "noop",
                    "stdout": output,
                    "returncode": record.proc.returncode,
                    "truncated": truncated,
                    "log_file": os.path.relpath(record.log_path, self.workspace),
                    "completion_notes": notes,
                }
        method = "term"
        try:
            os.killpg(record.proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        if not self._wait_record(record, self.kill_grace_s):
            method = "kill"
            try:
                os.killpg(record.proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            self._wait_record(record, max(1.0, self.kill_grace_s))
        with self._lock:
            self._close_stream(record)
            output, truncated = self._output(record)
            if self.foreground is record:
                self.foreground = None
            self.background.pop(record.proc.pid, None)
            self.completed.pop(record.proc.pid, None)
            if self.completed_foreground_pid == record.proc.pid:
                self.completed_foreground_pid = None
            return {
                "running": False,
                "bash": str(target),
                "pid": record.proc.pid,
                "method": method,
                "stdout": output,
                "returncode": record.proc.returncode,
                "truncated": truncated,
                "log_file": os.path.relpath(record.log_path, self.workspace),
                "completion_notes": notes,
            }

    def shutdown(self) -> None:
        with self._lock:
            records = ([self.foreground] if self.foreground is not None else []) + list(
                self.background.values()
            )
        for record in records:
            if self._record_running(record):
                self.kill_command(record.proc.pid)
        with self._lock:
            self.foreground = None
            self.background.clear()
            self.completed.clear()
            self.completed_foreground_pid = None


class BashTool(Tool):
    name = "bash"
    description = """Run a shell command and capture its output (mirrors Claude `Bash` / OpenAI `ShellTool`).

The explicit shell escape hatch -- bounded by the container, not by path checks.
stdout and stderr are merged into stdout. Default cwd is the workspace; set cwd
to run elsewhere. timeout defaults to 120s (cap 600s) and returns control without
killing a still-running command. Use wait_command or kill_command to re-enter it.

For long-running HPC compute, submit jobs and use wait_for_jobflow -- not local bash.
run_in_background launches the command detached, streaming output to a workspace log
file, and returns {"pid","background","log_file"} without waiting."""

    inputs = {
        "command": {"type": "string", "description": "The shell command to run."},
        "timeout": {"type": "integer", "description": "Seconds before returning control without killing work (default 120, cap 600).", "nullable": True},
        "max_output_chars": {"type": "integer", "description": "Cap on captured stdout/stderr (default 30000).", "nullable": True},
        "cwd": {"type": "string", "description": "Working directory (default: workspace).", "nullable": True},
        "run_in_background": {"type": "boolean", "description": "Launch detached, stream to a log file. Default False.", "nullable": True},
    }
    output_type = "object"

    _TIMEOUT_CAP = 600
    _DEFAULT_TIMEOUT = 120
    _DEFAULT_MAX_CHARS = 30_000

    def __init__(self, workspace: Path, state: _LocalExecState | None = None):
        super().__init__()
        self._workspace = workspace.resolve()
        self._state = state or _LocalExecState(self._workspace)

    def forward(
        self,
        command: str,
        timeout: int = 120,
        max_output_chars: int = 30_000,
        cwd: str | None = None,
        run_in_background: bool = False,
    ) -> dict:
        return self._state.run_bash(
            command,
            timeout=timeout,
            max_output_chars=max_output_chars,
            cwd=cwd,
            run_in_background=run_in_background,
        )


def _require_bash_target(state: _LocalExecState, target: str | int) -> None:
    """Reject kernel targets: these Tool objects only see the harness bash state."""
    if state.is_local_target(target):
        return
    raise ValueError(
        f"{target!r} is not a bash target: this tool object covers 'bash' and background "
        "PIDs only, and kernel targets are reachable only through the kernel runtime's "
        "RPC stubs."
    )


class WaitCommandTool(Tool):
    name = "wait_command"
    description = """Wait briefly for a running local kernel or Bash target.

This is a bounded check-in, not a second execution. It returns completed output, or
current output and process vitals when the target is still running. Re-call it to
wait again, or use the diagnostics to decide whether to act. Default timeout is 60
seconds, capped at 600."""
    inputs = {
        "target": {"type": "string", "description": "Kernel name, 'bash', or background PID."},
        "timeout": {"type": "integer", "description": "Maximum check-in wait in seconds (default 60, cap 600).", "nullable": True},
    }
    output_type = "object"

    def __init__(self, state: _LocalExecState):
        super().__init__()
        self._state = state

    def forward(self, target: str, timeout: int = 60) -> dict:
        _require_bash_target(self._state, target)
        return self._state.wait_command(target, timeout)


class KillCommandTool(Tool):
    name = "kill_command"
    description = """Stop a running local kernel or Bash target with the harness-owned kill ladder.

Use this after a bounded check-in shows that the work should stop. The ladder is
automatic and reports the method used and, for kernels, whether the namespace
survived; there are no signal or force parameters."""
    inputs = {
        "target": {"type": "string", "description": "Kernel name, 'bash', or background PID."},
    }
    output_type = "object"

    def __init__(self, state: _LocalExecState):
        super().__init__()
        self._state = state

    def forward(self, target: str) -> dict:
        _require_bash_target(self._state, target)
        return self._state.kill_command(target)


# --- Remote transfer tools ---


class RemotePutTool(Tool):
    name = "remote_put"
    description = """Upload a file or directory from workspace to remote HPC via SSH.

Supports both single files and directories. Directories are transferred as
tar archives (packed locally, uploaded, extracted remotely).

For the remote directory, prefer a scratch path such as $SCRATCH/agent_tmp_dir
(avoid /tmp on remote -- it is node-local and periodically cleaned).

Returns the remote path of the uploaded file or directory."""

    inputs = {
        "local_rel_path": {
            "type": "string",
            "description": "Path relative to workspace to upload",
        },
        "remote_dir": {
            "type": "string",
            "description": "Remote directory to upload into (created if needed)",
        },
        "project_name": {
            "type": "string",
            "description": "jobflow-remote project name (e.g., 'perlmutter')",
        },
        "worker_name": {
            "type": "string",
            "description": "jobflow-remote worker name (e.g., 'perlmutter_debug')",
        },
    }
    output_type = "string"

    def __init__(self, workspace: Path):
        super().__init__()
        self._workspace = workspace.resolve()

    def forward(
        self,
        local_rel_path: str,
        remote_dir: str,
        project_name: str,
        worker_name: str,
    ) -> str:
        import tarfile
        import tempfile

        local_abs = _safe_path(self._workspace, local_rel_path)
        if not local_abs.exists():
            raise FileNotFoundError(f"Local path not found: {local_abs}")

        host = _get_ssh_host(project_name, worker_name)
        remote_target = f"{remote_dir}/{local_abs.name}"

        if local_abs.is_file():
            host.mkdir(remote_dir)
            host.put(str(local_abs), remote_target)
        elif local_abs.is_dir():
            with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
                tmp_path = tmp.name
            try:
                with tarfile.open(tmp_path, "w:gz") as tar:
                    tar.add(str(local_abs), arcname=local_abs.name)
                remote_tar = f"{remote_dir}/_agent_upload_{local_abs.name}.tar.gz"
                host.mkdir(remote_dir)
                host.put(tmp_path, remote_tar)
                _, stderr, rc = host.execute(
                    f"tar -xzf {remote_tar} -C {remote_dir} && rm {remote_tar}"
                )
                if rc != 0:
                    raise RuntimeError(f"remote_put tar extraction failed: {stderr}")
            finally:
                Path(tmp_path).unlink(missing_ok=True)
        else:
            raise ValueError(f"Not a file or directory: {local_abs}")

        print(f"[remote_put] {local_abs} -> {remote_target}", flush=True)
        return remote_target


class RemoteGetTool(Tool):
    name = "remote_get"
    description = """Download a file or directory from remote HPC to workspace via SSH.

Supports both single files and directories. Directories are transferred as
tar archives (packed remotely, downloaded, extracted locally).

Use this to retrieve simulation outputs (trajectories, models, logs) from
the HPC cluster for local analysis.

Returns the absolute local path of the downloaded file or directory."""

    inputs = {
        "remote_path": {
            "type": "string",
            "description": "Absolute path on the remote HPC system",
        },
        "local_rel_path": {
            "type": "string",
            "description": "Destination path relative to workspace",
        },
        "project_name": {
            "type": "string",
            "description": "jobflow-remote project name (e.g., 'perlmutter')",
        },
        "worker_name": {
            "type": "string",
            "description": "jobflow-remote worker name (e.g., 'perlmutter_debug')",
        },
    }
    output_type = "string"

    def __init__(self, workspace: Path):
        super().__init__()
        self._workspace = workspace.resolve()

    def forward(
        self,
        remote_path: str,
        local_rel_path: str,
        project_name: str,
        worker_name: str,
    ) -> str:
        import shutil
        import tarfile
        import tempfile

        local_abs = _safe_path(self._workspace, local_rel_path)
        host = _get_ssh_host(project_name, worker_name)

        stdout, stderr, rc = host.execute(
            f"test -d {remote_path} && echo DIR || echo FILE"
        )
        if rc != 0 and "DIR" not in stdout and "FILE" not in stdout:
            raise RuntimeError(f"Cannot stat remote path {remote_path}: {stderr}")
        is_dir = stdout.strip() == "DIR"

        if is_dir:
            remote_name = Path(remote_path).name
            remote_parent = str(Path(remote_path).parent)
            remote_tar = f"{remote_parent}/_agent_download_{remote_name}.tar.gz"
            _, stderr, rc = host.execute(
                f"tar -czf {remote_tar} -C {remote_parent} {remote_name}"
            )
            if rc != 0:
                raise RuntimeError(f"remote_get tar creation failed: {stderr}")
            with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
                tmp_path = tmp.name
            try:
                host.get(remote_tar, tmp_path)
                host.execute(f"rm {remote_tar}")
                local_abs.parent.mkdir(parents=True, exist_ok=True)
                with tarfile.open(tmp_path, "r:gz") as tar:
                    tar.extractall(str(local_abs.parent))
                extracted = local_abs.parent / remote_name
                if extracted != local_abs and extracted.exists():
                    if local_abs.exists():
                        shutil.rmtree(local_abs)
                    extracted.rename(local_abs)
            finally:
                Path(tmp_path).unlink(missing_ok=True)
        else:
            local_abs.parent.mkdir(parents=True, exist_ok=True)
            host.get(remote_path, str(local_abs))

        print(f"[remote_get] {remote_path} -> {local_abs}", flush=True)
        return str(local_abs)


class RemoteLsTool(Tool):
    name = "remote_ls"
    description = """List files in a remote directory on HPC via SSH.

Returns a list of filenames (not full paths) in the specified remote
directory. Useful for discovering job outputs in a job's dir_name after
completion.

Returns an empty list if the directory does not exist."""

    inputs = {
        "remote_path": {
            "type": "string",
            "description": "Absolute path of directory to list on remote HPC",
        },
        "project_name": {
            "type": "string",
            "description": "jobflow-remote project name (e.g., 'perlmutter')",
        },
        "worker_name": {
            "type": "string",
            "description": "jobflow-remote worker name (e.g., 'perlmutter_debug')",
        },
    }
    output_type = "array"

    def forward(
        self,
        remote_path: str,
        project_name: str,
        worker_name: str,
    ) -> list[str]:
        host = _get_ssh_host(project_name, worker_name)
        return host.listdir(remote_path)


# --- Web access tools (web_fetch + web_search) ---
#
# web_fetch mirrors the Anthropic API web_fetch server tool (url in -> raw content out;
# no prompt/sub-model -- the agent reads the content itself). It runs client-side in this
# harness, so it does NOT enforce Anthropic's "URL must be in context" rule: bash already
# has unrestricted container network, so restricting web_fetch URLs would add no real
# protection, and the agent legitimately fetches canonical repo/PyPI URLs it knows.
#
# web_search is provider-native: it reaches Google Search via Gemini "Grounding with
# Google Search", invoked through the litellm MatClaw already uses. The model and key are
# resolved in create_agent (from agent.web_search, falling back to providers.<provider>)
# and passed in -- the tool never reads a hardcoded env-var name.
# See docs/exec-plans/active/2026-06-05_web-access-tools.md.


def _normalize_fetch_url(url: str) -> str:
    """Rewrite the friendly GitHub/PyPI URLs the agent knows into endpoints that return
    real content (GitHub pages are JS-rendered SPAs whose file text a plain GET misses):

      github.com/<o>/<r>/blob/<ref>/<path>  -> raw.githubusercontent.com/<o>/<r>/<ref>/<path>
      github.com/<o>/<r>                    -> api.github.com/repos/<o>/<r>/readme
      pypi.org/project/<name>               -> pypi.org/pypi/<name>/json

    Anything else is returned unchanged.
    """
    import re

    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/blob/(.+)$", url)
    if m:
        return f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/{m.group(3)}"
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/?$", url)
    if m:
        return f"https://api.github.com/repos/{m.group(1)}/{m.group(2)}/readme"
    m = re.match(r"https?://pypi\.org/project/([^/]+)/?$", url)
    if m:
        return f"https://pypi.org/pypi/{m.group(1)}/json"
    return url


@tool
def web_fetch(url: str, max_chars: int = 40000) -> str:
    """Fetch a web page or API endpoint and return its text (HTML rendered to markdown).

    Returns the raw page content for you to read (this agent IS the model -- there is no
    sub-model and no prompt argument). Reliable for env bring-up targets: GitHub (READMEs,
    pyproject/requirements, releases), PyPI (versions + dependencies), Hugging Face, and
    project docs. GitHub blob URLs are auto-rewritten to raw.githubusercontent.com, a bare
    github.com/<org>/<repo> fetches the README, and pypi.org/project/<name> is rewritten to
    the JSON metadata endpoint. JSON and plain text pass through unchanged; HTML is converted
    to markdown. Set GITHUB_TOKEN in the environment to raise the GitHub rate limit. For PDFs,
    download with bash and read with read_pdf.

    Args:
        url: The URL to fetch (https). GitHub/PyPI URLs are normalized automatically.
        max_chars: Truncate the returned text to this many characters (default 40000).

    Returns:
        The page text: markdown for HTML pages, raw text for JSON/plain endpoints.
    """
    import requests
    from markdownify import markdownify

    url = _normalize_fetch_url(url)
    headers = {"User-Agent": "MatClaw/1.0"}
    if "api.github.com" in url:
        headers["Accept"] = "application/vnd.github.raw+json"  # raw README, not base64 JSON
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()  # fail-fast: surface 404/403/rate-limit as the tool's error
    ctype = resp.headers.get("Content-Type", "").lower()
    text = markdownify(resp.text) if "html" in ctype else resp.text
    text = text.strip()
    if len(text) > max_chars:
        text = text[:max_chars] + f"\n\n[truncated at {max_chars} chars]"
    return text


def _extract_grounding_sources(resp, max_results: int = 5) -> list[tuple[str, str]]:
    """Pull (title, url) source pages from a Gemini grounding response.

    Walks the serialized response for groundingChunks ({"web": {"uri","title"}}) -- litellm
    surfaces Gemini's groundingMetadata in version-dependent places, so we search broadly --
    then resolves the expiring vertexaisearch redirect URIs to their real destinations (one
    HTTP request each) so web_fetch works on them directly. De-dups by resolved URL and caps
    to max_results. Best-effort: returns [] if no grounding metadata is present.
    """
    import requests

    blobs = []
    try:
        blobs.append(resp.model_dump())
    except Exception:  # noqa: BLE001 -- best-effort metadata extraction
        pass
    hidden = getattr(resp, "_hidden_params", None)
    if isinstance(hidden, dict):
        blobs.append(hidden)

    raw: list[tuple[str, str]] = []

    def walk(obj):
        if isinstance(obj, dict):
            web = obj.get("web") if isinstance(obj.get("web"), dict) else None
            if web and web.get("uri"):
                raw.append((web.get("title") or web["uri"], web["uri"]))
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    for blob in blobs:
        walk(blob)

    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for title, uri in raw:
        try:
            r = requests.get(
                uri, allow_redirects=True, timeout=10, stream=True,
                headers={"User-Agent": "MatClaw/1.0"},
            )
            final = r.url
            r.close()
        except Exception:  # noqa: BLE001 -- fall back to the redirect URL if resolution fails
            final = uri
        if final in seen:
            continue
        seen.add(final)
        out.append((title, final))
        if len(out) >= max_results:
            break
    return out


class WebSearchTool(Tool):
    name = "web_search"
    description = (
        "Search the web (Google, via Gemini grounding) and return a short grounded summary "
        "with source URLs. Use this for the 'I don't know the URL' case (an install recipe, a "
        "dependency conflict discussed in an issue); if you already know the URL, prefer "
        "web_fetch. Do NOT use web search for correctness-critical facts (DFT settings, energy "
        "corrections) -- read those from the installed library source with grep."
    )

    inputs = {
        "query": {"type": "string", "description": "The search query."},
        "max_results": {
            "type": "integer",
            "description": "Cap on the number of source links returned (default 5).",
            "nullable": True,
        },
    }
    output_type = "string"

    def __init__(self, model: str, api_key: str | None = None):
        super().__init__()
        self._model = model
        self._api_key = api_key  # the RESOLVED key value (not an env-var name); may be None

    def forward(self, query: str, max_results: int = 5) -> str:
        from litellm import completion

        try:
            # One-shot grounding call. Fail-soft: a missing key / network / quota error
            # becomes an agent-readable message, never a crash of the run.
            resp = completion(
                model=self._model,
                api_key=self._api_key,
                messages=[{"role": "user", "content": query}],
                tools=[{"googleSearch": {}}],
            )
        except Exception as e:  # noqa: BLE001 -- report to the agent, do not propagate
            return (
                f"web_search unavailable ({type(e).__name__}: {e}). "
                "Try web_fetch with a known URL."
            )

        answer = (resp.choices[0].message.content or "").strip()
        sources = _extract_grounding_sources(resp, max_results)
        if sources:
            answer += "\n\nSources:\n" + "\n".join(f"- {t}: {u}" for t, u in sources)
        return answer or f"No results for: {query}"
