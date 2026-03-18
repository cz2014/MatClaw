"""VASP INCAR generation benchmark runner.

Evaluates the agent's ability to generate correct VASP INCAR files for
multi-step calculations (adsorption energy, NEB). Tasks come from VaspAgent
(arxiv 2512.19458). Three-layer evaluation: syntax, config constraints,
LLM-as-judge (optional).

Usage:
    python benchmark/vasp_incar/run_incar.py                          # Run all tasks
    python benchmark/vasp_incar/run_incar.py --task absorptionE1_Ir   # Run one task
    python benchmark/vasp_incar/run_incar.py --tasklist tasks.json    # Use task manifest
    python benchmark/vasp_incar/run_incar.py --limit 1                # Run first N tasks
    python benchmark/vasp_incar/run_incar.py --rag                    # With VASP wiki RAG
    python benchmark/vasp_incar/run_incar.py --llm-judge              # With LLM evaluation
    python benchmark/vasp_incar/run_incar.py --trace                  # With telemetry

Outputs results to benchmark/vasp_incar/results_{timestamp}.jsonl
"""

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from benchmark.vasp_incar.evaluate import evaluate_incar_task
from core.agent import create_agent
from core.telemetry import setup_telemetry
from core.tools import RagSearchTool

BENCHMARK_DIR = Path(__file__).parent
QUESTIONS_DIR = BENCHMARK_DIR / "question_segments"
DELAY_SECONDS = 0.5


def reject_all_none(final_answer, memory, **kwargs):
    """Reject final answers where all values are None -- forces agent to retry."""
    if isinstance(final_answer, dict) and len(final_answer) > 0:
        if all(v is None for v in final_answer.values()):
            raise ValueError(
                "All property values are None. This usually means a broad "
                "try/except caught a fixable bug. Remove the try/except, "
                "let the error surface, read the traceback, and fix the code."
            )
    return True


def reject_non_file(final_answer, memory, **kwargs):
    """Reject final answers where values are not existing file paths."""
    if isinstance(final_answer, dict):
        for key, val in final_answer.items():
            if not isinstance(val, str) or not Path(val).exists():
                raise ValueError(
                    f"'{key}' must be a file path from write_text(), "
                    f"got: {val!r}. Write the INCAR file first, then "
                    f"return the path from write_text()."
                )
    return True


def make_self_review(inject_artifacts=True):
    """Force one self-review cycle before accepting final_answer.

    On first submission, rejects with a review prompt. If inject_artifacts is
    True, reads artifact files from disk and includes their contents in the
    error message. On resubmission with the same answer, accepts.
    """
    seen = set()

    def _self_review(final_answer, memory, **kwargs):
        if not isinstance(final_answer, dict):
            return True

        sig = str(sorted(final_answer.items()))
        if sig in seen:
            return True
        seen.add(sig)

        # Optionally read artifact contents to inject into review message
        artifacts = []
        if inject_artifacts:
            for key, path in final_answer.items():
                if isinstance(path, str) and Path(path).exists():
                    content = Path(path).read_text(encoding="utf-8")
                    artifacts.append(f"--- {key} ---\n{content}")

        msg = (
            "Self-review: before submitting, review your "
            + ("output files below" if artifacts else "conversation")
            + " and verify each requirement in the task description is satisfied.\n\n"
            "Review process:\n"
            "1. For each parameter you generated, confirm you are confident "
            "it is correct for this specific task. If unsure about any "
            "parameter, call rag_search to verify before resubmitting.\n"
            "2. Check that no parameters are missing that the task requires.\n"
            "3. If everything checks out, call final_answer again with the EXACT "
            "same dictionary (same keys, same file paths). Do NOT regenerate or "
            "rewrite the files -- just call final_answer(result_dict) unchanged. "
            "If you find issues, fix the files first, then call final_answer."
        )
        if artifacts:
            msg += "\n\n" + "\n\n".join(artifacts)

        raise ValueError(msg)

    return _self_review


