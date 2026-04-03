"""Tool definitions for the MatClaw."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from smolagents import Tool, tool

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


def _get_ssh_host(project_name: str, worker_name: str):
    """Get connected SSH host from jobflow-remote config."""
    from jobflow_remote.config.manager import ConfigManager

    cm = ConfigManager()
    project = cm.get_project(project_name)
    worker = project.workers[worker_name]
    host = worker.get_host()
    host.connect()
    return host


# Project paths for RAG
_PROJECT_ROOT = Path(__file__).parent.parent
_DEFAULT_CORPUS_DIR = _PROJECT_ROOT / "data" / "corpus"
_RAG_CONFIG_PATH = _PROJECT_ROOT / "config" / "rag_config.yaml"


def _load_rag_config(config_path: Path | None = None) -> dict:
    """Load RAG configuration from rag_config.yaml."""
    path = config_path or _RAG_CONFIG_PATH
    if not path.exists():
        return {}
    import yaml

    with open(path) as f:
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
        if _pause_controller is not None:
            _pause_controller.wait_if_paused(
                context=f"During jobflow polling (flow={flow_uuid}, elapsed={int(elapsed)}s)"
            )


class TrainDeePMDTool(Tool):
    """Tool that creates a DeePMD training job for use in jobflow.

    Returns a jobflow Job object (not execution result), to be used in Flow with submit_flow().
    """

    name = "train_deepmd"
    description = """Create a DeePMD training job from MD output or pre-prepared training data.

Returns a jobflow Job object. Use it in a Flow with submit_flow():
    dp_job = train_deepmd(md_job.output, type_map=["C"], numb_steps=500)
    flow = Flow([md_job, dp_job])
    submit_flow(flow, worker="anvil_cpu", project="anvil")
    out = wait_for_jobflow("anvil", dp_job.uuid)

data_source accepts:
- VASP TaskDoc output (from MDMaker) -- resolves OUTCAR from dir_name
- ForcefieldTaskDoc output (from ForceFieldMDMaker) -- extracts from ionic_steps
  IMPORTANT: ForceFieldMDMaker defaults ionic_step_data=None, which produces EMPTY
  ionic_steps. You MUST set ionic_step_data=("energy", "forces", "mol_or_struct")
  when creating the ForceFieldMDMaker for the data to be available to train_deepmd.
- Raw dpdata-compatible dict (fields matching dpdata.LabeledSystem.DTYPES).
  Must include: cells, coords, energies, forces, atom_types, atom_names.
  Also needs: atom_numbs (list[int], count per type), orig (np.zeros(3)),
  nopbc (bool). If atom_numbs/orig/nopbc are omitted, they are auto-populated.
- Path string to deepmd/npy directory on remote filesystem
- List of ANY of the above (merged automatically). Use this for multi-iteration
  training: combine remote paths from previous iterations with new inline data.
  Example: train_deepmd([prev_data_path, new_inline_dict], type_map=["Cu","In","P","S"])

Output structure (atomate2-compatible, same pattern as RelaxMaker/MDMaker):
    out["output"]["model_path"]      # Absolute path to frozen model (.pth)
    out["output"]["data_total_path"] # All input frames (deepmd/npy), pre-split
    out["output"]["data_train_path"] # 80% training split (deepmd/npy)
    out["output"]["data_valid_path"] # 20% validation split (deepmd/npy)
    out["output"]["n_total_frames"]  # Total frames before split
    out["output"]["n_train_frames"]  # Frames in training split (80%)
    out["output"]["n_valid_frames"]  # Frames in validation split (20%)
    out["output"]["mae_e"]           # Energy MAE (eV/atom), float or None
    out["output"]["rmse_e"]          # Energy RMSE (eV/atom), float or None
    out["output"]["mae_f"]           # Force MAE (eV/Angstrom), float or None
    out["output"]["rmse_f"]          # Force RMSE (eV/Angstrom), float or None

For multi-iteration active learning: pass `data_total_path` (not
`data_train_path`) as input to the next iteration to preserve all
frames. `data_train_path` contains only the 80% training split and
will cause cumulative data loss if reused as the sole data source.

