"""Config-loading helpers in core.agent (yaml read, env expansion, prompt templates).

Durable across all later phases; previously untested.
"""

from __future__ import annotations

import pytest

from core.agent import _build_prompt_templates, _expand_env_strict, _read_yaml


def test_read_yaml_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        _read_yaml(tmp_path / "nope.yaml")


def test_read_yaml_roundtrip(tmp_path):
    p = tmp_path / "x.yaml"
    p.write_text("a: 1\nb: two\n")
    assert _read_yaml(p) == {"a": 1, "b": "two"}


def test_read_yaml_non_mapping_raises(tmp_path):
    p = tmp_path / "list.yaml"
    p.write_text("- 1\n- 2\n")
    with pytest.raises(TypeError):
        _read_yaml(p)


def test_expand_env_strict_resolves(monkeypatch):
    monkeypatch.setenv("MATCLAW_TEST_VAR", "secret-value")
    assert _expand_env_strict("${MATCLAW_TEST_VAR}") == "secret-value"


def test_expand_env_strict_unresolved_raises(monkeypatch):
    monkeypatch.delenv("MATCLAW_TEST_MISSING", raising=False)
    with pytest.raises(ValueError):
        _expand_env_strict("${MATCLAW_TEST_MISSING}")


def test_build_prompt_templates_empty_returns_none():
    assert _build_prompt_templates({}) is None


def test_build_prompt_templates_null_system_prompt_raises():
    with pytest.raises(ValueError):
        _build_prompt_templates({"system_prompt": None})


def test_build_prompt_templates_with_system_prompt():
    pt = _build_prompt_templates({"system_prompt": "hello world"})
    assert pt is not None
    assert pt["system_prompt"] == "hello world"


# --- P4: the opened runtime -- full-access config wires to the thin exec() executor ---
# (P4 removed the agent.executor rollback flag once exec was validated; exec is the only path.)

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
_CONFIGS_DIR = _REPO_ROOT / "configs"


def test_shipped_config_is_full_access():
    """The shipped llm_config opens imports to '*' (the opened runtime, P4)."""
    cfg = _read_yaml(_CONFIGS_DIR / "llm_config.yaml")["agent"]
    assert cfg["additional_authorized_imports"] == ["*"]


def test_create_agent_uses_exec_executor(make_agent):
    """create_agent builds the thin ExecPythonExecutor in the real agent (no AST fallback)."""
    agent = make_agent()
    assert type(agent.python_executor).__name__ == "ExecPythonExecutor"
