# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A code-first agent for ML force-field (MLFF) workflows using HuggingFace's `smolagents` CodeAgent. The agent executes Python to manipulate structures and workflows (data generation -> VASP labeling -> dataset curation -> DeepMD training -> iteration).

**Design philosophy**: Minimal tools, maximal library usage. The agent thinks in Python and composes loops/conditionals naturally rather than relying on many custom tools.

## Commands

```bash
# Install dependencies
pip install -e .
pip install -e ".[rag]"        # RAG dependencies (bm25s, tiktoken, astchunk)
pip install -e ".[pdf]"        # PDF reading (pymupdf)
cd scripts && npm install      # code-chunk Node.js dependency

# Build RAG corpus (default: code-chunk method, 800 tokens, bm25s tokenizer)
python scripts/build_corpus.py
python scripts/build_corpus.py --method cast  # Use astchunk instead

# Run the agent (CLI)
matclaw run --task task.txt --project perlmutter              # from workspace dir
matclaw run --task task.txt --config ./config --project anvil  # explicit config dir
matclaw run --resume                                           # resume crashed run

# Run the agent (legacy, for old test scripts only)
# main.py moved to tests/main.py -- new code should use `matclaw run` or `core.runner.run_agent()`

# Extract QA subsets from MatTools zips
python benchmark/qa/extract_qa.py                # Code QA (qa_120.json, qa_300.json)
python benchmark/qa/extract_qa.py --source doc   # Doc QA (qa_doc_120.json, qa_doc_300.json)

# Run QA benchmark (default: qa_120.json, no --limit = all questions)
python benchmark/qa/run_qa.py
python benchmark/qa/run_qa.py --questions qa_doc_120.json  # Doc QA
python benchmark/qa/run_qa.py --limit 5   # Quick test with first 5 questions
python benchmark/qa/run_qa.py --api-probe  # Enable api_probe introspection tool

# Generate QA questions for Python library benchmark
python benchmark/qa_pylib/generate_qa.py                    # All corpus files
python benchmark/qa_pylib/generate_qa.py --limit 5          # Quick test (5 files)
python benchmark/qa_pylib/curate_qa.py --sizes 120 300      # Curate balanced sets
python benchmark/qa_pylib/run_qa.py                         # Run benchmark (default: qa_120.json)
python benchmark/qa_pylib/run_qa.py --questions qa_300.json  # Run on 300 questions
python benchmark/qa_pylib/run_qa.py --prompts prompts_default.yaml  # No-RAG baseline

# Experience log tests
python tests/test_experience.py                                                # Unit tests (4 tests, no LLM calls)
python tests/test_experience.py --integration                                  # + magic spell lifecycle integration test (requires LLM)

# MongoDB query tool tests
python tests/test_query_jobstore.py                                            # Unit tests (5 tests, no LLM calls)
python tests/test_query_jobstore.py --integration                              # + 2-phase HPC integration test (perlmutter debug queue)
python tests/test_query_jobstore.py --integration --monitor                    # + health-check daemon

# Context management tests
python tests/test_context_pruning.py                                           # Unit tests (15 tests, no LLM calls)
python tests/test_context_pruning.py --continuous --context-window 30000       # + continuous QA integration test

# History writer + fetch_history tests
python tests/test_history_fetch.py                                             # Unit tests (11 tests, no LLM calls)
python tests/test_history_fetch.py --integration                               # + resume + recall-after-pruning integration tests

# Image injection tests
python tests/test_image_inject.py                                              # Unit test: callback mechanics (no LLM)
python tests/test_image_inject.py --live                                       # + LLM vision tests (direct + callback pipeline)
```

## Architecture

