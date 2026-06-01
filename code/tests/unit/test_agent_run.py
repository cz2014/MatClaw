"""Behavioral tests for the agent.run() loop, driven by a scripted (fake) LLM.

No real LLM/network: the `make_agent` fixture replaces the model with a fake that returns
pre-written {phase, plan, code, summary} steps. We assert the loop's observable contract --
structured-output parsing, code execution, namespace persistence across steps, calling a tool
from the namespace, history.jsonl writing, and final-answer termination. This fills the single
biggest coverage gap (the orchestration loop has no other automated test).
"""

from __future__ import annotations

import json

from core._smol import tool


@tool
def echo_tool(text: str) -> str:
    """Return the input prefixed with 'echo:'.

    Args:
        text: the string to echo back.
    """
    return f"echo:{text}"


def _step(code: str, phase: str = "P", plan: str = "pl", summary: str = "s") -> dict:
    return {"phase": phase, "plan": plan, "code": code, "summary": summary}


def test_run_executes_code_and_returns_final_answer(make_agent):
    """Structured output is parsed, code runs, state persists across steps, final_answer ends."""
    agent = make_agent(steps=[
        _step("x = 41"),                      # step 1: set a variable (no final answer -> continue)
        _step("final_answer(str(x + 1))"),    # step 2: use it -> proves persistence
    ])
    result = agent.run("compute the answer")
    assert result.output == "42"
    # the fake model was called once per step
    assert len(agent._fake_calls) == 2


def test_run_calls_namespace_tool(make_agent):
    """A tool passed to create_agent is callable from inside the code action."""
    agent = make_agent(
        steps=[_step("y = echo_tool('hi')"), _step("final_answer(y)")],
        tools=[echo_tool],
    )
    result = agent.run("use the echo tool")
    assert result.output == "echo:hi"


def test_run_opened_runtime_native_io_and_subprocess(make_agent, tmp_workspace):
    """O2: the opened runtime (executor: exec) supports native open()/pathlib + subprocess.

    None of these worked under the old AST executor (no open(), import allow-list). This drives
    them through the REAL agent loop and asserts both the filesystem effect and that captured
    subprocess stdout reaches the step observations.
    """
    code = (
        "import subprocess\n"
        "from pathlib import Path\n"
        "Path('sub/dir').mkdir(parents=True, exist_ok=True)\n"
        "Path('sub/dir/x.txt').write_text('hi from pathlib')\n"
        "r = subprocess.run(['echo', 'shell-says-hi'], capture_output=True, text=True)\n"
        "print(r.stdout.strip())\n"
    )
    agent = make_agent(steps=[
        _step(code),
        _step("final_answer(Path('sub/dir/x.txt').read_text())"),
    ])
    result = agent.run("exercise the opened runtime")
    assert result.output == "hi from pathlib"
    assert (tmp_workspace / "sub" / "dir" / "x.txt").exists()
    observations = " ".join(
        (getattr(s, "observations", "") or "") for s in agent.memory.steps
    )
    assert "shell-says-hi" in observations


def test_run_uses_basic_primitives(make_agent, tmp_workspace):
    """O3: the renamed write_file + new glob/bash helpers are reachable in the real loop."""
    code = (
        "write_file('out/data.txt', 'alpha\\nbeta\\n')\n"
        "files = glob('out/*.txt')\n"
        "shown = bash('cat out/data.txt')\n"
        "print('FILES', files)\n"
        "print('CAT', shown['stdout'].strip())\n"
    )
    agent = make_agent(steps=[_step(code), _step("final_answer('ok')")], default_tools=True)
    result = agent.run("use the basic primitives")
    assert result.output == "ok"
    assert (tmp_workspace / "out" / "data.txt").read_text() == "alpha\nbeta\n"
    obs = " ".join((getattr(s, "observations", "") or "") for s in agent.memory.steps)
    assert "data.txt" in obs  # glob result printed
    assert "alpha" in obs  # bash cat output printed


def test_run_writes_history(make_agent, tmp_workspace):
    """history.jsonl is written with assistant records carrying phase + summary.

    Two steps: a step's assistant output is recorded into history when the *next* step
    includes it as input (the writer diffs model_input_messages), so we assert on step 1.
    """
    agent = make_agent(steps=[
        _step("x = 1", phase="Phase 1", summary="set up"),
        _step("final_answer('done')", phase="Phase 2", summary="finish up"),
    ])
    agent.run("a task")

    history = tmp_workspace / "history.jsonl"
    assert history.exists(), "history.jsonl should be written to the workspace"
    records = [json.loads(line) for line in history.read_text().splitlines() if line.strip()]
    assert records, "history.jsonl should not be empty"

    assistant = [r for r in records if r.get("role") == "assistant"]
    assert assistant, "expected at least one assistant record"
    assert any(r.get("summary") == "set up" for r in assistant)
    assert any(r.get("phase") == "Phase 1" for r in assistant)