def _prepare_workspace(task_name: str, workspace_dir: Path) -> Path:
    """Create per-task workspace and copy POSCAR files from data/.

    Returns the task workspace path.
    """
    task_workspace = workspace_dir / task_name
    if task_workspace.exists():
        shutil.rmtree(task_workspace)
    task_workspace.mkdir(parents=True)

    # Copy all data files into workspace root
    data_dir = QUESTIONS_DIR / task_name / "data"
    if data_dir.exists():
        for f in data_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, task_workspace / f.name)

    return task_workspace


def load_task(task_dir: Path) -> dict:
    """Load task definition from a question_segments subdirectory.

    Reads question.txt and loads properties.json metadata.

    Returns:
        {"name": str, "question": str, "properties": dict, "unit_test_path": Path}
    """
    task_name = task_dir.name
    question_text = (task_dir / "question.txt").read_text(encoding="utf-8")

    properties = json.loads(
        (task_dir / "properties.json").read_text(encoding="utf-8")
    )

    return {
        "name": task_name,
        "question": question_text,
        "properties": properties,
        "unit_test_path": task_dir / "new_unit_test.py",
    }


def discover_tasks(task_filter: str | None = None) -> list[Path]:
    """Find task directories under question_segments/.

    Each valid task directory must contain question.txt and new_unit_test.py.
    """
    if not QUESTIONS_DIR.exists():
        raise FileNotFoundError(f"Questions directory not found: {QUESTIONS_DIR}")

    task_dirs = []
    for d in sorted(QUESTIONS_DIR.iterdir()):
        if not d.is_dir():
            continue
        if not (d / "question.txt").exists():
            continue
        if not (d / "new_unit_test.py").exists():
            continue
        if task_filter and d.name != task_filter:
            continue
        task_dirs.append(d)

    if task_filter and not task_dirs:
        raise ValueError(f"Task '{task_filter}' not found in {QUESTIONS_DIR}")
    return task_dirs


def format_task_prompt(question: str) -> str:
    """Format question text into agent task prompt."""
    return f"""{question}

Return your result as a Python dictionary via final_answer(result_dict),
where keys are the step names and values are the file paths from write_text().
"""


def extract_output_dict(result) -> dict | None:
    """Extract dict from agent result."""
    output = result.output if hasattr(result, "output") else result
    if isinstance(output, dict):
        return output
    if isinstance(output, str):
        try:
            parsed = json.loads(output)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
    return None


