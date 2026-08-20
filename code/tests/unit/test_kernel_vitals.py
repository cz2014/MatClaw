"""Kernel roster and recent-window process vitals."""

from __future__ import annotations

import re
import subprocess
import time
from types import SimpleNamespace


def test_spin_and_sleep_cpu_windows(fresh_manager):
    spin = fresh_manager.execute("while True:\n    pass", "default", 1)
    try:
        assert spin["vitals"]["cpu_over_wall"] > 0.5
    finally:
        fresh_manager.kill_command("default")

    sleeping = fresh_manager.execute("import time; time.sleep(10)", "default", 1)
    try:
        assert sleeping["vitals"]["cpu_over_wall"] < 0.2
    finally:
        fresh_manager.kill_command("default")


def test_rss_delta_and_actionable_field_summary(fresh_manager):
    running = fresh_manager.execute(
        "import subprocess, time\n"
        "vitals_mem = bytearray(64 * 1024 * 1024)\n"
        "vitals_child = subprocess.Popen(['sleep', '10'])\n"
        "time.sleep(10)",
        "default",
        1,
    )
    try:
        assert running["vitals"]["rss_delta"] > 32 * 1024 * 1024
        assert set(running["vitals"]) == {
            "cpu_over_wall",
            "rss_bytes",
            "rss_delta",
            "log_growth_bytes",
        }
    finally:
        fresh_manager.kill_command("default")


def test_kernel_resource_totals_exclude_zombie_and_dead_descendants(monkeypatch):
    import psutil
    from core.kernel import KernelManager

    class FakeProcess:
        def __init__(self, status, cpu, rss, children=()):
            self._status = status
            self._cpu = cpu
            self._rss = rss
            self._children = list(children)

        def children(self, recursive=True):
            return self._children

        def is_running(self):
            return self._status != "dead"

        def status(self):
            return self._status

        def cpu_times(self):
            return (self._cpu, 0.0)

        def memory_info(self):
            return SimpleNamespace(rss=self._rss)

    live = FakeProcess(psutil.STATUS_RUNNING, 2.0, 100)
    zombie = FakeProcess(psutil.STATUS_ZOMBIE, 50.0, 10_000)
    dead = FakeProcess("dead", 60.0, 20_000)
    parent = FakeProcess(psutil.STATUS_RUNNING, 1.0, 50, [live, zombie, dead])
    monkeypatch.setattr("core.kernel.psutil.Process", lambda _pid: parent)
    assert KernelManager._kernel_resources(SimpleNamespace(pid=123)) == (3.0, 150)


def test_log_growth_between_checkins(fresh_manager):
    running = fresh_manager.execute(
        "import time\nprint('a' * 1000, flush=True)\ntime.sleep(1.5)\n"
        "print('b' * 1000, flush=True)\ntime.sleep(10)",
        "default",
        1,
    )
    assert running["vitals"]["log_growth_bytes"] >= 1000
    try:
        checked = fresh_manager.wait_command("default", timeout=1)
        assert checked["running"] is True
        assert checked["vitals"]["log_growth_bytes"] >= 1000
    finally:
        fresh_manager.kill_command("default")


def test_roster_busy_idle_and_human_duration(fresh_manager):
    fresh_manager.execute("import time; time.sleep(20)", "default", 1)
    try:
        fresh_manager.kernels["default"].current.started_at = time.monotonic() - 7980
        roster = fresh_manager.roster_line()
        assert roster.startswith("kernels: default(busy 2h13m")
        assert "cpu " in roster and "rss " in roster
    finally:
        fresh_manager.kill_command("default")
    # An idle kernel still reports the memory it is holding (a hot model is idle
    # memory), so the roster's memory columns never disappear.
    assert re.fullmatch(r"kernels: default\(idle, rss \d+\.\dG\)", fresh_manager.roster_line())


def test_gpu_is_an_ordinary_name_on_cpu_host(fresh_manager):
    result = fresh_manager.execute("40 + 2", "gpu", 10)
    assert result["output"] == 42
    assert fresh_manager.kernels["gpu"].manager.is_alive()


def test_vram_query_present_and_soft_fail(monkeypatch, fresh_manager):
    pid = fresh_manager.kernels["default"].pid

    def present(*args, **kwargs):
        return SimpleNamespace(stdout=f"{pid}, 512\n999999, 100\n", returncode=0)

    monkeypatch.setattr(subprocess, "run", present)
    assert fresh_manager._vram_bytes(pid) == 512 * 1024 * 1024

    def missing(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(subprocess, "run", missing)
    assert fresh_manager._vram_bytes(pid) is None


def test_vram_appears_in_busy_roster(monkeypatch, fresh_manager):
    monkeypatch.setattr(fresh_manager, "_vram_bytes", lambda pid: 1024**3)
    fresh_manager.execute("import time; time.sleep(10)", "default", 1)
    try:
        assert "vram 1.0G" in fresh_manager.roster_line()
    finally:
        fresh_manager.kill_command("default")


def test_vram_appears_in_idle_roster(monkeypatch, fresh_manager):
    monkeypatch.setattr(fresh_manager, "_vram_bytes", lambda pid: 4.8 * 1024**3)
    assert fresh_manager.kernels["default"].current is None
    roster = fresh_manager.roster_line()
    assert re.fullmatch(r"kernels: default\(idle, rss \d+\.\dG, vram 4\.8G\)", roster)