```
core/                   # Python package
  cli.py                # CLI entry point: `matclaw run` command (argparse, delegates to runner.py)
  runner.py             # Agent runner: workspace setup, TeeWriter, telemetry, pause/resume, agent.run()
  agent.py              # CodeAgent initialization + sandboxed file I/O + remote transfer (remote_put/get/ls) + RAG nudge callback + context management + history writer (history.jsonl) + resume from history + experience reloader (dynamic injection from experience.md) + pause/resume + auto-pause on connection errors + transient API error retry
  context.py            # Unified zone-based context window management (pruning + caching for hysteresis)
  tools.py              # Tool definitions (wait_for_jobflow, train_deepmd, batch_static_eval, rag_search, api_probe, fetch_history, write_experience, query_jobstore, read_pdf)
  rag.py                # RAG chunking methods (fixed-width, AST, code-chunk, cast)
  retrievers/           # Retriever backends (BM25, Gemini embeddings)
  telemetry/            # OpenTelemetry instrumentation with Phoenix backend
scripts/                # Build and monitoring scripts
  build_corpus.py       # RAG corpus builder (default: code-chunk, 800 tokens)
  chunk_with_context.mjs # Node.js wrapper for code-chunk (tree-sitter)
  monitor.py            # Health-check daemon: agent/runner/MongoDB/SSH checks with macOS notifications (--project for HPC target)
  analyze_steps.py      # Step log analysis: summary, errors, timeline, token usage
config/                 # Configuration files
  llm_config.yaml       # Multi-provider LLM config (openai, gemini, deepseek, local) + agent settings
  experience.md         # Cross-session experience notes (auto-injected into prompts, writable by agent + humans)
  rag_config.yaml       # RAG settings: per-corpus retriever method + description
  prompts.yaml          # smolagents PromptTemplates structure
  prompts_v5.yaml       # Extended prompts with MD->DeePMD workflow example
  prompts_default.yaml  # Baseline prompt templates (no workflow examples)
remote_jobs/            # Jobflow job definitions for remote execution
  jobs.py               # @job decorated functions (train_deepmd, batch_static_eval)
  _deepmd.py            # DeePMD training implementation (multi-source: VASP, ForceField MD, deepmd/npy)
  _batch_eval.py        # Batch static evaluation implementation (inline dicts or remote .traj/.xyz/.extxyz)
workspace/              # Agent runtime outputs (required, gitignored)
data/                   # RAG data (tracked in git, shared across all branches)
  sources/              # Copied Python package source files
  docs/                 # Documentation source files (vasp/, deepmd-kit/, dpgen/)
  corpus/               # Built retriever indices (one subdir per corpus)
benchmark/              # Evaluation benchmarks
  qa/                   # Code QA multiple-choice benchmark
    run_qa.py           # QA runner (default: qa_120.json, --api-probe for introspection tool)
    extract_qa.py       # Question extraction from MatTools zips (--source code|doc)
    qa_120.json         # 120 code QA pairs (seed=42)
    qa_300.json         # 300 code QA pairs (seed=123, no overlap with qa_120)
    qa_doc_120.json     # 120 doc QA pairs (seed=42)
    qa_doc_300.json     # 300 doc QA pairs (seed=123, no overlap with qa_doc_120)
    config/             # QA-specific configs (llm_config.yaml, prompts.yaml, rag_config.yaml, prompts_v4_api.yaml)
    save/               # QA results archive (save_archive_YYYYMMDD.tar.gz with results_*.jsonl)
  vasp_incar/           # VASP INCAR generation benchmark
    run_incar.py        # Runner: per-task workspace, --rag/--llm-judge flags
    evaluate.py         # Three-layer evaluator (syntax, config, LLM judge)
    config/             # Benchmark configs (prompts.yaml, llm_config.yaml, rag_config.yaml)
    question_segments/  # Task dirs (question.txt, properties.json, data/)
    save/               # Experiment results archive (self_review_log.md, model_comparison.md)
  qa_vasp/              # VASP wiki QA benchmark (500 questions)
    run_qa.py           # QA runner
    config/             # Benchmark configs
    save/               # Results archive
  qa_pylib/             # Generalizable Python library QA benchmark (jobflow-remote)
    generate_qa.py      # LLM-based question generation from source code
    curate_qa.py        # Validation + balanced category selection
    run_qa.py           # QA runner (agent loop + evaluation)
    config/             # Benchmark configs (llm_config.yaml, rag_config.yaml, prompts.yaml)
    corpus/             # Python source files for target package
    data/               # Built retriever index (BM25)
    save/               # Results archive
tests/                  # Test scripts and utilities
  main.py               # Legacy entry point for old test scripts (test1-test10). Delegates to core.runner.run_agent(). New code should use `matclaw run` CLI or core.runner directly.
  utils.py              # Test helpers (save_last_step, analyze_agent_errors, parse_step_counts, get_total_token_usage, extract_message, generate_benchmark_summary)
  benchmark.py          # Benchmark runner with token usage and step count tracking
  test_rag.py           # RAG retrieval evaluation (build index, search, measure recall)
  test_anvil_connection.py  # Trivial smoke test (hello_anvil job on Anvil)
  test_jobflow_min.py   # MoS2 relaxation via jobflow-remote on Anvil
  test2_mos2_jobflow.py # Agent-driven MoS2 relaxation (e2e test)
  test_mlff_jobflow.py  # Direct VASP MD -> DeePMD training test
  test_train_chain.py   # Chained ForceFieldMD -> train_deepmd Flow + list-of-sources merge test (perlmutter)
  test3_mlff_jobflow.py # Agent-driven VASP MD -> DeePMD training test (graphene, default: anvil)
  test4_cips.py         # Agent-driven CIPS AIMD -> DeePMD test (default: perlmutter GPU)
  test5_cips_al.py      # Agent-driven CIPS active learning loop (DP-GEN, default: perlmutter GPU, --monitor, --workspace)
  test6_cips_distill.py # Agent-driven CIPS model distillation (teacher->student, no DFT, default: perlmutter GPU, --monitor, --workspace)
  test7_cips_distill.py # Extended CIPS distillation stress test (20 iterations or MAE_f < 0.15, default: perlmutter GPU, --monitor, --workspace)
  test8_cips_curie.py   # Broad research task: CIPS Curie temperature investigation with image feedback (default: perlmutter GPU, --monitor)
  test10_cips_distill_pdf.py # CIPS distillation with paper-derived AL strategy: agent reads He et al. DP-GEN paper via read_pdf, writes experience notes, then executes distillation (default: perlmutter GPU, --monitor)
  test_batch_static_eval.py # batch_static_eval integration test: inline dict + remote path modes (perlmutter, --model-path required)
  test_llm_retry.py    # RetryingLiteLLMModel transient API error retry tests
  test_experience.py   # Experience log unit tests (4) + integration test (magic spell lifecycle, requires LLM)
  test_query_jobstore.py # QueryJobstoreTool unit tests (5) + integration test (2-phase HPC workflow + MongoDB query, perlmutter)
  test_context_pruning.py # Context management unit tests + continuous QA integration test
  test_history_fetch.py # History writer + FetchHistoryTool unit tests + resume/recall integration tests
  test_image_inject.py # Image injection: callback unit test + LLM vision via direct delivery and callback pipeline (--live)
```

