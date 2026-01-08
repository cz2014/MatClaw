"""CodeAgent initialization from YAML config and prompt templates (simplified)."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from smolagents import CodeAgent, LiteLLMModel
from smolagents.agents import (
    FinalAnswerPromptTemplate,
    PlanningPromptTemplate,
    PromptTemplates,
)

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
WORKSPACE_DIR = PROJECT_ROOT / "workspace"

_ENV_PATTERN = re.compile(r"\$\{[^}]+\}")  # leftover ${VAR} after expandvars


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


def _build_prompt_templates(prompts_cfg: dict[str, Any]) -> PromptTemplates | None:
    """Build PromptTemplates only if user actually set any prompt content.

    IMPORTANT: do NOT default missing fields to "", because that can wipe defaults.
    """
    if not prompts_cfg:
        return None

    system_prompt = prompts_cfg.get("system_prompt")
    planning_cfg = prompts_cfg.get("planning") or {}
    final_cfg = prompts_cfg.get("final_answer") or {}

    # Determine if anything is actually provided
    has_any = any(
        bool(x)
        for x in [
            system_prompt,
            planning_cfg.get("plan"),
            planning_cfg.get("update_plan_pre_messages"),
            planning_cfg.get("update_plan_post_messages"),
            final_cfg.get("pre_messages"),
            final_cfg.get("post_messages"),
        ]
    )
    if not has_any:
        return None

    planning = PlanningPromptTemplate(
        plan=planning_cfg.get("plan"),
        update_plan_pre_messages=planning_cfg.get("update_plan_pre_messages"),
        update_plan_post_messages=planning_cfg.get("update_plan_post_messages"),
    )
    final_answer = FinalAnswerPromptTemplate(
        pre_messages=final_cfg.get("pre_messages"),
        post_messages=final_cfg.get("post_messages"),
    )

    return PromptTemplates(
        system_prompt=system_prompt,
        planning=planning,
        final_answer=final_answer,
    )


def create_agent(
    provider_name: str | None = None,
    enable_step_logging: bool = True,
    workspace_dir: Path = WORKSPACE_DIR,
    planning_interval: int | None = None,
) -> CodeAgent:
    """Create a CodeAgent with config from YAML files.

    Args:
        provider_name: LLM provider name. Defaults to config default_provider.
        enable_step_logging: Whether to log steps to JSONL file in workspace.
        workspace_dir: Directory for log files. Defaults to WORKSPACE_DIR.
        planning_interval: Steps between planning updates. None disables planning.

    Returns:
        Configured CodeAgent instance.
    """
    llm_cfg = _read_yaml(CONFIG_DIR / "llm_config.yaml")
    prompts_path = CONFIG_DIR / "prompts.yaml"
    prompts_cfg = _read_yaml(prompts_path) if prompts_path.exists() else {}

    provider_name = provider_name or llm_cfg["default_provider"]
    provider_cfg = llm_cfg["providers"][provider_name]

    model = LiteLLMModel(
        model_id=provider_cfg["model_id"],
        api_key=_expand_env_strict(provider_cfg["api_key"]),
    )

    agent_cfg = llm_cfg.get("agent", {})
    prompt_templates = _build_prompt_templates(prompts_cfg)

    kwargs: dict[str, Any] = dict(
        tools=[],
        model=model,
        max_steps=agent_cfg.get("max_steps", 10),
        add_base_tools=False,
        return_full_result=True,
    )

    if prompt_templates is not None:
        kwargs["prompt_templates"] = prompt_templates

    additional_imports = agent_cfg.get("additional_authorized_imports") or []
    if additional_imports:
        kwargs["additional_authorized_imports"] = additional_imports

    if planning_interval is not None:
        kwargs["planning_interval"] = planning_interval

    if enable_step_logging:
        steps_log = _make_steps_log_path(workspace_dir)
        kwargs["step_callbacks"] = [_step_jsonl_logger(steps_log)]
        print(f"[agent] steps_log={steps_log}")

    return CodeAgent(**kwargs)
