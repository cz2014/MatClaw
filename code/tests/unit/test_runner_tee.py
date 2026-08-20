"""Run-scoped console/logging lifecycle regressions."""

from __future__ import annotations

import logging
import sys
from types import SimpleNamespace

import pytest

import core.runner as runner


class _Callbacks:
    def register(self, *_args):
        return None


class _Agent:
    def __init__(self, action=None):
        self.python_executor = SimpleNamespace(
            tool_server=SimpleNamespace(state=SimpleNamespace(pause_controller=None))
        )
        self.model = SimpleNamespace()
        self.step_callbacks = _Callbacks()
        self.action = action or (lambda: None)
        self.cleaned = 0

    def run(self, *_args, **_kwargs):
        self.action()
        return SimpleNamespace(output="ok")

    def cleanup(self):
        self.cleaned += 1


def _run(monkeypatch, workspace, agent, *, resume=False):
    monkeypatch.setattr(runner, "create_agent", lambda **_kwargs: agent)
    monkeypatch.setattr(runner, "start_keyboard_listener", lambda _controller: None)
    runner.run_agent(
        task="task", workspace_dir=workspace, config_dir=workspace, resume=resume
    )


def test_fresh_truncates_and_resume_appends(monkeypatch, tmp_path):
    log = tmp_path / "output.log"
    log.write_text("UNRELATED OLD RUN\n")

    _run(monkeypatch, tmp_path, _Agent(lambda: print("fresh marker")))
    fresh = log.read_text()
    assert "UNRELATED OLD RUN" not in fresh
    assert "fresh marker" in fresh

    _run(monkeypatch, tmp_path, _Agent(lambda: print("resume marker")), resume=True)
    resumed = log.read_text()
    assert "fresh marker" in resumed
    assert "resume marker" in resumed
    assert resumed.index("fresh marker") < resumed.index("resume marker")


def test_stdout_stderr_and_core_logging_share_one_ordered_log(monkeypatch, tmp_path):
    def action():
        print("stdout-one")
        print("stderr-two", file=sys.stderr)
        logging.getLogger("core.context").info("core-three")

    _run(monkeypatch, tmp_path, _Agent(action))
    content = (tmp_path / "output.log").read_text()
    assert content.count("stdout-one") == 1
    assert content.count("stderr-two") == 1
    assert content.count("core-three") == 1
    assert content.index("stdout-one") < content.index("stderr-two") < content.index("core-three")


def test_failure_traceback_is_persisted_and_runtime_state_restored(monkeypatch, tmp_path):
    core_logger = logging.getLogger("core")
    before = (list(core_logger.handlers), core_logger.level, core_logger.propagate)
    previous_stdout, previous_stderr = sys.stdout, sys.stderr
    created = []
    original_tee = runner.TeeWriter

    class RecordingTee(original_tee):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            created.append(self)

    monkeypatch.setattr(runner, "TeeWriter", RecordingTee)

    def fail():
        raise RuntimeError("fatal sentinel")

    agent = _Agent(fail)
    with pytest.raises(RuntimeError, match="fatal sentinel"):
        _run(monkeypatch, tmp_path, agent)

    content = (tmp_path / "output.log").read_text()
    assert "Traceback (most recent call last)" in content
    assert "RuntimeError: fatal sentinel" in content
    assert sys.stdout is previous_stdout
    assert sys.stderr is previous_stderr
    assert (list(core_logger.handlers), core_logger.level, core_logger.propagate) == before
    assert created[0].file is created[1].file
    assert created[0].file.closed
    assert agent.cleaned == 1


def test_construction_failure_restores_logger_and_streams(monkeypatch, tmp_path):
    core_logger = logging.getLogger("core")
    before = (list(core_logger.handlers), core_logger.level, core_logger.propagate)
    previous_stdout, previous_stderr = sys.stdout, sys.stderr
    monkeypatch.setattr(
        runner, "create_agent", lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("build failed"))
    )

    with pytest.raises(RuntimeError, match="build failed"):
        runner.run_agent(task="task", workspace_dir=tmp_path, config_dir=tmp_path)

    assert "RuntimeError: build failed" in (tmp_path / "output.log").read_text()
    assert sys.stdout is previous_stdout
    assert sys.stderr is previous_stderr
    assert (list(core_logger.handlers), core_logger.level, core_logger.propagate) == before
