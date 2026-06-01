"""Unit tests for the thin exec() executor (P4 O1, the crux change).

Drives core.exec.ExecPythonExecutor directly against the PythonExecutor contract
the vendored CodeAgent relies on. Asserts the opened-runtime behavior (full
imports incl. open(), no op-cap) and the parity points (state persistence,
final_answer sentinel, stdout capture incl. on error, last-expression output).

These also close the P0-deferred "executor sandbox" test, now with the permissive
expectation: the swap's whole point is that there is no allow-list to assert.
"""

from __future__ import annotations

import signal

import pytest

from core.exec import ExecPythonExecutor


def _exec(exec_timeout_s=None):
    ex = ExecPythonExecutor(exec_timeout_s=exec_timeout_s)
    ex.send_variables({})
    ex.send_tools({})  # injects the final_answer sentinel
    return ex


# -- opened runtime: the three driver errors are gone -------------------------


def test_imports_unrestricted():
    """Modules absent from the old allow-list (os/subprocess/pathlib/shutil/glob/re) import freely."""
    out = _exec()(
        "import os, subprocess, pathlib, shutil, glob, re, tempfile\n"
        "ok = all(m is not None for m in (os, subprocess, pathlib, shutil, glob, re, tempfile))\n"
        "ok"
    )
    assert out.output is True


def test_open_builtin_read_write(tmp_path):
    """The previously-banned open() builtin is available for native read/write."""
    p = tmp_path / "f.txt"
    out = _exec()(
        f"_w = open({str(p)!r}, 'w'); _w.write('data'); _w.close()\n"
        f"open({str(p)!r}).read()"
    )
    assert out.output == "data"
    assert p.read_text() == "data"


def test_no_op_cap():
    """A pure-Python loop exceeding MAX_OPERATIONS=10_000_000 completes (cap removed, D-P4-3).

    A >1M loop would not trip the real 10M AST cap, so the loop must exceed 10M to
    actually prove the cap is gone.
    """
    out = _exec()("total = 0\nfor _i in range(11_000_000):\n    total += 1\ntotal")
    assert out.output == 11_000_000


# -- contract parity ----------------------------------------------------------


def test_state_persists_across_calls():
    ex = _exec()
    ex("a = 7")
    out = ex("a + 1")
    assert out.output == 8


def test_send_variables_injects():
    ex = ExecPythonExecutor()
    ex.send_variables({"foo": 99})
    ex.send_tools({})
    assert ex("foo * 2").output == 198


def test_send_tools_exposes_tools_and_final_answer():
    ex = ExecPythonExecutor()
    ex.send_variables({})
    ex.send_tools({"shout": lambda s: s.upper()})
    out = ex("print(shout('hi'))")
    assert "HI" in out.logs
    # final_answer is always injected alongside the supplied tools.
    assert "final_answer" in ex.state


def test_final_answer_sets_is_final_and_output():
    out = _exec()("final_answer(42)")
    assert out.is_final_answer is True
    assert out.output == 42


def test_final_answer_survives_try_except_Exception():
    """The BaseException sentinel must not be swallowed by the agent's own try/except."""
    out = _exec()(
        "try:\n"
        "    final_answer('done')\n"
        "except Exception:\n"
        "    print('swallowed')"
    )
    assert out.is_final_answer is True
    assert out.output == "done"
    assert "swallowed" not in out.logs


def test_print_captured_in_logs():
    out = _exec()("print('hello world')")
    assert "hello world" in out.logs


def test_partial_stdout_on_error():
    """On a real exception the loop reads state['_print_outputs'] for partial logs (parity)."""
    ex = _exec()
    with pytest.raises(ValueError):
        ex("print('before')\nraise ValueError('boom')")
    assert "before" in ex.state["_print_outputs"]


def test_trailing_expression_is_output():
    """A trailing bare expression becomes CodeOutput.output (preserves 'Out: ...')."""
    out = _exec()("x = 5\nx * 2")
    assert out.output == 10


def test_no_trailing_expression_output_is_none():
    """A block ending in a statement (not an expression) yields output None."""
    out = _exec()("y = 3")
    assert out.output is None
    assert out.is_final_answer is False


# -- opt-in wall-clock watchdog (D-P4-3) --------------------------------------


def test_watchdog_off_by_default():
    """No deadline is armed unless exec_timeout_s is set (a fast op completes normally)."""
    assert _exec()("1 + 1").output == 2


@pytest.mark.skipif(not hasattr(signal, "SIGALRM"), reason="SIGALRM watchdog needs a POSIX platform")
def test_watchdog_interrupts_hang():
    """The opt-in SIGALRM watchdog bounds a hung step and surfaces a TimeoutError."""
    ex = _exec(exec_timeout_s=0.5)
    with pytest.raises(TimeoutError):
        ex("while True:\n    pass")
    # The deadline is disarmed afterward: a subsequent fast call is unaffected.
    assert ex("2 + 2").output == 4
