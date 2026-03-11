"""CodeAgent initialization from YAML config and prompt templates (simplified)."""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from smolagents import CodeAgent, LiteLLMModel, LocalPythonExecutor

from core.tools import batch_static_eval, rag_search, train_deepmd, wait_for_jobflow
from smolagents.agents import (
    FinalAnswerPromptTemplate,
    ManagedAgentPromptTemplate,
    PlanningPromptTemplate,
    PromptTemplates,
)
from smolagents.models import CODEAGENT_RESPONSE_FORMAT

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent

# Monkey-patch structured output schema:
# 1. Rename "thought" -> "plan" to avoid GPT-5.2 ContentPolicyViolationError
#    (OpenAI's input filter rejects "thought process" / chain-of-thought framing)
# 2. Add "summary" field (placed last so LLM generates plan and code first)
_so_schema = CODEAGENT_RESPONSE_FORMAT["json_schema"]["schema"]
_so_schema["properties"]["plan"] = {
    "description": "Explain what this step does and how it contributes to next steps.",
    "title": "Plan",
    "type": "string",
}
del _so_schema["properties"]["thought"]
_so_schema["properties"]["code"]["description"] = (
    "Valid Python code snippet implementing the plan."
)
_so_schema["required"] = ["plan", "code"]
_so_schema["title"] = "PlanAndCodeAnswer"
CODEAGENT_RESPONSE_FORMAT["json_schema"]["name"] = "PlanAndCodeAnswer"
_so_schema["properties"]["summary"] = {
    "description": (
        "One-line summary of what this step does "
        "(e.g. 'Search RAG for VASP INCAR parameters')."
    ),
    "title": "Summary",
    "type": "string",
}
_so_schema["required"].append("summary")

_ENV_PATTERN = re.compile(r"\$\{[^}]+\}")  # leftover ${VAR} after expandvars
_API_ERROR_PATTERN = re.compile(
    r"(AttributeError|TypeError|ImportError|ModuleNotFoundError|has no attribute|unexpected keyword)",
    re.IGNORECASE,
)
_MAX_ERROR_CHARS = 20_000  # cap error messages to match smolagents' MAX_LENGTH_TRUNCATE_CONTENT


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
            "step": step.dict() if hasattr(step, "dict") else repr(step),
        }
        with log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")

    return cb


