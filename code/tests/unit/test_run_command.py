"""Unit tests for the generic ``run_command`` primitive (``remote_jobs.jobs``).

``_run_command_impl`` is pure stdlib and runs in the current directory, so the full
behavior contract is covered offline -- no cluster, no LLM, no external engine. These
exercise the helper directly via ``monkeypatch.chdir`` into a tmp run dir. The five
validated behaviors under test: stdout/stderr redirected to files + returned as a bounded
tail; nonzero exit / timeout returned as data (never raised); recursive ``produced_files``
that captures an output directory; ``env``/``setup`` injection; and ``run_dir`` reporting.
"""

from __future__ import annotations

import os

from remote_jobs.jobs import _run_command_impl


def test_writes_inputs_and_runs(monkeypatch, tmp_path):
    """input_files are written into the run dir and the command can read them."""
    monkeypatch.chdir(tmp_path)
    res = _run_command_impl({"a.txt": "hi"}, "cat a.txt")
    assert (tmp_path / "a.txt").read_text() == "hi"
    assert res["returncode"] == 0
    assert res["timed_out"] is False
    assert "hi" in res["stdout_tail"]


def test_stdout_redirected_and_tailed(monkeypatch, tmp_path):
    """Full stdout lands on disk; only the last N lines come back in the tail."""
    monkeypatch.chdir(tmp_path)
    res = _run_command_impl(
        {}, 'for i in $(seq 1000); do echo "line$i"; done', stdout_tail_lines=10
    )
    on_disk = (tmp_path / "stdout.log").read_text().splitlines()
    assert len(on_disk) == 1000 and on_disk[-1] == "line1000"
    tail_lines = res["stdout_tail"].splitlines()
    assert len(tail_lines) == 10  # only the tail, not the whole 1000-line log
    assert "line1000" in res["stdout_tail"] and "line991" in res["stdout_tail"]
    assert "line990" not in res["stdout_tail"]


def test_nonzero_returncode_no_raise(monkeypatch, tmp_path):
    """A nonzero exit is returned as data, not raised."""
    monkeypatch.chdir(tmp_path)
    res = _run_command_impl({}, "exit 3")  # must not raise
    assert res["returncode"] == 3
    assert res["timed_out"] is False


def test_missing_binary_no_raise(monkeypatch, tmp_path):
    """A missing binary inside the command is a nonzero exit (127), not a spawn failure."""
    monkeypatch.chdir(tmp_path)
    res = _run_command_impl({}, "no_such_bin_xyz")  # must not raise
    assert res["returncode"] not in (0, None)
    assert res["timed_out"] is False


def test_timeout_sets_flag(monkeypatch, tmp_path):
    """A command exceeding timeout_s is killed; timed_out=True, returncode=None, no raise."""
    monkeypatch.chdir(tmp_path)
    res = _run_command_impl({}, "sleep 5", timeout_s=1)
    assert res["timed_out"] is True
    assert res["returncode"] is None


def test_env_injected(monkeypatch, tmp_path):
    """The env dict is merged into the subprocess environment."""
    monkeypatch.chdir(tmp_path)
    res = _run_command_impl({}, "echo $FOO", env={"FOO": "bar"})
    assert "bar" in res["stdout_tail"]


def test_setup_runs_before_command(monkeypatch, tmp_path):
    """The setup preamble runs in the same shell, before the command."""
    monkeypatch.chdir(tmp_path)
    res = _run_command_impl({}, "echo $BAZ", setup="export BAZ=qux")
    assert "qux" in res["stdout_tail"]


def test_produced_files_recursive(monkeypatch, tmp_path):
    """output_globs are matched recursively, so a nested output directory is captured."""
    monkeypatch.chdir(tmp_path)
    res = _run_command_impl(
        {}, "mkdir -p OUT.x/sub && echo data > OUT.x/sub/f", output_globs=["OUT.*/**"]
    )
    produced = {pf["path"]: pf["size"] for pf in res["produced_files"]}
    assert "OUT.x/sub/f" in produced and produced["OUT.x/sub/f"] > 0


def test_run_dir_is_cwd(monkeypatch, tmp_path):
    """run_dir is the per-job run dir (the current working directory)."""
    monkeypatch.chdir(tmp_path)
    res = _run_command_impl({}, "true")
    assert os.path.realpath(res["run_dir"]) == os.path.realpath(str(tmp_path))
