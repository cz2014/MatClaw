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
from core._smol import CodeAgent, LiteLLMModel

from core.context import _get_content_str, _get_role
from core.tools import wait_for_jobflow
from core._smol.agents import PromptTemplates

logger = logging.getLogger(__name__)

# repo root: code/core/agent.py -> core -> code -> repo root
PROJECT_ROOT = Path(__file__).parent.parent.parent

# NOTE: the structured-output schema (phase/plan/code/summary) is now defined
# directly in core/_smol/models.py CODEAGENT_RESPONSE_FORMAT (P-B1, folded in P2).
# No import-time monkeypatch here anymore.

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


def _load_corpus_registry(path: Path, corpus_dir: Path) -> list[dict]:
    """Load the reference-doc corpus registry (configs/corpus.yaml).

    Each entry has a `path` (relative to corpus_dir) + a 1-line `description`. Returns the
    resolved, existing corpora as [{"name", "path" (resolved Path), "description"}], skipping
    (with a warning) any whose directory is missing. Missing/empty config -> []. These corpora
    are added to grep's search roots and described in the system prompt so the agent knows what
    reference documentation exists and where to grep it (code lives in site-packages instead).
    """
    if not path.exists():
        return []
    cfg = _read_yaml(path)
    out: list[dict] = []
    for name, entry in (cfg.get("corpus") or {}).items():
        rel = (entry or {}).get("path")
        if not rel:
            continue
        resolved = (corpus_dir / rel).resolve()
        if not resolved.is_dir():
            logger.warning("corpus %r path not found, skipping: %s", name, resolved)
            continue
        out.append({
            "name": name,
            "path": resolved,
            "description": (entry.get("description") or "").strip(),
        })
    return out


def _corpus_instructions(site_packages: Path, corpora: list[dict]) -> str:
    """Build the system-prompt section: where to search for code (site-packages) + reference docs."""
    lines = [
        "## Searching for reference material",
        f"Source code for the installed Python packages lives under `{site_packages}`. Use `grep`/`glob` "
        "to search it, scoping to the relevant package (e.g. "
        f'`grep(pattern, path="{site_packages}/pymatgen")` or `glob("**/pymatgen/**")`).',
    ]
    if corpora:
        lines.append(
            "Additional reference documentation corpora (grep these directly for non-code references):"
        )
        for c in corpora:
            lines.append(f"  - {c['name']} (`{c['path']}`): {c['description']}")
    return "\n".join(lines)


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


def _extract_images_b64(msg) -> list[str]:
    """Extract PIL images from message content blocks, return as base64 PNG strings."""
    import base64
    import io

    images: list[str] = []
    if isinstance(msg, dict):
        content = msg.get("content", [])
    else:
        content = getattr(msg, "content", [])
    if not isinstance(content, list):
        return images
    for block in content:
        if isinstance(block, dict) and block.get("type") == "image":
            pil_img = block.get("image")
            if pil_img is not None:
                buf = io.BytesIO()
                pil_img.save(buf, format="PNG")
                images.append(base64.b64encode(buf.getvalue()).decode("ascii"))
    return images


