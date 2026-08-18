"""Thin executor contract and real-kernel integration tests."""

from __future__ import annotations

import time
from types import SimpleNamespace

import psutil
import pytest

from core.exec import ExecPythonExecutor, _bare_control_call


def _exec(manager):
    executor = ExecPythonExecutor(manager)
    executor.send_variables({})
    executor.send_tools({})
    return executor


def _finished_background_pid(state, command: str) -> int:
    pid = state.run_bash(command, run_in_background=True)["pid"]
    record = state.background[pid]
    deadline = time.monotonic() + 5
    while record.proc.poll() is None and time.monotonic() < deadline:
        time.sleep(0.05)
    assert record.proc.poll() is not None
    return pid


def test_imports_unrestricted(fresh_manager):
    out = _exec(fresh_manager)(
        "import os, subprocess, pathlib, shutil, glob, re, tempfile\n"
        "all(m is not None for m in (os, subprocess, pathlib, shutil, glob, re, tempfile))"
    )
    assert out.output is True


def test_open_builtin_read_write(fresh_manager, tmp_path):
    path = tmp_path / "f.txt"
    out = _exec(fresh_manager)(
        f"_w = open({str(path)!r}, 'w'); _w.write('data'); _w.close()\n"
        f"open({str(path)!r}).read()"
    )
    assert out.output == "data" and path.read_text() == "data"


def test_no_op_cap(fresh_manager):
    out = _exec(fresh_manager)(
        "total = 0\nfor _i in range(11_000_000):\n    total += 1\ntotal"
    )
    assert out.output == 11_000_000


def test_state_persists_across_calls(fresh_manager):
    executor = _exec(fresh_manager)
    executor("executor_persist = 7")
    assert executor("executor_persist + 1").output == 8


def test_send_variables_crosses_to_kernel(fresh_manager):
    executor = ExecPythonExecutor(fresh_manager)
    executor.send_variables({"executor_foo": 99})
    executor.send_tools({})
    assert executor("executor_foo * 2").output == 198


def test_send_variables_rejects_unpicklable(fresh_manager):
    executor = ExecPythonExecutor(fresh_manager)
    with open(__file__) as handle, pytest.raises(TypeError, match="not picklable"):
        executor.send_variables({"handle": handle})


def test_shadow_state_tracks_injected_tools(fresh_manager, tmp_path):
    from core.tools import ReadFileTool

    executor = ExecPythonExecutor(fresh_manager)
    tool = ReadFileTool(tmp_path)
    executor.send_tools({"read_file": tool})
    assert executor.state["read_file"] is tool


def test_final_answer_sets_is_final_and_output(fresh_manager):
    out = _exec(fresh_manager)("final_answer(42)")
    assert out.is_final_answer is True and out.output == 42


def test_final_answer_survives_try_except_exception(fresh_manager):
    out = _exec(fresh_manager)(
        "try:\n"
        "    final_answer('done')\n"
        "except Exception:\n"
        "    print('swallowed')"
    )
    assert out.is_final_answer is True and out.output == "done"
    assert "swallowed" not in out.logs


def test_caught_baseexception_final_record_does_not_poison_next_step(fresh_manager):
    executor = _exec(fresh_manager)
    first = executor(
        "try:\n"
        "    final_answer('caught')\n"
        "except BaseException:\n"
        "    print('deliberately caught')"
    )
    assert first.is_final_answer is False
    with pytest.raises(RuntimeError, match="ValueError: real failure"):
        executor("raise ValueError('real failure')")


def test_print_captured_with_status_lines(fresh_manager):
    out = _exec(fresh_manager)("print('hello world')")
    assert "hello world" in out.logs
    assert "kernels: default(idle, rss " in out.logs
    assert out.logs.endswith("background: none")


def test_partial_stdout_and_status_on_error(fresh_manager):
    executor = _exec(fresh_manager)
    with pytest.raises(RuntimeError, match="ValueError: boom"):
        executor("print('before')\nraise ValueError('boom')")
    assert "before" in executor.state["_print_outputs"]
    assert "kernels:" in executor.state["_print_outputs"]


def test_background_failure_note_reaches_the_next_code_step_once(fresh_manager):
    executor = _exec(fresh_manager)
    state = fresh_manager.tool_server.state
    pid = _finished_background_pid(state, "exit 7")
    note = f"background PID {pid} completed with returncode 7"

    step = executor("1 + 1")
    assert step.output == 2
    assert step.logs.count(note) == 1
    assert note not in executor("2 + 2").logs
    assert note not in str(state.run_bash("printf later")["completion_notes"])


