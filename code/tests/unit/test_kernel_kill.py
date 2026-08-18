"""Kernel interrupt/restart ladder and namespace-loss contract."""

from __future__ import annotations

import inspect
import subprocess
import sys
import time
from pathlib import Path

import psutil
import pytest

from core.kernel import KernelManager


def test_failed_restart_unfreezes_registration(fresh_manager, monkeypatch):
    kernel = fresh_manager.kernels["default"]

    def boom(_kernel):
        raise RuntimeError("bootstrap boom")

    monkeypatch.setattr(fresh_manager, "_bootstrap", boom)
    with pytest.raises(RuntimeError, match="bootstrap boom"):
        fresh_manager._restart(kernel)
    assert "default" not in fresh_manager.tool_server._frozen_process_registration


def test_failed_restart_is_an_error_not_a_refusal(fresh_manager, monkeypatch):
    dead = fresh_manager.execute("import os\nos._exit(7)", "default", 10)
    assert dead["error"]["ename"] == "KernelDied"

    def boom(_kernel):
        raise RuntimeError("no comeback")

    monkeypatch.setattr(fresh_manager, "_restart", boom)
    with pytest.raises(RuntimeError, match="no comeback"):
        fresh_manager.execute("x = 1", "default", 10)


def _assert_pids_exit(pid_file, timeout=2):
    pids = [int(line) for line in pid_file.read_text().splitlines() if line]
    assert len(pids) >= 5
    deadline = time.monotonic() + timeout
    while any(psutil.pid_exists(pid) for pid in pids) and time.monotonic() < deadline:
        time.sleep(0.05)
    assert not [pid for pid in pids if psutil.pid_exists(pid)]


def test_interrupt_rung_preserves_namespace(fresh_manager):
    fresh_manager.execute("interrupt_keep = 17", "default", 10)
    running = fresh_manager.execute("while True:\n    pass", "default", 1)
    assert running["running"]
    killed = fresh_manager.kill_command("default")
    assert killed["method"] == "interrupt"
    assert killed["namespace_preserved"] is True
    assert fresh_manager.execute("interrupt_keep", "default", 10)["output"] == 17


def test_restart_rung_loses_namespace_and_rebootstraps_stubs(fresh_manager):
    fresh_manager.execute("restart_lost = 19", "default", 10)
    running = fresh_manager.execute(
        "import signal, time\nsignal.signal(signal.SIGINT, signal.SIG_IGN)\n"
        "while True:\n    time.sleep(0.05)",
        "default",
        1,
    )
    assert running["running"]
    killed = fresh_manager.kill_command("default")
    assert killed["method"] == "restart"
    assert killed["namespace_preserved"] is False
    missing = fresh_manager.execute("restart_lost", "default", 10)
    assert missing["error"]["ename"] == "NameError"
    final = fresh_manager.execute("final_answer('rebootstrapped')", "default", 10)
    assert final["is_final_answer"] and final["output"] == "rebootstrapped"


def test_restart_rung_when_keyboard_interrupt_is_swallowed(fresh_manager):
    running = fresh_manager.execute(
        "import time\nwhile True:\n"
        "    try:\n        time.sleep(0.05)\n"
        "    except KeyboardInterrupt:\n        pass",
        "default",
        1,
    )
    assert running["running"]
    killed = fresh_manager.kill_command("default")
    assert killed["method"] == "restart"
    assert killed["namespace_preserved"] is False


def test_idle_kill_is_noop(fresh_manager):
    result = fresh_manager.kill_command("default")
    assert result == {
        "running": False,
        "kernel": "default",
        "method": "noop",
        "namespace_preserved": True,
    }


def test_kill_signature_has_no_signal_or_force_parameters():
    parameters = inspect.signature(KernelManager.kill_command).parameters
    assert list(parameters) == ["self", "target"]


def test_no_replay_or_resurrection_api():
    forbidden = {"replay", "restore", "resurrect", "checkpoint_namespace"}
    assert forbidden.isdisjoint(dir(KernelManager))


