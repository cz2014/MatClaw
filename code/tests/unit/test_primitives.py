"""Unit tests for the P4 basic agent primitives (O3).

Covers the renamed IO helpers (read_file/write_file) and the mainstream basic-tool
set added in P4 (edit_file/grep/glob/bash), reproducing the upstream behaviors the
plan specifies (Claude Read/Write/Edit/Glob/Grep/Bash) and the deliberate code-action
adaptations (RAW read, structured grep/glob/bash returns, path confinement). Tools are
exercised directly via .forward() against tmp_path-scoped roots.
"""

from __future__ import annotations

import json
import os
import shutil

import pytest

from core.tools import (
    BashTool,
    EditFileTool,
    GlobTool,
    GrepTool,
    ReadFileTool,
    WriteFileTool,
)

requires_rg = pytest.mark.skipif(shutil.which("rg") is None, reason="ripgrep (rg) not installed")


# -- read_file (mirrors Claude Read) ------------------------------------------


def test_read_file_returns_raw(tmp_path):
    """RAW by default (no cat -n) so the result composes directly in code."""
    (tmp_path / "d.json").write_text('{"a": 1, "b": [2, 3]}')
    out = ReadFileTool(tmp_path).forward("d.json")
    assert json.loads(out) == {"a": 1, "b": [2, 3]}  # parses back, unmodified


def test_read_file_offset_limit_and_2000_default(tmp_path):
    (tmp_path / "big.txt").write_text("\n".join(f"line{i}" for i in range(1, 2501)))
    t = ReadFileTool(tmp_path)
    default = t.forward("big.txt")
    assert "line1\n" in default + "\n" and "line2000" in default
    assert "line2001" not in default
    assert "truncated" in default.lower()
    page = t.forward("big.txt", offset=2001)
    assert "line2001" in page and "line2500" in page
    assert "line2000\n" not in page


def test_read_file_long_line_truncation(tmp_path):
    (tmp_path / "long.txt").write_text("x" * 3000)
    t = ReadFileTool(tmp_path)
    # RAW mode is faithful (composes in code) -- no long-line truncation:
    assert "x" * 3000 in t.forward("long.txt")
    # view mode (line_numbers) truncates at 2000 chars/line, Claude-style:
    viewed = t.forward("long.txt", line_numbers=True)
    assert "[line truncated]" in viewed
    assert "x" * 2000 in viewed and "x" * 2001 not in viewed


def test_read_file_path_traversal_rejected(tmp_path):
    with pytest.raises(ValueError):
        ReadFileTool(tmp_path).forward("../escape.txt")


# -- write_file (mirrors Claude Write) ----------------------------------------


def test_write_file_overwrite_and_auto_mkdir(tmp_path):
    t = WriteFileTool(tmp_path)
    p = t.forward("a/b/c.txt", "hello")
    assert (tmp_path / "a" / "b" / "c.txt").read_text() == "hello"
    t.forward("a/b/c.txt", "world")  # full overwrite, no append
    assert (tmp_path / "a" / "b" / "c.txt").read_text() == "world"


def test_write_file_size_cap(tmp_path):
    with pytest.raises(ValueError):
        WriteFileTool(tmp_path).forward("big.txt", "x" * 5_000_001)


# -- edit_file (mirrors Claude Edit) ------------------------------------------


def test_edit_file_exact_unique_replace(tmp_path):
    (tmp_path / "f.txt").write_text("alpha beta gamma")
    EditFileTool(tmp_path).forward("f.txt", "beta", "BETA")
    assert (tmp_path / "f.txt").read_text() == "alpha BETA gamma"


def test_edit_file_nonunique_errors(tmp_path):
    (tmp_path / "f.txt").write_text("x x x")
    with pytest.raises(ValueError):
        EditFileTool(tmp_path).forward("f.txt", "x", "y")


def test_edit_file_replace_all(tmp_path):
    (tmp_path / "f.txt").write_text("x x x")
    EditFileTool(tmp_path).forward("f.txt", "x", "y", replace_all=True)
    assert (tmp_path / "f.txt").read_text() == "y y y"


def test_edit_file_absent_old_errors(tmp_path):
    (tmp_path / "f.txt").write_text("hello")
    with pytest.raises(ValueError):
        EditFileTool(tmp_path).forward("f.txt", "nope", "x")


# -- grep (mirrors Claude Grep; ripgrep front-end) ----------------------------


@requires_rg
def test_grep_files_with_matches_default(tmp_path):
    (tmp_path / "a.py").write_text("import os\nclass Foo:\n    pass\n")
    (tmp_path / "b.py").write_text("x = 1\n")
    res = GrepTool([tmp_path], tmp_path).forward("class Foo", path=str(tmp_path))
    assert isinstance(res, list)
    assert any(r.endswith("a.py") for r in res)
    assert not any(r.endswith("b.py") for r in res)


@requires_rg
def test_grep_content_mode_structured(tmp_path):
    (tmp_path / "a.py").write_text("import os\nclass Foo:\n    pass\n")
    res = GrepTool([tmp_path], tmp_path).forward("class Foo", path=str(tmp_path), output_mode="content")
    assert isinstance(res, dict) and "matches" in res and "truncated" in res
    m = res["matches"][0]
    assert {"file", "line", "text"} <= set(m)
    assert m["line"] == 2 and "class Foo" in m["text"]


