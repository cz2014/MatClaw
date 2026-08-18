"""Config-loading helpers in core.agent (yaml read, env expansion, prompt templates).

Durable across all later phases; previously untested.
"""

from __future__ import annotations

from pathlib import Path

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


def test_create_agent_failure_after_runtime_start_cleans_resources(monkeypatch, tmp_path):
    import core.agent as agent_module
    from core.toolserver import ToolServer

    for key in ("CLAUDE_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "DEEPSEEK_API_KEY"):
        monkeypatch.setenv(key, "test-dummy")
    removed = []
    original_stop = ToolServer.stop

    def stop(server):
        path = server.socket_path
        original_stop(server)
        if path is not None:
            removed.append(not path.exists() and not path.parent.exists())

    class BrokenCodeAgent:
        def __init__(self, **kwargs):
            raise RuntimeError("agent construction failed")

    monkeypatch.setattr(ToolServer, "stop", stop)
    monkeypatch.setattr(agent_module, "CodeAgent", BrokenCodeAgent)
    with pytest.raises(RuntimeError, match="agent construction failed"):
        agent_module.create_agent(
            config_dir=_CONFIGS_DIR,
            workspace_dir=tmp_path,
            tools=[],
        )
    assert removed == [True]


def test_executor_construction_failure_cleans_started_manager(monkeypatch, tmp_path):
    import core.agent as agent_module
    import core.exec as exec_module
    from core.kernel import KernelManager

    for key in ("CLAUDE_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "DEEPSEEK_API_KEY"):
        monkeypatch.setenv(key, "test-dummy")
    shutdowns = []
    original_shutdown = KernelManager.shutdown

    def shutdown(manager):
        shutdowns.append(tuple(kernel.pid for kernel in manager.kernels.values()))
        original_shutdown(manager)

    class BrokenExecutor:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("executor construction failed")

    monkeypatch.setattr(KernelManager, "shutdown", shutdown)
    monkeypatch.setattr(exec_module, "ExecPythonExecutor", BrokenExecutor)
    with pytest.raises(RuntimeError, match="executor construction failed"):
        agent_module.create_agent(
            config_dir=_CONFIGS_DIR,
            workspace_dir=tmp_path,
            tools=[],
        )
    assert len(shutdowns) == 1 and shutdowns[0]


def test_exec_timeout_config_cannot_resurface():
    """The removed hidden watchdog must stay absent from shipped runtime inputs."""
    forbidden = "exec_" + "timeout_s"
    assert forbidden not in (_CONFIGS_DIR / "llm_config.yaml").read_text()
    for rel_path in ("core/agent.py", "core/exec.py"):
        assert forbidden not in (_REPO_ROOT / "code" / rel_path).read_text()
