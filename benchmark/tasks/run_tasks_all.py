"""Unified task benchmark runner for cross-model comparison.

Usage:
    python benchmark/tasks/run_tasks_all.py --model gemini/gemini-2.0-flash --provider gemini
    python benchmark/tasks/run_tasks_all.py --model gpt-5.4 --provider openai
    python benchmark/tasks/run_tasks_all.py --model gpt-4.1 --provider openai --delay 1.0
    python benchmark/tasks/run_tasks_all.py --model gpt-5.4 --provider openai --resume results_gpt-5.4_20260317_120000.jsonl

Outputs results to benchmark/tasks/results_{model}_{timestamp}.jsonl
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from benchmark.tasks.evaluate import evaluate_task
from core.agent import create_agent
from core.telemetry import setup_telemetry
from core.tools import RagSearchTool

TASKS_DIR = Path(__file__).parent
QUESTIONS_DIR = TASKS_DIR / "question_segments"
DATA_DIR = TASKS_DIR / "data"

# Path prefix in question.txt that needs rewriting to absolute data dir
DATA_PATH_PREFIX = "tool_source_code/pymatgen-analysis-defects/tests/test_files/"


def _normalize_key(key):
    """Normalize dict keys: non-string keys (e.g. Element) -> str."""
    if isinstance(key, str):
        return key
    return str(key)


def _normalize_value(val):
    """Recursively normalize numpy scalars to native Python types."""
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


def load_task(task_dir: Path) -> dict:
    """Load task definition from a question_segments subdirectory."""
    task_name = task_dir.name
    question_text = (task_dir / "question.txt").read_text(encoding="utf-8")

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


def format_task_prompt(question: str) -> str:
    """Format question text into agent task prompt."""
    return f"""{question}

Return your result as a Python dictionary via final_answer(result_dict),
where keys are the property names and values are the computed results.
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


def _get_completed_tasks(results_path: Path) -> tuple[list[dict], set[str]]:
    """Load existing results and return (results_list, set of completed task names)."""
    results = []
    completed = set()
    if not results_path.exists():
        return results, completed
    with open(results_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if record.get("type") == "summary":
                continue
            results.append(record)
            completed.add(record["task"])
    return results, completed


def main():
    parser = argparse.ArgumentParser(description="Unified task benchmark runner")
    parser.add_argument("--model", required=True, help="LiteLLM model ID")
    parser.add_argument("--provider", required=True, choices=["gemini", "openai", "deepseek"])
    parser.add_argument("--tasklist", type=str, default="tasks.json")
    parser.add_argument("--task", type=str, default=None, help="Run single task (overrides --tasklist)")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between tasks (default: 0.5)")
    parser.add_argument("--resume", type=str, default=None, help="Resume from existing results file")
    parser.add_argument("--trace", action="store_true", help="Enable Phoenix telemetry")
    args = parser.parse_args()

    if args.trace:
        os.environ["MLFF_ENABLE_TELEMETRY"] = "1"
        if setup_telemetry(project_name="task-benchmark"):
            print("Telemetry enabled - traces at http://localhost:6006")

    config_dir = TASKS_DIR / "config"

    # Load configs
    llm_cfg = yaml.safe_load(open(config_dir / "llm_config.yaml"))
    rag_cfg = yaml.safe_load(open(config_dir / "rag_config.yaml"))

    # Override model and provider
    llm_cfg["default_provider"] = args.provider
    llm_cfg["providers"][args.provider]["model_id"] = args.model

    # Force RAG enabled
    rag_cfg["enabled"] = True

    # Build tools
    tools = [
        RagSearchTool(
            corpus=rag_cfg.get("corpus"),
            top_k=rag_cfg.get("top_k"),
        )
    ]

    # Load task list
    if args.task:
        task_names = [args.task]
    else:
        tasklist_path = TASKS_DIR / args.tasklist
        with open(tasklist_path) as f:
            task_names = json.load(f)
        if args.limit:
            task_names = task_names[:args.limit]

    # Validate and load tasks
    tasks = []
    for name in task_names:
        task_dir = QUESTIONS_DIR / name
        if not (task_dir / "question.txt").exists():
            raise ValueError(f"Task '{name}' not found in {QUESTIONS_DIR}")
        tasks.append(load_task(task_dir))

    # Workspace
    workspace_dir = TASKS_DIR / "workspace"
    workspace_dir.mkdir(exist_ok=True)

    # Create agent with patched config via temp directory (Option C)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_config = Path(tmp)
        for f in config_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, tmp_config / f.name)
        with open(tmp_config / "llm_config.yaml", "w") as fh:
            yaml.dump(llm_cfg, fh, default_flow_style=False)
        with open(tmp_config / "rag_config.yaml", "w") as fh:
            yaml.dump(rag_cfg, fh, default_flow_style=False)

        agent = create_agent(
            config_dir=tmp_config,
            workspace_dir=workspace_dir,
            tools=tools,
            enable_step_logging=True,
            final_answer_checks=[reject_all_none],
        )

    # Output path and resume handling
    model_short = args.model.split("/")[-1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.resume:
        output_path = TASKS_DIR / args.resume
        results, completed_set = _get_completed_tasks(output_path)
        task_correct = sum(1 for r in results if r.get("status") == "ok")
        total_subtasks_correct = sum(r.get("correct_subtasks", 0) for r in results)
        total_subtasks = sum(r.get("total_subtasks", 0) for r in results)
        print(f"Resume: {len(completed_set)} already completed, {task_correct} correct")
        file_mode = "a"
    else:
        output_path = TASKS_DIR / f"results_{model_short}_{timestamp}.jsonl"
        results = []
        task_correct = 0
        total_subtasks_correct = 0
        total_subtasks = 0
        completed_set = set()
        file_mode = "w"

    print(f"Model: {args.model}")
    print(f"Provider: {args.provider}")
    print(f"RAG enabled: True")
    print(f"Tasks: {len(tasks)}")
    print(f"Delay: {args.delay}s")
    print(f"Output: {output_path}")
    print("-" * 40)

    with open(output_path, file_mode) as f:
        for i, task in enumerate(tasks):
            if task["name"] in completed_set:
                continue

            if i > 0:
                time.sleep(args.delay)

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
                "model_id": args.model,
                "provider": args.provider,
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

            f.write(json.dumps(record) + "\n")
            f.flush()

            sub = f"{eval_result['correct_subtasks']}/{eval_result['total_subtasks']} subtasks correct"
            print(f"[{i + 1}/{len(tasks)}] {task['name']}: {eval_result['status']} ({sub})")
            if eval_result["errors"]:
                for err in eval_result["errors"]:
                    print(f"  - {err}")

    # Summary
    n_tasks = len(results)
    task_acc = task_correct / n_tasks if n_tasks else 0
    subtask_acc = total_subtasks_correct / total_subtasks if total_subtasks else 0

    print("-" * 40)
    print(f"Task accuracy: {task_correct}/{n_tasks} ({task_acc:.1%})")
    print(f"Subtask accuracy: {total_subtasks_correct}/{total_subtasks} ({subtask_acc:.1%})")

    total_steps = sum(r["steps"] for r in results if r.get("type") != "summary")
    total_input = sum(r["input_tokens"] for r in results if r.get("type") != "summary")
    total_output = sum(r["output_tokens"] for r in results if r.get("type") != "summary")

    summary = {
        "type": "summary",
        "model_id": args.model,
        "provider": args.provider,
        "rag_enabled": True,
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
