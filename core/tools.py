"""Tool definitions for the MLFF agent."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from smolagents import Tool, tool

# Project paths for RAG
_PROJECT_ROOT = Path(__file__).parent.parent
_DEFAULT_CORPUS_DIR = _PROJECT_ROOT / "data" / "corpus"
_RAG_CONFIG_PATH = _PROJECT_ROOT / "config" / "rag_config.yaml"


def _load_rag_config() -> dict:
    """Load RAG configuration from rag_config.yaml."""
    if not _RAG_CONFIG_PATH.exists():
        return {}
    import yaml

    with open(_RAG_CONFIG_PATH) as f:
        return yaml.safe_load(f) or {}


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


class TrainDeePMDTool(Tool):
    """Tool that creates a DeePMD training job for use in jobflow.

    Returns a jobflow Job object (not execution result), to be used in Flow with submit_flow().
    """

    name = "train_deepmd"
    description = """Create a DeePMD training job from VASP MD output.

Returns a jobflow Job object. Use it in a Flow with submit_flow():
    dp_job = train_deepmd(md_job.output, type_map=["C"], numb_steps=500)
    flow = Flow([md_job, dp_job])
    submit_flow(flow, worker="anvil_cpu", project="anvil")
    out = wait_for_jobflow("anvil", dp_job.uuid)

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


def _load_chunks_from_paths(paths: list[Path]) -> list:
    """Read chunks.json from each path and return combined chunk list.

    Each chunks.json has format: {"use_code_tokenize": bool, "chunks": [...]}.
    Returns list of Chunk objects.
    """
    from core.rag import Chunk

    all_chunks = []
    for p in paths:
        chunks_file = p / "chunks.json"
        if not chunks_file.exists():
            raise FileNotFoundError(
                f"No chunks.json at {chunks_file}. "
                f"Run 'python scripts/build_corpus.py' or 'python scripts/split_corpus.py' first."
            )
        import json

        with chunks_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        for c in data["chunks"]:
            all_chunks.append(
                Chunk(
                    chunk_id=c["chunk_id"],
                    software=c["software"],
                    file_path=c["file_path"],
                    start_line=c["start_line"],
                    end_line=c["end_line"],
                    symbol=c["symbol"],
                    content=c["content"],
                )
            )
    return all_chunks


class RagSearchTool(Tool):
    """Tool for searching code documentation and examples via RAG.

    Returns verbatim code snippets from indexed package source code.
    Uses multi-query RRF fusion when multiple queries are provided.
    """

    name = "rag_search"
    description = """Search for code documentation, API signatures, and examples.

Provide 1-3 search queries in the `queries` list. Multiple paraphrases improve recall.
Keep technical terms (ALL_CAPS tags, filenames, exact values) in all queries.

Use this tool when:
- You need to discover where a symbol lives (module/class/function) across packages.
- You need a verbatim code snippet/example to copy a correct usage pattern.
- You want to verify behavior by reading surrounding implementation context.
- You encounter AttributeError, TypeError, or "has no attribute" and want source evidence.

Returns {"results": [{"source": "path/file.py:10-50", "snippet": "code..."}, ...]}.

Example:
rag_search(queries=[
    "ALGO blocked-Davidson-iteration scheme",
    "ALGO Normal IALGO 38 blocked Davidson",
    "blocked Davidson algorithm ALGO setting"
], software=["vasp"])
"""
    inputs = {
        "queries": {
            "type": "array",
            "items": {"type": "string"},
            "description": "1-3 search queries (paraphrases improve recall)",
        },
        "software": {
            "type": "array",
            "description": "Filter by package names, e.g. ['pymatgen', 'atomate2']. None for all.",
            "nullable": True,
        },
    }
    output_type = "object"

    def __init__(
        self,
        corpus: list[str] | None = None,
        corpus_path: Path | None = None,
        corpus_dir: Path | None = None,
        top_k: int | None = None,
        retriever_method: str | None = None,
    ):
        """Initialize RAG search tool.

        Args:
            corpus: List of package names to load (e.g. ["vasp", "atomate2"]).
                Each name maps to a subdir under corpus_dir.
            corpus_path: Legacy: single pre-built corpus directory.
            corpus_dir: Base directory for per-package subdirs. Defaults to data/corpus.
            top_k: Number of results to return. Overrides config value.
            retriever_method: Override retriever method (bm25/gemini). Defaults to config value.
        """
        super().__init__()
        self._corpus = corpus
        self._corpus_path = corpus_path
        self._corpus_dir = corpus_dir or _DEFAULT_CORPUS_DIR
        self._top_k_override = top_k
        self._retriever_method = retriever_method
        self._index = None
        self._top_k = 5  # default, overridden in _load_index

    def _load_index(self) -> None:
        """Lazy-load the RAG retriever."""
        if self._index is not None:
            return

        config = _load_rag_config()
        defaults = config.get("defaults", {})

        if self._corpus_path:
            # Legacy mode: single pre-built corpus directory
            if self._retriever_method is not None:
                method = self._retriever_method
            else:
                method = defaults.get("retriever_method",
                                      config.get("retriever", {}).get("method", "bm25"))

            gemini_task_type = config.get("gemini_task_type", "RETRIEVAL_QUERY")

            if method == "bm25":
                index_path = self._corpus_path
            else:
                index_path = self._corpus_path / method

            if not index_path.exists():
                raise FileNotFoundError(
                    f"RAG corpus not found at {index_path}. "
                    f"Run 'python scripts/build_corpus.py --retriever {method}' first."
                )

            from core.retrievers import load_retriever

            self._index = load_retriever(method, index_path, gemini_task_type=gemini_task_type)
            self._top_k = self._top_k_override or defaults.get("top_k", 5)
            return

        # New mode: per-package subdirs under corpus_dir
        corpus_registry = config.get("corpus", {})
        packages = self._corpus or list(corpus_registry.keys())

        # Resolve retriever method
        if self._retriever_method is not None:
            method = self._retriever_method
        else:
            methods = set()
            for pkg in packages:
                pkg_cfg = corpus_registry.get(pkg, {})
                methods.add(pkg_cfg.get("retriever_method",
                                        defaults.get("retriever_method", "bm25")))
            if len(methods) > 1:
                raise ValueError(
                    f"Cannot combine corpora with different retriever methods: {methods}"
                )
            method = methods.pop() if methods else defaults.get("retriever_method", "bm25")

        self._top_k = self._top_k_override or defaults.get("top_k", 5)
        paths = [self._corpus_dir / pkg for pkg in packages]

        # Single package with pre-built BM25 index: load directly
        if len(paths) == 1 and (paths[0] / "bm25").exists() and method == "bm25":
            from core.retrievers import load_retriever

            self._index = load_retriever(method, paths[0])
        else:
            # Multiple packages: load chunks and build combined in-memory index
            from core.retrievers.bm25 import BM25Retriever

            all_chunks = _load_chunks_from_paths(paths)
            self._index = BM25Retriever(chunks=all_chunks)

    def forward(
        self,
        queries: list[str],
        software: list[str] | None = None,
    ) -> dict:
        """Execute RAG search with multi-query fusion.

        Args:
            queries: List of 1-3 search query paraphrases
            software: Optional package filter

        Returns:
            Dict with results list containing source locations and code snippets.
        """
        from core.rag import search_multi

        self._load_index()

        results = search_multi(
            self._index,
            queries=queries,
            top_k=self._top_k,
            software=software,
            per_query_k=20,
            rrf_k=60,
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