## Prompt Architecture (3-tier)

All benchmarks and the main agent use the same 3-tier prompt composition:

| Tier | File | Scope | What goes here |
|------|------|-------|---------------|
| 1 | `config/prompts.yaml` `system_prompt` | Persona + protocol | Jinja2 template: persona, tool injection, examples, execution contract, `custom_instructions` hook |
| 2 | `config/llm_config.yaml` `agent.instructions` | Operational rules | Plain text injected into Tier 1 via `custom_instructions`: file I/O, error handling, domain rules |
| 3 | `question.txt` | Task description | User message to `agent.run()`: problem, data paths, return format |

Composition: `system_prompt = render(prompts.yaml, custom_instructions=instructions)`, then `agent.run(question.txt)`.

Domain expertise (e.g. VASP knowledge) belongs in Tier 3 (question.txt) and optionally RAG, not in Tier 1/2. The same generic materials-science template works across all benchmarks.

## Key Dependencies

- **smolagents[litellm]**: HuggingFace agent framework with multi-provider LLM support
- **pymatgen**: Structure manipulation (supercells, defects, substitutions, symmetry)
- **jobflow / jobflow-remote**: Workflow orchestration and remote job submission
- **atomate2**: VASP job makers (MDMaker, RelaxMaker, etc.)
- **dpdata**: Training data conversion (VASP OUTCAR, ForceField MD output, deepmd/npy)
- **deepmd-kit**: ML force field training (dp train/freeze/test)
- **bm25s**: BM25 retrieval for RAG
- **astchunk**: AST-based code chunking with context headers (cast method)
- **tiktoken**: Token counting for chunk sizing
- **pyyaml**: Config file loading
- **code-chunk** (npm): Tree-sitter based chunking with scope context

## HPC Infrastructure

Architecture A: MongoDB + runner + agent run locally on Mac; jobs submitted to remote HPC via SSH with SLURM batch scheduling. Both clusters share the same local MongoDB instance with separate databases.

### Anvil (CPU)

See `how_I_connect_now.md` for full setup instructions.
Config: `~/.jfremote/anvil.yaml`

### Perlmutter (GPU)

See `how_I_connect_now2.md` for full setup instructions.
Config: `~/.jfremote/perlmutter.yaml` (debug queue backup: `~/.jfremote/backups/perlmutter_debug.yaml`)

### Multi-project usage

```bash
# Start runners (separate terminals or daemons)
jf -p anvil runner start
jf -p perlmutter runner start

# Monitor jobs
jf -p anvil job list
jf -p perlmutter job list

# Run pipeline tests (--project flag selects cluster)
python tests/test_anvil_connection.py              # Smoke test (hello_anvil)
python tests/test2_mos2_jobflow.py                 # MoS2 relaxation (default: anvil)
python tests/test2_mos2_jobflow.py --project perlmutter
python tests/test3_mlff_jobflow.py --project perlmutter --monitor  # AIMD + DeePMD on GPU
python tests/test4_cips.py --project perlmutter --monitor          # CIPS AIMD + DeePMD on GPU
python tests/test5_cips_al.py --project perlmutter --monitor       # CIPS active learning (DP-GEN)
python tests/test5_cips_al.py --monitor --workspace workspace_run1 # Parallel run with custom workspace
python tests/test6_cips_distill.py --project perlmutter --monitor  # CIPS distillation (no DFT)
python tests/test7_cips_distill.py --project perlmutter --monitor  # CIPS distillation stress test (20 iter)
python tests/test8_cips_curie.py --project perlmutter              # CIPS Curie temperature (broad research task, image feedback)
python tests/test10_cips_distill_pdf.py --project perlmutter --monitor  # CIPS distillation with paper-derived AL strategy
```

## LLM Providers

Configured in `config/llm_config.yaml`. Set API keys via environment variables:
- `OPENAI_API_KEY` for OpenAI
- `GEMINI_API_KEY` for Gemini
- `DEEPSEEK_API_KEY` for DeepSeek
- Local (Ollama) uses `api_key: ollama` in config

**LiteLLM model naming convention**: Model IDs must include provider prefix for correct routing:
- `gemini/gemini-3-flash-preview` → Google AI Studio (API key auth)
- `gemini-3-flash-preview` (no prefix) → Vertex AI (requires `google-auth` package)
- `deepseek/deepseek-chat` → DeepSeek API
- `gpt-4o` → OpenAI (no prefix needed)

Current default: `gemini/gemini-3-flash-preview` (newest Gemini model via Google AI Studio)

## Logging

- Conversation history: `workspace/history.jsonl` via `_history_writer` callback (primary storage, always enabled). Each message stored once with globally unique step numbers. Used by `FetchHistoryTool` to recover pruned context and by `resume=True` to reconstruct agent state after crash.
- Agent steps: `workspace/steps.jsonl` via `step_callbacks` (optional, `enable_step_logging=True`)
- Stdout capture: `workspace/output.log` (TeeWriter)
- Config snapshot: `workspace/.llm_config.yaml`, `.prompts.yaml`, `.rag_config.yaml` (copied at agent creation for reproducibility)
- Telemetry: Set `MLFF_ENABLE_TELEMETRY=1` for Phoenix tracing at http://localhost:6006

## Per-Workspace Configuration

Each workspace is self-contained with its own `config/` directory. The `matclaw run` CLI reads config from `<workspace>/config/` by default (override with `--config`).