def test_note_drained_by_a_bash_call_is_not_repeated_by_a_code_step(fresh_manager):
    executor = _exec(fresh_manager)
    state = fresh_manager.tool_server.state
    pid = _finished_background_pid(state, "exit 3")
    note = f"background PID {pid} completed with returncode 3"

    assert note in state.run_bash("printf drained")["completion_notes"]
    assert note not in executor("1 + 1").logs


def test_trailing_expression_is_output(fresh_manager):
    assert _exec(fresh_manager)("x = 5\nx * 2").output == 10


def test_no_trailing_expression_output_is_none(fresh_manager):
    out = _exec(fresh_manager)("executor_y = 3")
    assert out.output is None and out.is_final_answer is False


def test_status_roster_reap_keeps_late_result_collectable(fresh_manager):
    executor = _exec(fresh_manager)
    first = executor("# kernel: default\n# timeout: 1\nimport time; time.sleep(1.2)\n42")
    assert first.output["running"] is True
    assert executor("# kernel: probe\nimport time; time.sleep(0.5)\n7").output == 7
    late = executor("wait_command('default', timeout=1)")
    assert late.output == 42
    following = executor("# kernel: probe\n'following-result'")
    assert following.output == "following-result"
    assert "output=42" not in following.logs


def test_same_kernel_reuse_surfaces_superseded_completion(fresh_manager):
    executor = _exec(fresh_manager)
    running = executor(
        "# timeout: 1\nimport time; time.sleep(1.2)\n'old-scientific-result'"
    )
    assert running.output["running"] is True
    assert executor("# kernel: probe\nimport time; time.sleep(0.5)\n'probe'").output == "probe"
    reused = executor("'new-result'")
    assert reused.output == "new-result"
    assert "old-scientific-result" in reused.logs


def test_same_kernel_reuse_surfaces_completion_even_when_new_step_runs(fresh_manager):
    executor = _exec(fresh_manager)
    executor("# timeout: 1\nimport time; time.sleep(1.2)\n'old-running-result'")
    executor("# kernel: probe\nimport time; time.sleep(0.5)")
    try:
        reused = executor("# timeout: 1\nimport time; time.sleep(10)")
        assert reused.output["running"] is True
        assert "old-running-result" in reused.logs
    finally:
        executor("kill_command('default')")


def test_assigned_wait_runs_inside_another_kernel(fresh_manager):
    executor = _exec(fresh_manager)
    running = executor("# timeout: 1\nimport time; time.sleep(10)")
    assert running.output["running"] is True
    try:
        checked = executor(
            "# kernel: probe\n"
            "r = wait_command('default', timeout=1)\n"
            "r['running']"
        )
        assert checked.output is True
        assert fresh_manager.execute("r['kernel']", "probe", 10)["output"] == "default"
    finally:
        executor("kill_command('default')")


def test_all_busy_fourth_kernel_refusal_is_free_checkin(fresh_manager):
    executor = _exec(fresh_manager)
    names = ("default", "probe", "analysis")
    try:
        for name in names:
            result = executor(f"# kernel: {name}\n# timeout: 1\nimport time; time.sleep(10)")
            assert result.output["running"] is True
        refused = executor("# kernel: fourth\n1 + 1")
        assert refused.output["refused"] is True
        assert "default(busy" in refused.logs and "analysis(busy" in refused.logs
    finally:
        for name in names:
            executor(f"kill_command({name!r})")


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("wait_command('default')", ("wait_command", {"target": "default"})),
        (
            "# comment\nwait_command('probe', timeout=2)",
            ("wait_command", {"target": "probe", "timeout": 2}),
        ),
        ("kill_command('default')", ("kill_command", {"target": "default"})),
        ("kill_command(target='probe')", ("kill_command", {"target": "probe"})),
    ],
)
def test_bare_control_call_exact_ast(code, expected):
    assert _bare_control_call(code) == expected


@pytest.mark.parametrize(
    "code",
    [
        "result = wait_command('default')",
        "wait_command(name)",
        "wait_command('default', 1, timeout=2)",
        "wait_command('default', timeout=1, timeout=2)",
        "wait_command(target='default', target='probe')",
        "wait_command('default', **options)",
        "print(wait_command('default'))",
        "kill_command('default', force=True)",
        "wait_command('default'); print('extra')",
    ],
)
def test_nonbare_or_nonliteral_control_call_is_not_escape_hatched(code):
    assert _bare_control_call(code) is None


