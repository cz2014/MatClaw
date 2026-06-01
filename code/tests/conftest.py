"""Shared pytest configuration for the MatClaw test suite.

Tiers (see docs/exec-plans/active/2026-05-31_p0_test_scaffolding.md):
  unit         offline, deterministic, no LLM/cluster -- the gate (default run)
  llm          needs a real LLM (Gemini 3.5 Flash); the llm/ tier
  integration  needs a real HPC/SSH/Mongo cluster; the integration/ tier

The `unit` / `llm` / `integration` markers are auto-applied by directory below (one dir per
tier). Agent-run demo scripts under tests/demos/ are not collected.

Fixtures (fake_llm / tmp_workspace / agent_factory) are added in the P0b step.
"""

import json
import os
from pathlib import Path

import pytest

# Demo / agent-run scripts are reproducibility artifacts, not tests.
collect_ignore = ["demos"]

_TESTS_DIR = Path(__file__).parent
REPO_ROOT = _TESTS_DIR.parent.parent  # code/tests -> code -> repo root
CONFIGS_DIR = REPO_ROOT / "configs"
_DUMMY_KEYS = ("CLAUDE_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "DEEPSEEK_API_KEY")


def pytest_addoption(parser):
    """Options for the live LLM tests. Only the env var NAME is passed -- the key VALUE stays in the
    environment (never on a command line), so nothing leaks. Defaults match the repo's cheap model.
    """
    parser.addoption(
        "--llm-provider", action="store", default="gemini",
        help="Provider for the live LLM tests (a key in configs/llm_config.yaml). Default: gemini.",
    )
    parser.addoption(
        "--llm-key-env", action="store", default="GEMINI_API_KEY",
        help="NAME of the host env var holding the API key for --llm-provider (value is read from "
             "the environment, never passed as a value). Default: GEMINI_API_KEY.",
    )


def pytest_collection_modifyitems(config, items):
    """Auto-apply the tier marker (`unit` / `llm` / `integration`) based on directory."""
    _by_dir = {"unit": "unit", "llm": "llm", "integration": "integration"}
    for item in items:
        path = Path(str(item.fspath)).resolve()
        try:
            rel = path.relative_to(_TESTS_DIR)
        except ValueError:
            continue
        top = rel.parts[0] if rel.parts else ""
        marker = _by_dir.get(top)
        if marker:
            item.add_marker(getattr(pytest.mark, marker))


# --- P0b fixtures: drive the real CodeAgent loop with a scripted (fake) LLM ---


@pytest.fixture
def tmp_workspace(tmp_path):
    """A throwaway workspace directory for an agent run."""
    return tmp_path


@pytest.fixture
def make_agent(monkeypatch, tmp_path):
    """Build a real CodeAgent (via create_agent) whose model is replaced by a scripted
    fake LLM, so agent.run() exercises the real loop offline (no network/API key).

    Usage:
        agent = make_agent(steps=[{"phase":.., "plan":.., "code":"x=1", "summary":..}, ...],
                           tools=[my_tool])
        result = agent.run("task")

    Each step's "code" is executed in the persistent interpreter; end a run with code that
    calls final_answer(...). When steps run out, a default final_answer step is returned so
    the loop always terminates. The message lists the model was called with are recorded on
    agent._fake_calls.
    """
    state = {"cwd": os.getcwd()}

    def _make(steps=None, tools=None, default_tools=False, **create_kwargs):
        for key in _DUMMY_KEYS:
            monkeypatch.setenv(key, "test-dummy")
        from core._smol.models import ChatMessage, MessageRole, TokenUsage

        from core.agent import create_agent

        if default_tools:
            tools = None  # let create_agent inject the full default toolset
        elif tools is None:
            tools = []  # minimal: skip the default scientific toolset (avoids RAG index load)
        agent = create_agent(
            config_dir=CONFIGS_DIR, workspace_dir=tmp_path, tools=tools, **create_kwargs
        )
        if hasattr(agent, "stream_outputs"):
            agent.stream_outputs = False

        queue = list(steps or [])
        calls = []
        default = {
            "phase": "end", "plan": "finish",
            "code": "final_answer('default')", "summary": "finish",
        }

        def fake_generate(messages, **kwargs):
            calls.append(messages)
            payload = queue.pop(0) if queue else default
            return ChatMessage(
                role=MessageRole.ASSISTANT,
                content=json.dumps(payload),
                token_usage=TokenUsage(input_tokens=1, output_tokens=1),
            )

        agent.model.generate = fake_generate
        agent._fake_calls = calls
        return agent

    yield _make
    os.chdir(state["cwd"])  # create_agent chdir's into the workspace; restore it