Network presets:
- 'sanity_check': Pipeline validation only (fast, low accuracy)
- 'fast': Active learning loops or limited compute
- 'balanced': Production-quality force fields (default)
"""
    inputs = {
        "data_source": {
            "type": "any",
            "description": "Training data: VASP TaskDoc output, ForceFieldMDMaker output, deepmd/npy path, inline dict, or list of any of these (merged)",
            "nullable": True,
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
        "show_source": {
            "type": "boolean",
            "description": (
                "If True, return the source code of the training implementation "
                "instead of creating a job. Useful for understanding accepted "
                "data formats and internal logic."
            ),
            "nullable": True,
        },
    }
    output_type = "object"

    def forward(
        self,
        data_source: Any = None,
        type_map: list[str] | None = None,
        numb_steps: int | None = None,
        net_size_preset: str | None = None,
        overrides: dict | None = None,
        show_source: bool | None = None,
    ):
        # Show source mode: return implementation source code
        if show_source:
            import inspect

            from remote_jobs._deepmd import _load_labeled_data, train_deepmd_impl

            return (
                "# _load_labeled_data (data dispatch logic)\n"
                + inspect.getsource(_load_labeled_data)
                + "\n\n# train_deepmd_impl (main training function)\n"
                + inspect.getsource(train_deepmd_impl)
            )

        # Size guard for inline dict data
        if isinstance(data_source, dict) and "cells" in data_source:
            import numpy as np

            estimated_bytes = sum(
                v.nbytes if isinstance(v, np.ndarray) else 0
                for v in data_source.values()
            )
            if estimated_bytes > 10 * 1024 * 1024:  # 10 MB
                raise ValueError(
                    f"Inline data dict is too large ({estimated_bytes / 1e6:.1f} MB). "
                    "MongoDB has a 16 MB document size limit. "
                    "Write data locally, use remote_put to upload to the remote "
                    "cluster, and pass the remote path string instead."
                )

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
        return _train_deepmd_job(data_source, **kwargs)


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


def _build_rag_description(
    corpus: list[str] | None = None,
    corpus_path: Path | None = None,
    rag_config_path: Path | None = None,
) -> tuple[str, str]:
    """Build dynamic rag_search description from rag_config.yaml.

    Returns (tool_description, software_input_description).
    """
    config = _load_rag_config(rag_config_path)
    corpus_registry = config.get("corpus", {})

    # Determine which packages are available
    if corpus_path:
        # Legacy mode: single corpus directory, can't enumerate packages
        packages = {}
    elif corpus:
        packages = {k: corpus_registry.get(k, {}) for k in corpus}
    else:
        packages = corpus_registry

    # Build corpus list for description
    if packages:
        corpus_lines = "\n".join(
            f"  - {name}: {cfg.get('description', name)}"
            for name, cfg in packages.items()
        )
        corpus_section = f"\nAvailable corpora (use in `software` filter):\n{corpus_lines}"
        pkg_names = list(packages.keys())
        software_desc = f"Filter by package names: {pkg_names}. None for all."
        example_pkg = pkg_names[0]
    else:
        corpus_section = ""
        software_desc = "Filter by package names. None for all."
        example_pkg = "vasp"

    description = (
        "Search for code documentation, API signatures, and examples.\n"
        "\n"
        "Provide 1-3 search queries in the `queries` list. Multiple paraphrases improve recall.\n"
        "Keep technical terms (ALL_CAPS tags, filenames, exact values) in all queries.\n"
        "\n"
        "Use this tool when:\n"
        "- You need to discover where a symbol lives (module/class/function) across packages.\n"
        "- You need a verbatim code snippet/example to copy a correct usage pattern.\n"
        "- You want to verify behavior by reading surrounding implementation context.\n"
        '- You encounter AttributeError, TypeError, or "has no attribute" and want source evidence.\n'
        "\n"
        'Returns {"results": [{"source": "path/file.py:10-50", "snippet": "code..."}, ...]}.\n'
        f"{corpus_section}\n"
        "Example:\n"
        "rag_search(queries=[\n"
        '    "ALGO blocked-Davidson-iteration scheme",\n'
        '    "ALGO Normal IALGO 38 blocked Davidson",\n'
        '    "blocked Davidson algorithm ALGO setting"\n'
        f'], software=["{example_pkg}"])'
    )

    return description, software_desc


class RagSearchTool(Tool):
    """Tool for searching code documentation and examples via RAG.

    Returns verbatim code snippets from indexed package source code.
    Uses multi-query RRF fusion when multiple queries are provided.
    """

    name = "rag_search"
    description = "Search for code documentation, API signatures, and examples."
    inputs = {
        "queries": {
            "type": "array",
            "items": {"type": "string"},
            "description": "1-3 search queries (paraphrases improve recall)",
        },
        "software": {
            "type": "array",
            "description": "Filter by package names. None for all.",
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
        rag_config_path: Path | None = None,
    ):
        """Initialize RAG search tool.

        Args:
            corpus: List of package names to load (e.g. ["vasp", "atomate2"]).
                Each name maps to a subdir under corpus_dir.
            corpus_path: Legacy: single pre-built corpus directory.
            corpus_dir: Base directory for per-package subdirs. Defaults to data/corpus.
            top_k: Number of results to return. Overrides config value.
            retriever_method: Override retriever method (bm25/gemini). Defaults to config value.
            rag_config_path: Path to rag_config.yaml. Defaults to PROJECT_ROOT/config/rag_config.yaml.
        """
        super().__init__()
        self._corpus = corpus
        self._corpus_path = corpus_path
        self._corpus_dir = corpus_dir or _DEFAULT_CORPUS_DIR
        self._top_k_override = top_k
        self._retriever_method = retriever_method
        self._rag_config_path = rag_config_path or _RAG_CONFIG_PATH
        self._index = None
        self._top_k = 5  # default, overridden in _load_index

        # Build dynamic description from rag_config.yaml
        desc, software_desc = _build_rag_description(
            corpus, corpus_path, rag_config_path=self._rag_config_path
        )
        self.description = desc
        self.inputs = {
            **self.inputs,
            "software": {**self.inputs["software"], "description": software_desc},
        }

    def _load_index(self) -> None:
        """Lazy-load the RAG retriever."""
        if self._index is not None:
            return

        config = _load_rag_config(self._rag_config_path)
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


class BatchStaticEvalTool(Tool):
    """Tool that creates a batch static evaluation job for use in jobflow.

    Returns a jobflow Job object (not execution result), to be used in Flow with submit_flow().
    """

    name = "batch_static_eval"
    description = """Run N force-field static evaluations in a single SLURM job.

