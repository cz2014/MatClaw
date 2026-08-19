"""Standalone real-ipykernel behavior for KernelManager."""

from __future__ import annotations

import queue
import time
from pathlib import Path


def test_default_and_on_demand_kernel_lifecycle(kernel_pool):
    assert {"default", "probe"} <= set(kernel_pool.kernels)
    assert all(kernel.manager.is_alive() for kernel in kernel_pool.kernels.values())


def test_namespace_persists_within_kernel_and_isolated_between(kernel_pool):
    assert not kernel_pool.execute("p3_persistent = 41", "default", 10).get("error")
    same = kernel_pool.execute("p3_persistent + 1", "default", 10)
    assert same["output"] == 42
    isolated = kernel_pool.execute("p3_persistent", "probe", 10)
    assert isolated["error"]["ename"] == "NameError"


def test_trailing_expression_preserves_picklable_value(kernel_pool):
    result = kernel_pool.execute("{'energy': -1.25, 'forces': [1, 2]}", "default", 10)
    assert result["output"] == {"energy": -1.25, "forces": [1, 2]}


def test_unpicklable_trailing_expression_degrades_to_repr(kernel_pool):
    result = kernel_pool.execute("lambda x: x", "default", 10)
    assert "function" in result["output"]
    assert "not picklable" in result["note"]


def test_kernel_local_class_output_falls_back_when_harness_cannot_unpickle(kernel_pool):
    result = kernel_pool.execute(
        "class P3LocalOutput:\n    pass\nP3LocalOutput()", "default", 10
    )
    assert "P3LocalOutput" in result["output"]
    assert "could not be unpickled" in result["note"]


def test_unpicklable_output_with_broken_repr_degrades_safely(kernel_pool):
    result = kernel_pool.execute(
        "class BrokenRepr:\n"
        "    def __repr__(self):\n"
        "        raise RuntimeError('repr boom')\n"
        "    def __reduce__(self):\n"
        "        raise TypeError('pickle boom')\n"
        "BrokenRepr()",
        "probe",
        10,
    )
    assert not result.get("error")
    assert "unrepresentable BrokenRepr" in result["output"]
    assert "repr failed" in result["note"]


def test_final_answer_crosses_process_and_survives_exception_handler(kernel_pool):
    result = kernel_pool.execute(
        "try:\n    final_answer({'done': True})\nexcept Exception:\n    print('swallowed')",
        "default",
        10,
    )
    assert result["is_final_answer"] is True
    assert result["output"] == {"done": True}
    assert "swallowed" not in result["logs"]


def test_kernel_local_final_answer_always_unwinds_with_repr_fallback(kernel_pool):
    result = kernel_pool.execute(
        "class P3LocalAnswer:\n    pass\n"
        "try:\n    final_answer(P3LocalAnswer())\n"
        "except Exception:\n    print('must-not-continue')",
        "default",
        10,
    )
    assert result["is_final_answer"] is True
    assert "P3LocalAnswer" in result["output"]
    assert "could not be unpickled" in result["note"]


def test_final_answer_with_broken_repr_still_unwinds(kernel_pool):
    result = kernel_pool.execute(
        "class BrokenFinal:\n"
        "    def __repr__(self):\n"
        "        raise RuntimeError('repr boom')\n"
        "    def __reduce__(self):\n"
        "        raise TypeError('pickle boom')\n"
        "try:\n"
        "    final_answer(BrokenFinal())\n"
        "except Exception:\n"
        "    print('continued')",
        "probe",
        10,
    )
    assert result["is_final_answer"] is True
    assert "unrepresentable BrokenFinal" in result["output"]
    assert "continued" not in result["logs"]
    assert "repr failed" in result["note"]
    assert "must-not-continue" not in result["logs"]


def test_same_cell_catch_then_raise_is_never_a_final_answer(kernel_pool):
    """A cell that ends in an uncaught error cannot claim an earlier final answer."""
    result = kernel_pool.execute(
        "try:\n    final_answer('hijacked')\nexcept BaseException:\n    pass\n"
        "raise ValueError('real failure')",
        "probe",
        10,
    )
    assert result["is_final_answer"] is False
    assert result["error"]["ename"] == "ValueError"
    assert "real failure" in result["error"]["evalue"]
    assert result["output"] is None
    follow_up = kernel_pool.execute("'clean'", "probe", 10)
    assert follow_up["is_final_answer"] is False and follow_up["output"] == "clean"


def test_error_preserves_partial_stdout_and_traceback(kernel_pool):
    result = kernel_pool.execute("print('before', flush=True)\nraise ValueError('boom')", "default", 10)
    assert result["error"]["ename"] == "ValueError"
    assert "boom" in result["error"]["evalue"]
    assert "before" in result["logs"] and "ValueError" in result["logs"]


