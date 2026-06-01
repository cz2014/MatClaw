"""Tool definitions for the MatClaw."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from core._smol import Tool, tool

# Pause controller for wait_for_jobflow polling
_pause_controller = None


def set_pause_controller(controller):
    """Set the pause controller for wait_for_jobflow polling."""
    global _pause_controller
    _pause_controller = controller


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


@tool
def wait_for_jobflow(
    project_name: str,
    job_uuid: str,
) -> dict:
    """Block until all jobs in a jobflow complete, showing progress for each.

    Given any job UUID from a flow, this function:
      1. Finds the parent flow containing that job
      2. Polls all jobs in the flow, printing status updates
      3. Returns the output of the specified job when complete
      4. Raises an exception if any job fails

    This function handles long SLURM queue waits automatically (up to 12 hours).
    Do not attempt to set your own timeout -- just call this and wait for it to
    return.

    Args:
        project_name: The jobflow-remote project (as configured in ~/.jfremote).
        job_uuid: Any Job UUID from the flow to monitor.

    Returns:
        The output dict of the specified job.
    """
    timeout_s = 43200  # 12h internal safeguard; not exposed to the agent
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

        # Timeout check -- return status dict instead of raising
        if elapsed > timeout_s:
            job_states = {
                _get(j, "name"): _state_val(_get(j, "state")) for j in jobs
            }
            print(f"  Timeout after {int(elapsed)}s. Job states: {job_states}", flush=True)
            return {
                "status": "timeout",
                "flow_uuid": flow_uuid,
                "job_uuid": job_uuid,
                "elapsed_s": int(elapsed),
                "job_states": job_states,
            }

        time.sleep(POLL_S)
        if _pause_controller is not None:
            _pause_controller.wait_if_paused(
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
not POSIX). By default searches the installed package source under site-packages; scope to a
package with path (e.g. ".../pymatgen") or glob/type. output_mode:
  - "files_with_matches" (default): list[str] of matching file paths.
  - "content": {"matches": [{"file","line","text"}], "truncated": bool}.
  - "count": {file: match_count}.
Scope with glob (e.g. "**/*.py") or type (e.g. "py"); -i via case_insensitive;
-C context lines; multiline matching; head_limit caps the number of entries.
Searches all files including .gitignored paths (the package source lives in a gitignored venv)."""

    inputs = {
        "pattern": {"type": "string", "description": "Ripgrep regex to search for."},
        "path": {"type": "string", "description": "Dir/file to search (default: corpus/sources).", "nullable": True},
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


class BashTool(Tool):
    name = "bash"
    description = """Run a shell command and capture its output (mirrors Claude `Bash` / OpenAI `ShellTool`).

The explicit shell escape hatch -- bounded by the container, not by path checks.
stdout and stderr are both captured. Default cwd is the workspace; set cwd to run
elsewhere (prefer the cwd arg over a `cd` in the command). timeout defaults to 120s
(cap 600s); output is capped at max_output_chars (default 30000) with a truncated
flag. Returns {"stdout","stderr","returncode","truncated"}.

For long-running HPC compute, submit jobs and use wait_for_jobflow -- not local bash.
run_in_background launches the command detached, streaming output to a workspace log
file, and returns {"pid","background","log_file"} without waiting."""

    inputs = {
        "command": {"type": "string", "description": "The shell command to run."},
        "timeout": {"type": "integer", "description": "Seconds before the command is killed (default 120, cap 600).", "nullable": True},
        "max_output_chars": {"type": "integer", "description": "Cap on captured stdout/stderr (default 30000).", "nullable": True},
        "cwd": {"type": "string", "description": "Working directory (default: workspace).", "nullable": True},
        "run_in_background": {"type": "boolean", "description": "Launch detached, stream to a log file. Default False.", "nullable": True},
    }
    output_type = "object"

    _TIMEOUT_CAP = 600
    _DEFAULT_TIMEOUT = 120
    _DEFAULT_MAX_CHARS = 30_000

    def __init__(self, workspace: Path):
        super().__init__()
        self._workspace = workspace.resolve()

    def forward(
        self,
        command: str,
        timeout: int = 120,
        max_output_chars: int = 30_000,
        cwd: str | None = None,
        run_in_background: bool = False,
    ) -> dict:
        run_cwd = str(self._workspace if cwd is None else Path(cwd))
        if run_in_background:
            log = self._workspace / f".bash_bg_{os.getpid()}_{int(time.time() * 1000)}.log"
            fh = open(log, "w", encoding="utf-8")
            proc = subprocess.Popen(
                command, shell=True, cwd=run_cwd, stdout=fh, stderr=subprocess.STDOUT, text=True
            )
            return {
                "pid": proc.pid,
                "background": True,
                "log_file": os.path.relpath(log, self._workspace),
                "returncode": None,
            }

        timeout = min(int(timeout or self._DEFAULT_TIMEOUT), self._TIMEOUT_CAP)
        cap = int(max_output_chars or self._DEFAULT_MAX_CHARS)
        try:
            proc = subprocess.run(
                command, shell=True, cwd=run_cwd, capture_output=True, text=True, timeout=timeout
            )
        except subprocess.TimeoutExpired as e:
            return {
                "stdout": (e.stdout or "") if isinstance(e.stdout, str) else "",
                "stderr": f"[bash: timed out after {timeout}s]",
                "returncode": None,
                "truncated": False,
                "timed_out": True,
            }
        stdout, stderr = proc.stdout or "", proc.stderr or ""
        truncated = len(stdout) > cap or len(stderr) > cap
        return {
            "stdout": stdout[:cap],
            "stderr": stderr[:cap],
            "returncode": proc.returncode,
            "truncated": truncated,
        }


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
