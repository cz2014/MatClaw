"""Resume-from-history reconstruction.

Writes a synthetic history.jsonl, then builds an agent with resume=True so
create_agent -> _restart_from_history rebuilds agent.memory from the log. Today this path is
only exercised indirectly by a demo's --resume flag.
"""

from __future__ import annotations

import json

import pytest

from core._smol import ActionStep
from core._smol.models import MessageRole


def _history(records: list[dict]) -> str:
    return "\n".join(json.dumps(r) for r in records) + "\n"


def _tool_call(step: int, call_id: str, arguments: str) -> dict:
    payload = [
        {
            "id": call_id,
            "type": "function",
            "function": {"name": "python_interpreter", "arguments": arguments},
        }
    ]
    return {"step": step, "role": "tool-call", "content": "Calling tools:\n" + str(payload)}


def _message_text(message) -> str:
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(
        block.get("text", "") for block in (content or []) if isinstance(block, dict)
    )


def test_resume_prompt_orders_task_before_restored_actions(make_agent, tmp_workspace):
    """The resumed task is bootstrap context, not a trailing post-history user turn."""
    records = [
        {"step": 0, "role": "system", "content": "system prompt"},
        {"step": 0, "role": "user", "content": "the task"},
        {
            "step": 1,
            "role": "assistant",
            "content": json.dumps(
                {"phase": "P1", "plan": "pl", "code": "x = 1", "summary": "s1"}
            ),
            "summary": "s1",
            "phase": "P1",
        },
        {"step": 1, "role": "tool-response", "content": "RESTORED-OBSERVATION"},
    ]
    (tmp_workspace / "history.jsonl").write_text(_history(records))
    agent = make_agent(
        steps=[
            {
                "phase": "end",
                "plan": "fin",
                "code": "final_answer('ok')",
                "summary": "fin",
            }
        ],
        resume=True,
    )

    agent.run("the task", reset=False)

    sent = agent._fake_calls[0]
    roles = [message.role for message in sent]
    texts = [_message_text(message) for message in sent]
    task_positions = [
        i
        for i, (role, text) in enumerate(zip(roles, texts, strict=True))
        if role == MessageRole.USER and "the task" in text
    ]
    restored_position = next(i for i, text in enumerate(texts) if "RESTORED-OBSERVATION" in text)
    assert roles[0] == MessageRole.SYSTEM
    assert task_positions == [1]
    assert roles[1] == MessageRole.USER
    assert restored_position > task_positions[0]


def test_fresh_run_prompt_order_is_unchanged(make_agent):
    agent = make_agent(
        steps=[
            {
                "phase": "end",
                "plan": "fin",
                "code": "final_answer('ok')",
                "summary": "fin",
            }
        ]
    )
    agent.run("fresh task", reset=True)
    sent = agent._fake_calls[0]
    assert sent[0].role == MessageRole.SYSTEM
    assert sent[1].role == MessageRole.USER
    assert "fresh task" in _message_text(sent[1])


def test_oversized_resume_prompt_keeps_latest_post_resume_turn(
    make_agent, tmp_workspace, monkeypatch
):
    """A pruned resumed prompt must still contain the immediately preceding result."""
    marker = "LATEST-POST-RESUME-OBSERVATION"
    records = [
        {"step": 0, "role": "system", "content": "system prompt"},
        {"step": 0, "role": "user", "content": "the task"},
        {
            "step": 1,
            "role": "assistant",
            "content": json.dumps(
                {"phase": "P1", "plan": "pl", "code": "x = 1", "summary": "s1"}
            ),
            "summary": "s1",
            "phase": "P1",
        },
        {"step": 1, "role": "tool-response", "content": "x" * 1_000_000},
    ]
    (tmp_workspace / "history.jsonl").write_text(_history(records))
    agent = make_agent(
        steps=[
            {"phase": "P2", "plan": "run", "code": f"print('{marker}')", "summary": "run"},
            {
                "phase": "end",
                "plan": "fin",
                "code": "final_answer('ok')",
                "summary": "fin",
            },
        ],
        resume=True,
    )
    monkeypatch.setattr(
        "core.context._count_tokens",
        lambda messages, _model_id, **_kwargs: (
            sum(len(_message_text(m)) for m in messages) // 4
        ),
    )
    scripted_generate = agent.model.generate
    sent_calls = []

    def managed_generate(messages, **kwargs):
        sent = agent.model.context_manager(messages)
        sent_calls.append(sent)
        return scripted_generate(sent, **kwargs)

    agent.model.generate = managed_generate
    agent.run("the task", reset=False)

    assert len(sent_calls) >= 2
    assert marker in "\n".join(_message_text(message) for message in sent_calls[1])


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