def _on_step_error(step, agent) -> None:
    """Truncate oversized errors + add RAG hints to help agent self-correct."""
    from smolagents import ActionStep

    if not isinstance(step, ActionStep):
        return
    if not step.error:
        return

    # --- Truncate oversized error messages ---
    # smolagents injects full str(error) into conversation with no size limit.
    # A BulkWriteError with a 19.9MB document dump produced a 28MB message that
    # destroyed all context in run 7. Cap to head + tail.
    err_msg = str(step.error)
    if len(err_msg) > _MAX_ERROR_CHARS:
        half = _MAX_ERROR_CHARS // 2
        truncated = (
            err_msg[:half]
            + f"\n\n...[truncated {len(err_msg) - _MAX_ERROR_CHARS:,} chars]...\n\n"
            + err_msg[-half:]
        )
        if hasattr(step.error, "message"):
            step.error.message = truncated
        step.error.args = (truncated,)
        print(f"[step_error] Truncated error at step {step.step_number} "
              f"from {len(err_msg):,} to {len(truncated):,} chars")
        err_msg = truncated  # use truncated version for hint check below

    # --- RAG hint for API errors ---
    if "rag_search" not in agent.tools:
        return
    tool_hint = "rag_search"

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

    def _get_ssh_host(project_name: str, worker_name: str):
        """Get SSH host connection from jobflow-remote config."""
        from jobflow_remote.config.manager import ConfigManager

        cm = ConfigManager()
        project = cm.get_project(project_name)
        worker = project.workers[worker_name]
        host_config = worker.get_host()
        host_config.connect()
        return host_config

    def remote_put(
        local_rel_path: str,
        remote_dir: str,
        project_name: str,
        worker_name: str,
    ) -> str:
        """Upload a file or directory from workspace to remote HPC.

        Args:
            local_rel_path: Path relative to workspace (enforced boundary).
            remote_dir: Remote directory to upload into.
            project_name: jobflow-remote project name.
            worker_name: jobflow-remote worker name.

        Returns:
            Remote path of uploaded file/directory.
        """
        local_abs = _safe_path(local_rel_path)
        if not local_abs.exists():
            raise FileNotFoundError(f"Local path not found: {local_abs}")

        host = _get_ssh_host(project_name, worker_name)
        remote_target = f"{remote_dir}/{local_abs.name}"

        if local_abs.is_file():
            host.mkdir(remote_dir)
            host.put(str(local_abs), remote_target)
        elif local_abs.is_dir():
            import tarfile
            import tempfile

            with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
                tmp_path = tmp.name
            try:
                with tarfile.open(tmp_path, "w:gz") as tar:
                    tar.add(str(local_abs), arcname=local_abs.name)
                remote_tar = f"/tmp/_agent_upload_{local_abs.name}.tar.gz"
                host.mkdir(remote_dir)
                host.put(tmp_path, remote_tar)
                host.execute(
                    f"tar -xzf {remote_tar} -C {remote_dir} && rm {remote_tar}"
                )
            finally:
                Path(tmp_path).unlink(missing_ok=True)
        else:
            raise ValueError(f"Not a file or directory: {local_abs}")

        print(f"[remote_put] {local_abs} -> {remote_target}", flush=True)
        return remote_target

    def remote_get(
        remote_path: str,
        local_rel_path: str,
        project_name: str,
        worker_name: str,
    ) -> str:
        """Download a file or directory from remote HPC to workspace.

        Args:
            remote_path: Absolute path on remote.
            local_rel_path: Destination path relative to workspace.
            project_name: jobflow-remote project name.
            worker_name: jobflow-remote worker name.

        Returns:
            Absolute local path of downloaded file/directory.
        """
        local_abs = _safe_path(local_rel_path)
        host = _get_ssh_host(project_name, worker_name)

        is_dir_result = host.execute(f"test -d {remote_path} && echo DIR || echo FILE")
        is_dir = is_dir_result.stdout.strip() == "DIR"

        if is_dir:
            import tarfile
            import tempfile

            remote_name = Path(remote_path).name
            remote_tar = f"/tmp/_agent_download_{remote_name}.tar.gz"
            remote_parent = str(Path(remote_path).parent)
            host.execute(
                f"tar -czf {remote_tar} -C {remote_parent} {remote_name}"
            )
            with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
                tmp_path = tmp.name
            try:
                host.get(remote_tar, tmp_path)
                host.execute(f"rm {remote_tar}")
                local_abs.parent.mkdir(parents=True, exist_ok=True)
                with tarfile.open(tmp_path, "r:gz") as tar:
                    tar.extractall(str(local_abs.parent))
            finally:
                Path(tmp_path).unlink(missing_ok=True)
        else:
            local_abs.parent.mkdir(parents=True, exist_ok=True)
            host.get(remote_path, str(local_abs))

        print(f"[remote_get] {remote_path} -> {local_abs}", flush=True)
        return str(local_abs)

    def remote_ls(
        remote_path: str,
        project_name: str,
        worker_name: str,
    ) -> list[str]:
        """List files in a remote directory.

        Args:
            remote_path: Absolute path on remote.
            project_name: jobflow-remote project name.
            worker_name: jobflow-remote worker name.

        Returns:
            List of filenames in the directory.
        """
        host = _get_ssh_host(project_name, worker_name)
        result = host.execute(f"ls -1 {remote_path}")
        entries = [e for e in result.stdout.strip().split("\n") if e]
        return entries

    return {
        "write_text": write_text,
        "read_text": read_text,
        "remote_put": remote_put,
        "remote_get": remote_get,
        "remote_ls": remote_ls,
    }