def test_wait_command_timeout_is_capped_at_max(fresh_manager, monkeypatch):
    fresh_manager.execute("import time\ntime.sleep(3)", "default", 1)
    execution = fresh_manager.kernels["default"].current
    assert execution is not None
    calls = []
    original_wait = execution.done.wait
    monkeypatch.setattr(
        execution.done, "wait", lambda timeout=None: calls.append(timeout) or original_wait(0.01)
    )
    fresh_manager.wait_command("default", timeout=100000)
    assert calls and max(calls) <= 72000


def test_roster_line_is_safe_under_concurrent_calls(kernel_pool):
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=4) as pool:
        rosters = list(pool.map(lambda _: kernel_pool.roster_line(), range(16)))
    assert all(roster.startswith("kernels: ") for roster in rosters)


def test_error_observation_is_clean_and_line_aligned(kernel_pool):
    """Failing steps show the agent's own source lines with no harness noise."""
    code = "# kernel: default\ndef f():\n    raise ValueError('boom')\nf()"
    result = kernel_pool.execute(code, "default", 10)
    traceback_text = "\n".join(result["error"]["traceback"])
    assert "raise ValueError('boom')" in traceback_text
    for noise in ("_matclaw_execute", "b64decode", "\x1b[", "Could not get source"):
        assert noise not in traceback_text, f"harness noise in traceback: {noise!r}"
    assert "\x1b[" not in result["logs"] and "_matclaw_execute" not in result["logs"]


def test_timeout_keeps_kernel_busy_and_other_kernel_usable(kernel_pool):
    try:
        running = kernel_pool.execute(
            "import time\nprint('started', flush=True)\ntime.sleep(2)\n'done'", "default", 1
        )
        assert running["running"] is True
        other = kernel_pool.execute("6 * 7", "probe", 10)
        assert other["output"] == 42
        done = kernel_pool.wait_command("default", timeout=3)
        assert done["running"] is False and done["output"] == "done"
    finally:
        if kernel_pool.kernels["default"].current is not None:
            kernel_pool.kill_command("default")


def test_busy_target_refusal_has_roster_and_same_log(kernel_pool):
    try:
        first = kernel_pool.execute("import time; time.sleep(5)", "default", 1)
        refused = kernel_pool.execute("raise AssertionError('must not run')", "default", 1)
        assert refused["running"] and refused["refused"]
        assert refused["log_file"] == first["log_file"]
        assert "default(busy" in refused["roster"]
    finally:
        kernel_pool.kill_command("default")


def test_spool_grows_while_step_is_running(kernel_pool):
    try:
        result = kernel_pool.execute(
            "import time\nprint('first-byte', flush=True)\ntime.sleep(5)", "default", 1
        )
        log = kernel_pool.workspace / result["log_file"]
        assert result["running"] and log.exists()
        assert "first-byte" in log.read_text()
    finally:
        kernel_pool.kill_command("default")


def test_large_logs_keep_head_tail_and_readable_spool(kernel_pool):
    result = kernel_pool.execute(
        "print('HEAD' + 'x' * 40000 + 'TAIL', flush=True)", "default", 10
    )
    assert result["truncated"] is True
    assert "HEAD" in result["logs"] and "TAIL" in result["logs"]
    assert "HEAD" in (kernel_pool.workspace / result["log_file"]).read_text()


def test_send_variables_pickles_and_rejects_unpicklable(kernel_pool):
    kernel_pool.send_variables({"p3_injected": 21})
    assert kernel_pool.execute("p3_injected * 2", "default", 10)["output"] == 42
    try:
        kernel_pool.send_variables({"bad": lambda: None})
    except TypeError as exc:
        assert "not picklable" in str(exc)
    else:
        raise AssertionError("unpicklable send_variables value was accepted")


def test_stateless_tool_bootstrap_works(kernel_pool):
    result = kernel_pool.execute("write_file('kernel_tool.txt', 'ok')", "probe", 10)
    assert Path(result["output"]).read_text() == "ok"


def test_disabled_stateful_tools_are_absent_after_bootstrap(fresh_manager):
    from dataclasses import replace

    fresh_manager.tool_spec = replace(
        fresh_manager.tool_spec,
        disabled=(*fresh_manager.tool_spec.disabled, "bash", "wait_command", "kill_command"),
    )
    fresh_manager._restart(fresh_manager.kernels["default"])
    for name in ("bash", "wait_command", "kill_command"):
        result = fresh_manager.execute(name, "default", 10)
        assert result["error"]["ename"] == "NameError"
    final = fresh_manager.execute("final_answer('still essential')", "default", 10)
    assert final["is_final_answer"] and final["output"] == "still essential"