def test_resume_restores_exact_tool_call_and_single_observation_prefix(
    make_agent, tmp_workspace
):
    code = "value = {'x': [1, 2]}"
    records = [
        {"step": 0, "role": "system", "content": "system"},
        {"step": 0, "role": "user", "content": "task"},
        {
            "step": 1,
            "role": "assistant",
            "content": json.dumps(
                {"phase": "P1", "plan": "p", "code": code, "summary": "s"}
            ),
            "code_action": code,
        },
        _tool_call(1, "original-call-id", code),
        {"step": 1, "role": "tool-response", "content": "Observation:\nOBSERVED"},
    ]
    (tmp_workspace / "history.jsonl").write_text(_history(records))

    agent = make_agent(resume=True)
    step = next(s for s in agent.memory.steps if isinstance(s, ActionStep))
    assert len(step.tool_calls) == 1
    call = step.tool_calls[0]
    assert (call.id, call.name, call.arguments) == (
        "original-call-id",
        "python_interpreter",
        code,
    )
    rendered = step.to_messages()
    tool_text = "\n".join(_message_text(message) for message in rendered)
    assert tool_text.count("Observation:\n") == 1
    assert "original-call-id" in tool_text


def test_resume_error_does_not_duplicate_rendered_error_response(make_agent, tmp_workspace):
    records = [
        {"step": 0, "role": "system", "content": "system"},
        {"step": 0, "role": "user", "content": "task"},
        {
            "step": 1,
            "role": "assistant",
            "content": json.dumps(
                {"phase": "P1", "plan": "p", "code": "boom()", "summary": "s"}
            ),
            "code_action": "boom()",
            "error": {"message": "NameError: boom"},
        },
        _tool_call(1, "error-call", "boom()"),
        {
            "step": 1,
            "role": "tool-response",
            "content": "Call id: error-call\nError:\nNameError: boom",
        },
        {
            "step": 2,
            "role": "assistant",
            "content": json.dumps(
                {"phase": "P2", "plan": "p", "code": "x = 1", "summary": "s2"}
            ),
            "code_action": "x = 1",
        },
        _tool_call(2, "next-call", "x = 1"),
        {"step": 2, "role": "tool-response", "content": "Observation:\nok"},
    ]
    (tmp_workspace / "history.jsonl").write_text(_history(records))

    agent = make_agent(resume=True)
    errored = next(
        step for step in agent.memory.steps if isinstance(step, ActionStep) and step.error
    )
    assert errored.observations is None
    responses = [m for m in errored.to_messages() if m.role == MessageRole.TOOL_RESPONSE]
    assert len(responses) == 1
    assert _message_text(responses[0]).count("NameError: boom") == 1


def test_resume_malformed_tool_call_uses_code_action_fallback(make_agent, tmp_workspace):
    code = "x = 1"
    records = [
        {"step": 0, "role": "system", "content": "system"},
        {"step": 0, "role": "user", "content": "task"},
        {"step": 1, "role": "user", "content": "legacy duplicate task"},
        {
            "step": 2,
            "role": "assistant",
            "content": json.dumps(
                {"phase": "P2", "plan": "p", "code": code, "summary": "s"}
            ),
            "code_action": code,
        },
        {"step": 2, "role": "tool-call", "content": "not a literal payload"},
        {"step": 2, "role": "tool-response", "content": "Observation:\nok"},
    ]
    (tmp_workspace / "history.jsonl").write_text(_history(records))

    agent = make_agent(resume=True)
    actions = [s for s in agent.memory.steps if isinstance(s, ActionStep)]
    assert len(actions) == 1
    assert actions[0].tool_calls[0].arguments == code
    assert actions[0].tool_calls[0].id == "call_2"


def test_resume_reconstructs_error_steps(make_agent, tmp_workspace):
    """Regression: a history record with a non-empty 'error' must not crash restart.

    _restart_from_history rebuilds the recorded error into an AgentError, whose
    __init__ requires an AgentLogger (it calls logger.log_error). Constructing it
    without that argument raised `TypeError: AgentError.__init__() missing 1
    required positional argument: 'logger'`, which made any run whose history
    contained an error step unresumable (the L4 opus run, 2026-06-05). This test
    covers both the dict-form and string-form error branches.
    """
    records = [
        {"step": 0, "role": "system", "content": "system prompt"},
        {"step": 0, "role": "user", "content": "the task"},
        {
            "step": 1, "role": "assistant",
            "content": json.dumps({"phase": "P1", "plan": "pl", "code": "boom()", "summary": "s1"}),
            "summary": "s1", "phase": "P1",
            # dict-form error (matches how MatClaw records errors in history)
            "error": {"message": "NameError: name 'boom' is not defined"},
        },
        {"step": 1, "role": "tool-response", "content": "observation 1"},
        {
            "step": 2, "role": "assistant",
            "content": json.dumps({"phase": "P2", "plan": "pl", "code": "boom2()", "summary": "s2"}),
            "summary": "s2", "phase": "P2",
            # string-form error (the other branch of the reconstruction)
            "error": "ValueError: bad value",
        },
        {"step": 2, "role": "tool-response", "content": "observation 2"},
        {
            "step": 3, "role": "assistant",
            "content": json.dumps(
                {"phase": "P3", "plan": "pl", "code": "final_answer('done')", "summary": "s3"}
            ),
            "summary": "s3", "phase": "P3",
        },
    ]
    (tmp_workspace / "history.jsonl").write_text(_history(records))

    # Must not raise. The bug raised TypeError during create_agent(resume=True).
    agent = make_agent(resume=True)

    action_steps = [s for s in agent.memory.steps if isinstance(s, ActionStep)]
    errored = [s for s in action_steps if s.error is not None]
    # both error steps reconstructed, each carrying its message
    assert len(errored) >= 2, "expected both error steps to be reconstructed"
    messages = " ".join(str(s.error) for s in errored)
    assert "boom" in messages          # dict-form message preserved
    assert "bad value" in messages     # string-form message preserved


