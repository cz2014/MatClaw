"""Integration smoke test: submit a trivial @job to an HPC cluster and verify the result.

Cluster-agnostic replacement for the old anvil-specific script. The target project/worker
come from the ``hpc_target`` fixture (``--hpc-project``/``--hpc-worker`` or
``$MATCLAW_TEST_PROJECT``/``$MATCLAW_TEST_WORKER``), so this exercises whatever cluster is
configured. It SKIPS when no HPC project is configured on the host and FAILS only when a
configured cluster is unreachable or returns the wrong result.

Tier: integration (auto-marked by directory; excluded from the unit gate). Needs a running
jobflow-remote runner for the project. Run with:

    uv run --project code --extra dev pytest code/tests -m integration --hpc-project anvil
"""

from __future__ import annotations


def test_hpc_connection(hpc_target):
    """A trivial @job runs on the worker and returns its hostname."""
    from jobflow import Flow
    from jobflow_remote import submit_flow

    from core.tools import wait_for_jobflow
    from remote_jobs.jobs import hello_hpc

    project, worker = hpc_target
    job = hello_hpc()
    submit_flow(Flow([job], name="hpc_connection_smoke"), worker=worker, project=project)

    out = wait_for_jobflow(project, job.uuid)
    result = out.get("output", out) if isinstance(out, dict) else out
    assert isinstance(result, dict) and result.get("hostname"), (
        f"hello_hpc did not return a hostname from {project}/{worker}; got: {out!r}"
    )