def _history_writer(history_file: Path, workspace_dir: Path):
    """Create a step callback that appends new messages to history.jsonl.

    Each message is stored exactly once. The callback diffs the current
    model_input_messages against a running count of previously-written
    messages (bootstrap messages are written on the first step).

    Uses a global step counter (next_step) instead of step.step_number to
    ensure globally unique step numbers across multiple run() calls.
    smolagents resets step_number to 1 on every run(), but our counter
    continues from the max step in existing history.

    On restart (history_file already exists), the first callback skips all
    reconstructed messages and resumes the counter from max(step) + 1.
    """
    _state: dict = {
        "written": 0,
        "skip_first": history_file.exists(),
        "next_step": 1,
    }

    def cb(step, agent):
        import dataclasses

        from core._smol import ActionStep

        if not isinstance(step, ActionStep):
            return

        messages = step.model_input_messages
        if messages is None:
            return

        if _state["skip_first"]:
            _state["written"] = len(messages)
            _state["skip_first"] = False
            # Resume step counter from existing history
            max_step = 0
            with history_file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            rec = json.loads(line)
                            max_step = max(max_step, rec.get("step", 0))
                        except json.JSONDecodeError:
                            pass
            _state["next_step"] = max_step + 1
            return

        written = _state["written"]
        if len(messages) <= written:
            return

        new_messages = messages[written:]
        step_num = _state["next_step"]

        with history_file.open("a", encoding="utf-8") as f:
            for msg in new_messages:
                role = _get_role(msg)
                content = _get_content_str(msg)

                if written == 0 and role in ("system", "user"):
                    msg_step = 0
                else:
                    msg_step = step_num

                rec: dict = {
                    "step": msg_step,
                    "role": role,
                    "content": content,
                }

                if role == "assistant":
                    try:
                        parsed = json.loads(content)
                        if isinstance(parsed, dict):
                            rec["summary"] = parsed.get("summary")
                            rec["phase"] = parsed.get("phase")
                    except (json.JSONDecodeError, TypeError):
                        pass

                    if step.timing:
                        rec["timing"] = {
                            "start_time": step.timing.start_time,
                            "end_time": step.timing.end_time,
                        }
                    if step.error:
                        rec["error"] = step.error.dict()
                    if step.code_action is not None:
                        rec["code_action"] = step.code_action
                    if step.is_final_answer:
                        rec["is_final_answer"] = True
                    if step.token_usage:
                        rec["token_usage"] = dataclasses.asdict(step.token_usage)

                images_b64 = _extract_images_b64(msg)
                if images_b64:
                    rec["images_b64"] = images_b64

                f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
                written += 1

        _state["written"] = written
        _state["next_step"] = step_num + 1

    return cb


def _on_step_error(step, agent) -> None:
    """Append self-correction hints (RAG / experience) to a step error.

    Error-size capping happens at the source now (core/_smol/memory.py truncates str(error)
    when building the conversation message -- P-B3/V3), so this callback only adds advisory
    hints. truncate_content keeps head+tail, so the hints (appended last) survive the cap.
    """
    from core._smol import ActionStep

    if not isinstance(step, ActionStep):
        return
    if not step.error:
        return

    err_msg = str(step.error)

    # --- Code-search hint for API errors ---
    if _API_ERROR_PATTERN.search(err_msg):
        err_msg += (
            "\n\nHint: If you are not 100% certain about an API path or kwarg, "
            "grep the installed package source (under site-packages) before trying variants."
        )

    # --- Experience hint (unconditional) ---
    err_msg += (
        "\n\nHint: If this error reflects a reusable lesson, "
        "call write_experience to record it for future runs."
    )

    # Update both .message attr and Exception.args for str() compatibility
    if hasattr(step.error, "message"):
        step.error.message = err_msg
    step.error.args = (err_msg,)


_MAX_IMAGES_PER_STEP = 5
_MAX_IMAGE_BYTES = 2 * 1024 * 1024  # 2 MB


def _inject_workspace_images(workspace: Path):
    """Step callback: inject new workspace images into observations for LLM vision."""
    workspace = workspace.resolve()
    seen: set[str] = set()

    def cb(step, agent):
        from core._smol import ActionStep
        if not isinstance(step, ActionStep):
            return
        current = set()
        for ext in ("**/*.png", "**/*.jpg", "**/*.jpeg"):
            current.update(str(p.resolve()) for p in workspace.glob(ext))
        new = sorted(current - seen)
        seen.update(current)
        logger.debug(
            "[image_inject] workspace=%s current=%d seen=%d new=%d",
            workspace, len(current), len(seen), len(new),
        )
        if not new:
            return
        import PIL.Image
        imgs = []
        for path in new[:_MAX_IMAGES_PER_STEP]:
            if Path(path).stat().st_size > _MAX_IMAGE_BYTES:
                logger.debug("[image_inject] skipped (too large): %s", path)
                continue
            img = PIL.Image.open(path)
            img.load()
            imgs.append(img)
            logger.info("[image_inject] %s", Path(path).name)
        if imgs:
            step.observations_images = (step.observations_images or []) + imgs

    return cb