class _StubState:
    def status_lines(self):
        return "bash: idle\nbackground: none"

    def take_completion_notes(self):
        return []


class _StubServer:
    def __init__(self):
        self.state = _StubState()
        self.calls = []
        self.stopped = False

    def dispatch(self, method, params):
        self.calls.append((method, params))
        return {"running": False, "method": method, "kernel": params["target"]}

    def stop(self):
        self.stopped = True


class _StubManager:
    def __init__(self, tmp_path):
        from core.tools import ToolSpec

        self.tool_server = _StubServer()
        self.tool_spec = ToolSpec(tmp_path, (tmp_path,), tmp_path, disabled=("web_fetch", "web_search"))
        self.executions = []
        self.variables = []
        self.stopped = False

    def send_variables(self, values):
        self.variables.append(values)

    def execute(self, code, kernel_name, timeout):
        self.executions.append((code, kernel_name, timeout))
        return {"running": False, "kernel": kernel_name, "output": 7, "logs": "ok"}

    def roster_line(self):
        return "kernels: default(idle)"

    def shutdown(self):
        self.stopped = True


def test_stub_pins_directive_routing_and_status_after_logs(tmp_path):
    manager = _StubManager(tmp_path)
    out = _exec(manager)("# kernel: probe\n# timeout: 9\n1 + 1")
    assert manager.executions == [("# kernel: probe\n# timeout: 9\n1 + 1", "probe", 9)]
    assert out.output == 7
    assert out.logs.startswith("ok\n") and out.logs.endswith("background: none")


def test_stub_bare_wait_runs_harness_side(tmp_path):
    manager = _StubManager(tmp_path)
    out = _exec(manager)("wait_command('default', timeout=3)")
    assert manager.executions == []
    assert manager.tool_server.calls == [("wait_command", {"target": "default", "timeout": 3})]
    assert out.output["method"] == "wait_command"


def test_send_tools_rejects_managed_agents(tmp_path):
    manager = _StubManager(tmp_path)
    with pytest.raises(TypeError, match="managed_agents"):
        ExecPythonExecutor(manager).send_tools({"worker": SimpleNamespace(name="worker")})


def test_send_tools_rejects_user_supplied_tools(tmp_path):
    from core._smol.tools import Tool

    class MyTool(Tool):
        name = "my_custom"
        description = "a user tool"
        inputs = {}
        output_type = "string"

        def forward(self):
            return "x"

    manager = _StubManager(tmp_path)
    with pytest.raises(ValueError, match="user-supplied tools"):
        ExecPythonExecutor(manager).send_tools({"my_custom": MyTool()})


def test_bare_kill_preserves_collected_final_answer(tmp_path):
    manager = _StubManager(tmp_path)
    manager.tool_server.dispatch = lambda method, params: {
        "running": False,
        "kernel": params["target"],
        "method": "noop",
        "is_final_answer": True,
        "output": {"energy": -1.25},
        "logs": "",
    }
    out = _exec(manager)("kill_command('default')")
    assert out.is_final_answer is True
    assert out.output == {"energy": -1.25}


def test_bare_kill_without_final_answer_returns_ladder_report(tmp_path):
    manager = _StubManager(tmp_path)
    out = _exec(manager)("kill_command('default')")
    assert out.is_final_answer is False
    assert out.output["method"] == "kill_command"


def test_cleanup_is_idempotent_and_orders_both_owners(tmp_path):
    manager = _StubManager(tmp_path)
    executor = ExecPythonExecutor(manager)
    executor.cleanup()
    executor.cleanup()
    assert manager.stopped and manager.tool_server.stopped


def test_real_cleanup_reaps_kernel_and_removes_socket(tmp_path):
    from core.kernel import KernelManager
    from core.tools import ToolSpec, _LocalExecState
    from core.toolserver import ToolServer

    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    server = ToolServer(state)
    socket_path = server.start()
    spec = ToolSpec(tmp_path, (tmp_path,), tmp_path, disabled=("web_fetch", "web_search"))
    manager = KernelManager(tmp_path, spec, server, grace_s=0.2)
    pid = manager.kernels["default"].pid
    executor = ExecPythonExecutor(manager, server)
    executor.cleanup()
    assert not psutil.pid_exists(pid)
    assert not socket_path.exists() and not socket_path.parent.exists()
    with pytest.raises(RuntimeError, match="closed"):
        executor("1 + 1")
    with pytest.raises(RuntimeError, match="closed"):
        executor.send_variables({"x": 1})
    with pytest.raises(RuntimeError, match="closed"):
        executor.send_tools({})
    assert manager.kernels == {}