Returns a jobflow Job object. Use it in a Flow with submit_flow():
    job = batch_static_eval(
        structures=[s.as_dict() for s in struct_list],
        force_field_name="DeepMD",
        calculator_kwargs={"model": "/path/to/model.pth"},
        type_map=["Cu", "In", "P", "S"],
    )
    flow = Flow([job])
    submit_flow(flow, worker="perlmutter_debug", project="perlmutter")
    out = wait_for_jobflow("perlmutter", job.uuid)

structures accepts:
- List of pymatgen Structure dicts (via struct.as_dict()) for inline mode
- Remote path string to a trajectory file (.traj, .xyz, .extxyz) for large sets

force_field_name matches atomate2 convention (currently "DeepMD" only).
calculator_kwargs: e.g. {"model": "/path/to/frozen_model.pth"} for DeePMD.

Output structure:
    out["output"]["energies"]  # list of float (eV), one per structure
    out["output"]["forces"]    # list of arrays (eV/A), shape [n_atoms, 3] each
    out["output"]["n_frames"]  # int, number of structures evaluated
"""
    inputs = {
        "structures": {
            "type": "any",
            "description": (
                "Structures to evaluate. Either a list of pymatgen Structure dicts "
                "(via struct.as_dict()), or a remote path to a trajectory file "
                "(.traj, .xyz, .extxyz). Use path for large sets (>1000 structures) "
                "to bypass MongoDB's 16 MB input limit."
            ),
        },
        "force_field_name": {
            "type": "string",
            "description": "Calculator name, e.g. 'DeepMD' (matches atomate2 convention)",
            "nullable": True,
        },
        "calculator_kwargs": {
            "type": "object",
            "description": "Kwargs for calculator, e.g. {'model': '/path/to/model.pth'}",
        },
        "type_map": {
            "type": "array",
            "description": "Element symbols in DeePMD type order, e.g. ['Cu','In','P','S']",
        },
        "show_source": {
            "type": "boolean",
            "description": "If True, return source code instead of creating a job",
            "nullable": True,
        },
    }
    output_type = "object"

    def forward(
        self,
        structures: list[dict] | str,
        calculator_kwargs: dict[str, Any],
        type_map: list[str],
        force_field_name: str | None = None,
        show_source: bool | None = None,
    ):
        if show_source:
            import inspect

            from remote_jobs._batch_eval import batch_static_eval_impl

            return inspect.getsource(batch_static_eval_impl)

        # Size guard for inline dicts
        if isinstance(structures, list):
            estimated_bytes = len(structures) * 3000
            if estimated_bytes > 10 * 1024 * 1024:
                raise ValueError(
                    f"Inline structures too large (~{estimated_bytes / 1e6:.1f} MB, "
                    f"{len(structures)} structures). MongoDB has a 16 MB document size "
                    "limit. Write structures to an .extxyz file locally, use remote_put "
                    "to upload, and pass the remote path string instead."
                )

        from remote_jobs.jobs import batch_static_eval as _batch_static_eval_job

        return _batch_static_eval_job(
            structures=structures,
            force_field_name=force_field_name or "DeepMD",
            calculator_kwargs=calculator_kwargs,
            type_map=tuple(type_map) if isinstance(type_map, list) else type_map,
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


class WriteTextTool(Tool):
    name = "write_text"
    description = """Write text content to a file in the workspace directory.