**Workspace layout:**
```
~/Work/matclaw_runs/my_task/
  task.txt                      # task description
  input_structure.cif           # input files
  config/                       # per-task configuration
    llm_config.yaml             # LLM provider, agent settings, experience file path
    prompts.yaml                # prompt templates
    rag_config.yaml             # RAG retriever settings
  # --- agent produces these at runtime ---
  history.jsonl
  steps.jsonl
  output.log
```

**Config resolution:**
- `llm_config.yaml` and `prompts.yaml`: resolved from `config_dir` parameter in `create_agent()`
- `rag_config.yaml`: resolved from `config_dir` via `RagSearchTool(rag_config_path=config_dir / "rag_config.yaml")`
- `experience_file`: relative paths in `llm_config.yaml` resolve against `config_dir`; absolute paths (including `~/...`) used as-is
- RAG corpus data (`data/`): tracked in git, shared across all branches. Rebuild with `scripts/build_corpus.py`

Old test scripts (test1-test10) use `tests/main.py` which explicitly passes `config_dir=PROJECT_ROOT / "config"` to read from the repo's config directory.

## Sandboxed File I/O

The agent has sandboxed file functions injected into its executor (configured in `llm_config.yaml`):
- `write_text(path, content) -> str`: Write file under workspace, returns absolute path
- `read_text(path) -> str`: Read file from workspace
- `remote_put(local_rel_path, remote_dir, project_name, worker_name) -> str`: Upload file/directory to remote HPC via SSH
- `remote_get(remote_path, local_rel_path, project_name, worker_name) -> str`: Download file/directory from remote HPC
- `remote_ls(remote_path, project_name, worker_name) -> list[str]`: List remote directory contents

`write_text`/`read_text` enforce workspace boundaries (no escaping via `../`). The remote transfer functions use jobflow-remote's SSH infrastructure (`ConfigManager` + Fabric/Paramiko). Directory transfers use tar for atomicity. The agent is instructed to use these instead of `open()`.

## Context Window Management

Unified zone-based context management, implemented in `core/context.py` and integrated via `create_agent()` in `core/agent.py`. Wraps `model.generate()` to prune/cap messages before each LLM call.

**Why**: smolagents has zero context management -- it sends all history to the LLM. On overflow, the agent crashes with `AgentGenerationError`. Neither litellm nor LLM server APIs truncate automatically.

### Zone-based pruning

Single mechanism that fires when total tokens exceed `context_window` (1.0x trigger). Four zones measured from END (newest to oldest) of non-bootstrap messages:

| Zone | Position (from end) | Treatment |
|------|---------------------|-----------|
| Zone 1 (protected) | Newest 30% | No modification |
| Zone 2 (soft-trim) | Next 20% | Tool-responses trimmed to head(1500) + `...[trimmed]...` + tail(1500) |
| Zone 3 (hard-clear) | Next 25% | Tool-responses replaced with `[Old tool result content cleared]` |
| Zone 4 (truncate) | Oldest 25% | All messages removed, single `[Context truncated: ...]` marker |

- **Bootstrap protected**: system + first user message always preserved regardless of zone
- **Progressive fallback**: if zone-based pruning is insufficient, truncation zone expands until context fits
- **No modification before trigger**: preserves LLM provider cache hits (Gemini 90% discount, OpenAI 50-90%)

### Pruned-result caching (hysteresis)

The wrapper caches the pruned result. Subsequent calls build from `cached + new_messages` instead of the full original list. Since pruning creates ~40% headroom, the combined total stays under the window for ~8 turns without re-pruning. This ensures stable prefixes for cache hits between triggers.

### Configuration

```yaml
# config/llm_config.yaml
providers:
  gemini:
    context_window: 100000     # Gemini: steep decay above 128K (MRCR v2)
  openai:
    context_window: 200000     # GPT-5.2: near-perfect at 256K (MRCR v2)

agent:
  context_pruning: true         # enable zone-based context management (default: true)
```

Context window resolution:
1. `provider.context_window` from config -- per-provider cap (priority)
2. `agent.context_window` from config -- global fallback cap
3. `litellm.get_model_info(model_id)["max_input_tokens"]` -- auto-detected
4. 128,000 -- hardcoded fallback for unknown models

### Conversation History and Resume

