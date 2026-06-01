"""Tests for Layer 3 experience log: WriteExperienceTool, dynamic reloader, integration."""

from __future__ import annotations

import logging
import tempfile
import time
from pathlib import Path


from core.tools import WriteExperienceTool

# ---------------------------------------------------------------------------
# Unit tests (no LLM needed)
# ---------------------------------------------------------------------------

UNIT_TESTS = []


def _unit(fn):
    UNIT_TESTS.append(fn)
    return fn


@_unit
def test_write_experience_tool():
    """WriteExperienceTool appends notes with correct ID numbering."""
    with tempfile.TemporaryDirectory() as tmpdir:
        exp_path = Path(tmpdir) / "experience.md"
        exp_path.write_text(
            "# Experience Notes\n\n"
            "## 1. First lesson\n\nDetails of first lesson.\n"
        )

        tool = WriteExperienceTool(exp_path)

        # Write a second note
        result = tool.forward(
            summary="Second lesson",
            details="Details of the second lesson.",
        )
        assert "note #2" in result.lower(), f"Expected 'note #2' in: {result}"

        content = exp_path.read_text()
        assert "## 2. Second lesson" in content
        assert "Details of the second lesson." in content

        # Write a third note
        result3 = tool.forward(summary="Third", details="Third details.")
        assert "note #3" in result3.lower()
        content = exp_path.read_text()
        assert "## 3. Third" in content


@_unit
def test_write_experience_tool_empty_file():
    """WriteExperienceTool creates note #1 on an empty/new file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        exp_path = Path(tmpdir) / "experience.md"
        # File doesn't exist yet
        tool = WriteExperienceTool(exp_path)
        result = tool.forward(summary="First note", details="Some details.")
        assert "note #1" in result.lower()
        content = exp_path.read_text()
        assert "## 1. First note" in content


@_unit
def test_experience_reloader_setup():
    """Verify reloader detects file changes and updates agent instructions."""
    from core.agent import _setup_experience_reloader

    with tempfile.TemporaryDirectory() as tmpdir:
        exp_path = Path(tmpdir) / "experience.md"
        exp_path.write_text("# Notes\n\n## 1. Original note\n\nOriginal details.\n")

        # Mock agent with attributes the reloader accesses.
        # Uses a list-based mock for step_callbacks with a register() method
        # to mimic smolagents' CallbackRegistry.
        class MockCallbackRegistry:
            def __init__(self):
                self._callbacks = []
            def register(self, step_cls, callback):
                self._callbacks.append(callback)

        class MockAgent:
            def __init__(self):
                self.instructions = "Base instructions."
                self.step_callbacks = MockCallbackRegistry()
                self._run_calls = []

            class memory:
                system_prompt = None

            @property
            def system_prompt(self):
                return f"SYSTEM: {self.instructions}"

            def run(self, task, **kwargs):
                # Mirror the vendored MultiStepAgent.run: fire on-run-start hooks (P2/V3).
                for hook in getattr(self, "_on_run_start", ()):
                    hook()
                self._run_calls.append(task)

        agent = MockAgent()
        _setup_experience_reloader(agent, exp_path)

        # After setup: initial load should have injected experience
        assert "Original note" in agent.instructions
        assert agent.instructions.startswith("Base instructions.")

        # Step callback: no change -> no-op
        step_cb = agent.step_callbacks._callbacks[-1]
        old_instructions = agent.instructions
        step_cb(None, agent=None)
        assert agent.instructions == old_instructions  # Mtime unchanged

        # Modify file
        time.sleep(0.1)
        exp_path.write_text("# Notes\n\n## 1. Updated note\n\nNew details.\n")

        # Step callback: mtime changed -> reload (agent=None so no system_prompt update)
        step_cb(None, agent=None)
        assert "Updated note" in agent.instructions
        assert "Original note" not in agent.instructions

        # Run wrapper: modify file again, verify run() refreshes
        time.sleep(0.1)
        exp_path.write_text("# Notes\n\n## 1. Third version\n\nThird details.\n")
        agent.run("test task")
        assert "Third version" in agent.instructions


@_unit
def test_experience_token_warning(caplog=None):
    """Verify warning is logged when experience file exceeds 10K tokens."""
    from core.agent import _setup_experience_reloader

    with tempfile.TemporaryDirectory() as tmpdir:
        exp_path = Path(tmpdir) / "experience.md"
        # 10K tokens ~ 40K chars at 4 chars/token
        large_content = "# Notes\n\n" + ("x" * 50_000) + "\n"
        exp_path.write_text(large_content)

        class MockCallbackRegistry:
            def __init__(self):
                self._callbacks = []
            def register(self, step_cls, callback):
                self._callbacks.append(callback)

        class MockAgent:
            def __init__(self):
                self.instructions = "Base."
                self.step_callbacks = MockCallbackRegistry()

            class memory:
                system_prompt = None

            @property
            def system_prompt(self):
                return self.instructions

            def run(self, *a, **kw):
                pass

        agent = MockAgent()

        with _capture_logs("core.agent", logging.WARNING) as logs:
            _setup_experience_reloader(agent, exp_path)

        warnings = [r for r in logs if "experience_search" in r.getMessage()]
        assert len(warnings) >= 1, (
            f"Expected warning about experience_search, got: "
            f"{[r.getMessage() for r in logs]}"
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

import contextlib


@contextlib.contextmanager
def _capture_logs(logger_name, level=logging.DEBUG):
    """Capture log records from a specific logger."""
    log = logging.getLogger(logger_name)
    records: list[logging.LogRecord] = []

    class _Handler(logging.Handler):
        def emit(self, record):
            records.append(record)

    handler = _Handler()
    handler.setLevel(level)
    log.addHandler(handler)
    old_level = log.level
    log.setLevel(level)
    try:
        yield records
    finally:
        log.removeHandler(handler)
        log.setLevel(old_level)


# ---------------------------------------------------------------------------
# Integration test (requires LLM)
# ---------------------------------------------------------------------------

SEED_EXPERIENCE = """\
# Experience Notes

## 1. The magic spell

The magic spell is: "zhima kaimen!"
"""


# ---------------------------------------------------------------------------
# CLI runner
# ---------------------------------------------------------------------------


def main():
    import argparse
    import traceback

    parser = argparse.ArgumentParser(description="Experience log tests")
    parser.add_argument(
        "--integration", action="store_true",
        help="Also run integration test (requires LLM API key)",
    )
    args = parser.parse_args()

    passed = 0
    failed = 0

    for test_fn in UNIT_TESTS:
        name = test_fn.__name__
        try:
            test_fn()
            print(f"  PASS  {name}")
            passed += 1
        except Exception:
            print(f"  FAIL  {name}")
            traceback.print_exc()
            failed += 1


    total = passed + failed
    print(f"\n{passed}/{total} tests passed")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
