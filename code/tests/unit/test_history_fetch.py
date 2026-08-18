"""Unit tests for history writer callback and FetchHistoryTool.

Run: python tests/test_history_fetch.py
     python tests/test_history_fetch.py --integration   # requires LLM API key
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock


# repo root: code/tests/unit/test_history_fetch.py -> unit -> tests -> code
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.tools import FetchHistoryTool  # noqa: E402  (sys.path setup above)


def _generate_reference_history(output_path: Path, n_steps: int = 30):
    """Generate a reference history.jsonl with synthetic data."""
    records = [
        {"step": 0, "role": "system", "content": "System prompt " + "S" * 2000},
        {"step": 0, "role": "user", "content": "Train a CIPS ML potential using active learning."},
    ]
    for i in range(1, n_steps + 1):
        summary = f"Step {i}: Process iteration data batch {i}"
        phase = f"Iteration {(i - 1) // 5 + 1}, Step {(i - 1) % 5 + 1}"
        assistant_content = json.dumps({
            "phase": phase,
            "plan": f"Plan for step {i}: process data and submit job...",
            "code": f"result_{i} = compute(data_{i})\nprint(result_{i})",
            "summary": summary,
        })
        records.append({
            "step": i, "role": "assistant", "content": assistant_content,
            "summary": summary, "phase": phase,
            "timing": {"start_time": 1709640000.0 + i * 10, "end_time": 1709640000.0 + i * 10 + 5},
            "code_action": f"result_{i} = compute(data_{i})",
            "token_usage": {"input_tokens": 1000 * i, "output_tokens": 100 * i},
        })
        records.append({
            "step": i, "role": "tool-response",
            "content": f"Tool output for step {i}: " + "x" * 5000,
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _generate_paired_fixtures(history_path: Path, steps_path: Path, n_steps: int = 10):
    """Generate matched history.jsonl and steps.jsonl for recovery comparison.

    The two files are consistent: for each step N in steps.jsonl,
    model_input_messages contains exactly the messages that history.jsonl
    records with step <= N.
    """
    system_msg = {"role": "system", "content": "System prompt " + "S" * 500}
    user_msg = {"role": "user", "content": "Train a CIPS ML potential."}

    history_records = [
        {"step": 0, "role": "system", "content": system_msg["content"]},
        {"step": 0, "role": "user", "content": user_msg["content"]},
    ]

    cumulative_messages = [system_msg, user_msg]

    history_path.parent.mkdir(parents=True, exist_ok=True)
    steps_path.parent.mkdir(parents=True, exist_ok=True)

    with history_path.open("w", encoding="utf-8") as hf, \
         steps_path.open("w", encoding="utf-8") as sf:

        for rec in history_records:
            hf.write(json.dumps(rec, ensure_ascii=False) + "\n")

        for i in range(1, n_steps + 1):
            summary = f"Step {i}: process batch {i}"
            phase = f"Iteration {(i - 1) // 5 + 1}, Step {(i - 1) % 5 + 1}"
            assistant_content = json.dumps({
                "phase": phase,
                "plan": f"Plan for step {i}",
                "code": f"result_{i} = compute(data_{i})",
                "summary": summary,
            })
            tool_content = f"Tool output for step {i}: " + "x" * 500

            assistant_msg = {"role": "assistant", "content": assistant_content}
            tool_msg = {"role": "tool-response", "content": tool_content}
            cumulative_messages.extend([assistant_msg, tool_msg])

            h_assistant = {
                "step": i, "role": "assistant", "content": assistant_content,
                "summary": summary, "phase": phase,
                "timing": {"start_time": 1000.0 + i * 10, "end_time": 1000.0 + i * 10 + 5},
                "code_action": f"result_{i} = compute(data_{i})",
                "token_usage": {"input_tokens": 500 * i, "output_tokens": 50 * i},
            }
            h_tool = {"step": i, "role": "tool-response", "content": tool_content}
            hf.write(json.dumps(h_assistant, ensure_ascii=False) + "\n")
            hf.write(json.dumps(h_tool, ensure_ascii=False) + "\n")

            t_start = 1000.0 + i * 10
            t_end = t_start + 5
            step_dict = {
                "step_number": i,
                "model_input_messages": list(cumulative_messages),
                "model_output": assistant_content,
                "timing": {
                    "start_time": t_start,
                    "end_time": t_end,
                    "duration": t_end - t_start,
                },
                "token_usage": {"input_tokens": 500 * i, "output_tokens": 50 * i},
                "code_action": f"result_{i} = compute(data_{i})",
                "observations": tool_content,
                "error": None,
                "is_final_answer": i == n_steps,
                "tool_calls": None,
            }
            step_rec = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "step_type": "ActionStep",
                "step": step_dict,
            }
            sf.write(json.dumps(step_rec, ensure_ascii=False, default=str) + "\n")


def test_index_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        _generate_reference_history(ws / "history.jsonl", n_steps=15)
        tool = FetchHistoryTool(ws)
        result = tool.forward(mode="index", start=1, end=10)
        assert "Step 1" in result
        assert "Step 10" in result
        assert "Step 11" not in result
        assert "Process iteration data batch 1" in result
        assert "Iteration 1, Step 1" in result
    print("  PASS: test_index_mode")


def test_index_mode_no_range():
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        _generate_reference_history(ws / "history.jsonl", n_steps=5)
        tool = FetchHistoryTool(ws)
        result = tool.forward(mode="index")
        assert "Step 1" in result
        assert "Step 5" in result
    print("  PASS: test_index_mode_no_range")


def test_detail_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        _generate_reference_history(ws / "history.jsonl", n_steps=10)
        tool = FetchHistoryTool(ws)
        result = tool.forward(mode="detail", steps=[3, 7])
        assert "=== Step 3 ===" in result
        assert "=== Step 7 ===" in result
        assert "compute(data_3)" in result
        assert "Tool output for step 7" in result
    print("  PASS: test_detail_mode")


def test_detail_no_steps_param():
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        _generate_reference_history(ws / "history.jsonl", n_steps=3)
        tool = FetchHistoryTool(ws)
        result = tool.forward(mode="detail")
        assert "Error" in result
    print("  PASS: test_detail_no_steps_param")


def test_empty_history():
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        tool = FetchHistoryTool(ws)
        result = tool.forward(mode="index")
        assert "No conversation history" in result
    print("  PASS: test_empty_history")


def test_unknown_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        _generate_reference_history(ws / "history.jsonl", n_steps=3)
        tool = FetchHistoryTool(ws)
        result = tool.forward(mode="bad")
        assert "Error" in result
        assert "bad" in result
    print("  PASS: test_unknown_mode")


def test_history_writer_callback():
    from core.agent import _history_writer
    from core._smol.memory import ActionStep, FinalAnswerStep
    from core._smol.monitoring import Timing

    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        hf = ws / "history.jsonl"
        cb = _history_writer(hf, ws)
        messages = [
            {"role": "system", "content": "You are an assistant"},
            {"role": "user", "content": "Do something"},
        ]

        codes = ("x=1", "y=2", "z=3", "u=4", "v=5")
        for i, code in enumerate(codes, start=1):
            step = ActionStep(
                step_number=1,  # deliberately reset: writer owns global numbering
                timing=Timing(start_time=100.0 * i, end_time=100.0 * i + 5),
                model_input_messages=list(messages),
                code_action=code,
            )
            cb(step, None)
            messages.extend([
                {"role": "assistant", "content": json.dumps({
                    "phase": "P1", "plan": f"step{i}", "code": code,
                    "summary": f"Step {i} summary",
                })},
                {"role": "tool-response", "content": f"Result: {i}"},
            ])

        class FakeAgent:
            def write_memory_to_messages(self):
                return messages

        cb(FinalAnswerStep("done"), FakeAgent())

        records = [json.loads(line) for line in hf.read_text().splitlines() if line]
        assert sorted(set(rec["step"] for rec in records)) == [0, 1, 2, 3, 4, 5]
        assistants = [rec for rec in records if rec["role"] == "assistant"]
        assert len(assistants) == 5, "the final action must be flushed"
        for i, rec in enumerate(assistants, start=1):
            assert rec["step"] == i
            assert rec["code_action"] == json.loads(rec["content"])["code"]
            assert rec["timing"]["start_time"] == 100.0 * i

    print("  PASS: test_history_writer_callback")


def test_restart_history_writer():
    from core.agent import _history_writer
    from core._smol.memory import ActionStep, FinalAnswerStep
    from core._smol.monitoring import Timing

    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        hf = ws / "history.jsonl"

        # Pre-populate with 3 steps (max step = 3)
        _generate_reference_history(hf, n_steps=3)
        original_count = len(hf.read_text().strip().split("\n"))

        # Create callback -- skip_first should be True since file exists
        cb = _history_writer(hf, ws)

        existing_messages = [{"role": "system", "content": "sys"}] * 8
        step = ActionStep(
            step_number=1,
            timing=Timing(start_time=200.0, end_time=205.0),
            model_input_messages=existing_messages,
            code_action="z=3",
        )
        cb(step, None)

        # Should NOT have written anything
        assert len(hf.read_text().strip().split("\n")) == original_count

        messages = existing_messages + [
            {"role": "assistant", "content": json.dumps({"phase": "P2", "plan": "new", "code": "z=3", "summary": "New step"})},
            {"role": "tool-response", "content": "new result"},
        ]
        class FakeAgent:
            def write_memory_to_messages(self):
                return messages

        cb(FinalAnswerStep("done"), FakeAgent())

        lines = hf.read_text().strip().split("\n")
        assert len(lines) == original_count + 2
        new_rec = json.loads(lines[-2])
        assert new_rec["summary"] == "New step"
        assert new_rec["step"] == 4, (
            f"After resume from 3-step history, new step should be 4, got {new_rec['step']}"
        )
        assert new_rec["code_action"] == json.loads(new_rec["content"])["code"] == "z=3"
        assert new_rec["timing"]["start_time"] == 200.0

    print("  PASS: test_restart_history_writer")


def test_history_writer_same_agent_reset_run():
    """A second run(reset=True) resets the message cursor, not global steps."""
    from core.agent import _history_writer
    from core._smol.memory import ActionStep, FinalAnswerStep
    from core._smol.monitoring import Timing

    with tempfile.TemporaryDirectory() as tmpdir:
        history = Path(tmpdir) / "history.jsonl"
        callback = _history_writer(history, Path(tmpdir))

        def finish_run(task: str, code: str):
            bootstrap = [
                {"role": "system", "content": "system"},
                {"role": "user", "content": task},
            ]
            action = ActionStep(
                step_number=1,
                timing=Timing(start_time=1.0, end_time=2.0),
                model_input_messages=bootstrap,
                code_action=code,
                is_final_answer=True,
            )
            callback(action, None)
            complete = bootstrap + [
                {"role": "assistant", "content": json.dumps({
                    "phase": "P", "plan": "finish", "code": code, "summary": task,
                })},
                {"role": "tool-response", "content": "done"},
            ]

            class FakeAgent:
                def write_memory_to_messages(self):
                    return complete

            callback(FinalAnswerStep("done"), FakeAgent())

        finish_run("run one", "final_answer('one')")
        finish_run("run two", "final_answer('two')")

        records = [json.loads(line) for line in history.read_text().splitlines() if line]
        assistants = [record for record in records if record["role"] == "assistant"]
        assert [record["step"] for record in assistants] == [1, 2]
        assert [json.loads(record["content"])["summary"] for record in assistants] == [
            "run one", "run two",
        ]


def test_history_writer_reset_at_equal_message_count():
    """A new run is detected even when its message list is exactly as long as what was written.

    A run cut short right after its first action callback (interrupt, crashed harness) leaves
    the writer holding exactly the system+task pair the next run starts with. Comparing lengths
    alone sees no shrink there and silently drops the second run's task record.
    """
    from core.agent import _history_writer
    from core._smol.memory import ActionStep
    from core._smol.monitoring import Timing

    with tempfile.TemporaryDirectory() as tmpdir:
        history = Path(tmpdir) / "history.jsonl"
        callback = _history_writer(history, Path(tmpdir))

        def start_run(task: str, code: str):
            bootstrap = [
                {"role": "system", "content": "system"},
                {"role": "user", "content": f"New task: {task}"},
            ]
            callback(
                ActionStep(
                    step_number=1,
                    timing=Timing(start_time=1.0, end_time=2.0),
                    model_input_messages=bootstrap,
                    code_action=code,
                ),
                None,
            )

        start_run("run one", "x = 1")  # interrupted here: nothing further is flushed
        start_run("run two", "y = 2")

        records = [json.loads(line) for line in history.read_text().splitlines() if line]
        tasks = [record["content"] for record in records if record["role"] == "user"]
        assert tasks == ["New task: run one", "New task: run two"]


def test_context_recovery_matches_steps():
    """For each step in steps.jsonl, verify history.jsonl reconstructs the same messages.

    Uses paired synthetic fixtures where both files are generated from the
    same source data. For step N, collecting all history records with step <= N
    should produce the same message sequence as model_input_messages in steps.jsonl.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        history_path = ws / "history.jsonl"
        steps_path = ws / "steps.jsonl"
        _generate_paired_fixtures(history_path, steps_path, n_steps=10)

        history_records = []
        with history_path.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    history_records.append(json.loads(line))

        step_entries = []
        with steps_path.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    step_entries.append(json.loads(line))

        for entry in step_entries:
            step_dict = entry["step"]
            step_num = step_dict["step_number"]
            expected_messages = step_dict["model_input_messages"]

            reconstructed = [r for r in history_records if r["step"] <= step_num]

            assert len(reconstructed) == len(expected_messages), (
                f"Step {step_num}: history has {len(reconstructed)} records, "
                f"steps.jsonl has {len(expected_messages)} messages"
            )

            for i, (h_rec, s_msg) in enumerate(zip(reconstructed, expected_messages)):
                assert h_rec["role"] == s_msg["role"], (
                    f"Step {step_num}, msg {i}: role mismatch: "
                    f"history={h_rec['role']}, steps={s_msg['role']}"
                )
                assert h_rec["content"] == s_msg["content"], (
                    f"Step {step_num}, msg {i}: content mismatch "
                    f"(history len={len(h_rec['content'])}, "
                    f"steps len={len(s_msg['content'])})"
                )

    print("  PASS: test_context_recovery_matches_steps")


