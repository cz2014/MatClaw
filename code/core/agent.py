"""CodeAgent initialization from YAML config and prompt templates (simplified)."""

from __future__ import annotations

import atexit
import ast
import json
import logging
import os
import re
import sys
import threading
import time
import weakref
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from core._smol import CodeAgent, LiteLLMModel

from core.context import _get_content_str, _get_role
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


def _resolve_web_search(llm_cfg: dict[str, Any], agent_cfg: dict[str, Any]) -> tuple[str, str | None]:
    """Resolve the web_search (model, api_key) from agent.web_search.

    Each of provider/model/api_key is optional and falls back to the matching
    providers.<provider> block, so by default web_search reuses the project's Gemini
    provider (its model_id and api_key template). The key template (e.g. "${GEMINI_API_KEY}")
    is expanded the same way as the agent's own provider key, so the tool receives a resolved
    value -- never a hardcoded env-var name.
    """
    ws_cfg = agent_cfg.get("web_search", {}) or {}
    provider = ws_cfg.get("provider", "gemini")
    prov_cfg = (llm_cfg.get("providers", {}) or {}).get(provider, {}) or {}
    model = ws_cfg.get("model") or prov_cfg.get("model_id") or "gemini/gemini-3.5-flash"
    key_tmpl = ws_cfg.get("api_key") or prov_cfg.get("api_key")
    api_key = _expand_env_strict(key_tmpl) if key_tmpl else None
    return model, api_key


def _filter_disabled_tools(tools: list, disabled: set[str]) -> list:
    """Drop any tool whose ``.name`` is in ``disabled``.

    Fail-fast on disabling the essential ``final_answer`` or naming a tool that is not
    registered (typo protection). Returns the list unchanged when ``disabled`` is empty.
    The disable policy is application-level, so it lives here, not in vendored ``_smol``.
    """
    if not disabled:
        return tools
    if "final_answer" in disabled:
        raise ValueError("Cannot disable the essential 'final_answer' tool.")
    registered = {t.name for t in tools}
    unknown = disabled - registered
    if unknown:
        raise ValueError(
            f"disabled_tools lists unknown tool(s): {sorted(unknown)}. "
            f"Registered tools: {sorted(registered)}."
        )
    return [t for t in tools if t.name not in disabled]


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

    Each message is stored exactly once. ``model_input_messages`` are captured
    at the start of an action, so an ActionStep callback flushes the metadata
    buffered from the preceding action. A FinalAnswerStep callback flushes the
    last buffered action from the agent's complete memory.

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
        "pending": None,
        "last_written": None,
    }

    def _fingerprint(msg) -> tuple[str, int]:
        return (_get_role(msg), hash(_get_content_str(msg)))

    def _is_reset(messages) -> bool:
        """True when ``messages`` starts a new conversation instead of extending the written one.

        A length comparison alone misses the boundary where the new list is exactly as long
        as what was written (e.g. an interrupted run wrote only its bootstrap system+task
        pair), so compare the message sitting at the last written position instead.
        """
        written = _state["written"]
        if written == 0:
            return False
        if len(messages) < written:
            return True
        return _fingerprint(messages[written - 1]) != _state["last_written"]

    def _resume_position(messages) -> None:
        _state["written"] = len(messages)
        _state["last_written"] = _fingerprint(messages[-1]) if messages else None
        _state["skip_first"] = False
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

    def _flush(messages, metadata_step) -> None:
        import dataclasses

        if messages is None:
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

                if metadata_step is None:
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

                    if metadata_step is not None and metadata_step.timing:
                        rec["timing"] = {
                            "start_time": metadata_step.timing.start_time,
                            "end_time": metadata_step.timing.end_time,
                        }
                    if metadata_step is not None and metadata_step.error:
                        rec["error"] = metadata_step.error.dict()
                    if metadata_step is not None and metadata_step.code_action is not None:
                        rec["code_action"] = metadata_step.code_action
                    if metadata_step is not None and metadata_step.is_final_answer:
                        rec["is_final_answer"] = True
                    if metadata_step is not None and metadata_step.token_usage:
                        rec["token_usage"] = dataclasses.asdict(metadata_step.token_usage)

                images_b64 = _extract_images_b64(msg)
                if images_b64:
                    rec["images_b64"] = images_b64

                f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
                written += 1

        _state["written"] = written
        _state["last_written"] = _fingerprint(messages[written - 1]) if written else None
        if metadata_step is not None:
            _state["next_step"] = step_num + 1

    def cb(step, agent):
        from core._smol import ActionStep
        from core._smol.memory import FinalAnswerStep

        if isinstance(step, ActionStep):
            messages = step.model_input_messages
            if messages is None:
                return
            if _state["skip_first"]:
                _resume_position(messages)
            else:
                # MultiStepAgent.run(reset=True) replaces its in-memory history.
                # Reset only the per-memory cursor; global history numbering must
                # continue across runs on the same agent instance.
                if _is_reset(messages):
                    _state["written"] = 0
                    _flush(messages, None)
                _flush(messages, _state["pending"])
            _state["pending"] = step
            return

        if isinstance(step, FinalAnswerStep) and _state["pending"] is not None:
            _flush(agent.write_memory_to_messages(), _state["pending"])
            _state["pending"] = None

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