def test_kernel_death_during_kill_grace_forces_restart(fresh_manager):
    running = fresh_manager.execute(
        "import os, signal, threading, time\n"
        "signal.signal(signal.SIGINT, signal.SIG_IGN)\n"
        "threading.Timer(1.2, lambda: os._exit(9)).start()\n"
        "while True:\n    time.sleep(0.05)",
        "default",
        1,
    )
    assert running["running"]
    result = fresh_manager.kill_command("default")
    assert result["method"] == "restart"
    assert result["namespace_preserved"] is False
    assert fresh_manager.kernels["default"].manager.is_alive()


def test_detached_child_reaped_after_kernel_crash_and_restart(fresh_manager, tmp_path):
    pid_file = tmp_path / "detached_pid.txt"
    crashed = fresh_manager.execute(
        "import os, pathlib, subprocess\n"
        "p = subprocess.Popen(['sleep', '30'], start_new_session=True)\n"
        f"pathlib.Path({str(pid_file)!r}).write_text(str(p.pid))\n"
        "os._exit(7)",
        "default",
        10,
    )
    assert crashed["error"]["ename"] == "KernelDied"
    child_pid = int(pid_file.read_text())
    assert psutil.pid_exists(child_pid)
    assert fresh_manager.execute("1 + 1", "default", 10)["output"] == 2
    deadline = time.monotonic() + 2
    while psutil.pid_exists(child_pid) and time.monotonic() < deadline:
        time.sleep(0.05)
    assert not psutil.pid_exists(child_pid)


def test_detached_child_reaped_by_shutdown_after_kernel_crash(fresh_manager, tmp_path):
    pid_file = tmp_path / "shutdown_detached_pid.txt"
    crashed = fresh_manager.execute(
        "import os, pathlib, subprocess\n"
        "p = subprocess.Popen(['sleep', '30'], start_new_session=True)\n"
        f"pathlib.Path({str(pid_file)!r}).write_text(str(p.pid))\n"
        "os._exit(8)",
        "default",
        10,
    )
    assert crashed["error"]["ename"] == "KernelDied"
    child_pid = int(pid_file.read_text())
    assert psutil.pid_exists(child_pid)
    fresh_manager.shutdown()
    deadline = time.monotonic() + 2
    while psutil.pid_exists(child_pid) and time.monotonic() < deadline:
        time.sleep(0.05)
    assert not psutil.pid_exists(child_pid)


def test_restart_closes_continuous_detached_spawn_race(fresh_manager, tmp_path):
    pid_file = tmp_path / "restart_spawned_pids.txt"
    running = fresh_manager.execute(
        "import signal, subprocess, time\n"
        "signal.signal(signal.SIGINT, signal.SIG_IGN)\n"
        f"_pid_log = open({str(pid_file)!r}, 'a', buffering=1)\n"
        "while True:\n"
        "    _p = subprocess.Popen(['sleep', '30'], start_new_session=True)\n"
        "    _pid_log.write(f'{_p.pid}\\n')\n"
        "    time.sleep(0.03)",
        "default",
        1,
    )
    assert running["running"]
    result = fresh_manager.kill_command("default")
    assert result["method"] == "restart"
    _assert_pids_exit(pid_file)


def test_shutdown_closes_continuous_detached_spawn_race(fresh_manager, tmp_path):
    pid_file = tmp_path / "shutdown_spawned_pids.txt"
    running = fresh_manager.execute(
        "import subprocess, time\n"
        f"_pid_log = open({str(pid_file)!r}, 'a', buffering=1)\n"
        "while True:\n"
        "    _p = subprocess.Popen(['sleep', '30'], start_new_session=True)\n"
        "    _pid_log.write(f'{_p.pid}\\n')\n"
        "    time.sleep(0.03)",
        "default",
        1,
    )
    assert running["running"]
    fresh_manager.shutdown()
    _assert_pids_exit(pid_file)


