"""Tool definitions for the MLFF agent."""

from __future__ import annotations

import importlib
import inspect
import time
import types
from pathlib import Path
from typing import Any

from smolagents import Tool, tool

# Project paths for RAG
_PROJECT_ROOT = Path(__file__).parent.parent
_DEFAULT_CORPUS_PATH = _PROJECT_ROOT / "data" / "corpus"
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


class ApiProbeTool(Tool):
    """Runtime API introspection via dir() + inspect.getattr_static()."""

    name = "api_probe"
    description = """Inspect the live Python runtime API for a module/class/function.

Introspects what is actually importable in the current environment. Returns:
- resolved: target summary (kind, name, module, signature, doc)
- dir: public dir() listing with counts

Usage: pass the full dotted path to the symbol you want to inspect.
  api_probe("pymatgen.analysis.defects.utils")           # module overview + dir
  api_probe("pymatgen.analysis.defects.utils.get_avg_chg")  # drill into function

Workflow: probe module/class -> read dir -> probe specific member by appending to path.

Use this tool when:
- You got AttributeError/TypeError and need correct attribute names or signatures.
- You suspect retrieval results refer to a different package/version.
- You want a dir()-like view without writing probing code.

After you find the correct symbol name, use rag_search for verbatim code snippets.
"""

    inputs = {
        "target": {
            "type": "string",
            "description": (
                "Full dotted import path to probe. "
                "Examples: 'pymatgen.analysis.defects.utils', "
                "'pymatgen.core.structure.Structure', "
                "'pymatgen.analysis.defects.utils.get_avg_chg'."
            ),
        },
    }
    output_type = "object"

    _DIR_LIMIT = 200
    _DOC_CHARS = 2000

    def forward(self, target: str) -> dict:
        def fail(msg: str, exc: Exception | None = None) -> dict:
            return {
                "ok": False,
                "error": f"{msg} ({type(exc).__name__}: {exc})" if exc else msg,
                "target": target,
            }

        def _truncate_doc(text: str | None) -> str | None:
            if not text:
                return None
            s = " ".join(text.strip().split())
            if len(s) > self._DOC_CHARS:
                return s[: self._DOC_CHARS - 3] + "..."
            return s

        def _safe_signature(obj) -> str | None:
            try:
                return str(inspect.signature(obj))
            except Exception:
                return None

        def _resolve_target(t: str):
            """Resolve import path to object."""
            if ":" in t:
                mod, rest = t.split(":", 1)
                mod = mod.strip()
                chain = [p for p in rest.strip().split(".") if p] if rest.strip() else []
                module = importlib.import_module(mod)
                obj = module
                for a in chain:
                    obj = inspect.getattr_static(obj, a)
                return obj

            # Longest importable prefix strategy
            parts = [p for p in t.split(".") if p]
            last_exc = None
            for i in range(len(parts), 0, -1):
                mod = ".".join(parts[:i])
                chain = parts[i:]
                try:
                    module = importlib.import_module(mod)
                    obj = module
                    for a in chain:
                        obj = inspect.getattr_static(obj, a)
                    return obj
                except Exception as e:
                    last_exc = e
            raise ModuleNotFoundError(f"Could not resolve '{t}'") from last_exc

        # -- Main flow --
        try:
            obj = _resolve_target(target)
        except Exception as e:
            return fail("Failed to resolve target.", e)

        # Resolved summary
        kind = "data"
        if isinstance(obj, types.ModuleType):
            kind = "module"
        elif inspect.isclass(obj):
            kind = "class"
        elif inspect.isfunction(obj):
            kind = "function"
        elif inspect.isbuiltin(obj):
            kind = "builtin"
        elif callable(obj):
            kind = "callable"

        resolved = {
            "kind": kind,
            "name": getattr(obj, "__name__", type(obj).__name__),
            "module": getattr(obj, "__module__", None),
            "signature": _safe_signature(obj) if callable(obj) else None,
            "doc": _truncate_doc(inspect.getdoc(obj)),
        }

        # dir() listing
        try:
            all_names = sorted(dir(obj))
        except Exception as e:
            return fail("dir() failed on target.", e)

        public_names = [n for n in all_names if not n.startswith("_")]
        dir_info = {
            "public_count": len(public_names),
            "public_listed": public_names[: self._DIR_LIMIT],
            "public_truncated": len(public_names) > self._DIR_LIMIT,
            "all_count": len(all_names),
        }

        return {
            "ok": True,
            "resolved": resolved,
            "dir": dir_info,
            "error": None,
        }


class RagSearchTool(Tool):
    """Tool for searching code documentation and examples via RAG.

    Returns verbatim code snippets from indexed package source code.
    Trust tier SOURCE indicates direct source code.
    """

    name = "rag_search"
    description = """Search for code documentation, API signatures, and examples.

Use this tool when:
- You need to discover where a symbol lives (module/class/function) across packages.
- You need a verbatim code snippet/example to copy a correct usage pattern.
- You want to verify behavior by reading surrounding implementation context.
- You encounter AttributeError, TypeError, or "has no attribute" and want source evidence.

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

    def __init__(
        self,
        corpus_path: Path | None = None,
        top_k: int = 5,
        retriever_method: str | None = None,
    ):
        """Initialize RAG search tool.

        Args:
            corpus_path: Path to corpus directory. Defaults to data/corpus.
            top_k: Number of results to return. Defaults to 5.
            retriever_method: Override retriever method (bm25/gemini). Defaults to config value.
        """
        super().__init__()
        self._corpus_path = corpus_path or _DEFAULT_CORPUS_PATH
        self._top_k = top_k
        self._retriever_method = retriever_method
        self._index = None

    def _load_index(self) -> None:
        """Lazy-load the RAG retriever."""
        if self._index is not None:
            return

        # Determine retriever method from config or override
        if self._retriever_method is not None:
            method = self._retriever_method
        else:
            config = _load_rag_config()
            method = config.get("retriever", {}).get("method", "bm25")

        # Determine index path based on method
        if method == "bm25":
            index_path = self._corpus_path
        else:
            # Vector retrievers use subdirectory (e.g., data/corpus/gemini)
            index_path = self._corpus_path / method

        if not index_path.exists():
            raise FileNotFoundError(
                f"RAG corpus not found at {index_path}. "
                f"Run 'python scripts/build_corpus.py --retriever {method}' first."
            )

        from core.retrievers import load_retriever

        self._index = load_retriever(method, index_path)

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
api_probe = ApiProbeTool()
rag_search = RagSearchTool()
