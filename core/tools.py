"""Tool definitions for the MLFF agent."""

from __future__ import annotations

import time
from typing import Any

from smolagents import tool


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
    TERMINAL_ERROR_STATES = {
        JobState.FAILED,
        JobState.REMOTE_ERROR,
        JobState.TERMINATED,
        JobState.STOPPED,
        JobState.USER_STOPPED,
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
            if state in TERMINAL_ERROR_STATES:
                raise RuntimeError(
                    f"Job '{_get(job, 'name')}' ({_get(job, 'uuid')}) failed: "
                    f"state={state}, error={_get(job, 'error') if isinstance(job, dict) else getattr(job, 'error', None)}"
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


@tool
def train_deepmd(
    vasp_dir: str,
    type_map: list[str] = ["C"],
    numb_steps: int = 2000,
    net_size_preset: str = "balanced",
    overrides: dict | None = None,
) -> dict[str, Any]:
    """Train a DeePMD model from VASP OUTCAR.

    Reads VASP MD trajectory (all frames), prepares training/validation data (80/20 split),
    trains the model, and returns accuracy metrics.

    Args:
        vasp_dir: Path to VASP run directory containing OUTCAR.
        type_map: Element symbols in order (e.g., ["C"] for graphene).
        numb_steps: Number of training steps.
        net_size_preset: Network architecture preset:
            - 'sanity_check': ONLY to verify pipeline runs without errors.
            - 'fast': Rapid iterations, Active Learning loops, or limited compute.
            - 'balanced': Default recommended choice for production-quality force fields.

            Mapping (descriptor_neuron, fitting_neuron):
            - sanity_check -> ([5, 10, 20], [20, 20, 20])
            - fast         -> ([10, 20, 40], [40, 40, 40])
            - balanced     -> ([20, 40, 80], [80, 80, 80])
            
        overrides: Optional dict to override any DeePMD input.json parameters.

    Returns:
        Dict with mae_e, rmse_e, mae_f, rmse_f (accuracy metrics) and model_path.
    """
    from remote_jobs._deepmd import train_deepmd_impl

    return train_deepmd_impl(
        vasp_dir,
        type_map=tuple(type_map),
        numb_steps=numb_steps,
        net_size_preset=net_size_preset,
        overrides=overrides,
    )
