"""Parity guards for the P2 smolagents vendoring (core/_smol).

These two tests pin the behavior the fake-LLM loop tests and the trivial live smoke do NOT
cover, so the V2-V4 refactors (prompt framing, retry/cache relocation, history-writer rewrite)
can be proven behavior-identical by the offline gate:

  test_system_prompt_framing -- the rendered system prompt keeps the phase/plan/code/summary
      framing and renders the jinja toolset (guards P-B4 template rendering + P-B5 prompt).
  test_history_golden -- the history.jsonl assistant-record schema is exactly as today
      (guards the V4 writer rewrite).

Both are deterministic (no LLM): the system prompt is rendered at construction from
configs/prompts.yaml, and the history writer is driven by the scripted fake model.
"""

from __future__ import annotations

import json


def _step(code: str, phase: str = "P", plan: str = "pl", summary: str = "s") -> dict:
    return {"phase": phase, "plan": plan, "code": code, "summary": summary}


def test_system_prompt_framing(make_agent):
    """The agent's rendered system prompt uses phase/plan/code/summary and renders the jinja."""
    agent = make_agent()  # tools=[] (plus the always-added I/O tools + final_answer)
    sp = agent.system_prompt

    # structured-output framing the agent depends on
    for token in ("phase", "plan", "code", "summary", "final_answer"):
        assert token in sp, f"system prompt missing {token!r}"
    # the four-keys instruction line from configs/prompts.yaml
    assert '"phase", "plan", "code", and "summary"' in sp

    # jinja must be fully rendered (tools loop expanded, no template literals left)
    assert "{%-" not in sp and "{{" not in sp, "system prompt still contains unrendered jinja"

    # no stale smolagents 'thought' framing (P-B5 reframing must hold)
    assert "thought" not in sp.lower(), "system prompt still contains 'thought' framing"


def test_history_golden(make_agent, tmp_workspace):
    """The history.jsonl assistant-record schema is exactly the current contract.

    A 2-step scripted run: step 1's assistant record is flushed when step 2 runs (the writer
    emits a record once the next step's input includes it). We pin that record's full shape.
    """
    agent = make_agent(steps=[
        _step("x = 1", phase="Phase 1", plan="set x", summary="set up"),
        _step("final_answer('done')", phase="Phase 2", plan="finish", summary="finish up"),
    ])
    agent.run("a task")

    history = tmp_workspace / "history.jsonl"
    records = [json.loads(line) for line in history.read_text().splitlines() if line.strip()]
    assistant = [r for r in records if r.get("role") == "assistant"]
    assert assistant, "expected at least one assistant record in history.jsonl"

    # the step-1 assistant record -- pin its exact schema + message-derived values.
    rec = next(r for r in assistant if r.get("phase") == "Phase 1")
    assert isinstance(rec["step"], int)
    assert rec["role"] == "assistant"
    # message-derived fields (stable; sourced from the assistant message content)
    assert rec["summary"] == "set up"
    assert rec["phase"] == "Phase 1"
    assert json.loads(rec["content"])["code"] == "x = 1"
    assert json.loads(rec["content"])["plan"] == "set x"
    # NOTE (current writer quirk): code_action/timing/token_usage come from the *callback's*
    # step, not the message, so they belong to the NEXT step (model_input_messages diffing).
    # V4/C2 fixes this attribution -- update these when V4 lands. For now just pin presence+type.
    assert isinstance(rec["code_action"], str) and rec["code_action"]
    # volatile fields: present + correctly typed (not value-pinned)
    assert isinstance(rec["timing"], dict) and {"start_time", "end_time"} <= set(rec["timing"])
    assert isinstance(rec["token_usage"], dict)

    # the record carries no unexpected top-level keys
    allowed = {
        "step", "role", "content", "summary", "phase", "timing", "error",
        "code_action", "is_final_answer", "token_usage", "images_b64",
    }
    assert set(rec) <= allowed, f"unexpected history keys: {set(rec) - allowed}"