def _restart_from_history(agent: CodeAgent, history_file: Path) -> int:
    """Reconstruct agent memory from history.jsonl for restart.

    Populates agent.memory.steps with ActionStep objects reconstructed
    from the history file. Returns the next step_number to use.

    Executor variables are NOT restored (Python state is lost on crash).
    A restart message is injected to inform the agent.
    """
    from core._smol import ActionStep
    from core._smol.memory import Timing

    records: list[dict] = []
    with history_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    if not records:
        return 1

    by_step: dict[int, list[dict]] = {}
    for rec in records:
        by_step.setdefault(rec["step"], []).append(rec)

    max_step = max(by_step.keys())

    for step_num in sorted(by_step.keys()):
        if step_num == 0:
            continue

        step_records = by_step[step_num]
        model_output = None
        observations = None
        code_action = None
        timing = Timing(start_time=0.0, end_time=0.0)
        error = None
        is_final_answer = False
        token_usage = None
        images: list = []

        for rec in step_records:
            role = rec["role"]
            content = rec.get("content", "")
            if role == "assistant":
                model_output = content
                try:
                    parsed = json.loads(content)
                    code_action = parsed.get("code")
                except (json.JSONDecodeError, TypeError):
                    pass
                if "timing" in rec:
                    t = rec["timing"]
                    timing = Timing(
                        start_time=t.get("start_time", 0.0),
                        end_time=t.get("end_time", 0.0),
                    )
                if "error" in rec and rec["error"]:
                    from core._smol.utils import AgentError
                    err = rec["error"]
                    # AgentError requires an AgentLogger (its __init__ calls
                    # logger.log_error). Pass agent.logger, not the module-level
                    # logging logger, or restart crashes on any history that
                    # contains an error step.
                    error = AgentError(
                        err.get("message", str(err)) if isinstance(err, dict) else str(err),
                        agent.logger,
                    )
                if rec.get("is_final_answer"):
                    is_final_answer = True
                if "token_usage" in rec and rec["token_usage"]:
                    import dataclasses as _dc

                    from core._smol.monitoring import TokenUsage
                    init_fields = {f.name for f in _dc.fields(TokenUsage) if f.init}
                    token_usage = TokenUsage(**{
                        k: v for k, v in rec["token_usage"].items()
                        if k in init_fields
                    })
                if rec.get("code_action") is not None:
                    code_action = rec["code_action"]
            elif role in ("tool-response", "tool"):
                observations = content

            if "images_b64" in rec:
                import base64
                import io

                import PIL.Image
                for b64 in rec["images_b64"]:
                    img = PIL.Image.open(io.BytesIO(base64.b64decode(b64)))
                    img.load()
                    images.append(img)

        action_step = ActionStep(
            step_number=step_num,
            timing=timing,
            model_output=model_output,
            code_action=code_action,
            observations=observations,
            error=error,
            is_final_answer=is_final_answer,
            token_usage=token_usage,
        )
        if images:
            action_step.observations_images = images
        agent.memory.steps.append(action_step)

    restart_msg = (
        "\n\nAGENT RESTARTED. All Python executor variables from previous steps "
        "are lost. Use fetch_history and read_file to recover state. "
        "Do NOT assume any variable from prior steps exists."
    )
    last_actions = [s for s in agent.memory.steps if isinstance(s, ActionStep)]
    if last_actions:
        last = last_actions[-1]
        last.observations = (last.observations or "") + restart_msg
    else:
        restart_step = ActionStep(
            step_number=max_step + 1,
            timing=Timing(start_time=time.time()),
            observations=restart_msg.lstrip(),
        )
        agent.memory.steps.append(restart_step)

    logger.info(
        "Agent restarted from history: %d steps recovered", max_step,
    )