def _save_config_snapshot(config_dir: Path, workspace_dir: Path, prompts_file: str) -> None:
    """Copy config files as hidden files into workspace for reproducibility."""
    import shutil

    files_to_copy = [
        ("llm_config.yaml", ".llm_config.yaml"),
        (prompts_file, ".prompts.yaml"),
        ("rag_config.yaml", ".rag_config.yaml"),
    ]
    for src_name, dst_name in files_to_copy:
        src = config_dir / src_name
        if src.exists():
            shutil.copy2(src, workspace_dir / dst_name)


def _build_prompt_templates(prompts_cfg: dict[str, Any]) -> PromptTemplates | None:
    """Build PromptTemplates only if user actually set any prompt content.

    IMPORTANT: do NOT default missing fields to "", because that can wipe defaults.
    """
    if not prompts_cfg:
        return None

    system_prompt = prompts_cfg.get("system_prompt")
    if system_prompt is None:
        raise ValueError(
            "system_prompt must not be null -- smolagents default prompt contains "
            "GPT-5.2-incompatible 'thought' framing. "
            "Provide an explicit system_prompt in your prompts YAML."
        )
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


class RetryingLiteLLMModel(LiteLLMModel):
    """LiteLLMModel that retries on empty content, transient API errors, and
    auto-pauses on connection errors.

    Empty-content retry: Gemini intermittently returns content=None with
    completion_tokens=0. LiteLLM treats this as success (HTTP 200), so its
    built-in retries don't trigger. This subclass retries up to EMPTY_RETRIES
    times before returning the empty response to smolagents.

    Transient API error retry: Some LLM errors (e.g. OpenAI content policy
    false positives) are transient -- the same prompt succeeds on retry.
    These are retried up to TRANSIENT_RETRIES times with exponential backoff,
    then auto-paused if a PauseController is set.

    Connection error pause: When a transient connection/server error is detected,
    the agent is paused (via PauseController) instead of crashing. The user can
    fix the issue and resume to retry the LLM call.
    """

    EMPTY_RETRIES = 3
    EMPTY_RETRY_WAIT = 1.0  # seconds, doubles each retry

    TRANSIENT_RETRIES = 3
    TRANSIENT_RETRY_WAIT = 5.0  # seconds, doubles each retry

    _CONNECTION_ERROR_PATTERNS = [
        "connection", "timeout", "timed out", "refused",
        "reset by peer", "broken pipe", "eof", "ssl",
        "service unavailable", "503", "502", "500",
        "internal server error", "bad gateway",
    ]

    _TRANSIENT_API_ERROR_PATTERNS = [
        "content policy", "usage policy",
        "overloaded", "temporarily unavailable",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pause_controller = None

    def set_pause_controller(self, pc):
        self._pause_controller = pc

    def _is_connection_error(self, exc: Exception) -> bool:
        """Check if exception is a transient connection/server error."""
        msg = str(exc).lower()
        return any(p in msg for p in self._CONNECTION_ERROR_PATTERNS)

    def _is_transient_api_error(self, exc: Exception) -> bool:
        """Check if exception is a transient API error worth retrying."""
        msg = str(exc).lower()
        return any(p in msg for p in self._TRANSIENT_API_ERROR_PATTERNS)

    def _inject_cache_control(self, messages):
        """Add cache_control breakpoints for Anthropic prompt caching.

        Marks the last content block of the last message with cache_control.
        Anthropic's incremental caching will read previously cached prefixes
        and extend the cache with each new step. Per the docs: "blocks that
        were previously marked with cache_control are later not marked with
        this, but they will still be considered a cache hit."

        Also marks the system message for caching (effective when the system
        prompt alone exceeds 2048 tokens, e.g. with large tool definitions).
        """
        if not self.model_id.startswith("anthropic/"):
            return
        # Mark system message
        for msg in messages:
            role = msg.role if hasattr(msg, "role") else msg.get("role")
            if role == "system" or (hasattr(role, "value") and role.value == "system"):
                content = msg.content if hasattr(msg, "content") else msg.get("content")
                if isinstance(content, list) and content:
                    content[-1]["cache_control"] = {"type": "ephemeral"}
                break
        # Mark the last message for incremental conversation caching
        if len(messages) >= 2:
            last = messages[-1]
            content = last.content if hasattr(last, "content") else last.get("content")
            if isinstance(content, list) and content:
                content[-1]["cache_control"] = {"type": "ephemeral"}
            elif isinstance(content, str):
                new_content = [{"type": "text", "text": content, "cache_control": {"type": "ephemeral"}}]
                if hasattr(last, "content"):
                    last.content = new_content
                else:
                    last["content"] = new_content

    def _generate_with_empty_retry(self, messages, stop_sequences=None, **kwargs):
        """Generate with retries for empty responses (Gemini content=None)."""
        self._inject_cache_control(messages)
        last_response = None
        for attempt in range(self.EMPTY_RETRIES + 1):
            result = super().generate(messages, stop_sequences=stop_sequences, **kwargs)
            if result.content is not None:
                return result
            last_response = result
            if attempt < self.EMPTY_RETRIES:
                wait = self.EMPTY_RETRY_WAIT * (2 ** attempt)
                logger.warning(
                    "Empty response from %s (attempt %d/%d, completion_tokens=0). "
                    "Retrying in %.1fs...",
                    self.model_id, attempt + 1, self.EMPTY_RETRIES, wait,
                )
                time.sleep(wait)
        logger.warning(
            "Empty response from %s persisted after %d retries.",
            self.model_id, self.EMPTY_RETRIES,
        )
        return last_response

    def generate(self, messages, stop_sequences=None, **kwargs):
        """Generate with retry for transient API errors and auto-pause on connection errors."""
        transient_attempt = 0
        while True:
            try:
                return self._generate_with_empty_retry(
                    messages, stop_sequences=stop_sequences, **kwargs
                )
            except Exception as exc:
                # Connection errors: auto-pause immediately (user must resume)
                if self._is_connection_error(exc):
                    if self._pause_controller is None:
                        raise
                    logger.warning(
                        "LLM connection error: %s. Pausing agent -- "
                        "fix the issue and resume to retry.", exc,
                    )
                    self._pause_controller.request_pause(
                        reason=f"LLM connection error: {exc}"
                    )
                    self._pause_controller.wait_if_paused()
                    logger.info("Resumed after connection error, retrying LLM call")
                    continue

                # Transient API errors: retry with backoff, then auto-pause
                if self._is_transient_api_error(exc):
                    transient_attempt += 1
                    if transient_attempt <= self.TRANSIENT_RETRIES:
                        wait = self.TRANSIENT_RETRY_WAIT * (2 ** (transient_attempt - 1))
                        logger.warning(
                            "Transient API error (attempt %d/%d): %s. "
                            "Retrying in %.1fs...",
                            transient_attempt, self.TRANSIENT_RETRIES, exc, wait,
                        )
                        time.sleep(wait)
                        continue
                    # Retries exhausted: auto-pause if possible
                    if self._pause_controller is not None:
                        logger.warning(
                            "Transient API error persisted after %d retries: %s. "
                            "Pausing agent.", self.TRANSIENT_RETRIES, exc,
                        )
                        self._pause_controller.request_pause(
                            reason=f"API error after {self.TRANSIENT_RETRIES} retries: {exc}"
                        )
                        self._pause_controller.wait_if_paused()
                        transient_attempt = 0
                        logger.info("Resumed after transient API error, retrying LLM call")
                        continue

                # All other errors: raise immediately
                raise


def _resolve_worker_instructions(project_name: str, llm_cfg: dict[str, Any]) -> str:
    """Build worker instructions from llm_config + jfremote project YAML.

    For each worker in this project:
    1. Injects the human-written description from llm_config.yaml
    2. Injects the raw jfremote worker YAML source for full technical details
    """
    workers_cfg = llm_cfg.get("workers", {})

    prefix = f"{project_name}."
    project_workers = {
        k[len(prefix):]: v
        for k, v in workers_cfg.items()
        if k.startswith(prefix)
    }
    if not project_workers:
        return ""

    jfremote_dir = Path.home() / ".jfremote"
    config_path = jfremote_dir / f"{project_name}.yaml"
    jfremote_workers: dict[str, Any] = {}
    if config_path.exists():
        jfremote_cfg = _read_yaml(config_path)
        jfremote_workers = jfremote_cfg.get("workers", {})

    lines = [
        "Remote HPC configuration:",
        f'- Project: "{project_name}"',
        "",
        "Available workers (use worker= kwarg in submit_flow):",
    ]

    for worker_name, wcfg in project_workers.items():
        desc = wcfg.get("description", "").strip()
        lines.append(f'- "{worker_name}": {desc}' if desc else f'- "{worker_name}"')

        if worker_name in jfremote_workers:
            raw_cfg = yaml.dump(
                {worker_name: jfremote_workers[worker_name]},
                default_flow_style=False,
                sort_keys=False,
            ).strip()
            lines.append("")
            lines.append(f"  Worker config ({project_name}.yaml):")
            for raw_line in raw_cfg.splitlines():
                lines.append(f"  {raw_line}")
            lines.append("")

    return "\n".join(lines)


def create_agent(
    config_dir: Path,
    workspace_dir: Path,
    provider_name: str | None = None,
    tools: list | None = None,
    enable_step_logging: bool = True,
    planning_interval: int | None = None,
    final_answer_checks: list | None = None,
    prompts_file: str = "prompts.yaml",
    project: str | None = None,
    instructions_extra: str | None = None,
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
        prompts_file: Prompts YAML filename in config_dir. Defaults to "prompts.yaml".
        project: HPC project name for auto-resolving worker config. When set,
            worker descriptions and raw jfremote YAML are injected into instructions.
        instructions_extra: Extra instructions appended to config instructions
            (for non-project overrides like task-specific constraints).

    Returns:
        Configured CodeAgent instance.
    """
    # Read all configs from config_dir
    llm_cfg = _read_yaml(config_dir / "llm_config.yaml")

    prompts_path = config_dir / prompts_file
    prompts_cfg = _read_yaml(prompts_path) if prompts_path.exists() else {}

    # Snapshot config files into workspace for reproducibility
    _save_config_snapshot(config_dir, workspace_dir, prompts_file)

    provider_name = provider_name or llm_cfg["default_provider"]
    provider_cfg = llm_cfg["providers"][provider_name]

    # Forward any extra provider config keys (e.g. timeout, api_base) to LiteLLM
    model_kwargs = {
        k: v for k, v in provider_cfg.items()
        if k not in ("model_id", "api_key", "context_window")
    }
    api_key = _expand_env_strict(provider_cfg["api_key"])
    model = RetryingLiteLLMModel(
        model_id=provider_cfg["model_id"],
        api_key=api_key,
        **model_kwargs,
    )

    agent_cfg = llm_cfg.get("agent", {})

    # Context window management (unified zone-based pruning + caching)
    if agent_cfg.get("context_pruning", True):
        from core.context import wrap_model_with_context_management

        model_id = provider_cfg["model_id"]
        try:
            import litellm as _litellm
            _model_info = _litellm.get_model_info(model_id)
            detected_tokens = _model_info.get("max_input_tokens", 128_000)
        except Exception:
            detected_tokens = 128_000
            logger.warning(
                "Unknown model %s, using default context_window=128000", model_id
            )

        # Per-provider context_window takes priority over global agent.context_window
        config_cap = provider_cfg.get("context_window") or agent_cfg.get("context_window")
        if config_cap and config_cap < detected_tokens:
            context_tokens = config_cap
            logger.info(
                "Context window capped to %d tokens (model has %d)",
                config_cap, detected_tokens,
            )
        else:
            context_tokens = detected_tokens

        model = wrap_model_with_context_management(model, context_tokens, model_id)
    else:
        logger.info("Context management disabled (context_pruning: false)")

    prompt_templates = _build_prompt_templates(prompts_cfg)

    # Create executor with sandboxed file functions
    additional_imports = agent_cfg.get("additional_authorized_imports") or []
    sandbox_funcs = _create_sandbox_functions(workspace_dir)
    os.chdir(workspace_dir.resolve())
    # Disable smolagents' 30s code execution timeout. It's broken in v1.24.0:
    # ThreadPoolExecutor.shutdown(wait=True) blocks until the thread finishes,
    # making the timeout useless. Our wait_for_jobflow has its own timeout.
    executor = LocalPythonExecutor(
        additional_imports,
        additional_functions=sandbox_funcs,
        timeout_seconds=None,
    )

    # Tools: use custom list or default (includes rag_search for main agent)
    if tools is None:
        tools = [wait_for_jobflow, train_deepmd, batch_static_eval, rag_search]

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
        use_structured_outputs_internally=True,
    )

    if prompt_templates is not None:
        kwargs["prompt_templates"] = prompt_templates

    instructions = agent_cfg.get("instructions", "")

    if project:
        worker_info = _resolve_worker_instructions(project, llm_cfg)
        if worker_info:
            instructions = instructions.rstrip() + "\n\n" + worker_info

    if instructions_extra:
        instructions = instructions.rstrip() + "\n" + instructions_extra

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


# --- Pause/resume support ---


class PauseController:
    """In-process pause/resume via threading.Event.

    Event SET = running (wait_if_paused returns immediately).
    Event CLEAR = paused (wait_if_paused blocks).
    Thread-safe: threading.Event + CPython GIL for bool access.
    """

    def __init__(self):
        self._event = threading.Event()
        self._event.set()  # start running
        self._reason = None

    @property
    def is_paused(self) -> bool:
        return not self._event.is_set()

    def request_pause(self, reason: str = ""):
        """Pause the agent. Called by keyboard listener or auto-pause on errors."""
        self._reason = reason
        self._event.clear()
        if reason:
            print(f"[PAUSED] {reason} -- Press 'r' to resume", flush=True)
        else:
            print("[PAUSED] Press 'r' to resume", flush=True)

    def resume(self):
        self._event.set()
        print("[RESUMED]", flush=True)

    def wait_if_paused(self, context: str = ""):
        if self._event.is_set():
            return
        if context:
            print(f"[PAUSED] {context}", flush=True)
        self._event.wait()


def start_keyboard_listener(controller: PauseController):
    """Daemon thread: 'p' to pause, 'r' to resume. Uses tty.setcbreak
    for single-char input. Returns None if stdin is not a TTY."""
    if not sys.stdin.isatty():
        return None

    def _listener():
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch == "p" and not controller.is_paused:
                    controller.request_pause()
                elif ch == "r" and controller.is_paused:
                    controller.resume()
        except (EOFError, OSError):
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    thread = threading.Thread(target=_listener, daemon=True, name="pause-listener")
    thread.start()
    return thread


def _make_pause_callback(controller: PauseController):
    """Step callback that blocks when paused. Register LAST (after JSONL logger)."""
    def cb(step, agent):
        controller.wait_if_paused(
            context=f"After step {getattr(step, 'step_number', '?')}"
        )
    return cb
