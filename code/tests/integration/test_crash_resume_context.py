"""Offline crash/resume replay across writer, reconstruction, and real pruning hook."""

from __future__ import annotations

import ast
import json

import pytest

from core._smol import ActionStep
from core._smol.models import MessageRole

pytestmark = pytest.mark.integration


def _text(message) -> str:
    if isinstance(message.content, str):
        return message.content
    return "".join(
        block.get("text", "")
        for block in (message.content or [])
        if isinstance(block, dict)
    )


def test_crash_resume_keeps_task_order_structure_and_latest_result(
    make_agent, monkeypatch, tmp_workspace
):
    """Replay the production freeze at small scale with no provider request."""
    oversized_code = "# " + "x" * 600_000 + "\nprint('PHASE-ONE')"
    first = make_agent(
        steps=[
            {"phase": "P1", "plan": "large", "code": oversized_code, "summary": "large"},
            {
                "phase": "end",
                "plan": "finish",
                "code": "final_answer('phase-one-done')",
                "summary": "finish",
            },
        ]
    )
    first.run("durable task")
    first.cleanup()

    marker = "LATEST-RESUMED-RESULT"
    resumed = make_agent(
        steps=[
            {"phase": "P2", "plan": "resume", "code": f"print('{marker}')", "summary": "resume"},
            {
                "phase": "end",
                "plan": "finish",
                "code": "final_answer('done')",
                "summary": "finish",
            },
        ],
        resume=True,
    )

    written_calls = []
    for line in (tmp_workspace / "history.jsonl").read_text().splitlines():
        record = json.loads(line)
        if record.get("role") != "tool-call":
            continue
        written_calls.extend(ast.literal_eval(record["content"].removeprefix("Calling tools:\n")))
    restored_calls = [
        {
            "id": call.id,
            "type": "function",
            "function": {"name": call.name, "arguments": call.arguments},
        }
        for step in resumed.memory.steps
        if isinstance(step, ActionStep)
        for call in (step.tool_calls or [])
    ]
    assert restored_calls == written_calls

    monkeypatch.setattr(
        "core.context._count_tokens",
        lambda messages, _model_id, **_kwargs: sum(len(_text(m)) for m in messages) // 4,
    )
    scripted_generate = resumed.model.generate
    sent_calls = []

    def scripted_provider(messages, **kwargs):
        sent_calls.append(messages)
        return scripted_generate(messages, **kwargs)

    monkeypatch.setattr(resumed.model, "_generate_with_empty_retry", scripted_provider)
    monkeypatch.delattr(resumed.model, "generate")
    resumed.run("durable task", reset=False)

    first_prompt = sent_calls[0]
    assert first_prompt[0].role == MessageRole.SYSTEM
    assert first_prompt[1].role == MessageRole.USER
    assert "durable task" in _text(first_prompt[1])
    assert sum(
        message.role == MessageRole.USER and "durable task" in _text(message)
        for message in first_prompt
    ) == 1
    assert any(message.role == MessageRole.TOOL_CALL for message in first_prompt)
    assert sent_calls[1] != first_prompt
    assert marker in "\n".join(_text(message) for message in sent_calls[1])
