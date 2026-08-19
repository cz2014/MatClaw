"""Harness-owned Bash foreground slot and background registry."""

from __future__ import annotations

import inspect
import os
import pickle
import time
from types import SimpleNamespace

import psutil
import pytest

from core.tools import (
    BashTool,
    KillCommandTool,
    ToolSpec,
    WaitCommandTool,
    _LocalExecState,
    _process_table_by_group,
    build_stateless_tools,
)


def _finished_background_record(state, command: str):
    pid = state.run_bash(command, run_in_background=True)["pid"]
    record = state.background[pid]
    deadline = time.monotonic() + 5
    while record.proc.poll() is None and time.monotonic() < deadline:
        time.sleep(0.05)
    assert record.proc.poll() is not None
    return record


def test_tool_spec_pickle_and_factory(tmp_path):
    spec = ToolSpec(
        workspace=tmp_path,
        search_roots=(tmp_path,),
        site_packages=tmp_path,
        disabled=("web_search", "web_fetch"),
    )
    restored = pickle.loads(pickle.dumps(spec))
    started = time.monotonic()
    names = {tool.name for tool in build_stateless_tools(restored)}
    assert time.monotonic() - started < 0.5
    assert {"read_file", "write_file", "wait_for_jobflow", "remote_ls"} <= names
    assert "bash" not in names and "final_answer" not in names


