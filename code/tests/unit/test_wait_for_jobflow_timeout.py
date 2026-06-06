"""Unit tests for the bounded wait_for_jobflow + the timeout diagnostic gather.

Offline -- no LLM, no MongoDB, no cluster. The JobController is mocked, the SSH
host is mocked, and core.tools.time is monkeypatched (a fake clock) so no real
waiting happens. Covers the wait_for_jobflow timeout contract (Group A), the
_collect_job_diagnostics gather (Group B), and the timeout default (Group C).

See docs/exec-plans/active/2026-06-04_bounded-wait-jobflow-stall-recovery.md S8.5.
"""

from __future__ import annotations

import inspect
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from core.tools import (
    JobflowWaitTimeout,
    _collect_job_diagnostics,
    _remote_probe_script,
    wait_for_jobflow,
)

UNIT_TESTS = []


def _unit(fn):
    UNIT_TESTS.append(fn)
    return fn


# --- fixtures -------------------------------------------------------------


def _job(name, uuid, state, db_id="1", worker="anvil_cpu", run_dir=None, pid=None, error=None):
    """A raw Mongo-style job doc (what get_jobs_info_by_flow_uuid returns)."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)  # naive UTC, as jobflow-remote stores
    started = now - timedelta(hours=2.5) if state in ("RUNNING", "COMPLETED") else None
    return {
        "job": {"name": name},
        "uuid": uuid,
        "db_id": db_id,
        "worker": worker,
        "state": state,
        "run_dir": run_dir,
        "remote": {"process_id": pid},
        "created_on": now - timedelta(hours=3),
        "start_time": started,
        "error": error,
    }


def _make_jc(jobs, output=None):
    """A mock JobController whose queries return `jobs`."""
    jc = MagicMock()
    jc.get_running_runner.return_value = "OK"  # not NO_DOCUMENT -> no warning
    jc.get_flow_info_by_job_uuid.return_value = {"uuid": "flow-abc123"}
    jc.get_jobs_info_by_flow_uuid.return_value = jobs
    jc.get_job_output.return_value = output if output is not None else {"output": {"energy": -1.0}}
    return jc


def _fake_clock(step=100_000.0):
    """A monkeypatch for core.tools.time: monotonic increments, sleep is a no-op."""
    state = {"t": 0.0}

    def monotonic():
        t = state["t"]
        state["t"] += step
        return t

    clock = MagicMock()
    clock.monotonic.side_effect = monotonic
    clock.sleep.return_value = None
    return clock


class _FakeHost:
    def __init__(self, stdout=""):
        self._stdout = stdout
        self.scripts = []

    def execute(self, script):
        self.scripts.append(script)
        return (self._stdout, "", 0)


def _run_wait(jc, host=None, **kwargs):
    """Call wait_for_jobflow with the JobController + clock (+ optional host) patched."""
    patches = [
        patch("jobflow_remote.jobs.jobcontroller.JobController.from_project_name", return_value=jc),
        patch("core.tools.time", _fake_clock()),
    ]
    if host is not None:
        patches.append(patch("core.tools._get_ssh_host", return_value=host))
    started = []
    try:
        for p in patches:
            p.start()
            started.append(p)
        return wait_for_jobflow.forward("anvil", "target-uuid", **kwargs)
    finally:
        for p in reversed(started):
            p.stop()


# --- Group A: the wait_for_jobflow timeout contract -----------------------


@_unit
def test_timeout_raises_jobflow_wait_timeout():
    """Target stays RUNNING + tiny timeout -> JobflowWaitTimeout (not RuntimeError, not a dict)."""
    jc = _make_jc([_job("relax", "target-uuid", "RUNNING")])
    try:
        _run_wait(jc, timeout_s=1)
        raise AssertionError("expected JobflowWaitTimeout")
    except JobflowWaitTimeout as e:
        assert "still active" in str(e)


@_unit
def test_completed_returns_output_before_timeout():
    """Target COMPLETED -> returns get_job_output, no raise (today's behaviour preserved)."""
    jc = _make_jc([_job("relax", "target-uuid", "COMPLETED")], output={"output": {"energy": -3.14}})
    result = _run_wait(jc, timeout_s=1)
    assert result == {"output": {"energy": -3.14}}


@_unit
def test_terminal_error_still_raises_runtime():
    """A USER_STOPPED job -> RuntimeError (the validated 2026-06-04 manual-stop path), NOT JobflowWaitTimeout."""
    jc = _make_jc([_job("relax", "target-uuid", "USER_STOPPED")])
    try:
        _run_wait(jc, timeout_s=99999)
        raise AssertionError("expected RuntimeError")
    except JobflowWaitTimeout:
        raise AssertionError("terminal error must raise RuntimeError, not JobflowWaitTimeout")
    except RuntimeError as e:
        assert "USER_STOPPED" in str(e)


@_unit
def test_timeout_s_is_honored():
    """No internal backstop: the call gives up at timeout_s, and a second wait raises too (unbounded re-waits)."""
    jc = _make_jc([_job("relax", "target-uuid", "RUNNING")])
    for _ in range(2):  # consecutive re-waits both raise -> no cap
        try:
            _run_wait(jc, timeout_s=5)
            raise AssertionError("expected JobflowWaitTimeout on each re-wait")
        except JobflowWaitTimeout:
            pass


@_unit
def test_payload_enumerates_done_vs_running():
    """3-job flow (2 COMPLETED, 1 RUNNING) -> structured .jobs marks 2 DONE / 1 RUNNING."""
    jobs = [
        _job("static_I", "u1", "COMPLETED", db_id="1"),
        _job("static_II", "u2", "COMPLETED", db_id="2"),
        _job("static_bilayer", "target-uuid", "RUNNING", db_id="3"),
    ]
    jc = _make_jc(jobs)
    try:
        _run_wait(jc, timeout_s=1)
        raise AssertionError("expected JobflowWaitTimeout")
    except JobflowWaitTimeout as e:
        done = [j for j in e.jobs if j["category"] == "DONE"]
        running = [j for j in e.jobs if j["category"] == "RUNNING"]
        assert len(done) == 2 and len(running) == 1
        assert running[0]["name"] == "static_bilayer"


# --- Group B: _collect_job_diagnostics (the gather) -----------------------


@_unit
def test_source_a_from_jobcontroller():
    """Per-job records come from the mocked DB only; no host call when nothing is probe-eligible."""
    jc = _make_jc([_job("relax", "u1", "COMPLETED", worker="anvil_cpu", run_dir="/scratch/x", pid="111")])
    with patch("core.tools._get_ssh_host") as ssh:
        diag = _collect_job_diagnostics(jc, "flow-abc123", "anvil", timeout_s=14400, elapsed_s=14400)
    ssh.assert_not_called()  # COMPLETED -> never probed
    (rec,) = diag.jobs
    assert rec["name"] == "relax" and rec["state"] == "COMPLETED"
    assert rec["worker"] == "anvil_cpu" and rec["category"] == "DONE"


@_unit
def test_remote_only_for_nonterminal():
    """The host is probed only for RUNNING jobs that have a run_dir+slurm id, never COMPLETED ones."""
    jobs = [
        _job("done", "u1", "COMPLETED", db_id="1", run_dir="/scratch/done", pid="100"),
        _job("live", "u2", "RUNNING", db_id="2", run_dir="/scratch/live", pid="200"),
    ]
    host = _FakeHost(stdout="===JOB 2 LS===\ntotal 0\n===JOB 2 END===\n")
    with patch("core.tools._get_ssh_host", return_value=host) as ssh:
        _collect_job_diagnostics(_make_jc(jobs), "flow-abc123", "anvil")
    ssh.assert_called_once()  # one worker
    assert len(host.scripts) == 1
    assert "/scratch/live" in host.scripts[0]
    assert "/scratch/done" not in host.scripts[0]  # the COMPLETED job is excluded


@_unit
def test_remote_command_is_code_agnostic():
    """Guard (S7.1): the probe script lists by mtime + tails standard streams, with no engine filenames or grep list."""
    script = _remote_probe_script([{"db_id": "1", "run_dir": "/scratch/x", "slurm_id": "999"}])
    for token in ("ls -la", "ls -t", "tail", "std_err.txt", "std_out.txt", "queue.err", "queue.out"):
        assert token in script, f"expected code-agnostic token {token!r}"
    for forbidden in ("OUTCAR", "OSZICAR", "vasp.out", "oom_kill", "Out Of Memory"):
        assert forbidden not in script, f"probe script must not hard-code {forbidden!r}"


@_unit
def test_raw_passthrough():
    """A fake oom_kill line in the remote output appears verbatim in the rendered message (no parse/relabel)."""
    stdout = (
        "===JOB 2 LS===\n-rw-r--r-- 1 u g 3200 2026-06-04 11:43 vasp.out\n"
        "===JOB 2 STREAMS===\n--- std_err.txt ---\n"
        "Detected 1 oom_kill event in StepId=17960736.1\n"
        "srun: error: a971: task 0: Out Of Memory\n"
        "===JOB 2 SCHED===\nRUNNING|2.43G|0:0\n===JOB 2 END===\n"
    )
    jobs = [_job("live", "u2", "RUNNING", db_id="2", run_dir="/scratch/live", pid="200")]
    with patch("core.tools._get_ssh_host", return_value=_FakeHost(stdout=stdout)):
        diag = _collect_job_diagnostics(_make_jc(jobs), "flow-abc123", "anvil")
    msg = diag.render()
    assert "oom_kill" in msg and "Out Of Memory" in msg


@_unit
def test_no_verdict_label():
    """Guard (S7.3): the rendered message carries no harness verdict."""
    jobs = [_job("live", "target", "RUNNING")]
    diag = _collect_job_diagnostics(_make_jc(jobs), "flow-abc123", "anvil")
    msg = diag.render()
    for verdict in ("HINT", "LIKELY STALLED", "DEFINITIVE"):
        assert verdict not in msg


@_unit
def test_constant_next_steps():
    """Guard: the fixed two-line menu is present and carries no job-specific advice."""
    jobs = [_job("live", "target", "RUNNING")]
    msg = _collect_job_diagnostics(_make_jc(jobs), "flow-abc123", "anvil").render()
    assert "keep waiting" in msg
    assert "use the jf command to cancel" in msg
    for specific in ("anvil_highmem", "cpus_per_task"):
        assert specific not in msg


@_unit
def test_gather_failure_is_soft():
    """If the SSH host raises, the gather still returns Source-A records and wait_for_jobflow still raises."""
    jobs = [_job("live", "target-uuid", "RUNNING", run_dir="/scratch/live", pid="200")]

    # (a) the gather alone: remote_error attached, records still returned
    with patch("core.tools._get_ssh_host", side_effect=RuntimeError("ssh down")):
        diag = _collect_job_diagnostics(_make_jc(jobs), "flow-abc123", "anvil")
    (rec,) = diag.jobs
    assert rec["category"] == "RUNNING"
    assert "ssh down" in rec["remote_error"]

    # (b) end to end: a gather failure must not suppress the JobflowWaitTimeout
    jc = _make_jc(jobs)
    with patch("core.tools._get_ssh_host", side_effect=RuntimeError("ssh down")):
        try:
            _run_wait(jc, timeout_s=1)
            raise AssertionError("expected JobflowWaitTimeout")
        except JobflowWaitTimeout:
            pass


# --- Group C: the timeout default -----------------------------------------


@_unit
def test_timeout_default_is_4h():
    """No explicit arg -> 14400s default; an explicit timeout_s overrides it."""
    # The default lives in the signature (not config / tool-wiring).
    sig = inspect.signature(wait_for_jobflow.forward)
    assert sig.parameters["timeout_s"].default == 14400

    jc = _make_jc([_job("relax", "target-uuid", "RUNNING")])

    # Default: the rendered message reports the 14400s bound.
    try:
        _run_wait(jc)
        raise AssertionError("expected JobflowWaitTimeout")
    except JobflowWaitTimeout as e:
        assert "after 14400s" in str(e)

    # Explicit override is honored.
    try:
        _run_wait(jc, timeout_s=42)
        raise AssertionError("expected JobflowWaitTimeout")
    except JobflowWaitTimeout as e:
        assert "after 42s" in str(e)


if __name__ == "__main__":
    import traceback

    failed = 0
    for fn in UNIT_TESTS:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
        except Exception:
            print(f"  FAIL  {fn.__name__}")
            traceback.print_exc()
            failed += 1
    if failed:
        raise SystemExit(1)
    print(f"\nAll {len(UNIT_TESTS)} unit tests passed!")