The path is relative to the workspace root. Parent directories are created
automatically. Paths that escape the workspace (e.g., '../etc/passwd') are
rejected. Maximum content size is 5 MB per call.

Use this instead of open() for all file writes.

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


class ReadTextTool(Tool):
    name = "read_text"
    description = """Read text content from a file in the workspace directory.

The path is relative to the workspace root. Paths that escape the workspace
are rejected.

Use this instead of open() for all file reads."""

    inputs = {
        "rel_path": {
            "type": "string",
            "description": "File path relative to workspace (e.g., 'data/input.cif')",
        },
    }
    output_type = "string"

    def __init__(self, workspace: Path):
        super().__init__()
        self._workspace = workspace.resolve()

    def forward(self, rel_path: str) -> str:
        p = _safe_path(self._workspace, rel_path)
        return p.read_text(encoding="utf-8")


class ReadPdfTool(Tool):
    name = "read_pdf"
    description = """Read text from a PDF file in the workspace directory.

The path is relative to the workspace root (same as read_text).
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


# --- Remote transfer tools ---


class RemotePutTool(Tool):
    name = "remote_put"
    description = """Upload a file or directory from workspace to remote HPC via SSH.

Supports both single files and directories. Directories are transferred as
tar archives (packed locally, uploaded, extracted remotely).

Default upload directory: /pscratch/sd/c/cz2014/agent_tmp_dir
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


