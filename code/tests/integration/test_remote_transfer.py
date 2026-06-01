"""Integration test for remote_put, remote_get, and remote_ls.

Tests all three sandbox remote transfer functions against a live HPC connection.
Uses perlmutter_debug by default.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def main():
    parser = argparse.ArgumentParser(description="Test remote transfer functions")
    parser.add_argument("--project", default="perlmutter")
    parser.add_argument("--worker", default="perlmutter_debug")
    parser.add_argument(
        "--remote-dir",
        default=os.environ.get("MATCLAW_TEST_REMOTE_DIR"),
        help="Writable remote scratch dir (or set $MATCLAW_TEST_REMOTE_DIR). "
             "On NERSC use your own $SCRATCH, e.g. /pscratch/sd/<x>/<user>/agent_tmp_dir.",
    )
    args = parser.parse_args()
    if not args.remote_dir:
        parser.error("--remote-dir is required (or set $MATCLAW_TEST_REMOTE_DIR)")

    from core.tools import RemoteGetTool, RemoteLsTool, RemotePutTool

    workspace = PROJECT_ROOT / "workspace_test_remote"
    workspace.mkdir(parents=True, exist_ok=True)
    remote_put = RemotePutTool(workspace)
    remote_get = RemoteGetTool(workspace)
    remote_ls = RemoteLsTool()

    test_subdir = f"{args.remote_dir}/test_remote_transfer"

    # --- Test 1: remote_put (single file) ---
    print("=== Test 1: remote_put (single file) ===")
    test_content = "Hello from test_remote_transfer.py\nLine 2\n"
    (workspace / "test_upload.txt").write_text(test_content)

    remote_path = remote_put(
        "test_upload.txt", test_subdir, args.project, args.worker
    )
    print(f"Uploaded to: {remote_path}")
    assert remote_path == f"{test_subdir}/test_upload.txt"

    # --- Test 2: remote_ls ---
    print("\n=== Test 2: remote_ls ===")
    entries = remote_ls(test_subdir, args.project, args.worker)
    print(f"Files in {test_subdir}: {entries}")
    assert "test_upload.txt" in entries, f"test_upload.txt not found in {entries}"

    # --- Test 3: remote_get (single file) ---
    print("\n=== Test 3: remote_get (single file) ===")
    local_path = remote_get(
        f"{test_subdir}/test_upload.txt",
        "downloaded_test.txt",
        args.project,
        args.worker,
    )
    print(f"Downloaded to: {local_path}")
    downloaded = Path(local_path).read_text()
    assert downloaded == test_content, f"Content mismatch: {downloaded!r}"

    # --- Test 4: remote_put (directory) ---
    print("\n=== Test 4: remote_put (directory) ===")
    test_dir = workspace / "test_dir"
    test_dir.mkdir(exist_ok=True)
    (test_dir / "a.txt").write_text("file a")
    (test_dir / "b.txt").write_text("file b")
    sub = test_dir / "sub"
    sub.mkdir(exist_ok=True)
    (sub / "c.txt").write_text("file c")

    remote_dir_path = remote_put(
        "test_dir", test_subdir, args.project, args.worker
    )
    print(f"Uploaded dir to: {remote_dir_path}")

    dir_entries = remote_ls(
        f"{test_subdir}/test_dir", args.project, args.worker
    )
    print(f"Remote dir contents: {dir_entries}")
    assert "a.txt" in dir_entries
    assert "b.txt" in dir_entries
    assert "sub" in dir_entries

    # --- Test 5: remote_get (directory) ---
    print("\n=== Test 5: remote_get (directory) ===")
    local_dir = remote_get(
        f"{test_subdir}/test_dir",
        "downloaded_dir",
        args.project,
        args.worker,
    )
    print(f"Downloaded dir to: {local_dir}")
    dl = Path(local_dir)
    assert (dl / "a.txt").read_text() == "file a"
    assert (dl / "b.txt").read_text() == "file b"
    assert (dl / "sub" / "c.txt").read_text() == "file c"

    # --- Test 6: remote_ls (nonexistent dir) ---
    print("\n=== Test 6: remote_ls (nonexistent dir) ===")
    try:
        empty_entries = remote_ls(
            f"{test_subdir}/nonexistent_dir_12345", args.project, args.worker
        )
        print(f"Nonexistent dir entries: {empty_entries}")
        assert empty_entries == [], f"Expected empty list, got {empty_entries}"
    except FileNotFoundError:
        print("Got FileNotFoundError (acceptable for nonexistent dir)")

    # --- Cleanup ---
    print("\n=== Cleanup ===")
    shutil.rmtree(workspace, ignore_errors=True)
    print("Local workspace cleaned")

    from jobflow_remote.config.manager import ConfigManager
    cm = ConfigManager()
    project = cm.get_project(args.project)
    worker = project.workers[args.worker]
    host = worker.get_host()
    host.connect()
    host.rmtree(test_subdir)
    print(f"Remote {test_subdir} cleaned")

    print("\nPASS: all remote transfer tests passed")


if __name__ == "__main__":
    main()
