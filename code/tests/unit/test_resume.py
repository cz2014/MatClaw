"""Resume-from-history reconstruction.

Writes a synthetic history.jsonl, then builds an agent with resume=True so
create_agent -> _restart_from_history rebuilds agent.memory from the log. Today this path is
only exercised indirectly by a demo's --resume flag.
"""

from __future__ import annotations

import json

from core._smol import ActionStep


def _history(records: list[dict]) -> str:
    return "\n".join(json.dumps(r) for r in records) + "\n"


def test_resume_reconstructs_memory(make_agent, tmp_workspace):
    records = [
        {"step": 0, "role": "system", "content": "system prompt"},
        {"step": 0, "role": "user", "content": "the task"},
        {
            "step": 1, "role": "assistant",
            "content": json.dumps({"phase": "P1", "plan": "pl", "code": "x = 1", "summary": "s1"}),
            "summary": "s1", "phase": "P1",
        },
        {"step": 1, "role": "tool-response", "content": "observation 1"},
        {
            "step": 2, "role": "assistant",
            "content": json.dumps(
                {"phase": "P2", "plan": "pl", "code": "final_answer('done')", "summary": "s2"}
            ),
            "summary": "s2", "phase": "P2",
        },
    ]
    (tmp_workspace / "history.jsonl").write_text(_history(records))

    agent = make_agent(resume=True)

    action_steps = [s for s in agent.memory.steps if isinstance(s, ActionStep)]
    # steps 1 and 2 reconstructed (step 0 is the system/user bootstrap)
    assert len(action_steps) >= 2

    # code_action is parsed back out of the assistant JSON content
    codes = [s.code_action for s in action_steps]
    assert "x = 1" in codes

    # the restart marker is injected so the agent knows executor variables were lost
    observations = " ".join((s.observations or "") for s in action_steps)
    assert "AGENT RESTARTED" in observations
