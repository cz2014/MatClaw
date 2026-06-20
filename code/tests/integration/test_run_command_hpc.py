"""Integration smoke test for the generic ``run_command`` @job.

Submits a ``run_command`` flow that runs ``hostname`` on a configured HPC worker and checks
the returned result dict -- confirming the @job serializes, deserializes on the worker, runs,
and returns through the jobstore. Code-agnostic (no external engine); mirrors
``test_hpc_connection.py``.

Cluster-agnostic via the ``hpc_target`` fixture (``--hpc-project``/``--hpc-worker`` or
``$MATCLAW_TEST_PROJECT``/``$MATCLAW_TEST_WORKER``). SKIPS when no HPC project is configured;
FAILS only when a configured cluster is unreachable or returns the wrong result.

Tier: integration (auto-marked by directory; excluded from the unit gate). Needs a running
jobflow-remote runner for the project. Run with:

    uv run --project code --extra dev pytest code/tests -m integration --hpc-project anvil
"""

from __future__ import annotations


def test_run_command_hostname(hpc_target):
    """run_command runs a trivial shell command on the worker and returns the result dict."""
    from jobflow import Flow
    from jobflow_remote import submit_flow

    from core.tools import wait_for_jobflow
    from remote_jobs.jobs import run_command

    project, worker = hpc_target
    job = run_command(input_files={}, command="hostname")
    submit_flow(Flow([job], name="run_command_smoke"), worker=worker, project=project)

    out = wait_for_jobflow(project, job.uuid)
    result = out.get("output", out) if isinstance(out, dict) else out
    assert isinstance(result, dict), f"unexpected output type from {project}/{worker}: {out!r}"
    assert result.get("returncode") == 0, f"run_command returned nonzero: {result!r}"
    assert result.get("stdout_tail", "").strip(), f"empty hostname output: {result!r}"