def _save_config_snapshot(config_dir: Path, workspace_dir: Path, prompts_file: str) -> None:
    """Copy config files as hidden files into workspace for reproducibility."""
    import shutil

    files_to_copy = [
        ("llm_config.yaml", ".llm_config.yaml"),
        (prompts_file, ".prompts.yaml"),
        ("corpus.yaml", ".corpus.yaml"),
    ]
    for src_name, dst_name in files_to_copy:
        src = config_dir / src_name
        if src.exists():
            shutil.copy2(src, workspace_dir / dst_name)


def _build_prompt_templates(prompts_cfg: dict[str, Any]) -> PromptTemplates | None:
    """Build PromptTemplates from config, returning only the fields actually set.

    Returns None when there is no prompt config (the agent then uses its built-in default).
    No "" padding (P-B4, folded in P2/V3): the vendored MultiStepAgent deep-merges any missing
    top-level/nested keys from EMPTY_PROMPT_TEMPLATES, so a partial dict is fine here.
    """
    if not prompts_cfg:
        return None

    # Fail-fast on missing essential config: MatClaw requires an explicit domain system_prompt
    # (configs/prompts.yaml); there is no implicit default worth degrading to silently.
    system_prompt = prompts_cfg.get("system_prompt")
    if system_prompt is None:
        raise ValueError(
            "system_prompt must not be null. Provide an explicit system_prompt in your "
            "prompts YAML (configs/prompts.yaml)."
        )

    templates: dict[str, Any] = {"system_prompt": system_prompt}
    for key in ("planning", "managed_agent", "final_answer"):
        cfg = prompts_cfg.get(key)
        if cfg:
            templates[key] = cfg
    return templates  # partial; the vendored agent fills the rest from EMPTY_PROMPT_TEMPLATES


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


def _setup_experience_reloader(agent: CodeAgent, experience_path: Path) -> None:
    """Set up dynamic experience injection: initial load + step callback + run wrapper.

    Monitors the experience file's mtime and refreshes the system prompt when
    the file changes. Handles three update scenarios:
    - Agent writes experience (step N) -> visible at step N+1 (step callback)
    - Human edits during a run -> visible next step (step callback)
    - Human edits between run() calls -> visible at run() start (run wrapper)
    """
    from core._smol import ActionStep
    from core._smol.agents import SystemPromptStep

    base_instructions = agent.instructions or ""

    _EXPERIENCE_MAX_TOKENS = 10_000
    _CHARS_PER_TOKEN = 4

    _cache: dict[str, float] = {"mtime": 0.0}

    def _refresh() -> bool:
        """Re-read experience file and update agent.instructions if changed."""
        if not experience_path.exists():
            return False
        mtime = experience_path.stat().st_mtime
        if mtime == _cache["mtime"]:
            return False
        _cache["mtime"] = mtime
        exp_text = experience_path.read_text(encoding="utf-8").strip()
        if exp_text:
            est_tokens = len(exp_text) // _CHARS_PER_TOKEN
            if est_tokens > _EXPERIENCE_MAX_TOKENS:
                logger.warning(
                    "Experience file %s is ~%d tokens (limit %d). "
                    "Consider pruning old notes or implementing experience_search.",
                    experience_path, est_tokens, _EXPERIENCE_MAX_TOKENS,
                )
            agent.instructions = base_instructions.rstrip() + "\n\n" + exp_text
        else:
            agent.instructions = base_instructions
        logger.info("Experience notes reloaded from %s", experience_path)
        return True

    # 1. Initial load
    _refresh()

    # 2. Step callback: within-run refresh (updates memory.system_prompt directly)
    # Signature (step, agent) matches smolagents CallbackRegistry convention:
    # 2-param callbacks receive (memory_step, agent=agent) via **kwargs.
    def _step_callback(step, agent=None):
        if _refresh() and agent is not None:
            agent.memory.system_prompt = SystemPromptStep(
                system_prompt=agent.system_prompt
            )

    # Register with CallbackRegistry if available, else append to list
    if hasattr(agent.step_callbacks, "register"):
        agent.step_callbacks.register(ActionStep, _step_callback)
    else:
        agent.step_callbacks.append(_step_callback)

    # 3. Run-start hook: between-run refresh (no run() reassignment -- P2/V3).
    # MultiStepAgent.run() invokes each callable in agent._on_run_start once per run.
    if not hasattr(agent, "_on_run_start"):
        agent._on_run_start = []
    agent._on_run_start.append(_refresh)