`workspace/history.jsonl` stores every message with globally unique step numbers (independent of smolagents' per-run reset). The `_history_writer` callback maintains its own counter:
- Fresh start: steps 1, 2, 3, ...
- Resume (`create_agent(resume=True)`): reads `max(step)` from existing file, continues from `max + 1`

**`FetchHistoryTool`**: Registered on every agent. Lets the agent recover pruned context:
1. `mode="index"` — step summaries (table of contents)
2. `mode="detail"` — full messages for specific steps

**Resume from crash** (`create_agent(resume=True)`): Reconstructs `agent.memory.steps` from `history.jsonl`. Executor variables are lost (Python state). A restart notice is appended to the last step's observations (not a separate step). The agent is instructed to use `fetch_history` and `read_text` to recover state.

**Step numbering**: smolagents resets `step_number` to 1 on every `run()` call (both `reset=True` and `reset=False`). The `_history_writer` ignores `step.step_number` and uses its own global counter to ensure unique step numbers in `history.jsonl`.

## Experience Log

Cross-session persistent memory for operational lessons. Stored in `config/experience.md`, auto-injected into every prompt via dynamic reloading.

### How it works

`_setup_experience_reloader()` in `core/agent.py` installs three mechanisms:

1. **Initial load**: reads `experience.md` and appends to `agent.instructions` at agent creation
2. **Step callback**: checks file mtime before each step; reloads if changed (human edits mid-run)
3. **Run wrapper**: checks file mtime before each `run()` call (human edits between runs)

The experience text is appended to the base instructions (Tier 2), so it flows through the normal `system_prompt` rendering pipeline. Context pruning's bootstrap protection ensures it's never pruned.

### Writing notes

- **Humans**: edit `config/experience.md` directly (detected on next step/run via mtime)
- **Agent**: `write_experience` tool appends numbered notes (`## N. Summary`)

### Configuration

```yaml
# config/llm_config.yaml
agent:
  experience_file: config/experience.md   # relative to PROJECT_ROOT, or absolute path
```

Path resolution: relative paths resolved against `PROJECT_ROOT`. The `experience_file` parameter in `create_agent()` overrides the config value.

### Token guard

If the experience file exceeds ~10K tokens (estimated as `len(text) // 4`), a warning is logged suggesting pruning or implementing `experience_search`. The content is still injected -- the guard is advisory only.

## Development Phases

**v0**: No RAG. Only `FinalAnswerTool`. Core loop + optional telemetry.
**v1**: RAG via `rag_search` tool (BM25 over pymatgen/atomate2/jobflow source code). RAG nudge callback encourages agent to search docs on API errors.

Currently on v1 with RAG and experience log enabled.

## Git Workflow

### Branch Layout

```
dev ── active development (all source, tests, dev docs, benchmark results)
 ├── main ── clean latest on GitHub (no tests, no demos, no personal info, orphan)
 ├── report ── paper writing (LaTeX, demo workspaces, figures)
 └── prod ── local worktree for stable production installs
release ── FROZEN (paper release with demos, not updated)
```

- **dev** (`~/Work/MLFF_agent/`): The central branch. All development happens here.
- **main** (GitHub, orphan): Clean latest runnable version. Updated from dev via selective checkout. No tests, no demos, no personal info.
- **report**: Paper writing on top of dev. Has LaTeX source, demo scripts, demo workspaces for paper.
- **prod** (`~/Work/MatClaw_prod/`, git worktree): Mirrors dev for stable production installs. Shares `.git` so commits are visible across worktrees.
- **release** (GitHub, orphan, FROZEN): Paper release with demo scripts and workspace outputs. No longer updated. README on main points here for examples.

### File Classification by Purpose

Every file belongs to a category. When a new file appears, match its purpose to decide which branches it belongs on.

| Category | Description | dev | main | report | release |
|----------|-------------|-----|------|--------|---------|
| Core source code | Agent source, configs, job definitions, scripts, pyproject.toml, .gitignore | YES | YES | YES | YES |
| Reference data | Crystal structures, reference papers for agent input (.ref/) | YES | YES | YES | YES |
| Project documentation | CLAUDE.md, README, benchmark methodology docs (porting_notes.md, model_comparison.md) | YES | YES | YES | YES |
| RAG corpus data | Source files, documentation, built BM25 indices (data/) | YES | YES | YES | YES |
| Benchmark infrastructure | QA JSONs, task segments, evaluation scripts, per-benchmark configs | YES | YES | YES | YES |
| Benchmark raw results | Per-run .jsonl output files, .tar.gz result archives | YES | NO | YES | NO |
| Benchmark runner/plot scripts | Cross-benchmark runners, plotting scripts, shell launchers | YES | NO | YES | NO |
| Full test suite | Unit tests, integration tests, test utilities, legacy entry point | YES | NO | YES | NO |
| Demo scripts | Curated run scripts for paper demonstrations (simplified from test suite) | NO | NO | YES | YES |
| Demo workspaces | Complete agent run outputs for paper reproducibility (workspace_demo*/) | NO | NO | YES | YES |
| Paper source | LaTeX files, bibliography, style files, figures, headers | NO | NO | YES | NO |
| Paper PDF | Compiled paper (paper/paper.pdf only) | NO | NO | YES | YES |
| Paper planning docs | Outlines, reviews, reference notes for writing the paper | NO | NO | YES | NO |
| Arxiv submission | Arxiv tarball and related submission artifacts | NO | NO | YES | NO |
| Dev planning notes | Implementation plans, targets, to-do lists, known issues | YES | NO | NO | NO |
| Personal HPC credentials | SSH paths, usernames, VASP binary locations, MongoDB configs, cluster setup guides | YES | NO | NO | NO |
| Release process docs | How-to-release instructions | YES | NO | NO | NO |
| Claude Code local config | .claude/ directory (skills, settings) | YES | NO | NO | NO |

**Decision rule for new files**: Ask "what is this file's purpose?" and match it to a category above. If it doesn't fit, the default is: dev=YES, main=only if useful to an external user with no personal/internal information, report=only if paper-relevant.

### Merge Rules

| From | To | Method | When |
|------|----|--------|------|
| dev | main | Selective `git checkout dev -- <dirs>` + unstage excluded + commit | When updating GitHub with latest code |
| dev | prod | `git merge dev` + `pip install -e .` | After code changes, before production runs |
| dev | report | `git merge dev` (resolve conflicts) | When report needs new code/features |

Release is frozen -- no more updates.

### Dev → Main Push

```bash
git checkout main
git checkout dev -- core/ config/ scripts/ remote_jobs/ .ref/ pyproject.toml .gitignore CLAUDE.md README.md
git checkout dev -- benchmark/
# Unstage excluded benchmark files (raw results, archives, runner/plot scripts, figures)
git reset HEAD -- $(git diff --cached --name-only | grep -E '\.(jsonl|tar\.gz)$')
git reset HEAD -- $(git diff --cached --name-only | grep -E 'benchmark/(plot_|run_|figures/)')
git commit --author="cz2014 <zcmben2014@gmail.com>" -m "Update: <description>"
git push origin main
git checkout dev
```

### Dev → Prod Sync

```bash
cd ~/Work/MatClaw_prod && git merge dev
pip install -e .   # needed because matclaw CLI resolves to prod's editable install
```

### Dev → Report Merge

```bash
git checkout report
git merge dev
# Resolve conflicts if any (report has paper/, demo workspaces that dev doesn't)
git checkout dev
```

### Main/Release Commit Rules

- **Author/committer**: only `cz2014 <zcmben2014@gmail.com>` -- no Co-Authored-By trailers
- **Orphan branches**: main and release have no parent relationship to dev/report. `git log --all` from these branches shows only their own commits.
- **No personal information**: HPC credentials, usernames, SSH key paths must never appear on main or release
- **Full release execution details**: `dev_notes/how_to_release.md`

## Known Issues

See `to_be_fixed.md` for all known issues: Gemini thought-loops (#1), smolagents `**` unpacking bug (#2), context compaction for 100+ step runs (#3), inject remote cluster info via config YAML (#4), telemetry orphaned spans (#5), `prompts_default.yaml` falls through to framework default (#6).

## QA Benchmark

Multiple-choice QA evaluation under `benchmark/qa/`. Tests agent ability to answer questions about pymatgen source code and documentation.

### QA Results (gemini/gemini-3-flash-preview, qa_doc_120.json)

Three configurations tested on doc QA (120 questions):

| Config | Accuracy | Avg Steps | Avg Input Tok | Avg Output Tok | Timestamp |
|--------|----------|-----------|---------------|----------------|-----------|
| pure LLM | 109/120 (90.8%) | 2.0 | 331 | 9 | 20260129_021433 |
| code RAG | 116/120 (96.7%) | 3.19 | 8,633 | 887 | 20260129_023252 |
| api_probe | 87/120 (72.5%) | 5.41 | 6,167 | 1,073 | 20260201_023918 |

- **code RAG** is the clear winner at 96.7%, +5.9pp over pure LLM.
- **api_probe hurts doc QA**: 72.5% is 18.3pp below pure LLM. The tool only returns signatures/docstrings/`dir()` listings, which can't answer questions about internal implementation details (code patterns, private functions, specific logic). The agent wastes steps probing APIs and hits max steps.
- Gemini NoneType issue: nearly every api_probe run wastes Step 1 on an empty response ("expected string or bytes-like object, got 'NoneType'").

Full results in `save/save_archive_20260201.tar.gz`.

## QA VASP Benchmark

VASP-specific QA evaluation under `benchmark/qa_vasp/`. Tests retrieval quality on 500 VASP-related questions using different retriever configurations.

### QA VASP Results (gemini/gemini-3-flash-preview, 500 questions)

Two retriever configurations tested with 3-query RRF fusion:

| Retriever | Accuracy | Avg Steps | Avg Input Tok | Avg Output Tok |
|-----------|----------|-----------|---------------|----------------|
| BM25 (3-query RRF) | 498/500 (99.6%) | 3.18 | 5,975 | 415 |
| Gemini RQ (3-query RRF) | 495/500 (99.0%) | 3.18 | 5,747 | 418 |

- **BM25 wins** by 0.6pp (3 additional correct answers).
- Both achieve >99% accuracy, demonstrating RAG effectiveness on domain-specific QA.
- 3-query RRF fusion significantly improves retrieval over single-query.

Full results in `save/save_archive_20260208.tar.gz`.

## QA Python Library Benchmark

Generalizable Python library QA benchmark under `benchmark/qa_pylib/`. Tests LLM ability to answer multiple-choice questions about Python library APIs, with and without RAG. Currently targets jobflow-remote; designed to work for any Python package by swapping corpus and config.

**Pipeline**: `generate_qa.py` (LLM generates MCQ from source files) -> `curate_qa.py` (validate + balanced selection) -> `run_qa.py` (agent evaluation).

**4 universal categories** (25% each): API_Identification, Parameter_Knowledge, Return_Value, Usage_Pattern.

**RAG control**: Set `rag_config.yaml` `enabled: true/false` to control whether `rag_search` tool is injected. Use `prompts.yaml` when RAG enabled, `prompts_default.yaml` when disabled. Mismatching causes Gemini empty responses.

### QA PyLib Results (qa_120.json, jobflow-remote)

| Model | Config | Accuracy | Avg Steps | Avg Input Tok | Avg Output Tok |
|-------|--------|----------|-----------|---------------|----------------|
| Gemini Flash | No RAG | 85/120 (70.8%) | 1.98 | 284 | 9 |
| Gemini Flash | RAG (BM25) | 106/113 (93.8%) | 3.27 | 8,819 | 440 |
| GPT-5.2 | No RAG | 82/120 (68.3%) | 2.00 | 278 | 14 |
| GPT-5.2 | RAG (BM25) | 115/120 (95.8%) | 2.97 | 6,491 | 1,294 |

- RAG improves accuracy by +23-28pp across models.
- GPT-5.2 + RAG is the best config (95.8%, zero API errors).
- API_Identification benefits most from RAG (+47-58pp).

Full results in `save/save_archive_20260228.tar.gz`.

## Task Benchmark

Real-world task evaluation under `benchmark/tasks/`. 48 tasks from pymatgen-analysis-defects, copied from MatTools (`question_segments/`). Each task directory contains `question.txt`, `properties.json`, `new_unit_test.py`, and `reference.py`.

- `reference.py`: Self-contained reference solution extracted from the original pymatgen-analysis-defects test suite. Contains inlined fixture setup code and the exact test body. Generated by `extract_reference.py`.
- `reference_tests/`: Archival copy of the 11 source test files (conftest.py + 10 test files) from pymatgen-analysis-defects.
- `save/`: Benchmark results archive. Contains `save_archive_YYYYMMDD.tar.gz` files with `results_*.jsonl` and `error_analysis_*.md` from completed benchmark runs.

```bash
python benchmark/tasks/run_tasks.py                          # Run all tasks (from tasks.json)
python benchmark/tasks/run_tasks.py --task test_adsorbate    # Run one task
python benchmark/tasks/run_tasks.py --tasklist tasks_1.json  # Run a batch split
python benchmark/tasks/run_tasks.py --limit 5                # Run first 5 tasks
python benchmark/tasks/run_tasks.py --api-probe              # Enable api_probe tool
python benchmark/tasks/run_tasks.py --trace                  # With telemetry

# Extract/regenerate reference.py for all 48 tasks
python benchmark/tasks/extract_reference.py
python benchmark/tasks/extract_reference.py --task test_vacancy  # Single task
python benchmark/tasks/extract_reference.py --dry-run            # Preview only
```

**Task lists**: `tasks.json` contains all 48 tasks. `tasks_1.json` through `tasks_5.json` are batch splits (10/10/10/9/9 tasks) for parallel execution. Launch all 5 with staggered delays to avoid API rate limits.

**Excluded tasks**: `test_interstitial` is excluded from all task lists due to a pymatgen version mismatch (nitrogen oxidation states changed between versions, causing expected values to differ).

### Benchmark Results (gemini/gemini-3-flash-preview, 48 tasks)

Three configurations tested on 2026-02-01:

| Config | Task Acc | Subtask Acc | Avg Input Tokens | Avg Output Tokens | Avg Steps |
|--------|----------|-------------|------------------|-------------------|-----------|
| api_probe | 38/48 (79.2%) | 115/127 (90.6%) | 20,066 | 2,040 | 4.6 |
| rag_search | 38/48 (79.2%) | 114/127 (89.8%) | 28,558 | 1,823 | 3.9 |
| no tools | 29/48 (60.4%) | 100/125 (80.0%) | 18,797 | 2,551 | 3.7 |

- **api_probe** and **rag_search** tie at 79.2% task accuracy, both far ahead of no-tools (60.4%).
- They solve different tasks: RAG uniquely solves `test_closest_sc_mat`; api_probe uniquely holds `test_formation_energy_diagram_numerical` and `test_SRHCapture`.
- RAG uses more input tokens (+52% vs no-tools from context injection) but fewer output tokens (-29%) and fewer steps than api_probe.
- 5 persistent failures across all configs need question.txt or test fixes, not tool changes: `test_competing_phases`, `test_dielectric_func`, `test_HarmonicDefect`, `test_lower_envelope`, `test_supercells`.

Full results and error analysis in `save/save_archive_20260201.tar.gz`.

**Runner-level output normalization**: `run_tasks.py` applies `normalize_output()` to agent dicts before evaluation. This converts numpy scalars (`np.bool_` → `bool`, `np.integer` → `int`, `np.floating` → `float`) and non-string dict keys (`Element('Ga')` → `"Ga"`) to JSON-safe types. A `reject_all_none` final-answer check forces the agent to retry when all property values are `None` (usually caused by a broad `try/except` masking a fixable bug). The check is passed to `create_agent()` via the `final_answer_checks` parameter.

**Adding a "Return format" section to question.txt**: The original MatTools `question.txt` files don't constrain how the agent produces return values, so the agent tends to hand-format strings instead of using object attributes. To fix this, append a "Return format" section that shows exact code for constructing the target object and calling `final_answer` with a dict built from its attributes. Pattern:

```
- Return format: Construct the <Object> and call final_answer with a dictionary using its attributes:
    ```python
    obj = <ClassName>(args...)
    final_answer({"property_a": obj.name, "property_b": str(obj)})
    ```
```

Derive the dict values from `properties.json` expected values: if the expected value comes from an object attribute (e.g. `.name`), use `obj.name`; if it comes from the string representation, use `str(obj)`. This tells the agent which API to call rather than guessing the output format.

**Modifying `new_unit_test.py` for JSON-safe comparison**: The agent's `final_answer(dict)` serializes through JSON, so non-serializable Python types in expected values cause comparison failures. Fix the test's comparison logic for these cases:

1. **Element dict keys** (`test_vacancy`, `test_substitution`, `test_complex`, `test_parsing_and_grouping_NamedDefects`): Expected values use `{Element('Ga'): -1}` but the agent returns `{"Ga": -1}`. Add normalization before comparison:
    ```python
    elif expected_format == "dict" and all(isinstance(k, Element) for k in expected_value):
        normalized_expected = {str(k): v for k, v in expected_value.items()}
        normalized_actual = {str(k): v for k, v in actual_value.items()}
        if normalized_actual != normalized_expected:
            errors.append(...)
    ```

2. **Set values** (`test_substitution_generators`, `test_get_localized_states`, `test_fed_plot`): Expected `"format": "set"` but agent returns a list. Accept lists and convert:
    ```python
    elif expected_format == "set":
        actual_as_set = set(actual_value) if isinstance(actual_value, (list, set)) else actual_value
        if not isinstance(actual_as_set, set):
            errors.append(f"{property_name} is not of type set (got {type(actual_value).__name__})")
            continue
        if actual_as_set != expected_value:
            errors.append(...)
    ```

3. **Tuple values** (`test_supercells`): Expected `"format": "tuple"` but agent returns a list. Accept lists:
    ```python
    elif expected_format == "tuple":
        actual_as_tuple = tuple(actual_value) if isinstance(actual_value, (list, tuple)) else actual_value
        if actual_as_tuple != expected_value:
            errors.append(...)
    ```

4. **List of tuples** (`test_lower_envelope`, `test_HarmonicDefect`): Inner tuples serialize as lists. Convert inner elements:
    ```python
    elif expected_format in ("list", "list of tuples"):
        if isinstance(actual_value, list) and expected_value and isinstance(expected_value[0], tuple):
            actual_value = [tuple(x) if isinstance(x, list) else x for x in actual_value]
        if actual_value != expected_value:
            errors.append(...)
    ```

5. **Dict with set values and key normalization** (`test_competing_phases`): Dict values are sets that serialize as lists, and dict keys may differ in separator/ordering (e.g. `"Ga:-1.75 Mg:-1.50"` vs `"Mg:-1.50,Ga:-1.75"`). Normalize both keys and values:
    ```python
    def _normalize_chempot_key(key):
        parts = re.split(r'[,\s]+', key.strip())
        return ','.join(sorted(p for p in parts if ':' in p))

    normalized_expected = {_normalize_chempot_key(k): set(v) if isinstance(v, set) else v for k, v in expected_value.items()}
    normalized_actual = {_normalize_chempot_key(k): set(v) if isinstance(v, (list, set)) else v for k, v in actual_value.items()}
    ```

## VASP INCAR Benchmark

VASP INCAR generation benchmark under `benchmark/vasp_incar/`. Evaluates the agent's ability to generate correct VASP INCAR files for multi-step calculations. Tasks from VaspAgent (arxiv 2512.19458). Three-layer evaluation: syntax (pymatgen), config constraints (properties.json), LLM-as-judge (optional).

```bash
# Run all tasks (default: no RAG, no LLM judge)
python benchmark/vasp_incar/run_incar.py

# Run specific task
python benchmark/vasp_incar/run_incar.py --task absorptionE1_Ir

# With VASP wiki RAG (BM25 over qa_vasp corpus)
python benchmark/vasp_incar/run_incar.py --rag

# With LLM-as-judge evaluation (Layer 3)
python benchmark/vasp_incar/run_incar.py --llm-judge

# With telemetry
python benchmark/vasp_incar/run_incar.py --trace
```

**Per-task workspace**: Each task gets a fresh workspace at `benchmark/vasp_incar/workspace/{task_name}/` with POSCAR files copied from `data/`. Agent writes INCAR files to disk via `write_text()` and returns file paths. A `reject_non_file` final-answer check forces retry if the agent returns raw strings instead of paths.

**16 tasks**: 10 absorption energy (CO adsorption on metal/oxide surfaces, 3 INCAR steps each) and 6 NEB transition state (ethylene hydrogenation, 3 INCAR steps each). Ported from VaspAgent (arxiv 2512.19458).

**Porting from VaspAgent_with_Benchmark**: See `benchmark/vasp_incar/porting_notes.md` for tips on adapting tasks and constraints (e.g., don't require tags with acceptable VASP defaults, use `in_set` over `exact` when multiple algorithms are valid).

**Experiment results**: Archived in `benchmark/vasp_incar/save/`. Contains `self_review_log.md` (per-run self-review experiment data) and `model_comparison.md` (cross-model analysis: GPT-5.2, Claude Opus/Sonnet, Gemini Pro/Flash on NEB1_AgPd and absorptionE1_Ir).

## Coding Principles

1. **Minimal moving parts**: Start with smallest agent that runs real tasks
2. **Code-first, tool-light**: Prefer calling mature libraries (pymatgen/jobflow) over custom tools
3. **Fail loudly, self-correct**: Runtime exceptions are data; prompt forces read error -> hypothesize -> patch -> rerun
4. **Determinism**: Push fragile choices into deterministic code (validation, schema checks)
5. **No global side effects**: Avoid `sys.stdout` mutation and global state changes in library code
6. **Pure library code**: Move I/O side effects (logging, file writes) to runner scripts
7. **Prefer stdlib**: Use `os.path.expandvars` over custom regex, etc.
8. **Don't blank defaults**: Never use `or ""` patterns that can overwrite framework defaults - pass `None` instead. Exception: smolagents PromptTemplates requires `""` (not `None`) for unused fields, matching its own `EMPTY_PROMPT_TEMPLATES`
9. **Load config once**: Read config files once in entry function, not repeatedly
10. **Minimize public API**: Mark internal helpers with `_` prefix; expose only what's needed
11. **Separate concerns**: Agent creation vs logging vs running are distinct responsibilities
12. **Reuse before abstraction**: When adding new functionality (e.g., tests), first parameterize existing code rather than creating new wrapper modules. Extract shared code only when there are 3+ callers with identical logic.
