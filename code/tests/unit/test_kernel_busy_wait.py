"""A busy resubmission waits once inside the harness instead of burning model turns."""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor


def test_busy_completion_returns_prior_result_and_does_not_run_new_code(
    fresh_manager, monkeypatch
):
    monkeypatch.setattr("core.kernel._BUSY_SUBMISSION_WAIT_S", 1.0)
    first = fresh_manager.execute(
        "import time; time.sleep(1.2); 'prior-result'", "default", 1
    )
    assert first["running"]

    returned = fresh_manager.execute("new_code_ran = True", "default", 10)
    assert returned["output"] == "prior-result"
    assert "NOT executed" in returned["note"]
    probe = fresh_manager.execute("'new_code_ran' in globals()", "default", 10)
    assert probe["output"] is False


def test_still_busy_refuses_with_control_hint_and_does_not_install_code(
    fresh_manager, monkeypatch
):
    monkeypatch.setattr("core.kernel._BUSY_SUBMISSION_WAIT_S", 0.1)
    fresh_manager.execute("import time; time.sleep(5)", "default", 1)
    old_source = fresh_manager.kernels["default"].current.source_path
    try:
        refused = fresh_manager.execute("MUST_NOT_BE_INSTALLED = True", "default", 10)
        assert refused["running"] and refused["refused"]
        assert "wait_command" in refused["note"]
        assert "kill_command" in refused["note"]
        assert "NOT executed" in refused["note"]
        assert "remaining_step_time" not in refused
        assert fresh_manager.kernels["default"].current.source_path == old_source
        assert "MUST_NOT_BE_INSTALLED" not in old_source.read_text()
    finally:
        fresh_manager.kill_command("default")


def test_capacity_refusal_remains_immediate(fresh_manager, monkeypatch):
    monkeypatch.setattr("core.kernel._BUSY_SUBMISSION_WAIT_S", 2.0)
    fresh_manager.execute("1", "probe", 10)
    fresh_manager.execute("2", "third", 10)
    started = time.monotonic()
    refused = fresh_manager.execute("3", "fourth", 10)
    assert time.monotonic() - started < 0.5
    assert refused["refused"] and "kernel cap" in refused["error"]


def test_busy_wait_does_not_hold_manager_lock(fresh_manager, monkeypatch):
    monkeypatch.setattr("core.kernel._BUSY_SUBMISSION_WAIT_S", 0.8)
    assert fresh_manager.execute("40 + 2", "probe", 10)["output"] == 42
    assert fresh_manager.execute("import time; time.sleep(5)", "default", 1)["running"]
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            waiting = pool.submit(
                fresh_manager.execute, "MUST_NOT_RUN = True", "default", 10
            )
            time.sleep(0.1)
            started = time.monotonic()
            other = fresh_manager.execute("6 * 7", "probe", 10)
            elapsed = time.monotonic() - started
            assert other["output"] == 42
            assert elapsed < 0.6
            assert waiting.result(timeout=2)["refused"]
    finally:
        fresh_manager.kill_command("default")