def test_stateful_bash_stub_roundtrip_uses_harness_server(kernel_pool):
    result = kernel_pool.execute("bash('printf rpc-ok')", "probe", 10)
    assert result["output"]["stdout"] == "rpc-ok"
    assert result["output"]["returncode"] == 0


def test_fourth_kernel_refused_with_roster(fresh_manager):
    assert fresh_manager.execute("1", "probe", 10)["output"] == 1
    assert fresh_manager.execute("2", "third", 10)["output"] == 2
    refused = fresh_manager.execute("3", "fourth", 10)
    assert refused["refused"] is True and "kernel cap 3" in refused["error"]
    assert all(name in refused["roster"] for name in ("default", "probe", "third"))


def test_kernel_crash_does_not_kill_other_kernel(fresh_manager):
    assert fresh_manager.execute("40 + 2", "probe", 10)["output"] == 42
    crashed = fresh_manager.execute("import os; os._exit(7)", "default", 10)
    assert crashed["error"]["ename"] == "KernelDied"
    assert crashed["namespace_preserved"] is False
    assert fresh_manager.execute("6 * 7", "probe", 10)["output"] == 42
    restarted = fresh_manager.execute("1 + 1", "default", 10)
    assert restarted["output"] == 2


def test_lazy_completion_note_prepended_to_next_use(kernel_pool):
    running = kernel_pool.execute("import time; time.sleep(1.2)", "default", 1)
    assert running["running"]
    time.sleep(0.4)
    next_result = kernel_pool.execute("'next'", "default", 10)
    assert next_result["output"] == "next"
    assert any("completed" in note for note in next_result["completion_notes"])


def test_completion_notes_survive_a_superseding_step(fresh_manager):
    """Two kernels reaped in one roster render both keep their completion note."""
    for name in ("probe", "third"):
        assert fresh_manager.execute("1", name, 10)["output"] == 1
    assert fresh_manager.execute("import time; time.sleep(3); 'p'", "probe", 1)["running"]
    assert fresh_manager.execute("import time; time.sleep(2.5); 't'", "third", 1)["running"]
    time.sleep(2.2)
    fresh_manager.roster_line()
    result = fresh_manager.execute("'next'", "probe", 10)
    notes = result["completion_notes"]
    assert any("kernel probe step completed" in note for note in notes)
    assert any("kernel third step completed" in note for note in notes)


def test_background_completion_is_never_delivered_twice(fresh_manager):
    assert fresh_manager.execute("import time; time.sleep(1.2); 'echoed'", "probe", 1)["running"]
    time.sleep(1.6)
    fresh_manager.roster_line()
    elsewhere = fresh_manager.execute("'elsewhere'", "default", 10)
    assert any("kernel probe step completed" in note for note in elsewhere["completion_notes"])
    late = fresh_manager.wait_command("probe", timeout=1)
    assert late["running"] is False
    assert not late.get("completion_notes")
    assert "echoed" not in repr(late)


def test_late_wait_collects_completed_result(kernel_pool):
    running = kernel_pool.execute("import time; time.sleep(1.1); 'late'", "default", 1)
    assert running["running"]
    time.sleep(0.3)
    result = kernel_pool.wait_command("default", timeout=1)
    assert result["running"] is False and result["output"] == "late"


def test_completion_during_vitals_is_collected_atomically(monkeypatch, kernel_pool):
    original = kernel_pool.vitals

    def slow_vitals(name):
        time.sleep(0.2)
        return original(name)

    monkeypatch.setattr(kernel_pool, "vitals", slow_vitals)
    result = kernel_pool.execute("import time; time.sleep(1.05); 4242", "default", 1)
    assert result["running"] is False and result["output"] == 4242


def test_execute_replies_are_drained(kernel_pool):
    for value in range(5):
        assert kernel_pool.execute(str(value), "probe", 10)["output"] == value
    try:
        leftover = kernel_pool.kernels["probe"].client.get_shell_msg(timeout=0.1)
    except queue.Empty:
        return
    raise AssertionError(f"undrained shell message: {leftover['header']['msg_type']}")


def test_live_unserializable_handle_reused_across_steps(kernel_pool):
    created = kernel_pool.execute(
        "p3_hot_handle = open('hot_handle.txt', 'w'); p3_hot_handle.write('hot')",
        "probe",
        10,
    )
    assert not created.get("error")
    reused = kernel_pool.execute(
        "p3_hot_handle.flush(); (not p3_hot_handle.closed, p3_hot_handle.tell())", "probe", 10
    )
    assert reused["output"] == (True, 3)
    kernel_pool.execute("p3_hot_handle.close()", "probe", 10)
