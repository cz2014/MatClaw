"""Kernel step spools are fresh and collision-free across manager lifetimes."""

from __future__ import annotations

from pathlib import Path

from core.kernel import KernelManager
from core.tools import ToolSpec, _LocalExecState
from core.toolserver import ToolServer


def _manager(workspace: Path):
    state = _LocalExecState(workspace, kill_grace_s=0.2)
    server = ToolServer(state)
    server.start()
    spec = ToolSpec(
        workspace=workspace,
        search_roots=(workspace,),
        site_packages=Path(__file__).resolve().parents[2] / ".venv" / "lib",
        disabled=("web_fetch", "web_search"),
    )
    return KernelManager(workspace, spec, server, grace_s=0.5), server


def test_step_log_names_are_unique_across_manager_restarts(tmp_path):
    first, first_server = _manager(tmp_path)
    try:
        first_result = first.execute("print('first')", "default", 10)
        first_path = first_result["log_file"]
    finally:
        first.shutdown()
        first_server.stop()

    second, second_server = _manager(tmp_path)
    try:
        second_result = second.execute("print('second')", "default", 10)
        second_path = second_result["log_file"]
    finally:
        second.shutdown()
        second_server.stop()

    assert first_path != second_path
    assert first._run_id in first_path
    assert second._run_id in second_path
    assert (tmp_path / first_path).read_text().strip() == "first"
    assert (tmp_path / second_path).read_text().strip() == "second"


def test_foreign_step_log_is_truncated_before_reader_starts(fresh_manager, monkeypatch):
    safe_name = "default"
    step = fresh_manager._step + 1
    path = fresh_manager.workspace / (
        f".kernel_{safe_name}_{fresh_manager._run_id}_step_{step}.log"
    )
    path.write_text("FOREIGN SESSION OUTPUT\n")
    observed = []
    original = fresh_manager._read_execution

    def inspect_then_read(kernel, execution):
        observed.append((execution.log_path.stat().st_size, kernel.sample_log_size))
        original(kernel, execution)

    monkeypatch.setattr(fresh_manager, "_read_execution", inspect_then_read)
    result = fresh_manager.execute("print('current')", "default", 10)

    assert observed == [(0, 0)]
    assert "FOREIGN SESSION OUTPUT" not in result["logs"]
    assert "current" in result["logs"]


def test_log_growth_never_negative_across_steps(fresh_manager):
    for marker in ("a", "b"):
        running = fresh_manager.execute(
            f"import time; print('{marker}' * 2000, flush=True); time.sleep(1.2)",
            "default",
            1,
        )
        assert running["vitals"]["log_growth_bytes"] >= 0
        fresh_manager.wait_command("default", timeout=2)