def test_analyze_steps_parses_history():
    """Verify analyze_steps.py can parse history.jsonl via the unified parse() entry."""
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
    from analyze_steps import parse

    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        history_path = ws / "history.jsonl"
        _generate_reference_history(history_path, n_steps=5)

        steps = parse(history_path)
        assert len(steps) == 5
        assert steps[0].step_number == 1
        assert steps[4].step_number == 5
        assert steps[0].phase == "Iteration 1, Step 1"
        assert steps[0].summary == "Step 1: Process iteration data batch 1"
        assert steps[2].duration is not None
        assert steps[2].input_tokens is not None

    print("  PASS: test_analyze_steps_parses_history")


# ---------------------------------------------------------------------------
# Integration tests (require LLM API key)
# ---------------------------------------------------------------------------

def test_resume_integration():
    """Structural test: resume from history.jsonl, verify step reconstruction.

    No LLM calls beyond agent creation. Verifies _restart_from_history
    populates memory.steps, injects restart notice into last step's
    observations, and FetchHistoryTool is registered.
    """
    import logging as _logging

    _logging.basicConfig(level=_logging.INFO, format="%(name)s: %(message)s")

    from core._smol import ActionStep

    from core.agent import create_agent

    config_dir = PROJECT_ROOT / "benchmark" / "qa" / "config"
    if not config_dir.exists():
        print("  SKIP: test_resume_integration (config dir not found)")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        history_path = ws / "history.jsonl"
        _generate_reference_history(history_path, n_steps=15)

        agent = create_agent(
            config_dir=config_dir,
            workspace_dir=ws,
            tools=[],
            enable_step_logging=False,
            resume=True,
        )

        assert len(agent.memory.steps) > 0, "Agent memory should have restored steps"

        step_numbers = [s.step_number for s in agent.memory.steps if hasattr(s, "step_number")]
        assert max(step_numbers) >= 15, "Should have recovered all 15 steps"

        # Restart notice should be in last ActionStep's observations, not a separate step
        action_steps = [s for s in agent.memory.steps if isinstance(s, ActionStep)]
        last_step = action_steps[-1]
        assert "AGENT RESTARTED" in (last_step.observations or ""), (
            "Restart notice should be appended to last step's observations"
        )
        assert last_step.step_number == 15, (
            f"Last step should be 15 (no extra restart step), got {last_step.step_number}"
        )

        has_fetch = "fetch_history" in agent.tools
        assert has_fetch, "FetchHistoryTool should be registered"

        tool = agent.tools["fetch_history"]
        result = tool.forward(mode="index", start=1, end=5)
        assert "Step 1" in result
        assert "Step 5" in result

    print("  PASS: test_resume_integration")


