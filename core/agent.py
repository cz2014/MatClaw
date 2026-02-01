"""CodeAgent initialization from YAML config and prompt templates (simplified)."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from smolagents import CodeAgent, LiteLLMModel, LocalPythonExecutor

from core.tools import api_probe, train_deepmd, wait_for_jobflow
from smolagents.agents import (
    FinalAnswerPromptTemplate,
    ManagedAgentPromptTemplate,
    PlanningPromptTemplate,
    PromptTemplates,
)

PROJECT_ROOT = Path(__file__).parent.parent

_ENV_PATTERN = re.compile(r"\$\{[^}]+\}")  # leftover ${VAR} after expandvars
_API_ERROR_PATTERN = re.compile(
    r"(AttributeError|TypeError|ImportError|ModuleNotFoundError|has no attribute|unexpected keyword)",
    re.IGNORECASE,
)


def _read_yaml(path: Path) -> dict[str, Any]:
    """Read YAML file, return empty dict if file doesn't exist or is empty."""
    if not path.exists():
        raise FileNotFoundError(f"YAML not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise TypeError(f"YAML root must be a mapping: {path}")
    return data


def _expand_env_strict(value: str) -> str:
    """Expand $VAR and ${VAR}; error if any ${...} remains unresolved."""
    expanded = os.path.expandvars(value)
    if _ENV_PATTERN.search(expanded):
        raise ValueError(f"Unresolved env var(s) in: {value!r}")
    return expanded


def _make_steps_log_path(workspace_dir: Path) -> Path:
    """Create workspace directory and return path for steps log."""
    workspace_dir.mkdir(parents=True, exist_ok=True)
    return workspace_dir / "steps.jsonl"


def _step_jsonl_logger(log_file: Path):
    """Create a step callback that logs each step to JSONL file."""

    def cb(step, agent):
        rec = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "step_type": type(step).__name__,
            "step": step.model_dump() if hasattr(step, "model_dump") else repr(step),
        }
        with log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    return cb


def _on_step_error(step, agent) -> None:
    """Add hints to step errors to help agent self-correct."""
    from smolagents import ActionStep

    if not isinstance(step, ActionStep):
        return
    if not step.error:
        return

    # Build tool hint from available tools
    has_rag = "rag_search" in agent.tools
    has_probe = "api_probe" in agent.tools
    if has_rag and has_probe:
        tool_hint = "rag_search or api_probe"
    elif has_probe:
        tool_hint = "api_probe"
    elif has_rag:
        tool_hint = "rag_search"
    else:
        return

    err_msg = str(step.error)
    if not _API_ERROR_PATTERN.search(err_msg):
        return

    # Soft nudge - append hint to error message
    hint = (
        "\n\nHint: If you are not 100% certain about an API path or kwarg, "
        f"call {tool_hint} before trying variants."
    )
    new_msg = err_msg + hint
    # Update both .message attr and Exception.args for str() compatibility
    if hasattr(step.error, "message"):
        step.error.message = new_msg
    step.error.args = (new_msg,)
    print(f"[step_error] Added hint to step {step.step_number}")


