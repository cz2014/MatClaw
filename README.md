# MatClaw

A code-first LLM agent for computational materials science workflows. Built on HuggingFace's smolagents, MatClaw executes Python to manipulate crystal structures, submit HPC jobs, curate training data, and iterate on model quality — composing loops, conditionals, and library calls naturally rather than relying on rigid tool chains.

## Install

```bash
pip install -e .
```

## Quick Start

1. Set your LLM API key:

```bash
export OPENAI_API_KEY=...       # for GPT models
# or
export GEMINI_API_KEY=...       # for Gemini models
# or
export CLAUDE_API_KEY=...       # for Claude models
```

2. Configure the default provider in `config/llm_config.yaml` (edit `default_provider`).

3. Run the agent:

```bash
python main.py
```

To run with a custom task, call `main()` programmatically:

```python
from main import main
main(task="Your task description here", workspace_dir=Path("workspace"))
```

## HPC Setup

MatClaw submits computational jobs to remote HPC clusters via [jobflow-remote](https://github.com/Matgenix/jobflow-remote). Each cluster needs:

1. A jobflow-remote project YAML in `~/.jfremote/` (see jobflow-remote docs)
2. SSH key access to the cluster
3. A running jobflow-remote runner daemon: `jf -p <project> runner run`

Multiple clusters can run simultaneously. Pass `project="<name>"` to `main()` to select the target cluster.

## RAG Corpus

Build retrieval indices for documentation-augmented generation:

```bash
# Install Node.js dependency for tree-sitter chunking
cd scripts && npm install && cd ..

# Build default corpus (code-chunk method, 800 tokens, BM25)
python scripts/build_corpus.py
```

RAG is configured via `config/rag_config.yaml`. Set `enabled: true/false` to control whether the `rag_search` tool is available to the agent.

## Benchmarks

```bash
# Code QA (pymatgen/atomate2, 120 or 300 questions)
python benchmark/qa/run_qa.py

# VASP wiki QA (500 questions)
python benchmark/qa_vasp/run_qa.py

# Python library QA (jobflow-remote, 120 questions)
python benchmark/qa_pylib/run_qa.py

# Real-world coding tasks (pymatgen-analysis-defects, 48 tasks)
python benchmark/tasks/run_tasks.py

# VASP INCAR generation (16 tasks)
python benchmark/vasp_incar/run_incar.py
```

## License

MIT