@requires_rg
def test_grep_count_mode(tmp_path):
    (tmp_path / "c.py").write_text("a\na\na\n")
    res = GrepTool([tmp_path], tmp_path).forward("a", path=str(tmp_path / "c.py"), output_mode="count")
    assert isinstance(res, dict)
    assert list(res.values())[0] == 3


@requires_rg
def test_grep_glob_type_filters(tmp_path):
    (tmp_path / "x.py").write_text("needle\n")
    (tmp_path / "x.txt").write_text("needle\n")
    t = GrepTool([tmp_path], tmp_path)
    by_glob = t.forward("needle", path=str(tmp_path), glob="*.py")
    assert any(r.endswith("x.py") for r in by_glob) and not any(r.endswith("x.txt") for r in by_glob)
    by_type = t.forward("needle", path=str(tmp_path), type="py")
    assert any(r.endswith("x.py") for r in by_type) and not any(r.endswith("x.txt") for r in by_type)


@requires_rg
def test_grep_case_insensitive_and_context(tmp_path):
    (tmp_path / "f.txt").write_text("LINE1\nNeedle here\nLINE3\n")
    res = GrepTool([tmp_path], tmp_path).forward(
        "needle", path=str(tmp_path / "f.txt"), output_mode="content", case_insensitive=True, context=1
    )
    texts = [m["text"] for m in res["matches"]]
    assert any("Needle here" in tx for tx in texts)  # matched case-insensitively
    assert any("LINE1" in tx for tx in texts) and any("LINE3" in tx for tx in texts)  # context lines


@requires_rg
def test_grep_head_limit_truncated_flag(tmp_path):
    (tmp_path / "f.txt").write_text("m\n" * 10)
    res = GrepTool([tmp_path], tmp_path).forward(
        "m", path=str(tmp_path / "f.txt"), output_mode="content", head_limit=3
    )
    assert len(res["matches"]) == 3 and res["truncated"] is True


@requires_rg
def test_grep_path_confined(tmp_path):
    with pytest.raises(ValueError):
        GrepTool([tmp_path], tmp_path).forward("x", path="/etc")


@requires_rg
def test_grep_searches_gitignored_paths(tmp_path):
    """P5c: grep uses --no-ignore so it can search the installed package source, which lives in a
    gitignored venv -- without it, ripgrep would skip the whole tree and retrieval would return nothing."""
    (tmp_path / ".gitignore").write_text("venv/\n")
    (tmp_path / "venv").mkdir()
    (tmp_path / "venv" / "mod.py").write_text("class Needle:\n    pass\n")
    res = GrepTool([tmp_path], tmp_path).forward("class Needle", path=str(tmp_path), output_mode="files_with_matches")
    assert any(r.endswith("mod.py") for r in res), "grep must find files inside a .gitignored dir"


# -- glob (mirrors Claude Glob) -----------------------------------------------


def test_glob_recursive_mtime_sorted_capped(tmp_path):
    d = tmp_path / "src"
    d.mkdir()
    for i in range(120):
        f = d / f"f{i}.py"
        f.write_text("x")
        os.utime(f, (i + 1, i + 1))  # strictly increasing mtime
    res = GlobTool([tmp_path], tmp_path).forward("src/**/*.py")
    assert len(res) == 100  # capped
    assert res[0].endswith("f119.py")  # most-recently-modified first
    assert all(r.startswith("src" + os.sep) for r in res)  # workspace-relative


def test_glob_does_not_apply_gitignore(tmp_path):
    (tmp_path / ".gitignore").write_text("ignored.py\n")
    (tmp_path / "ignored.py").write_text("x")
    (tmp_path / "visible.py").write_text("x")
    names = {os.path.basename(r) for r in GlobTool([tmp_path], tmp_path).forward("*.py")}
    assert "ignored.py" in names and "visible.py" in names


# -- bash (mirrors Claude Bash / OpenAI ShellTool) ----------------------------


def test_bash_captures_stdout_and_stderr(tmp_path):
    res = BashTool(tmp_path).forward("echo out; echo err 1>&2")
    assert res["stdout"].strip() == "out"
    assert res["stderr"].strip() == "err"
    assert res["returncode"] == 0 and res["truncated"] is False


def test_bash_timeout_enforced(tmp_path):
    res = BashTool(tmp_path).forward("sleep 5", timeout=1)
    assert res.get("timed_out") is True
    assert res["returncode"] is None


def test_bash_output_cap_truncated_flag(tmp_path):
    res = BashTool(tmp_path).forward("printf '%0500d' 0", max_output_chars=100)
    assert len(res["stdout"]) == 100 and res["truncated"] is True


def test_bash_default_cwd_is_workspace(tmp_path):
    (tmp_path / "marker.txt").write_text("hi")
    res = BashTool(tmp_path).forward("ls")
    assert "marker.txt" in res["stdout"]
    pwd = BashTool(tmp_path).forward("pwd -P")["stdout"].strip()
    from pathlib import Path

    assert Path(pwd).resolve() == tmp_path.resolve()