def _create_sandbox_functions(workspace: Path) -> dict[str, callable]:
    """Create sandboxed file I/O functions bound to workspace."""
    workspace = workspace.resolve()

    def _safe_path(rel_path: str) -> Path:
        p = (workspace / rel_path).resolve()
        if p == workspace or workspace in p.parents:
            return p
        raise ValueError(f"Path outside workspace: {rel_path}")

    def write_text(rel_path: str, content: str) -> str:
        """Write text to a file in workspace. Returns absolute path."""
        p = _safe_path(rel_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        if len(content) > 5_000_000:
            raise ValueError("Refusing to write >5MB in one call")
        p.write_text(content, encoding="utf-8")
        return str(p)

    def read_text(rel_path: str) -> str:
        """Read text from a file in workspace."""
        p = _safe_path(rel_path)
        return p.read_text(encoding="utf-8")

    return {"write_text": write_text, "read_text": read_text}


def _build_prompt_templates(prompts_cfg: dict[str, Any]) -> PromptTemplates | None:
    """Build PromptTemplates only if user actually set any prompt content.

    IMPORTANT: do NOT default missing fields to "", because that can wipe defaults.
    """
    if not prompts_cfg:
        return None

    system_prompt = prompts_cfg.get("system_prompt")
    planning_cfg = prompts_cfg.get("planning") or {}
    managed_cfg = prompts_cfg.get("managed_agent") or {}
    final_cfg = prompts_cfg.get("final_answer") or {}

    # Determine if anything is actually provided
    has_any = any(
        bool(x)
        for x in [
            system_prompt,
            planning_cfg.get("initial_plan"),
            planning_cfg.get("update_plan_pre_messages"),
            planning_cfg.get("update_plan_post_messages"),
            managed_cfg.get("task"),
            managed_cfg.get("report"),
            final_cfg.get("pre_messages"),
            final_cfg.get("post_messages"),
        ]
    )
    if not has_any:
        return None

    # Use "" for any None/missing fields -- smolagents TypedDicts require all keys
    # present, and populate_template(None, {}) crashes. The framework itself uses
    # "" in EMPTY_PROMPT_TEMPLATES for unused fields.
    planning = PlanningPromptTemplate(
        initial_plan=planning_cfg.get("initial_plan") or "",
        update_plan_pre_messages=planning_cfg.get("update_plan_pre_messages") or "",
        update_plan_post_messages=planning_cfg.get("update_plan_post_messages") or "",
    )
    managed_agent = ManagedAgentPromptTemplate(
        task=managed_cfg.get("task") or "",
        report=managed_cfg.get("report") or "",
    )
    final_answer = FinalAnswerPromptTemplate(
        pre_messages=final_cfg.get("pre_messages") or "",
        post_messages=final_cfg.get("post_messages") or "",
    )

    return PromptTemplates(
        system_prompt=system_prompt,
        planning=planning,
        managed_agent=managed_agent,
        final_answer=final_answer,
    )


def create_agent(
    config_dir: Path,
    workspace_dir: Path,
    provider_name: str | None = None,
    tools: list | None = None,
    enable_step_logging: bool = True,
    planning_interval: int | None = None,
    final_answer_checks: list | None = None,
) -> CodeAgent:
    """Create a CodeAgent with config from YAML files.

    Args:
        config_dir: Directory containing llm_config.yaml, prompts.yaml, rag_config.yaml.
        workspace_dir: Directory for workspace and logs.
        provider_name: LLM provider name. Defaults to config default_provider.
        tools: Custom tools list. Defaults to [wait_for_jobflow, train_deepmd].
        enable_step_logging: Whether to log steps to JSONL file in workspace.
        planning_interval: Steps between planning updates. None disables planning.
        final_answer_checks: List of check functions passed to CodeAgent.

    Returns:
        Configured CodeAgent instance.
    """
    # Read all configs from config_dir
    llm_cfg = _read_yaml(config_dir / "llm_config.yaml")

    prompts_path = config_dir / "prompts.yaml"
    prompts_cfg = _read_yaml(prompts_path) if prompts_path.exists() else {}

    provider_name = provider_name or llm_cfg["default_provider"]
    provider_cfg = llm_cfg["providers"][provider_name]

    # Forward any extra provider config keys (e.g. timeout, api_base) to LiteLLM
    model_kwargs = {
        k: v for k, v in provider_cfg.items()
        if k not in ("model_id", "api_key")
    }
    model = LiteLLMModel(
        model_id=provider_cfg["model_id"],
        api_key=_expand_env_strict(provider_cfg["api_key"]),
        **model_kwargs,
    )

    agent_cfg = llm_cfg.get("agent", {})
    prompt_templates = _build_prompt_templates(prompts_cfg)

    # Create executor with sandboxed file functions
    additional_imports = agent_cfg.get("additional_authorized_imports") or []
    sandbox_funcs = _create_sandbox_functions(workspace_dir)
    executor = LocalPythonExecutor(
        additional_imports,
        additional_functions=sandbox_funcs,
    )

    # Tools: use custom list or default
    if tools is None:
        tools = [wait_for_jobflow, train_deepmd, api_probe]

    # Max steps from config
    max_steps = agent_cfg.get("max_steps", 10)

    kwargs: dict[str, Any] = dict(
        tools=tools,
        model=model,
        executor=executor,
        additional_authorized_imports=additional_imports,
        max_steps=max_steps,
        add_base_tools=False,
        return_full_result=True,
    )

    if prompt_templates is not None:
        kwargs["prompt_templates"] = prompt_templates

    instructions = agent_cfg.get("instructions")
    if instructions:
        kwargs["instructions"] = instructions

    if planning_interval is not None:
        kwargs["planning_interval"] = planning_interval

    if final_answer_checks:
        kwargs["final_answer_checks"] = final_answer_checks

    # Error hint callback runs first to modify errors before logging
    callbacks = [_on_step_error]
    if enable_step_logging:
        steps_log = _make_steps_log_path(workspace_dir)
        callbacks.append(_step_jsonl_logger(steps_log))
        print(f"[agent] steps_log={steps_log}")

    kwargs["step_callbacks"] = callbacks

    return CodeAgent(**kwargs)