class EFieldMDTool(Tool):
    """Tool that creates an E-field MD job for use in jobflow."""

    name = "efield_md"
    description = """Create an E-field MD job: ForceFieldMDMaker + external electric field.

Identical to ForceFieldMDMaker with two extra parameters (efield, efield_charges).
Internally uses SumCalculator([DeePMD, UniformElectricForce]) so the total force
on atom i is F_DP(i) + q_i * E and the total energy includes -sum(q_i * r_i . E).

Returns a jobflow Job. Use in a Flow with submit_flow() + wait_for_jobflow():
    job = efield_md(structure, efield=(0,0,-0.05),
                    efield_charges={"Cu": 0.765, "In": -0.085, ...},
                    calculator_kwargs={"model": "/path/to/model.pb"},
                    n_steps=19000, temperature=230, time_step=2.0)
    flow = Flow([job], name="efield_md")
    submit_flow(flow, project="perlmutter", worker="perlmutter_debug")
    out = wait_for_jobflow("perlmutter", job.uuid)

E-field specific args:
    structure: pymatgen Structure (input geometry)
    efield: Electric field vector in eV/A/e, e.g. (0, 0, -0.05) for -z field
    efield_charges: Element symbol -> Born effective charge (e), e.g. {"Cu": 0.765, ...}

ForceFieldMDMaker args (passed through):
    calculator_kwargs: Dict for DeePMD calculator, e.g. {"model": "/path/to/model.pb"}
    n_steps: Number of MD steps
    temperature: Temperature in K
    time_step: Timestep in fs (default 2.0)
    traj_file: Trajectory filename (e.g. "trajectory.traj")
    traj_interval: Save trajectory every N steps
    ionic_step_data: Tuple of data to record per step, e.g. ("energy", "forces", "mol_or_struct").
        WARNING: setting this to anything non-None causes atomate2 to store full Structure
        objects for EVERY frame in MongoDB, creating huge additional_store_data.json files
        (600+ MB for 500 atoms x 1900 frames). Only set this if you need per-step data
        for training (train_deepmd). For analysis-only runs, leave as None (default).
    store_trajectory: Whether to store Trajectory object in MongoDB. Default "no".
        The .traj file is always written to disk regardless. Set to "partial" or "full"
        only if you need the trajectory in MongoDB (adds ~200 MB for large runs).
    name: Job name (optional)

Introspection:
    show_source: If True, return the source code of UniformElectricForce and
                 EFieldMDMaker instead of creating a job. Useful for understanding
                 the force/energy formulas and SumCalculator composition.
"""
    inputs = {
        "structure": {"type": "object", "description": "pymatgen Structure", "nullable": True},
        "efield": {"type": "object", "description": "E-field vector (3-tuple, eV/A/e)", "nullable": True},
        "efield_charges": {"type": "object", "description": "Element -> Born effective charge dict", "nullable": True},
        "calculator_kwargs": {"type": "object", "description": "DeePMD calculator kwargs, e.g. {'model': '...'}", "nullable": True},
        "name": {"type": "string", "description": "Job name (optional)", "nullable": True},
        "n_steps": {"type": "integer", "description": "Number of MD steps", "nullable": True},
        "temperature": {"type": "number", "description": "Temperature in K", "nullable": True},
        "time_step": {"type": "number", "description": "Timestep in fs (default 2.0)", "nullable": True},
        "traj_file": {"type": "string", "description": "Trajectory filename, e.g. 'traj.traj'", "nullable": True},
        "traj_interval": {"type": "integer", "description": "Save trajectory every N steps", "nullable": True},
        "ionic_step_data": {"type": "object", "description": "Tuple of data per step, e.g. ('energy', 'forces', 'mol_or_struct')", "nullable": True},
        "store_trajectory": {"type": "string", "description": "Store Trajectory in MongoDB: 'no' (default), 'partial', or 'full'", "nullable": True},
        "show_source": {"type": "boolean", "description": "If True, return source code instead of creating a job", "nullable": True},
    }
    output_type = "object"

    def forward(
        self,
        structure=None,
        efield=None,
        efield_charges=None,
        calculator_kwargs=None,
        name=None,
        n_steps=None,
        temperature=None,
        time_step=None,
        traj_file=None,
        traj_interval=None,
        ionic_step_data=None,
        store_trajectory=None,
        show_source=None,
    ):
        if show_source:
            import inspect

            from remote_jobs._efield_calculator import EFieldMDMaker, UniformElectricForce

            return (
                "# UniformElectricForce (E-field ASE calculator)\n"
                + inspect.getsource(UniformElectricForce)
                + "\n\n# EFieldMDMaker (ForceFieldMDMaker subclass)\n"
                + inspect.getsource(EFieldMDMaker)
            )

        from remote_jobs._efield_calculator import EFieldMDMaker

        passthrough = {
            "name": name,
            "n_steps": n_steps,
            "temperature": temperature,
            "time_step": time_step,
            "traj_file": traj_file,
            "traj_interval": traj_interval,
            "ionic_step_data": ionic_step_data,
            "store_trajectory": store_trajectory if store_trajectory is not None else "no",
        }
        maker = EFieldMDMaker(
            force_field_name="DeepMD",
            efield=tuple(efield) if efield is not None else (0, 0, 0),
            efield_charges=efield_charges,
            calculator_kwargs=calculator_kwargs,
            **{k: v for k, v in passthrough.items() if v is not None},
        )
        return maker.make(structure)


# Instantiate tools for use in agent
train_deepmd = TrainDeePMDTool()
batch_static_eval = BatchStaticEvalTool()
efield_md = EFieldMDTool()
