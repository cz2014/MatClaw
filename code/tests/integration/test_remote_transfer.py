"""Integration test for the remote_put / remote_get / remote_ls sandbox tools.

Exercises all three against a live HPC connection (cluster-agnostic via the ``hpc_target``
fixture). Needs a writable remote scratch dir in ``$MATCLAW_TEST_REMOTE_DIR`` (e.g. on NERSC
``/pscratch/sd/<x>/<user>/agent_tmp``; on Anvil ``/anvil/scratch/<user>/agent_tmp``). Skips
when no HPC project is configured or no remote dir is given. Best-effort cleans up the remote
dir afterwards.

Tier: integration. Run with:

    MATCLAW_TEST_REMOTE_DIR=/anvil/scratch/x-cz2014/agent_tmp \\
      uv run --project code --extra dev pytest code/tests -m integration --hpc-project anvil
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest


def test_remote_transfer_roundtrip(hpc_target, tmp_path):
    remote_root = os.environ.get("MATCLAW_TEST_REMOTE_DIR")
    if not remote_root:
        pytest.skip("set $MATCLAW_TEST_REMOTE_DIR to a writable remote scratch dir")

    from core.tools import RemoteGetTool, RemoteLsTool, RemotePutTool

    project, worker = hpc_target
    remote_put = RemotePutTool(tmp_path)
    remote_get = RemoteGetTool(tmp_path)
    remote_ls = RemoteLsTool()
    test_subdir = f"{remote_root}/test_remote_transfer"

    try:
        # --- single file round-trip ---
        content = "Hello from test_remote_transfer\nLine 2\n"
        (tmp_path / "up.txt").write_text(content)
        remote_path = remote_put("up.txt", test_subdir, project, worker)
        assert remote_path == f"{test_subdir}/up.txt"
        assert "up.txt" in remote_ls(test_subdir, project, worker)
        local = remote_get(f"{test_subdir}/up.txt", "down.txt", project, worker)
        assert Path(local).read_text() == content

        # --- directory round-trip ---
        tree = tmp_path / "tree"
        (tree / "sub").mkdir(parents=True)
        (tree / "a.txt").write_text("a")
        (tree / "sub" / "c.txt").write_text("c")
        remote_put("tree", test_subdir, project, worker)
        entries = remote_ls(f"{test_subdir}/tree", project, worker)
        assert {"a.txt", "sub"} <= set(entries), f"unexpected dir listing: {entries}"
        got = Path(remote_get(f"{test_subdir}/tree", "tree_dl", project, worker))
        assert (got / "a.txt").read_text() == "a"
        assert (got / "sub" / "c.txt").read_text() == "c"
    finally:
        # best-effort remote cleanup (don't fail the test on cleanup errors)
        try:
            from jobflow_remote.config.manager import ConfigManager

            host = ConfigManager().get_project(project).workers[worker].get_host()
            host.connect()
            host.rmtree(test_subdir)
        except Exception:
            pass
