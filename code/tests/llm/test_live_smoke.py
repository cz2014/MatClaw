"""Live-tier smoke test: a real Gemini 3.5 Flash call through create_agent.

These exercise the live path on real models. In the llm/ tier (auto-marked @llm), so the default
Unit gate skips them; run with `-m llm`. Which provider-specific test runs is selected by
`--llm-provider` (default gemini), consistent with the docker live test -- e.g.
`-m llm --llm-provider=claude` runs the Claude path. The selected provider's API key must be set
(otherwise the test fails loudly -- you opted into `-m llm`).
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

CONFIGS_DIR = Path(__file__).resolve().parents[3] / "configs"


def _skip_unless_provider(request, provider: str) -> None:
    """Skip unless --llm-provider selects this test's provider (default: gemini).

    Provider *selection* (not key presence) decides which provider-specific live test runs, so this
    suite is consistent with the docker live test. No hardcoded key-name checks: if the selected
    provider's key is missing, the live call fails loudly rather than silently skipping.
    """
    selected = request.config.getoption("--llm-provider")
    if selected != provider:
        pytest.skip(f"--llm-provider={selected!r}; this test exercises {provider!r}")


def test_live_gemini_smoke(tmp_path, request):
    _skip_unless_provider(request, "gemini")

    from core.agent import create_agent

    cwd = os.getcwd()
    try:
        agent = create_agent(
            config_dir=CONFIGS_DIR,
            workspace_dir=tmp_path,
            provider_name="gemini",
            tools=[],
        )
        result = agent.run(
            "Do not write any analysis or extra code. In your very first step, immediately "
            "call final_answer with exactly the single word: DONE"
        )
        assert result.output is not None
        assert "DONE" in str(result.output).upper()
    finally:
        os.chdir(cwd)


def test_live_claude_smoke(tmp_path, request):
    """A real Claude (anthropic/claude-opus-4-8) call through create_agent.

    This is the one test that exercises the live ANTHROPIC generate path -- including
    cache_control injection and the thinking config -- which the Gemini smoke cannot cover.
    Verifies the V3 generate-path refactor (context-manager hook ordering, retry/cache) still
    drives a real Claude call end-to-end. Runs only with `--llm-provider=claude`.
    """
    _skip_unless_provider(request, "claude")

    from core.agent import create_agent

    cwd = os.getcwd()
    try:
        agent = create_agent(
            config_dir=CONFIGS_DIR,
            workspace_dir=tmp_path,
            provider_name="claude",
            tools=[],
        )
        result = agent.run(
            "Do not write any analysis or extra code. In your very first step, immediately "
            "call final_answer with exactly the single word: DONE",
            max_steps=3,
        )
        assert result.output is not None
        assert "DONE" in str(result.output).upper()
    finally:
        os.chdir(cwd)


def test_live_gemini_vision(tmp_path, request):
    """The one irreducible LLM mechanism: the model actually *sees* an attached image.

    Uses a self-contained synthetic image (a solid red canvas) -- no external figure -- and
    asserts the model reports its color via final_answer. Gemini 3.5 Flash is multimodal.
    Runs only with `--llm-provider=gemini` (the default).
    """
    _skip_unless_provider(request, "gemini")

    import PIL.Image

    from core.agent import create_agent

    img = PIL.Image.new("RGB", (128, 128), "red")
    cwd = os.getcwd()
    try:
        agent = create_agent(
            config_dir=CONFIGS_DIR,
            workspace_dir=tmp_path,
            provider_name="gemini",
            tools=[],
        )
        result = agent.run(
            "An image is attached. Do not write analysis. Call final_answer with ONLY the "
            "dominant color of the image as a single lowercase word.",
            images=[img],
            max_steps=3,
        )
        assert result.output is not None
        assert "red" in str(result.output).lower()
    finally:
        os.chdir(cwd)
