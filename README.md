# MatClaw

An autonomous, code-first LLM agent for end-to-end materials computations. MatClaw writes and runs Python to drive real domain libraries (pymatgen, ASE, atomate2, jobflow) and submit jobs to remote HPC clusters. No predefined tool functions.

## Demo

MoS2 lattice relaxation on Perlmutter — from natural language task to VASP results in a single command:

<p align="center">
  <video src="https://github.com/user-attachments/assets/d81f1400-e43c-4f2a-9a52-62bd1a1ad66e" controls width="700"></video>
</p>

## How It Works

<p align="center">
  <img src="matclaw.jpg" alt="MatClaw architecture" width="800">
</p>

You describe a task in natural language. The agent writes and runs Python to build structures, submit HPC jobs (e.g. VASP), and analyze results. It reads its own output and errors, self-corrects, and iterates until the task is done.

**Key design choices.** Coding agents live in a repository. MatClaw lives in a long-running Python session wired to a supercomputer — closer to a scientist at a notebook than a bot in a shell.

- **Exploration runs against live state.** Each step executes in a named persistent IPython kernel, so the namespace — a loaded ML potential, an in-memory trajectory, a half-built DataFrame, a handle to a remote job — is working memory that carries across steps. And the agent maintains multiple kernels: an interpreter blocks while it evaluates, so a long computation ties up only one while exploration continues in the others — and its result arrives as a live object, not a log file to reparse.
- **Its tools are whatever it writes.** The action space is the interpreter itself — Python against pymatgen, ASE, and atomate2, with loops, branches, and functions defined on the spot — not a fixed menu of schema-defined tools.
- **The cluster is part of the agent.** It authors input decks, submits SLURM jobs through jobflow-remote, and supervises hours-long DFT/MD runs from a laptop-weight process.

## What's New

- **2026-08-18 — Multi-kernel persistent REPL.** Code steps run in named persistent kernels with check-in timeouts, process vitals, and a supervised interrupt/restart kill ladder.
- **2026-06-20 — Generic external-code primitive.** `run_command` runs any simulation code (ABACUS, LAMMPS, ...) on HPC from hand-written input decks, no per-code integration required.
- **2026-06-01 — ripgrep replaces the RAG index.** The agent greps installed package sources and registered doc corpora directly, with no retrieval index to build or maintain.
- **2026-05-31 — Whole-process container runtime.** A locked-down Docker container wraps the entire agent process and serves as the real safety boundary for unrestricted code execution.
- **2026-05-31 — Coding-CLI file and shell tools.** Read/write/edit, glob, ripgrep search, and a background-capable shell, following the tool designs proven in Claude's and OpenAI's coding agents.
- **2026-05-31 — Self-contained core.** The agent loop is a vendored, heavily customized copy of [smolagents](https://github.com/huggingface/smolagents), with no external agent-framework dependency.

## Install

The Python package lives under `code/`. Reproducible environment from the committed lockfile (Python 3.12 + exact pinned deps):

```bash
uv sync --project code
```

Or with pip:

```bash
pip install -e code
```

## Quick Start

Run these from the repo directory (where you installed).

1. Activate the environment so the `matclaw` CLI is on your PATH:

```bash
source code/.venv/bin/activate
```

(Or skip activation and prefix each command with `uv run --project code`.)

2. Set your LLM API key and pick a provider:

```bash
export CLAUDE_API_KEY=...        # or OPENAI_API_KEY / GEMINI_API_KEY
```

Edit `configs/llm_config.yaml` to set `default_provider`.

3. Create a run workspace with a task (plus any input files the task references):

```bash
mkdir -p ~/runs/my_task
echo "Build a conventional FCC aluminium cell (a = 4.05 A), run a quick relaxation on the remote cluster, and report the final total energy." > ~/runs/my_task/task.txt
```

4. Run the agent — `--workspace` holds the task and outputs; `--config` points at this repo's `configs/` (so its sibling `corpus/` resolves too):

```bash
matclaw run --workspace ~/runs/my_task --config configs --project perlmutter
```

Resume a crashed run:

```bash
matclaw run --workspace ~/runs/my_task --config configs --resume
```

## HPC Setup

MatClaw submits computational jobs to remote HPC clusters via [jobflow-remote](https://github.com/Matgenix/jobflow-remote). Each cluster needs:

1. A jobflow-remote project YAML in `~/.jfremote/` (see jobflow-remote docs)
2. SSH key access to the cluster
3. A running jobflow-remote runner daemon: `jf -p <project> runner run`

Multiple clusters can run simultaneously. Select the target cluster with `--project <name>` on `matclaw run`.

On the container host (Linux or macOS), `docker/host_up.sh` brings up and verifies these singletons in one idempotent step: it starts MongoDB so the container can reach it via `host.docker.internal`, proves the connection, ensures the jobflow-remote runner is up, and checks the HPC workers and stores with `jf project check`. Run it before launching `docker/run.sh`. Both scripts read host-specific settings (mongod/jf paths, image, project, resource caps) from an optional launcher config at `~/.config/matclaw/launcher.env` (copy `docker/launcher.env.example`); environment variables override it, so the repo carries no host paths.

## Reference Documentation

There is no index to build. The agent finds API usage by grepping the installed package
source directly (resolved under `site-packages`), so it always reads the code that is actually
installed. Non-code references (e.g. the VASP wiki under `corpus/docs/`) are registered in
`configs/corpus.yaml` with a path and a one-line description, and the agent greps those too.

To add a reference corpus, drop the docs under `corpus/<name>/` and add an entry to
`configs/corpus.yaml`:

```yaml
corpus:
  newpackage:
    path: docs/newpackage
    description: "One-line description of what this corpus contains."
```

## Citation

Zhang, C., & Yakobson, B. I. (2026). *MatClaw: An Autonomous Code-First LLM Agent for End-to-End Materials Exploration.* arXiv:2604.02688. https://arxiv.org/abs/2604.02688

```bibtex
@misc{zhang2026matclaw,
  title         = {MatClaw: An Autonomous Code-First {LLM} Agent for End-to-End Materials Exploration},
  author        = {Zhang, Chenmu and Yakobson, Boris I.},
  year          = {2026},
  eprint        = {2604.02688},
  archivePrefix = {arXiv},
  primaryClass  = {cond-mat.mtrl-sci},
  doi           = {10.48550/arXiv.2604.02688},
  url           = {https://arxiv.org/abs/2604.02688}
}
```

## License

MIT