def test_bash_timeout_keeps_process_alive(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        result = state.run_bash("sleep 10", timeout=1)
        assert result["running"] is True
        assert psutil.pid_exists(result["pid"])
        assert state.foreground is not None
    finally:
        state.shutdown()


def test_busy_slot_refuses_without_starting_second_command(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        first = state.run_bash("sleep 10", timeout=1)
        second = state.run_bash("touch should_not_exist", timeout=1)
        assert first["pid"] == second["pid"]
        assert second["running"] and second["refused"]
        assert not (tmp_path / "should_not_exist").exists()
    finally:
        state.shutdown()


def test_spool_contains_output_before_process_finishes(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        result = state.run_bash("printf first; sleep 10", timeout=1)
        assert result["running"] is True
        assert "first" in (tmp_path / result["log_file"]).read_text()
    finally:
        state.shutdown()


def test_wait_command_early_completion_and_signature(tmp_path):
    assert inspect.signature(_LocalExecState.wait_command).parameters["timeout"].default == 60
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        state.run_bash("sleep 1.2; printf done", timeout=1)
        result = WaitCommandTool(state).forward("bash", timeout=3)
        assert result["running"] is False
        assert result["returncode"] == 0 and "done" in result["stdout"]
        assert state.foreground is None
    finally:
        state.shutdown()


def test_wait_command_expiry_reports_vitals(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        state.run_bash("sleep 10", timeout=1)
        result = state.wait_command("bash", timeout=1)
        assert result["running"] is True
        assert result["vitals"]["pid"] == result["pid"]
    finally:
        state.shutdown()


def test_kill_command_term_rung(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.5)
    try:
        state.run_bash("sleep 10", timeout=1)
        result = KillCommandTool(state).forward("bash")
        assert result["method"] == "term"
        assert result["running"] is False and state.foreground is None
    finally:
        state.shutdown()


def test_kill_command_escalates_to_sigkill(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        state.run_bash("trap '' TERM; while :; do sleep 1; done", timeout=1)
        result = state.kill_command("bash")
        assert result["method"] == "kill"
        assert not psutil.pid_exists(result["pid"])
    finally:
        state.shutdown()


def test_background_allowed_while_foreground_busy(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        state.run_bash("sleep 10", timeout=1)
        bg = state.run_bash("printf bg", run_in_background=True)
        assert bg["background"] is True
        done = state.wait_command(str(bg["pid"]), timeout=3)
        assert done["running"] is False and "bg" in done["stdout"]
        assert state.foreground is not None
    finally:
        state.shutdown()


def test_start_new_session_and_shutdown_reaps(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    result = state.run_bash("sleep 10", timeout=1)
    assert os.getpgid(result["pid"]) == result["pid"]
    state.shutdown()
    assert not psutil.pid_exists(result["pid"])


def test_shutdown_kills_descendant_after_shell_leader_exits(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    result = state.run_bash("sleep 30 & echo $!", timeout=1)
    child_pid = int(result["stdout"].strip().splitlines()[0])
    assert result["running"] is True and psutil.pid_exists(child_pid)
    state.shutdown()
    deadline = time.monotonic() + 2
    while psutil.pid_exists(child_pid) and time.monotonic() < deadline:
        time.sleep(0.05)
    assert not psutil.pid_exists(child_pid)


def test_lazy_reap_frees_slot_and_reports_note(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        first = state.run_bash("sleep 1.1", timeout=1)
        assert first["running"]
        time.sleep(0.3)
        second = state.run_bash("printf next", timeout=2)
        assert second["returncode"] == 0 and "next" in second["stdout"]
        assert any("completed" in note for note in second["completion_notes"])
    finally:
        state.shutdown()


def test_completed_background_result_remains_collectable(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        bg = state.run_bash("printf completed", run_in_background=True)
        time.sleep(0.2)
        result = state.wait_command(str(bg["pid"]), timeout=1)
        assert result["running"] is False
        assert result["returncode"] == 0 and result["stdout"] == "completed"
        assert result["log_file"] == bg["log_file"]
    finally:
        state.shutdown()


def test_recent_cpu_window_distinguishes_spin_and_sleep(tmp_path):
    spin = _LocalExecState(tmp_path, kill_grace_s=0.2)
    sleep = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        spinning = spin.run_bash("python -c 'while True: pass'", timeout=1)
        sleeping = sleep.run_bash("sleep 10", timeout=1)
        assert spinning["vitals"]["cpu_over_wall"] > 0.5
        assert sleeping["vitals"]["cpu_over_wall"] < 0.2
    finally:
        spin.shutdown()
        sleep.shutdown()


def test_recent_cpu_window_detects_compute_then_sleep(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        result = state.run_bash(
            "python -c \"import time; end=time.monotonic()+0.5; "
            "exec('while time.monotonic() < end: pass'); time.sleep(10)\"",
            timeout=2,
        )
        assert result["running"] is True
        assert result["vitals"]["cpu_time_s"] > 0.3
        assert result["vitals"]["cpu_over_wall"] < 0.2
    finally:
        state.shutdown()


def test_completed_foreground_result_collectable_by_bash_alias(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        first = state.run_bash("sleep 1.1; printf done", timeout=1)
        assert first["running"] is True
        time.sleep(0.3)
        result = state.wait_command("bash", timeout=1)
        assert result["running"] is False
        assert result["returncode"] == 0 and result["stdout"] == "done"
        assert result["log_file"] == first["log_file"]
    finally:
        state.shutdown()


def test_vitals_sampling_does_not_extend_timeout_or_report_completed_running(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        started = time.monotonic()
        result = state.run_bash("sleep 1.5; printf done", timeout=1)
        duration = time.monotonic() - started
        assert duration < 1.3
        assert result["running"] is True and psutil.pid_exists(result["pid"])
        completed = state.wait_command("bash", timeout=2)
        assert completed["running"] is False and completed["stdout"] == "done"
    finally:
        state.shutdown()


def test_rss_delta_and_log_growth(tmp_path):
    memory = _LocalExecState(tmp_path, kill_grace_s=0.2)
    logs = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        allocated = memory.run_bash(
            "python -c \"import time; x=bytearray(64*1024*1024); time.sleep(10)\"",
            timeout=1,
        )
        assert allocated["vitals"]["rss_delta"] > 32 * 1024 * 1024

        first = logs.run_bash(
            "python -u -c \"import time; print('a'*1000); time.sleep(1.5); "
            "print('b'*1000); time.sleep(10)\"",
            timeout=1,
        )
        assert first["vitals"]["log_growth_bytes"] >= 1000
        second = logs.wait_command("bash", timeout=1)
        assert second["running"] is True
        assert second["vitals"]["log_growth_bytes"] >= 1000
    finally:
        memory.shutdown()
        logs.shutdown()


def test_head_and_tail_are_retained(tmp_path):
    result = BashTool(tmp_path).forward(
        "printf HEAD; printf '%0500d' 0; printf TAIL", max_output_chars=100
    )
    assert result["truncated"] is True
    assert "HEAD" in result["stdout"] and "TAIL" in result["stdout"]


def test_stale_group_signal_does_not_wedge_a_finished_job(tmp_path, monkeypatch):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        record = _finished_background_record(state, "exit 5")
        pid = record.proc.pid
        monkeypatch.setattr(_LocalExecState, "_group_alive", staticmethod(lambda pgid: True))
        assert _LocalExecState._record_running(record) is False
        assert "background: none" in state.status_lines()
        assert any(f"PID {pid} completed with returncode 5" in n for n in state._take_notes())
    finally:
        state.shutdown()


def test_reused_leader_pid_is_not_reported_running(tmp_path, monkeypatch):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        record = _finished_background_record(state, "exit 0")
        pid = record.proc.pid
        assert record.create_time is not None
        impostor = SimpleNamespace(pid=pid, create_time=lambda: record.create_time + 60.0)
        monkeypatch.setattr(_LocalExecState, "_group_alive", staticmethod(lambda pgid: True))
        monkeypatch.setattr(
            _LocalExecState,
            "_group_processes",
            staticmethod(lambda pgid, max_age_s=0.0: [impostor]),
        )
        assert _LocalExecState._record_running(record) is False
        assert state.kill_command(pid)["method"] == "noop"
    finally:
        state.shutdown()


def test_wait_and_kill_tools_reject_kernel_targets(tmp_path):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        with pytest.raises(ValueError, match="RPC stubs"):
            WaitCommandTool(state).forward("analysis")
        with pytest.raises(ValueError, match="RPC stubs"):
            KillCommandTool(state).forward("analysis")
        assert WaitCommandTool(state).forward("bash", timeout=1)["running"] is False
        bg = state.run_bash("sleep 10", run_in_background=True)
        assert KillCommandTool(state).forward(str(bg["pid"]))["running"] is False
    finally:
        state.shutdown()


def test_process_table_scan_is_shared_within_a_tick(monkeypatch):
    scans = []
    real = psutil.process_iter

    def counted(*args, **kwargs):
        scans.append(time.monotonic())
        return real(*args, **kwargs)

    monkeypatch.setattr(psutil, "process_iter", counted)
    first = _process_table_by_group(0.0)
    assert len(scans) == 1
    assert _process_table_by_group(0.15) is first and len(scans) == 1
    assert _process_table_by_group(0.0) is not first and len(scans) == 2


def test_concurrent_samplers_share_one_scan_per_tick(tmp_path, monkeypatch):
    scans = []
    real = psutil.process_iter

    def counted(*args, **kwargs):
        scans.append(time.monotonic())
        return real(*args, **kwargs)

    monkeypatch.setattr(psutil, "process_iter", counted)
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        for _ in range(3):
            state.run_bash("sleep 10", run_in_background=True)
        scans.clear()
        time.sleep(1.0)
        # Three samplers tick 5x/s each; unshared that is 15+ full table walks.
        assert 1 <= len(scans) <= 11
        assert all(record.latest_vitals for record in state.background.values())
    finally:
        state.shutdown()


def test_bash_wait_command_timeout_is_capped_at_600(tmp_path, monkeypatch):
    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    try:
        assert state.run_bash("sleep 5", timeout=1)["running"]
        calls = []
        original = state._wait_record
        monkeypatch.setattr(
            state,
            "_wait_record",
            lambda record, timeout: calls.append(timeout) or original(record, 0.01),
        )
        assert state.wait_command("bash", timeout=100000)["running"]
        assert calls and max(calls) <= 600
    finally:
        state.shutdown()


def test_collapse_cr_keeps_final_progress_frame():
    from core.tools import _collapse_cr

    assert _collapse_cr("plain\n") == "plain\n"
    assert _collapse_cr("10%\r50%\r100%") == "100%"
    assert _collapse_cr("10%\r50%\r100%\nDone\n") == "100%\nDone\n"
    # CRLF line endings keep the line content
    assert _collapse_cr("line1\r\nline2\r\n") == "line1\nline2\n"


def test_command_display_skips_env_prefix():
    display = _LocalExecState._command_display
    assert (
        display("OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 python analyze.py")
        == "python analyze.py"
    )
    assert display("python analyze.py") == "python analyze.py"
    # Pure-assignment commands fall back to the raw string
    assert display("A=1") == "A=1"