def test_kill_reports_processes_that_outlived_the_sweep(fresh_manager, monkeypatch):
    """A descendant that escaped the ladder is named, not reported as a clean kill."""
    escapee = subprocess.Popen(["sleep", "30"], start_new_session=True)
    scans = []
    original = KernelManager._owned_processes

    def scan(kernel):
        scans.append(kernel.name)
        found = list(original(kernel))
        # The sweep itself cannot see a descendant that re-setsid away; the
        # verification scan afterwards finds it still running.
        if len(scans) > 1 and psutil.pid_exists(escapee.pid):
            found.append(psutil.Process(escapee.pid))
        return found

    monkeypatch.setattr(fresh_manager, "_owned_processes", scan)
    try:
        running = fresh_manager.execute(
            "import signal, time\nsignal.signal(signal.SIGINT, signal.SIG_IGN)\n"
            "while True:\n    time.sleep(0.05)",
            "default",
            1,
        )
        assert running["running"]
        result = fresh_manager.kill_command("default")
        assert result["method"] == "restart"
        assert result["running"] is False
        assert result["survivors"] == [escapee.pid]
    finally:
        escapee.kill()
        escapee.wait()


def test_clean_kill_reports_no_survivors(fresh_manager):
    running = fresh_manager.execute(
        "import subprocess, signal, time\n"
        "signal.signal(signal.SIGINT, signal.SIG_IGN)\n"
        "subprocess.Popen(['sleep', '30'])\n"
        "while True:\n    time.sleep(0.05)",
        "default",
        1,
    )
    assert running["running"]
    result = fresh_manager.kill_command("default")
    assert result["method"] == "restart"
    assert "survivors" not in result


def test_kernel_subprocess_fails_closed_when_tool_server_is_unreachable(fresh_manager):
    """Registration is the orphan invariant: no server, no child, and a named error."""
    kernel = fresh_manager.kernels["default"]
    socket_path = Path(fresh_manager.tool_server.socket_path)
    hidden = socket_path.with_name(socket_path.name + ".hidden")
    socket_path.rename(hidden)
    try:
        result = fresh_manager.execute(
            "import subprocess\nsubprocess.Popen(['sleep', '30'], start_new_session=True)",
            "default",
            10,
        )
    finally:
        hidden.rename(socket_path)
    assert result["error"]["ename"] == "RuntimeError"
    assert "tool server unreachable" in result["error"]["evalue"]
    deadline = time.monotonic() + 2
    while KernelManager._owned_processes(kernel) and time.monotonic() < deadline:
        time.sleep(0.05)
    assert KernelManager._owned_processes(kernel) == []


def test_restart_freezes_registered_worker_before_descendant_sweep(fresh_manager, tmp_path):
    pid_file = tmp_path / "worker_spawned_pids.txt"
    worker_file = tmp_path / "worker_pid.txt"
    worker_code = (
        "import pathlib, signal, subprocess, time\n"
        "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
        f"log = open({str(pid_file)!r}, 'a', buffering=1)\n"
        "while True:\n"
        "    child = subprocess.Popen(['sleep', '30'], start_new_session=True)\n"
        "    log.write(f'{child.pid}\\n')\n"
        "    time.sleep(0.03)\n"
    )
    running = fresh_manager.execute(
        "import pathlib, signal, subprocess, sys, time\n"
        "signal.signal(signal.SIGINT, signal.SIG_IGN)\n"
        f"worker = subprocess.Popen([{sys.executable!r}, '-c', {worker_code!r}])\n"
        f"pathlib.Path({str(worker_file)!r}).write_text(str(worker.pid))\n"
        "while True:\n"
        "    time.sleep(0.03)",
        "default",
        1,
    )
    assert running["running"]
    worker_pid = int(worker_file.read_text())
    result = fresh_manager.kill_command("default")
    assert result["method"] == "restart"
    _assert_pids_exit(pid_file)
    assert not psutil.pid_exists(worker_pid)