def _restart_from_history(agent: CodeAgent, history_file: Path) -> None:
    """Reconstruct agent memory from history.jsonl for restart.

    Populates agent.memory.steps with ActionStep objects reconstructed
    from the history file.

    Executor variables are NOT restored (Python state is lost on crash).
    A restart message is injected to inform the agent.
    """
    from core._smol import ActionStep
    from core._smol.memory import Timing, ToolCall

    records: list[dict] = []
    with history_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    if not records:
        return

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
        tool_calls: list[ToolCall] = []
        saw_tool_call = False

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
            elif role == "tool-call":
                saw_tool_call = True
                try:
                    payload_text = content.removeprefix("Calling tools:\n")
                    payload = ast.literal_eval(payload_text)
                    if not isinstance(payload, list):
                        raise ValueError("tool-call payload is not a list")
                    parsed_calls = []
                    for item in payload:
                        if not isinstance(item, dict) or item.get("type") != "function":
                            raise ValueError("tool-call item is not a function mapping")
                        function = item.get("function")
                        if not isinstance(function, dict):
                            raise ValueError("tool-call function is not a mapping")
                        call_id = item.get("id")
                        name = function.get("name")
                        if not isinstance(call_id, str) or not isinstance(name, str):
                            raise ValueError("tool-call id/name is missing")
                        if "arguments" not in function:
                            raise ValueError("tool-call arguments are missing")
                        parsed_calls.append(
                            ToolCall(
                                id=call_id,
                                name=name,
                                arguments=function["arguments"],
                            )
                        )
                    tool_calls.extend(parsed_calls)
                except (SyntaxError, ValueError, TypeError):
                    logger.warning(
                        "Malformed legacy tool-call payload at step %d; using code_action fallback",
                        step_num,
                    )
            elif role in ("tool-response", "tool"):
                observations = content.removeprefix("Observation:\n")
            elif role in ("user", "system"):
                # Histories written before bootstrap moved to step 0 can carry
                # the task as step 1. It is not an ActionStep.
                continue

            if "images_b64" in rec:
                import base64
                import io

                import PIL.Image
                for b64 in rec["images_b64"]:
                    img = PIL.Image.open(io.BytesIO(base64.b64decode(b64)))
                    img.load()
                    images.append(img)

        if model_output is None and code_action is None and observations is None and error is None:
            continue
        if not tool_calls and code_action is not None:
            tool_calls = [
                ToolCall(
                    id=f"call_{step_num}",
                    name="python_interpreter",
                    arguments=code_action,
                )
            ]
            if saw_tool_call:
                logger.info("Synthesized tool call for malformed history step %d", step_num)
        # Error rendering already produces the tool response. Restoring the
        # rendered response as an observation would duplicate and corrupt it.
        if error is not None:
            observations = None

        action_step = ActionStep(
            step_number=step_num,
            timing=timing,
            model_output=model_output,
            tool_calls=tool_calls or None,
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


# An agent's executor owns kernel processes and their child forests. The normal teardown is
# the caller's finally block (see run_agent), but an exit path that skips it would orphan
# them, so every executor is also reachable from an interpreter-exit backstop. The weak set
# keeps long-lived processes from retaining dead agents, and cleanup is idempotent, so the
# backstop is harmless when the finally block already ran.
_ACTIVE_EXECUTORS: weakref.WeakSet = weakref.WeakSet()
_ATEXIT_REGISTERED = False


def _cleanup_active_executors() -> None:
    """Tear down every executor still alive. Safe to call repeatedly."""
    for executor in list(_ACTIVE_EXECUTORS):
        executor.cleanup()


def _register_executor_cleanup(executor) -> None:
    """Track ``executor`` for the exit backstop, registering the atexit hook on first use."""
    global _ATEXIT_REGISTERED
    _ACTIVE_EXECUTORS.add(executor)
    if not _ATEXIT_REGISTERED:
        atexit.register(_cleanup_active_executors)
        _ATEXIT_REGISTERED = True


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
        tools: Extra tools list. Defaults to [wait_for_jobflow] (+ the always-added
            primitives). Only tools from the built-in set are supported: user-defined
            Tool objects cannot cross the kernel boundary and the executor rejects them.
        enable_step_logging: Whether to log steps to JSONL file in workspace.
        planning_interval: Steps between planning updates. None disables planning.
        final_answer_checks: List of check functions passed to CodeAgent.
        prompts_file: Prompts YAML filename in config_dir. Defaults to "prompts.yaml".
        project: HPC project name for auto-resolving worker config. When set,
            worker descriptions and raw jfremote YAML are injected into instructions.
        instructions_extra: Extra instructions appended to config instructions
            (for non-project overrides like task-specific constraints).

    Returns:
        Configured CodeAgent instance. The agent owns live execution resources (one
        ipykernel process per kernel plus the tool server), so the caller must call
        ``agent.cleanup()`` when the run is over -- ``run_agent`` does this in a finally
        block, and an atexit backstop covers a normal interpreter exit, but a caller that
        drives the agent itself is responsible for the teardown.
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

    # Resolve the complete per-kernel tool construction spec before starting
    # execution resources. The harness retains only stateful local process state.
    additional_imports = agent_cfg.get("additional_authorized_imports") or []
    os.chdir(workspace_dir.resolve())
    import sysconfig

    from core.tools import (
        BashTool,
        KillCommandTool,
        ToolSpec,
        WaitCommandTool,
        _LocalExecState,
        build_stateless_tools,
    )
    from core.toolserver import ToolServer

    site_packages = Path(sysconfig.get_paths()["purelib"]).resolve()
    corpus_dir = (config_dir.parent / "corpus").resolve()
    corpora = _load_corpus_registry(config_dir / "corpus.yaml", corpus_dir)
    search_roots = [workspace_dir.resolve(), site_packages, *(c["path"] for c in corpora)]

    # web_search backend: model/key fall back to the matching providers.<provider> entry, so by
    # default search reuses the project's Gemini provider. The key template is resolved here (same
    # ${VAR} expansion as the agent's provider key) -- nothing hardcoded to an env-var name.
    ws_model, ws_api_key = _resolve_web_search(llm_cfg, agent_cfg)

    disabled = set(agent_cfg.get("disabled_tools", []))
    unfiltered_spec = ToolSpec(
        workspace=workspace_dir.resolve(),
        search_roots=tuple(search_roots),
        site_packages=site_packages,
        experience_path=experience_path,
        web_search_model=ws_model,
        web_search_api_key=ws_api_key,
    )
    tool_spec = ToolSpec(
        workspace=unfiltered_spec.workspace,
        search_roots=unfiltered_spec.search_roots,
        site_packages=unfiltered_spec.site_packages,
        experience_path=unfiltered_spec.experience_path,
        web_search_model=unfiltered_spec.web_search_model,
        web_search_api_key=unfiltered_spec.web_search_api_key,
        disabled=tuple(sorted(disabled)),
    )
    local_state = _LocalExecState(workspace_dir)
    stateful_tools = [
        BashTool(workspace_dir, local_state),
        WaitCommandTool(local_state),
        KillCommandTool(local_state),
    ]
    default_tools = build_stateless_tools(unfiltered_spec) + stateful_tools
    tools = _filter_disabled_tools(list(tools or []) + default_tools, disabled)
    if disabled:
        logger.info("Tools disabled by config: %s", sorted(disabled))

    tool_server = ToolServer(local_state)

    # Max steps from config
    max_steps = agent_cfg.get("max_steps", 10)

    kwargs: dict[str, Any] = dict(
        tools=tools,
        model=model,
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

    # History writer -- always enabled (primary conversation storage). Register
    # its final flush for FinalAnswerStep as well as the ordinary action callbacks.
    history_file = workspace_dir / "history.jsonl"
    history_callback = _history_writer(history_file, workspace_dir)

    if enable_step_logging:
        steps_log = _make_steps_log_path(workspace_dir)
        callbacks.append(_step_jsonl_logger(steps_log))
        print(f"[agent] steps_log={steps_log}")

    from core._smol import ActionStep
    from core._smol.memory import FinalAnswerStep

    kwargs["step_callbacks"] = {
        ActionStep: [*callbacks, history_callback],
        FinalAnswerStep: [history_callback],
    }

    executor = None
    kernel_manager = None
    try:
        from core.exec import ExecPythonExecutor
        from core.kernel import KernelManager

        tool_server.start()
        kernel_manager = KernelManager(workspace_dir, tool_spec, tool_server)
        executor = ExecPythonExecutor(kernel_manager, tool_server)
        _register_executor_cleanup(executor)
        kwargs["executor"] = executor
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
    except BaseException:
        if executor is not None:
            executor.cleanup()
        elif kernel_manager is not None:
            try:
                kernel_manager.shutdown()
            finally:
                tool_server.stop()
        else:
            tool_server.stop()
        raise


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