def test_runner_resume_continues_not_reset(make_agent, tmp_workspace, monkeypatch):
    """Regression: the runner must resume (reset=False), not restart fresh.

    create_agent(resume=True) reconstructs memory from history, but agent.run()
    defaults to reset=True (memory.reset() clears it). The runner must call
    agent.run(task, reset=not resume) -- otherwise --resume silently restarts the
    task from scratch, which on a real run re-explores inputs and re-submits
    already-completed HPC jobs (the L4 opus run, 2026-06-05). This drives the
    actual run_agent so the wiring is pinned, not just the agent-level invariant.
    """
    marker = "PRIOR_RUN_OBSERVATION_MARKER"
    records = [
        {"step": 0, "role": "system", "content": "system prompt"},
        {"step": 0, "role": "user", "content": "the task"},
        {
            "step": 1, "role": "assistant",
            "content": json.dumps({"phase": "P1", "plan": "pl", "code": "x = 1", "summary": "s1"}),
            "summary": "s1", "phase": "P1",
        },
        {"step": 1, "role": "tool-response", "content": marker},
    ]
    (tmp_workspace / "history.jsonl").write_text(_history(records))

    # A resume-reconstructed agent whose scripted model finishes in one step.
    agent = make_agent(
        steps=[{"phase": "end", "plan": "fin", "code": "final_answer('ok')", "summary": "fin"}],
        resume=True,
    )
    assert any(
        marker in (s.observations or "")
        for s in agent.memory.steps if isinstance(s, ActionStep)
    ), "precondition: memory reconstructed from history before the run"

    import sys
    import core.runner as runner_mod

    # Inject this exact (already-resumed) agent into the runner, then run resumed.
    monkeypatch.setattr(runner_mod, "create_agent", lambda **kw: agent)
    saved_stdout = sys.stdout
    try:
        runner_mod.run_agent(
            task="the task", workspace_dir=tmp_workspace,
            config_dir=tmp_workspace, resume=True,
        )
    finally:
        sys.stdout = saved_stdout  # run_agent installs a TeeWriter; restore

    # The reconstructed observation must still be present: a reset=True run would
    # have wiped it and restarted fresh.
    assert any(
        marker in (s.observations or "")
        for s in agent.memory.steps if isinstance(s, ActionStep)
    ), "runner wiped reconstructed memory: resume restarted fresh instead of continuing"


def test_runner_cleans_agent_when_run_raises(make_agent, tmp_workspace, monkeypatch):
    import sys

    import core.runner as runner_mod

    agent = make_agent()
    cleaned = []
    original_cleanup = agent.cleanup

    def cleanup():
        cleaned.append(True)
        original_cleanup()

    def fail_run(*args, **kwargs):
        raise RuntimeError("model failed")

    agent.cleanup = cleanup
    agent.run = fail_run
    monkeypatch.setattr(runner_mod, "create_agent", lambda **kwargs: agent)
    saved_stdout = sys.stdout
    try:
        with pytest.raises(RuntimeError, match="model failed"):
            runner_mod.run_agent(
                task="failure", workspace_dir=tmp_workspace, config_dir=tmp_workspace
            )
    finally:
        sys.stdout = saved_stdout
    assert cleaned == [True]


def test_runner_cleans_agent_when_pause_setup_raises(make_agent, tmp_workspace, monkeypatch):
    import sys

    import core.runner as runner_mod

    agent = make_agent()
    cleaned = []
    original_cleanup = agent.cleanup

    def cleanup():
        cleaned.append(True)
        original_cleanup()

    def fail_pause_setup(controller):
        raise RuntimeError("pause setup failed")

    agent.cleanup = cleanup
    agent.model.set_pause_controller = fail_pause_setup
    monkeypatch.setattr(runner_mod, "create_agent", lambda **kwargs: agent)
    saved_stdout = sys.stdout
    try:
        with pytest.raises(RuntimeError, match="pause setup failed"):
            runner_mod.run_agent(
                task="failure", workspace_dir=tmp_workspace, config_dir=tmp_workspace
            )
    finally:
        sys.stdout = saved_stdout
    assert cleaned == [True]


