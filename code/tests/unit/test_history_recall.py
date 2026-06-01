"""Deterministic check (fake LLM): fetch_history recalls an earlier step's content mid-run.

The pruning logic itself is unit-tested in test_context_pruning.py; history.jsonl is the full,
un-pruned record that fetch_history reads. Here we verify the *wiring*: during a run, a later
step can call fetch_history and recover content from an earlier step -- the mechanism that lets
the agent recover information after the live context has been pruned. No LLM, no qa_120.json.
"""

from __future__ import annotations


def _step(code: str, phase: str = "P", plan: str = "pl", summary: str = "s") -> dict:
    return {"phase": phase, "plan": plan, "code": code, "summary": summary}


def test_fetch_history_recalls_earlier_step(make_agent):
    marker = "SECRET_MARKER_4242"
    agent = make_agent(steps=[
        _step("recalled = 'SECRET_MARKER_4242'", phase="P1", summary="store the secret"),
        _step("x = 1"),  # filler step so step 1's assistant message lands in history.jsonl
        _step("r = fetch_history(mode='detail', steps=[1, 2, 3, 4, 5]); final_answer(r)"),
    ])
    result = agent.run("store a value, then recall it from history")
    # fetch_history returned step 1's record (incl. its code), recovering the marker.
    assert marker in str(result.output)