def create_agent(
    config_dir: Path,
    workspace_dir: Path,
    provider_name: str | None = None,
    tools: list | None = None,
    enable_step_logging: bool = False,
    planning_interval: int | None = None,
    final_answer_checks: list | None = None,
    prompts_file: str = "prompts.yaml",
    project: str | None = None,
    instructions_extra: str | None = None,
    inject_images: bool = False,
    resume: bool = False,
    experience_file: str | Path | None = None,
) -> CodeAgent:
    """Create a CodeAgent with config from YAML files.

    Args:
        config_dir: Directory containing llm_config.yaml, prompts.yaml, corpus.yaml.
        workspace_dir: Directory for workspace and logs.
        provider_name: LLM provider name. Defaults to config default_provider.
        tools: Custom tools list. Defaults to [wait_for_jobflow] (+ the always-added primitives).
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
    model = LiteLLMModel(
        model_id=provider_cfg["model_id"],
        api_key=api_key,
        **model_kwargs,
    )

    agent_cfg = llm_cfg.get("agent", {})

    # Resolve experience file path (parameter overrides config)
    exp_cfg = experience_file or agent_cfg.get("experience_file")
    experience_path = None
    if exp_cfg:
        p = Path(os.path.expanduser(exp_cfg))
        if p.is_absolute():
            experience_path = p
        else:
            # Relative to config_dir (e.g., "../experience.md" -> workspace/experience.md)
            experience_path = config_dir / p
        if not experience_path.exists():
            logger.warning("experience_file not found: %s", experience_path)
            experience_path = None

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

    # Create executor: the thin ExecPythonExecutor (the P4 opened runtime). It inherits
    # the real builtins (open, __import__, ...) and enforces no import policy and no
    # op-cap -- the P3 container is the execution boundary. No code-execution timeout by
    # default (the broken 30s ThreadPoolExecutor timeout was removed in P2/P-B2); the
    # opt-in `agent.exec_timeout_s` arms a best-effort SIGALRM watchdog. (The vendored AST
    # LocalPythonExecutor is no longer selectable: P4 removed the rollback flag once the
    # opened runtime was validated. The vendored class stays dormant in core/_smol until
    # P6 owns the loop.)
    additional_imports = agent_cfg.get("additional_authorized_imports") or []
    os.chdir(workspace_dir.resolve())
    from core.exec import ExecPythonExecutor

    executor = ExecPythonExecutor(exec_timeout_s=agent_cfg.get("exec_timeout_s"))

    # Tools: use the custom list, or the default agent toolset. (RAG was removed in P5c -- the agent
    # retrieves by grepping the installed package source; see the grep/glob wiring below.)
    if tools is None:
        tools = [wait_for_jobflow]

    # I/O, search, shell, and remote transfer tools are always added.
    # The IO trio (read_file/write_file/edit_file) is workspace-bound; bash is the
    # container-bounded shell escape hatch. grep/glob default to the installed package source
    # (site-packages) -- the agent searches the real library code, scoping by package -- and also
    # reach the reference-doc corpora declared in configs/corpus.yaml (e.g. the VASP wiki, which is
    # not pip-installed). sysconfig resolves site-packages correctly on the host .venv AND in the P3
    # container; corpus is config_dir.parent/corpus on both (host repo, /work in the container).
    import sysconfig

    from core.tools import (
        BashTool,
        EditFileTool,
        FetchHistoryTool,
        GlobTool,
        GrepTool,
        QueryJobstoreTool,
        ReadFileTool,
        ReadPdfTool,
        RemoteGetTool,
        RemoteLsTool,
        RemotePutTool,
        WriteExperienceTool,
        WriteFileTool,
    )
    site_packages = Path(sysconfig.get_paths()["purelib"]).resolve()
    corpus_dir = (config_dir.parent / "corpus").resolve()
    corpora = _load_corpus_registry(config_dir / "corpus.yaml", corpus_dir)
    search_roots = [workspace_dir.resolve(), site_packages, *(c["path"] for c in corpora)]
    tools = list(tools) + [
        WriteFileTool(workspace_dir),
        ReadFileTool(workspace_dir),
        EditFileTool(workspace_dir),
        ReadPdfTool(workspace_dir),
        GrepTool(search_roots, site_packages),
        GlobTool(search_roots, workspace_dir.resolve()),
        BashTool(workspace_dir),
        FetchHistoryTool(workspace_dir),
        RemotePutTool(workspace_dir),
        RemoteGetTool(workspace_dir),
        RemoteLsTool(),
        QueryJobstoreTool(),
    ]

    # Experience tool: only add if experience_file is configured
    if experience_path:
        tools.append(WriteExperienceTool(experience_path))

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

    # Tell the agent where code lives (site-packages) and what reference-doc corpora exist (resolved
    # paths + descriptions from configs/corpus.yaml). Injected via instructions (the codebase's
    # additive-prompt mechanism, like the image-feedback block below) -- this is how the agent learns
    # to grep e.g. the VASP wiki now that RAG is gone.
    corpus_note = _corpus_instructions(site_packages, corpora)
    instructions = (instructions.rstrip() + "\n\n" + corpus_note) if instructions.strip() else corpus_note

    if project:
        worker_info = _resolve_worker_instructions(project, llm_cfg)
        if worker_info:
            instructions = instructions.rstrip() + "\n\n" + worker_info

    if instructions_extra:
        instructions = instructions.rstrip() + "\n" + instructions_extra

    if planning_interval is not None:
        kwargs["planning_interval"] = planning_interval

    if final_answer_checks:
        kwargs["final_answer_checks"] = final_answer_checks

    # Error hint callback runs first to modify errors before logging
    callbacks = [_on_step_error]
    if inject_images:
        callbacks.append(_inject_workspace_images(workspace_dir))
        instructions = instructions.rstrip() + "\n\n" + (
            "IMAGE FEEDBACK: When you save a .png or .jpg file to the workspace "
            "(e.g., via plt.savefig()), the image will be shown to you automatically "
            "at the start of the next step. Only newly created images are shown -- "
            "each image appears once. Use this to verify your figures before finalizing."
        )

    # Store instructions AFTER all modifications (base, worker, extra, image feedback)
    if instructions:
        kwargs["instructions"] = instructions

    # History writer -- always enabled (primary conversation storage)
    history_file = workspace_dir / "history.jsonl"
    callbacks.append(_history_writer(history_file, workspace_dir))

    if enable_step_logging:
        steps_log = _make_steps_log_path(workspace_dir)
        callbacks.append(_step_jsonl_logger(steps_log))
        print(f"[agent] steps_log={steps_log}")

    kwargs["step_callbacks"] = callbacks

    agent = CodeAgent(**kwargs)

    # Dynamic experience injection (must be before resume to include in system prompt)
    if experience_path:
        _setup_experience_reloader(agent, experience_path)

    if resume:
        history_file = workspace_dir / "history.jsonl"
        if history_file.exists():
            _restart_from_history(agent, history_file)
        else:
            logger.warning("resume=True but no history.jsonl found in %s", workspace_dir)

    return agent


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
