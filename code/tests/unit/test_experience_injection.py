"""Deterministic check (fake LLM): the experience-log lifecycle wiring.

A scripted write_experience call appends a note to the experience file, and a *fresh* agent's
instructions then include that note (the dynamic experience reloader). The WriteExperienceTool
and reloader are also unit-tested in isolation (test_experience.py); this asserts the
end-to-end wiring without an LLM.
"""

from __future__ import annotations


def _step(code: str, phase: str = "P", plan: str = "pl", summary: str = "s") -> dict:
    return {"phase": phase, "plan": plan, "code": code, "summary": summary}


def test_experience_written_then_injected(make_agent, tmp_workspace):
    exp = tmp_workspace / "experience.md"
    exp.write_text("# Experience log\n")
    note = "Always preconverge CIPS structures before AIMD"

    agent_a = make_agent(
        steps=[
            _step(
                "write_experience(summary='Always preconverge CIPS structures before AIMD', "
                "details='context body')"
            ),
            _step("final_answer('ok')"),
        ],
        experience_file=exp,
    )
    agent_a.run("learn a lesson and record it")
    assert note in exp.read_text()  # write_experience appended the note

    # A fresh agent picks the note up via the experience reloader (injected into its prompt).
    agent_b = make_agent(steps=[], experience_file=exp)
    assert note in (agent_b.instructions or "")
