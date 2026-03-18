"""Evaluation helpers for task benchmark.

Dynamically loads unit test functions from task directories
and runs them against agent output dicts.
"""

import importlib.util
from pathlib import Path


def load_test_function(unit_test_path: Path, task_name: str) -> callable:
    """Dynamically import test function from new_unit_test.py.

    Args:
        unit_test_path: Path to new_unit_test.py file.
        task_name: Task name (e.g. "test_adsorbate"), used as function name.

    Returns:
        The test function callable.
    """
    spec = importlib.util.spec_from_file_location(
        f"unit_test_{task_name}", unit_test_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    fn = getattr(module, task_name, None)
    if fn is None:
        raise ValueError(
            f"No function '{task_name}' in {unit_test_path}"
        )
    return fn


def evaluate_task(output_dict: dict, unit_test_path: Path, task_name: str) -> dict:
    """Run unit test on agent output dict.

    Args:
        output_dict: Dict of property names to values from agent.
        unit_test_path: Path to new_unit_test.py file.
        task_name: Task name (e.g. "test_adsorbate").

    Returns:
        {"status": "ok"|"partial"|"error"|"function_error",
         "correct_subtasks": int,
         "total_subtasks": int,
         "errors": list[str]}
    """
    try:
        test_fn = load_test_function(unit_test_path, task_name)
    except Exception as e:
        return {
            "status": "function_error",
            "correct_subtasks": 0,
            "total_subtasks": 0,
            "errors": [f"Failed to load test function: {e}"],
        }

    try:
        result = test_fn(output_dict)
    except Exception as e:
        return {
            "status": "function_error",
            "correct_subtasks": 0,
            "total_subtasks": 0,
            "errors": [f"Test function raised: {e}"],
        }

    if result == "ok":
        # Count total subtasks from properties.json (load alongside)
        # For "ok", all subtasks passed. Infer total from output_dict keys.
        total = len(output_dict)
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

    # Unexpected format
    return {
        "status": "error",
        "correct_subtasks": 0,
        "total_subtasks": 0,
        "errors": [f"Unexpected test result format: {result!r}"],
    }