def test_runner_installs_sigterm_handler(make_agent, tmp_workspace, monkeypatch):
    """The run path turns SIGTERM into SystemExit so the teardown paths still run.

    Without it, a plain `kill` of the harness skips the finally block and leaves the agent's
    kernel processes and their children orphaned. The previous handler is restored on exit.
    """
    import signal
    import sys

    import core.runner as runner_mod

    agent = make_agent(steps=[
        {"phase": "end", "plan": "fin", "code": "final_answer('ok')", "summary": "fin"},
    ])
    monkeypatch.setattr(runner_mod, "create_agent", lambda **kwargs: agent)

    original_handler = signal.getsignal(signal.SIGTERM)
    seen = {}
    real_run = agent.run

    def run(*args, **kwargs):
        seen["handler"] = signal.getsignal(signal.SIGTERM)
        return real_run(*args, **kwargs)

    agent.run = run
    saved_stdout = sys.stdout
    try:
        runner_mod.run_agent(
            task="a task", workspace_dir=tmp_workspace, config_dir=tmp_workspace
        )
    finally:
        sys.stdout = saved_stdout

    assert seen["handler"] is runner_mod._sigterm_exit
    assert signal.getsignal(signal.SIGTERM) is original_handler
    with pytest.raises(SystemExit):
        runner_mod._sigterm_exit(signal.SIGTERM, None)


def test_resume_continues_step_numbering(make_agent, tmp_workspace):
    """Regression: a resumed run must continue step numbering, not restart at 1.

    smolagents resets self.step_number=1 in _run_stream; on a continued run
    (reset=False with reconstructed memory) it must start from the highest
    existing ActionStep so the displayed and recorded ActionStep.step_number
    continue from where the prior run stopped, instead of restarting at 1 and
    colliding with the reconstructed steps. (The L4 opus run showed 'Step 1'
    after resuming from step 44.)
    """
    records = [
        {"step": 0, "role": "system", "content": "sys"},
        {"step": 0, "role": "user", "content": "task"},
    ]
    for n in (1, 2, 3):
        records.append({
            "step": n, "role": "assistant",
            "content": json.dumps({"phase": f"P{n}", "plan": "p", "code": f"v{n}={n}", "summary": f"s{n}"}),
            "summary": f"s{n}", "phase": f"P{n}",
        })
        records.append({"step": n, "role": "tool-response", "content": f"obs{n}"})
    (tmp_workspace / "history.jsonl").write_text(_history(records))

    # max recovered step is 3 -> a continued run must number the next step 4+.
    agent = make_agent(
        steps=[{"phase": "end", "plan": "fin", "code": "final_answer('ok')", "summary": "fin"}],
        resume=True,
    )
    recovered = [s.step_number for s in agent.memory.steps if isinstance(s, ActionStep)]
    assert max(recovered) == 3, "precondition: 3 steps recovered from history"

    agent.run("task", reset=False)

    assert agent.step_number >= 4, (
        f"resumed run restarted step numbering at {agent.step_number}, "
        "expected it to continue from the recovered history max (3) + 1"
    )
    # and no newly created step collides with the reconstructed step numbers 1-3
    new_steps = [
        s for s in agent.memory.steps
        if isinstance(s, ActionStep) and s.step_number is not None and s.step_number >= 4
    ]
    assert new_steps, "the continued run did not produce a step numbered >= 4"


def test_monitor_step_summary_uses_step_number():
    """The Monitor's '[Step N: Duration ...]' summary must use the step's own
    step_number, not len(step_durations), so a resumed run's per-step summary
    continues (e.g. Step 45) instead of restarting at 1. (Second step-counter
    found in the L4 opus resume after the header counter was fixed.)
    """
    from types import SimpleNamespace

    from core._smol.monitoring import Monitor

    logged: list[str] = []

    class _CapLogger:
        def log(self, text, level=None, **kwargs):
            logged.append(str(text))

    monitor = Monitor(tracked_model=SimpleNamespace(), logger=_CapLogger())
    step = SimpleNamespace(
        step_number=45,
        timing=SimpleNamespace(duration=1.23),
        token_usage=None,
    )
    monitor.update_metrics(step)

    joined = " ".join(logged)
    assert "Step 45" in joined, f"summary did not use step_number: {logged}"
    assert "Step 1:" not in joined, f"summary restarted the counter at 1: {logged}"
