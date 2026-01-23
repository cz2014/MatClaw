"""Tool definitions for the MLFF agent."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from smolagents import Tool, tool

# Project paths for RAG
_PROJECT_ROOT = Path(__file__).parent.parent
_DEFAULT_CORPUS_PATH = _PROJECT_ROOT / "data" / "corpus"


@tool
def wait_for_jobflow(
    project_name: str,
    job_uuid: str,
    timeout_s: int = 3600,
) -> dict:
    """Block until all jobs in a jobflow complete, showing progress for each.

    Given any job UUID from a flow, this function:
      1. Finds the parent flow containing that job
      2. Polls all jobs in the flow, printing status updates
      3. Returns the output of the specified job when complete
      4. Raises an exception if any job fails or times out

    Args:
        project_name: The jobflow-remote project (as configured in ~/.jfremote).
        job_uuid: Any Job UUID from the flow to monitor.
        timeout_s: Maximum wall time to wait, in seconds. Default 3600 (1 hour).

    Returns:
        The output dict of the specified job (e.g., DeePMD metrics).
    """
    from jobflow_remote.jobs.jobcontroller import JobController
    from jobflow_remote.jobs.state import JobState

    POLL_S = 10
    # Use .value for comparison since state can be string or enum
    TERMINAL_ERROR_VALUES = {
        JobState.FAILED.value,
        JobState.REMOTE_ERROR.value,
        JobState.TERMINATED.value,
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

        # Timeout check
        if elapsed > timeout_s:
            states_summary = ", ".join(
                f"{_get(j, 'name')}={_state_val(_get(j, 'state'))}" for j in jobs
            )
            raise TimeoutError(f"Timed out after {timeout_s}s. States: {states_summary}")

        time.sleep(POLL_S)


class TrainDeePMDTool(Tool):
    """Tool that creates a DeePMD training job for use in jobflow.

    Returns a jobflow Job object (not execution result), to be used in Flow with submit_flow().
    """

    name = "train_deepmd"
    description = """Create a DeePMD training job from VASP MD output.

Returns a jobflow Job object. Use it in a Flow with submit_flow():
    dp_job = train_deepmd(md_job.output, type_map=["C"], numb_steps=500)
    flow = Flow([md_job, dp_job])
    submit_flow(flow, worker="local_shell", project="default")
    out = wait_for_jobflow("default", dp_job.uuid)

Output structure (atomate2-compatible, same pattern as RelaxMaker/MDMaker):
    out["output"]["mae_e"]      # Energy MAE (eV/atom), float or None
    out["output"]["rmse_e"]     # Energy RMSE (eV/atom), float or None
    out["output"]["mae_f"]      # Force MAE (eV/Angstrom), float or None
    out["output"]["rmse_f"]     # Force RMSE (eV/Angstrom), float or None
    out["output"]["model_path"] # Absolute path to frozen model (.pb)

Network presets:
- 'sanity_check': Pipeline validation only (fast, low accuracy)
- 'fast': Active learning loops or limited compute
- 'balanced': Production-quality force fields (default)
"""
    inputs = {
        "vasp_source": {
            "type": "any",
            "description": "TaskDoc output from MDMaker (md_job.output), or path to VASP dir with OUTCAR",
        },
        "type_map": {
            "type": "array",
            "description": "Element symbols in order, e.g. ['C'] or ['Mo', 'S']",
            "nullable": True,
        },
        "numb_steps": {
            "type": "integer",
            "description": "Number of training steps (500 for sanity, 2000+ for production)",
            "nullable": True,
        },
        "net_size_preset": {
            "type": "string",
            "description": "Network size: 'sanity_check', 'fast', or 'balanced'",
            "nullable": True,
        },
        "overrides": {
            "type": "object",
            "description": "Optional dict to override DeePMD input.json parameters",
            "nullable": True,
        },
    }
    output_type = "object"

    def forward(
        self,
        vasp_source: Any,
        type_map: list[str] | None = None,
        numb_steps: int | None = None,
        net_size_preset: str | None = None,
        overrides: dict | None = None,
    ):
        # Import here to avoid circular imports at module load time
        from remote_jobs.jobs import train_deepmd as _train_deepmd_job

        # Build kwargs, only including non-None values to use @job defaults
        kwargs: dict[str, Any] = {}
        if type_map is not None:
            kwargs["type_map"] = tuple(type_map) if isinstance(type_map, list) else type_map
        if numb_steps is not None:
            kwargs["numb_steps"] = numb_steps
        if net_size_preset is not None:
            kwargs["net_size_preset"] = net_size_preset
        if overrides is not None:
            kwargs["overrides"] = overrides

        # Call @job function - returns a Job object
        return _train_deepmd_job(vasp_source, **kwargs)


class RagSearchTool(Tool):
    """Tool for searching code documentation and examples via RAG.

    Returns verbatim code snippets from indexed package source code.
    Trust tier SOURCE indicates direct source code.
    """

    name = "rag_search"
    description = """Search for code documentation, API signatures, and examples.

Use this tool when:
- You encounter AttributeError, TypeError, or "has no attribute" errors in your execution environment.
- You need to verify correct method names, signatures, or kwargs before writing code.
- You need to see a real-world code snippet to understand how to initialize a complex object.

Returns {"results": [{"source": "path/file.py:10-50", "snippet": "code..."}, ...]}.

Example: rag_search("Structure from_file", software=["pymatgen"])
"""
    inputs = {
        "query": {
            "type": "string",
            "description": "Search query (e.g., 'MDMaker' or 'submit_flow jobflow')",
        },
        "software": {
            "type": "array",
            "description": "Filter by package names, e.g. ['pymatgen', 'atomate2']. None for all.",
            "nullable": True,
        },
    }
    output_type = "object"

    def __init__(self, corpus_path: Path | None = None, top_k: int = 5):
        """Initialize RAG search tool.

        Args:
            corpus_path: Path to corpus directory. Defaults to data/corpus.
            top_k: Number of results to return. Defaults to 5.
        """
        super().__init__()
        self._corpus_path = corpus_path or _DEFAULT_CORPUS_PATH
        self._top_k = top_k
        self._index = None

    def _load_index(self) -> None:
        """Lazy-load the RAG index."""
        if self._index is not None:
            return

        if not self._corpus_path.exists():
            raise FileNotFoundError(
                f"RAG corpus not found at {self._corpus_path}. "
                "Run 'python scripts/build_corpus.py' first."
            )

        from core.rag import RagIndex

        self._index = RagIndex.load(self._corpus_path)

    def forward(
        self,
        query: str,
        software: list[str] | None = None,
    ) -> dict:
        """Execute RAG search.

        Args:
            query: Search query
            software: Optional package filter

        Returns:
            Dict with results list containing source locations and code snippets.
        """
        from core.rag import search

        self._load_index()

        results = search(
            self._index,
            query=query,
            top_k=self._top_k,
            software=software,
        )

        if not results:
            # Check if software filter caused empty results
            if software:
                available = {c.software for c in self._index._chunks}
                missing = [s for s in software if s not in available]
                if missing:
                    return {
                        "results": [],
                        "note": f"Package(s) not in corpus: {missing}. Available: {sorted(available)}",
                    }
            return {"results": [], "note": "No relevant code found for this query"}

        return {
            "results": [
                {"source": r.source, "snippet": r.snippet}
                for r in results
            ]
        }


# Instantiate tools for use in agent
train_deepmd = TrainDeePMDTool()
rag_search = RagSearchTool()