def main():
    parser = argparse.ArgumentParser(description="Run VASP INCAR benchmark")
    parser.add_argument(
        "--task", type=str, default=None,
        help="Run specific task (e.g. absorptionE1_Ir), overrides --tasklist",
    )
    parser.add_argument(
        "--tasklist", type=str, default="tasks_mini.json",
        help="Task list JSON file (default: tasks.json)",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Limit number of tasks to run",
    )
    parser.add_argument(
        "--trace", action="store_true",
        help="Enable Phoenix telemetry tracing",
    )
    parser.add_argument(
        "--rag", action="store_true",
        help="Enable VASP wiki RAG (BM25 over qa_vasp corpus)",
    )
    parser.add_argument(
        "--llm-judge", action="store_true",
        help="Enable Layer 3 LLM-as-judge evaluation",
    )
    parser.add_argument(
        "--judge-model", type=str, default=None,
        help="LiteLLM model ID for LLM-as-judge (default: same as agent model)",
    )
    parser.add_argument(
        "--workdir", type=str, default=None,
        help="Working directory for workspace and results (default: benchmark dir). "
             "Use different --workdir values to run multiple instances in parallel.",
    )
    parser.add_argument(
        "--no-artifacts", action="store_true",
        help="Disable artifact injection in self-review (pure conversation review)",
    )
    args = parser.parse_args()

    if args.trace:
        os.environ["MLFF_ENABLE_TELEMETRY"] = "1"
        if setup_telemetry(project_name="incar-benchmark"):
            print("Telemetry enabled - traces at http://localhost:6006")

    # Config directory
    config_dir = BENCHMARK_DIR / "config"

    # Load configs
    llm_cfg = yaml.safe_load(open(config_dir / "llm_config.yaml"))
    rag_cfg = yaml.safe_load(open(config_dir / "rag_config.yaml"))

    # Load task list
    if args.task:
        task_names = [args.task]
    else:
        tasklist_path = BENCHMARK_DIR / args.tasklist
        with open(tasklist_path) as f:
            task_names = json.load(f)
        if args.limit:
            task_names = task_names[: args.limit]

    # Validate and load tasks
    tasks = []
    for name in task_names:
        task_dir = QUESTIONS_DIR / name
        if not (task_dir / "question.txt").exists():
            raise ValueError(f"Task '{name}' not found in {QUESTIONS_DIR}")
        tasks.append(load_task(task_dir))

    # Setup shared tools (RagSearchTool lazy-loads index once, reused across agents)
    rag_enabled = args.rag or rag_cfg.get("enabled", False)
    shared_tools = []
    if rag_enabled:
        shared_tools.append(
            RagSearchTool(
                corpus=rag_cfg.get("corpus"),
                top_k=rag_cfg.get("top_k"),
            )
        )

    # Workspace root and output path
    work_base = Path(args.workdir) if args.workdir else BENCHMARK_DIR
    work_base.mkdir(parents=True, exist_ok=True)
    workspace_root = work_base / "workspace"
    workspace_root.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = work_base / f"results_{timestamp}.jsonl"

    print(f"RAG enabled: {rag_enabled}")
    print(f"LLM judge: {args.llm_judge}")
    print(f"Tasks: {len(tasks)}")
    print(f"Max steps: {llm_cfg.get('agent', {}).get('max_steps', 10)}")
    print(f"Judge model: {args.judge_model or '(default from config)'}")
    print(f"Workdir: {work_base}")
    print(f"Output: {output_path}")
    print("-" * 40)

    results = []
    task_correct = 0
    total_subtasks_correct = 0
    total_subtasks = 0

    with open(output_path, "w") as f:
        for i, task in enumerate(tasks):
            if i > 0:
                time.sleep(DELAY_SECONDS)

            # Per-task workspace: clean slate with POSCAR files copied in
            task_workspace = _prepare_workspace(task["name"], workspace_root)

            # Per-task agent: workspace_dir is baked into sandbox functions
            inject = not args.no_artifacts
            checks = [reject_all_none, reject_non_file, make_self_review(inject_artifacts=inject)]

            agent = create_agent(
                config_dir=config_dir,
                workspace_dir=task_workspace,
                tools=shared_tools,
                enable_step_logging=True,
                final_answer_checks=checks,
            )

            prompt = format_task_prompt(task["question"])
            start_time = time.time()

            try:
                result = agent.run(prompt)
                output = result.output if hasattr(result, "output") else str(result)
                error = None
                steps = len(result.steps) if hasattr(result, "steps") else 0
                token_usage = getattr(result, "token_usage", None)
                input_tokens = token_usage.input_tokens if token_usage else 0
                output_tokens = token_usage.output_tokens if token_usage else 0
            except Exception as e:
                output = None
                error = str(e)
                steps = 0
                input_tokens = 0
                output_tokens = 0

            elapsed = time.time() - start_time

            # Extract dict from agent output
            output_dict = extract_output_dict(
                result if error is None else None
            ) if error is None else None

            # Evaluate with three-layer evaluator
            if output_dict is not None:
                eval_result = _evaluate(
                    output_dict, task, args.judge_model, args.llm_judge
                )
            else:
                n_props = len(task["properties"].get("properties", {}))
                eval_result = {
                    "status": "error",
                    "correct_subtasks": 0,
                    "total_subtasks": n_props,
                    "errors": [
                        error or f"Agent did not return a dict (got: {type(output).__name__})"
                    ],
                }

            # Track totals
            if eval_result["status"] == "ok":
                task_correct += 1
            total_subtasks_correct += eval_result["correct_subtasks"]
            total_subtasks += eval_result["total_subtasks"]

            record = {
                "task": task["name"],
                "status": eval_result["status"],
                "correct_subtasks": eval_result["correct_subtasks"],
                "total_subtasks": eval_result["total_subtasks"],
                "eval_errors": eval_result["errors"],
                "raw_output": str(output) if output is not None else None,
                "agent_error": error,
                "elapsed_seconds": elapsed,
                "steps": steps,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            }
            results.append(record)

            # Write result immediately
            f.write(json.dumps(record) + "\n")
            f.flush()

            # Progress
            sub = f"{eval_result['correct_subtasks']}/{eval_result['total_subtasks']} subtasks correct"
            print(f"[{i + 1}/{len(tasks)}] {task['name']}: {eval_result['status']} ({sub})")
            if eval_result["errors"]:
                for err in eval_result["errors"]:
                    print(f"  - {err}")

    # Summary
    n_tasks = len(tasks)
    task_acc = task_correct / n_tasks if n_tasks else 0
    subtask_acc = total_subtasks_correct / total_subtasks if total_subtasks else 0

    print("-" * 40)
    print(f"Task accuracy: {task_correct}/{n_tasks} ({task_acc:.1%})")
    print(f"Subtask accuracy: {total_subtasks_correct}/{total_subtasks} ({subtask_acc:.1%})")

    # Token/step averages
    total_steps = sum(r["steps"] for r in results)
    total_input = sum(r["input_tokens"] for r in results)
    total_output = sum(r["output_tokens"] for r in results)

    # Append summary as last line of JSONL
    summary = {
        "type": "summary",
        "rag_enabled": rag_enabled,
        "llm_judge": args.llm_judge,
        "judge_model": args.judge_model,
        "total_tasks": n_tasks,
        "tasks_correct": task_correct,
        "task_accuracy": task_acc,
        "total_subtasks": total_subtasks,
        "subtasks_correct": total_subtasks_correct,
        "subtask_accuracy": subtask_acc,
        "avg_steps": round(total_steps / n_tasks, 2) if n_tasks else 0,
        "avg_input_tokens": round(total_input / n_tasks, 1) if n_tasks else 0,
        "avg_output_tokens": round(total_output / n_tasks, 1) if n_tasks else 0,
        "timestamp": timestamp,
    }
    with open(output_path, "a") as f_out:
        f_out.write(json.dumps(summary) + "\n")
    print(f"Results: {output_path}")


