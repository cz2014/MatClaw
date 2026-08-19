"""Unix-socket RPC tests for harness-owned stateful tools."""

from __future__ import annotations

import json
import socket
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from core.tools import _LocalExecState
from core.tools import _wait_if_paused
from core.toolserver import (
    FinalAnswerSignal,
    ToolClient,
    ToolServer,
    build_stateful_stubs,
)


@pytest.fixture
def server(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    instance = ToolServer(state)
    path = instance.start()
    try:
        yield instance, ToolClient(path)
    finally:
        instance.stop()


def test_bind_roundtrip_and_short_path(server):
    instance, client = server
    assert len(str(instance.socket_path).encode()) < 104
    assert client.call("pause_status") == {"paused": False}


def test_bash_roundtrip_merges_streams(server):
    _, client = server
    result = client.call("bash", {"command": "echo out; echo err 1>&2"})
    assert result["returncode"] == 0
    assert "out" in result["stdout"] and "err" in result["stdout"]


def test_wait_and_kill_roundtrip(server):
    _, client = server
    running = client.call("bash", {"command": "sleep 10", "timeout": 1})
    assert running["running"]
    check = client.call("wait_command", {"target": "bash", "timeout": 1})
    assert check["running"]
    killed = client.call("kill_command", {"target": "bash"})
    assert killed["running"] is False


def test_final_answer_roundtrip(server):
    instance, _ = server
    final_answer = build_stateful_stubs(str(instance.socket_path), "probe")["final_answer"]
    with pytest.raises(FinalAnswerSignal) as raised:
        final_answer({"energy": -1.25})
    assert raised.value.value == {"energy": -1.25}
    assert instance.take_final_answer("probe") == ({"energy": -1.25}, None)


def test_unpicklable_final_answer_degrades_with_note(server):
    instance, _ = server
    final_answer = build_stateful_stubs(str(instance.socket_path), "probe")["final_answer"]
    def value():
        return None

    with pytest.raises(FinalAnswerSignal) as raised:
        final_answer(value)
    stored, note = instance.take_final_answer("probe")
    assert isinstance(stored, str) and "function" in stored
    assert raised.value.note == note and "not picklable" in note


def test_unknown_method_does_not_kill_server(server):
    _, client = server
    with pytest.raises(RuntimeError, match="unknown RPC method"):
        client.call("missing")
    assert client.call("pause_status") == {"paused": False}


def test_malformed_json_does_not_kill_server(server):
    instance, client = server
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as raw:
        raw.connect(str(instance.socket_path))
        raw.sendall(b"not-json\n")
        response = json.loads(raw.makefile("rb").readline())
    assert response["error"]["type"] == "JSONDecodeError"
    assert client.call("pause_status") == {"paused": False}


def test_concurrent_clients(server):
    instance, _ = server

    def call_status(_):
        return ToolClient(instance.socket_path).call("pause_status")

    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(call_status, range(12)))
    assert len(results) == 12 and all(result == {"paused": False} for result in results)


def test_state_lives_in_harness_across_clients(server):
    instance, _ = server
    first = ToolClient(instance.socket_path)
    second = ToolClient(instance.socket_path)
    bg = first.call("bash", {"command": "sleep 10", "run_in_background": True})
    assert second.call("wait_command", {"target": str(bg["pid"]), "timeout": 1})[
        "running"
    ]
    second.call("kill_command", {"target": str(bg["pid"])})


def test_reaped_background_pid_is_still_collectable(server):
    """A finished background job stays reachable by PID after lazy reaping."""
    instance, client = server
    pid = client.call("bash", {"command": "echo done", "run_in_background": True})["pid"]
    deadline = time.monotonic() + 5
    while pid in instance.state.background and time.monotonic() < deadline:
        instance.state.status_lines()  # runs on every step return; triggers the reap
        time.sleep(0.05)
    assert pid in instance.state.completed
    result = client.call("wait_command", {"target": str(pid), "timeout": 1})
    assert result["running"] is False
    assert "done" in result["stdout"]


def test_unknown_pid_target_reports_unknown_target(server):
    """A numeric target never falls through to kernel routing."""
    _, client = server
    with pytest.raises(RuntimeError, match="unknown target: 99999999"):
        client.call("wait_command", {"target": "99999999", "timeout": 1})
    with pytest.raises(RuntimeError, match="unknown target: 99999999"):
        client.call("kill_command", {"target": "99999999"})


def test_kernel_targets_route_to_the_kernel_manager(server):
    """Kernel wait/kill go through dispatch, never through the bash Tool objects."""
    instance, client = server

    class Manager:
        def __init__(self):
            self.calls = []

        def wait_command(self, target, timeout):
            self.calls.append(("wait", target, timeout))
            return {"running": False, "kernel": target}

        def kill_command(self, target):
            self.calls.append(("kill", target))
            return {"running": False, "kernel": target}

    manager = Manager()
    instance.set_kernel_manager(manager)
    assert client.call("wait_command", {"target": "analysis", "timeout": 1})["kernel"] == "analysis"
    assert client.call("kill_command", {"target": "analysis"})["kernel"] == "analysis"
    assert manager.calls == [("wait", "analysis", 1), ("kill", "analysis")]


def test_pause_ping(server):
    instance, client = server

    class Paused:
        is_paused = True

    instance.state.pause_controller = Paused()
    assert client.call("pause_status") == {"paused": True}


def test_stop_removes_socket_and_directory(tmp_path):
    instance = ToolServer(_LocalExecState(tmp_path, kill_grace_s=0.2))
    path = instance.start()
    directory = path.parent
    instance.stop()
    assert not path.exists() and not directory.exists()


def test_stateful_stub_fails_cleanly_without_server(tmp_path):
    missing = tmp_path / "missing.sock"
    bash = build_stateful_stubs(str(missing))["bash"]
    with pytest.raises((ConnectionError, FileNotFoundError, OSError)):
        bash("echo no")


def test_pause_ping_skips_stale_socket(monkeypatch, tmp_path):
    monkeypatch.setenv("MATCLAW_TOOL_SOCKET", str(tmp_path / "stale.sock"))
    _wait_if_paused("test")


class _StubKernelManager:
    def __init__(self, remaining):
        self._remaining = remaining

    def remaining_step_time(self, name):
        return self._remaining


def test_in_kernel_wait_clamped_to_step_deadline(tmp_path):
    instance = ToolServer(_LocalExecState(tmp_path), kernel_manager=_StubKernelManager(30.0))
    timeout, note = instance._clamp_wait_timeout("default", 120)
    assert timeout == 25
    assert "clamped" in note


def test_bare_wait_and_idle_caller_are_never_clamped(tmp_path):
    instance = ToolServer(_LocalExecState(tmp_path), kernel_manager=_StubKernelManager(None))
    assert instance._clamp_wait_timeout(None, 120) == (120, None)
    assert instance._clamp_wait_timeout("default", 120) == (120, None)


def test_wait_clamp_floors_at_one_second(tmp_path):
    # Both wait_command implementations treat timeout 0 as "use the default".
    instance = ToolServer(_LocalExecState(tmp_path), kernel_manager=_StubKernelManager(2.0))
    timeout, _ = instance._clamp_wait_timeout("default", 120)
    assert timeout == 1


def test_kernel_stub_reports_caller_for_clamping(server):
    instance, _ = server
    stub = build_stateful_stubs(str(instance.socket_path), "analysis")["wait_command"]
    result = stub("bash", timeout=1)
    assert result["running"] is False
