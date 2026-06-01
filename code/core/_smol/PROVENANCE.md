# PROVENANCE -- core/_smol

Vendored from **smolagents 1.24.0** (PyPI, published 2026-01-16), Apache-2.0 (see `LICENSE`).
Copied verbatim from the installed package, then pruned and edited in place. This directory is
**owned, first-party code** now -- edit it directly; do not re-pull from PyPI.

- Upstream: https://github.com/huggingface/smolagents (v1.24.0)
- Decision: `docs/exec-plans/completed/.../2026-05-31_framework_migration.md` §2 (KEEP code-first,
  DECOUPLE the dependency) and the execution plan `2026-05-31_p2_vendor_smolagents.{md,html}`.

## Why vendored

MatClaw is a code-action agent; the smolagents `CodeAgent` loop + `LocalPythonExecutor` +
`LiteLLMModel` are the paradigm-bearing core. Vendoring lets us own and debug that core, fold our
monkeypatches into direct edits, and drop the `==1.24.0` pin.

## Local changes vs upstream 1.24.0

Recorded as each phase lands (V1 mechanical vendor + prune; V2-V4 fold patches + clean compat):

### V1 -- mechanical vendor + prune (behavior-identical)
- `__init__.py` replaced with a curated public surface (only the subset MatClaw imports).
- Dropped modules (not copied / deleted): `remote_executors.py`, `gradio_ui.py`,
  `vision_web_browser.py`, `mcp_client.py`, `cli.py`, `pyodide_deno_executor.bak.py`, `tmp.py`.
- `agents.py`: removed the `remote_executors` import + the non-`local` branch of
  `create_python_executor`; removed `ToolCallingAgent`.
- `models.py`: removed all non-LiteLLM providers (kept base `Model`, `LiteLLMModel`,
  `ChatMessage`/`MessageRole`, `CODEAGENT_RESPONSE_FORMAT`).
- `default_tools.py`: trimmed to `FinalAnswerTool`; `TOOL_MAPPING = {}`.
- `models.py`: removed the 8 non-LiteLLM providers (2085 -> 878 LOC); kept `Model`/`ApiModel`/`LiteLLMModel`.
- `agents.py`: removed `remote_executors` import + non-local branch of `create_python_executor`,
  removed `ToolCallingAgent`; repointed prompt-resource + dynamic-import paths to `core._smol.*`.
- Converted the absolute `from smolagents.X` imports inside kept modules
  (`memory`/`monitoring`/`utils`/`tools`/`agents`) to relative, so the copy is self-contained.
- **DEFERRED:** `tools.py` Hub/Space/Gradio helpers (`save`/`push_to_hub`/`from_hub`/`from_space`/
  `from_gradio`/`from_langchain` + module-level `launch_gradio_demo`/`load_tool`/`ToolCollection`)
  and the matching `agents.py` `save`/`from_dict`/`from_hub` serialization machinery were NOT removed:
  they are dead but cross-coupled (`agents.save`->`Tool.save`, `agents.from_dict`->`Tool.from_code`),
  so safe removal needs coordinated surgery with no behavioral benefit. `huggingface-hub` stays a
  dep (consistent with the plan's "trim later" note).

### V2 -- folded workarounds (direct edits in the owned source)
- **P-B1** `models.py`: `CODEAGENT_RESPONSE_FORMAT` literal is the phase/plan/code/summary schema
  (was a runtime dict mutation in core/agent.py).
- **P-B2** `local_python_executor.py`: removed the broken `ThreadPoolExecutor` `timeout` decorator,
  `ExecutionTimeoutError`, and the `timeout_seconds` plumbing (no code-exec timeout; Docker is the
  boundary).
- **L6** `local_python_executor.py`: `evaluate_with()` calls `__exit__` on the context manager, not
  the value returned by `__enter__` (smolagents 1.25.0 #2029/#2033).
- **P-B4** `agents.py`: `MultiStepAgent.__init__` deep-merges missing prompt-template keys from
  `EMPTY_PROMPT_TEMPLATES` (tolerates partial dicts) instead of asserting all keys present.
- **P-B3** `memory.py`: `ActionStep` error message wrapped with `truncate_content` at the source.

### V3 -- dissolve RetryingLiteLLMModel into LiteLLMModel
- `models.py` `LiteLLMModel`: folded in `_inject_cache_control` (Anthropic, gated), empty-content
  retry (`_generate_with_empty_retry`), the transient/connection retry + auto-pause loop
  (`generate` wraps `_generate_once`), and the `context_manager` / `set_pause_controller` hooks.
  The product-side `RetryingLiteLLMModel` subclass + the `model.generate=`/`agent.run=` instance
  reassignments are gone (zero monkeypatches in `core/`). `MultiStepAgent.run()` invokes
  `_on_run_start` hooks.
- `generate`: `tool_choice="auto"` for anthropic + thinking + response_format (Anthropic forbids
  thinking with a forced tool_choice; the model still emits the structured schema).

### V4 -- steps.jsonl kept (opt-in writer); all consumers read history.jsonl
No `_smol` change. (`scripts`/`tests`/skills updated outside `_smol`.)

**Deferred (separate pass):** C2 (history-writer off-by-one fix) + C3 (`AgentMemory.load_history`).