def _evaluate(
    output_dict: dict,
    task: dict,
    judge_model: str | None,
    run_llm_judge: bool,
) -> dict:
    """Run evaluation on agent output.

    Delegates to evaluate_incar_task() and converts its return format
    into the standard {status, correct_subtasks, total_subtasks, errors} dict.
    """
    task_name = task["name"]
    result = evaluate_incar_task(
        output_dict,
        task_name,
        task_description=task["question"],
        judge_model=judge_model,
        run_llm_judge=run_llm_judge,
    )

    if result == "ok":
        total = len(task["properties"].get("properties", {}))
        return {
            "status": "ok",
            "correct_subtasks": total,
            "total_subtasks": total,
            "errors": [],
        }

    # Error list format: [msg, msg, ..., n_errors, n_total]
    if isinstance(result, list) and len(result) >= 2:
        n_errors = result[-2]
        n_total = result[-1]
        error_msgs = [str(e) for e in result[:-2]]
        correct = n_total - n_errors
        status = "partial" if correct > 0 else "error"
        return {
            "status": status,
            "correct_subtasks": correct,
            "total_subtasks": n_total,
            "errors": error_msgs,
        }

    return {
        "status": "error",
        "correct_subtasks": 0,
        "total_subtasks": 0,
        "errors": [f"Unexpected eval result format: {result!r}"],
    }


if __name__ == "__main__":
    main()