def test_multi_run_unique_steps():
    """After simulated multi-run history, verify step numbers are globally unique.

    Simulates: run 1 produces steps 1-3, then resume + run 2 produces steps 4-5.
    smolagents resets step_number to 1 for run 2, but the writer should assign 4-5.
    FetchHistoryTool detail mode for steps 4-5 should only return run 2 messages.
    """
    from core.agent import _history_writer
    from core._smol.memory import ActionStep, FinalAnswerStep
    from core._smol.monitoring import Timing

    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir)
        hf = ws / "history.jsonl"

        # --- Run 1: fresh start, 3 steps ---
        cb1 = _history_writer(hf, ws)
        msgs = [
            {"role": "system", "content": "System prompt"},
            {"role": "user", "content": "Task 1"},
        ]
        for i in range(1, 4):
            step = ActionStep(
                step_number=i,
                timing=Timing(start_time=100.0 + i, end_time=105.0 + i),
                model_input_messages=list(msgs),
                code_action=f"x={i}",
                is_final_answer=(i == 3),
            )
            cb1(step, None)
            msgs = list(msgs) + [
                {"role": "assistant", "content": json.dumps({"phase": "R1", "plan": f"step{i}", "code": f"x={i}", "summary": f"Run1 step {i}"})},
                {"role": "tool-response", "content": f"Run1 result {i}"},
            ]

        class Run1Agent:
            def write_memory_to_messages(self):
                return msgs

        cb1(FinalAnswerStep("run1 done"), Run1Agent())

        # --- Simulate resume: create new writer (file exists) ---
        cb2 = _history_writer(hf, ws)

        # First callback after resume: skip_first triggers
        # Run 2: two steps. The first callback establishes the resume position
        # while retaining that action as the pending step.
        for i in range(1, 3):
            step = ActionStep(
                step_number=i,
                timing=Timing(start_time=200.0 + i, end_time=205.0 + i),
                model_input_messages=list(msgs),
                code_action=f"y={i}",
                is_final_answer=(i == 2),
            )
            cb2(step, None)
            msgs = list(msgs) + [
                {"role": "assistant", "content": json.dumps({"phase": "R2", "plan": f"step{i}", "code": f"y={i}", "summary": f"Run2 step {i}"})},
                {"role": "tool-response", "content": f"Run2 result {i}"},
            ]

        class Run2Agent:
            def write_memory_to_messages(self):
                return msgs

        cb2(FinalAnswerStep("run2 done"), Run2Agent())

        # Verify: parse history and check step numbers
        records = []
        with hf.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))

        step_nums = sorted(set(r["step"] for r in records))
        assert step_nums == [0, 1, 2, 3, 4, 5], (
            f"Expected steps [0,1,2,3,4,5], got {step_nums}"
        )

        # Run2 messages should be at steps 4 and 5
        run2_assistants = [r for r in records if r.get("phase") == "R2"]
        run2_steps = sorted(set(r["step"] for r in run2_assistants))
        assert run2_steps == [4, 5], f"Run2 steps should be [4,5], got {run2_steps}"

        # FetchHistoryTool detail mode for steps 4-5 should only return Run2 data
        tool = FetchHistoryTool(ws)
        detail = tool.forward(mode="detail", steps=[4, 5])
        assert "Run2 step 1" in detail
        assert "Run2 step 2" in detail
        assert "Run1 step" not in detail

    print("  PASS: test_multi_run_unique_steps")


class _patch_isinstance:
    """Context manager to make isinstance(obj, cls) return True for a mock."""
    def __init__(self, obj, cls):
        self._obj = obj
        self._cls = cls
        self._original = type(obj).__class__

    def __enter__(self):
        self._obj.__class__ = self._cls
        return self

    def __exit__(self, *args):
        self._obj.__class__ = MagicMock


UNIT_TESTS = [
    test_index_mode,
    test_index_mode_no_range,
    test_detail_mode,
    test_detail_no_steps_param,
    test_empty_history,
    test_unknown_mode,
    test_history_writer_callback,
    test_restart_history_writer,
    test_history_writer_same_agent_reset_run,
    test_context_recovery_matches_steps,
    test_analyze_steps_parses_history,
    test_multi_run_unique_steps,
]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="History fetch tests")
    parser.add_argument(
        "--integration", action="store_true",
        help="Run integration tests (requires LLM API key)",
    )
    args = parser.parse_args()

    print("Running history fetch unit tests...")
    for test_fn in UNIT_TESTS:
        test_fn()
    print(f"\nAll {len(UNIT_TESTS)} unit tests passed!")
