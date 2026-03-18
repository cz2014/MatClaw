"""Real-world task benchmark runner - reuses core.create_agent.

Tasks are multi-step coding problems where the agent writes Python to compute
material properties, returning a dict via final_answer(). Results are evaluated
against unit tests from MatTools.

Usage:
    python benchmark/tasks/run_tasks.py                          # Run all tasks
    python benchmark/tasks/run_tasks.py --task test_adsorbate    # Run one task
    python benchmark/tasks/run_tasks.py --tasklist tasks.json    # Use task manifest
    python benchmark/tasks/run_tasks.py --limit 5                # Run first 5 tasks
    python benchmark/tasks/run_tasks.py --trace                  # With telemetry

Outputs results to benchmark/tasks/results_{timestamp}.jsonl
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from benchmark.tasks.evaluate import evaluate_task
from core.agent import create_agent
from core.telemetry import setup_telemetry
from core.tools import RagSearchTool

TASKS_DIR = Path(__file__).parent
QUESTIONS_DIR = TASKS_DIR / "question_segments"
DATA_DIR = TASKS_DIR / "data"
DELAY_SECONDS = 0.5  # Rate limiting between requests


def _normalize_key(key):
    """Normalize dict keys: non-string keys (e.g. Element) -> str."""
    if isinstance(key, str):
        return key
    return str(key)


def _normalize_value(val):
    """Recursively normalize numpy scalars to native Python types.

    - np.bool_ -> bool  (MUST check before np.integer: np.bool_ is a subclass)
    - np.integer -> int
    - np.floating -> float
    - np.ndarray -> unchanged (needed for np.allclose checks)
    - dict -> recurse values, normalize keys
    - list -> recurse items
    """
    import numpy as np

    if isinstance(val, np.bool_):
        return bool(val)
    if isinstance(val, np.integer):
        return int(val)
    if isinstance(val, np.floating):
        return float(val)
    if isinstance(val, np.ndarray):
        return val
    if isinstance(val, dict):
        return {_normalize_key(k): _normalize_value(v) for k, v in val.items()}
    if isinstance(val, list):
        return [_normalize_value(item) for item in val]
    return val


def normalize_output(output_dict):
    """Normalize agent output types for evaluation."""
    return {k: _normalize_value(v) for k, v in output_dict.items()}


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

# Path prefix in question.txt that needs rewriting to absolute data dir
DATA_PATH_PREFIX = "tool_source_code/pymatgen-analysis-defects/tests/test_files/"


def load_task(task_dir: Path) -> dict:
    """Load task definition from a question_segments subdirectory.

    Reads question.txt, rewrites data file paths to absolute paths,
    and loads properties.json metadata.

    Returns:
        {"name": str, "question": str, "properties": dict, "unit_test_path": Path}
    """
    task_name = task_dir.name
    question_text = (task_dir / "question.txt").read_text(encoding="utf-8")

    # Rewrite data file paths to absolute paths
    abs_data_dir = str(DATA_DIR.resolve()) + "/"
    question_text = question_text.replace(DATA_PATH_PREFIX, abs_data_dir)

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

    Args:
        task_filter: If set, only return the task with this name.

    Returns:
        Sorted list of task directory paths.
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
        raise ValueError(
            f"Task '{task_filter}' not found in {QUESTIONS_DIR}"
        )
    return task_dirs


def format_task_prompt(question: str) -> str:
    """Format question text into agent task prompt.

    Wraps the question with instructions to return a dict via final_answer().
    """
    return f"""{question}

Return your result as a Python dictionary via final_answer(result_dict),
where keys are the property names and values are the computed results.
"""


def extract_output_dict(result) -> dict | None:
    """Extract dict from agent result.

    The agent should call final_answer(dict). Extract the dict from
    the AgentResult object.
    """
    output = result.output if hasattr(result, "output") else result
    if isinstance(output, dict):
        return output
    if isinstance(output, str):
        # Try parsing as JSON in case agent returned a string representation
        try:
            parsed = json.loads(output)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
    return None


def main():
    parser = argparse.ArgumentParser(description="Run task benchmark")
    parser.add_argument(
        "--task", type=str, default=None,
        help="Run specific task (e.g. test_adsorbate), overrides --tasklist",
    )
    parser.add_argument(
        "--tasklist", type=str, default="tasks.json",
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
    args = parser.parse_args()

    if args.trace:
        os.environ["MLFF_ENABLE_TELEMETRY"] = "1"
        if setup_telemetry(project_name="task-benchmark"):
            print("Telemetry enabled - traces at http://localhost:6006")

    # Config directory
    config_dir = TASKS_DIR / "config"

    # Load configs
    llm_cfg = yaml.safe_load(open(config_dir / "llm_config.yaml"))
    rag_cfg = yaml.safe_load(open(config_dir / "rag_config.yaml"))
    max_steps = llm_cfg.get("agent", {}).get("max_steps", 10)

    # Load task list
    if args.task:
        task_names = [args.task]
    else:
        tasklist_path = TASKS_DIR / args.tasklist
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

    # Setup tools from config
    tools = []
    if rag_cfg.get("enabled", False):
        tools.append(
            RagSearchTool(
                corpus=rag_cfg.get("corpus"),
                top_k=rag_cfg.get("top_k"),
            )
        )

    # Create workspace directory
    workspace_dir = TASKS_DIR / "workspace"
    workspace_dir.mkdir(exist_ok=True)

    # Create agent
    agent = create_agent(
        config_dir=config_dir,
        workspace_dir=workspace_dir,
        tools=tools,
        enable_step_logging=True,
        final_answer_checks=[reject_all_none],
    )

    # Output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = TASKS_DIR / f"results_{timestamp}.jsonl"

    print(f"RAG enabled: {rag_cfg.get('enabled', False)}")
    print(f"Tasks: {len(tasks)}")
    print(f"Max steps: {max_steps}")
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

            # Normalize numpy scalars and non-string keys before evaluation
            if output_dict is not None:
                output_dict = normalize_output(output_dict)

            # Evaluate against unit test
            if output_dict is not None:
                eval_result = evaluate_task(
                    output_dict, task["unit_test_path"], task["name"]
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
        "rag_enabled": rag_cfg.get("enabled", False),
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


if __name__ == "__main__":
    main()
