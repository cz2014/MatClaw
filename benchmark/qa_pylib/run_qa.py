"""QA benchmark runner - reuses core.create_agent.

Usage:
    python benchmark/qa_pylib/run_qa.py                           # Run all questions
    python benchmark/qa_pylib/run_qa.py --questions qa_120.json   # Use specific questions file
    python benchmark/qa_pylib/run_qa.py --limit 5                 # Run first 5 questions (test)
    python benchmark/qa_pylib/run_qa.py --resume results_xxx.jsonl  # Resume interrupted run
    python benchmark/qa_pylib/run_qa.py --trace                   # Enable telemetry tracing

Outputs results to benchmark/qa_pylib/results_{timestamp}.jsonl
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.agent import create_agent
from core.telemetry import setup_telemetry
from core.tools import RagSearchTool

QA_DIR = Path(__file__).parent
DELAY_SECONDS = 0.5  # Rate limiting between requests


def format_qa_task(question: dict) -> str:
    """Format question dict into task string for agent."""
    choices_str = "\n".join(
        f"{k}. {v}" for k, v in sorted(question["choices"].items())
    )
    return f"""{question['question']}

{choices_str}
"""


def extract_answer(output: str) -> str | None:
    """Extract single letter answer from agent output."""
    if output is None:
        return None
    output = str(output).strip().upper()
    # Try to find a single letter A-D
    match = re.search(r"\b([A-D])\b", output)
    if match:
        return match.group(1)
    # If output is just a letter
    if output in ["A", "B", "C", "D"]:
        return output
    return None


def _get_answered_questions(results_path: Path) -> tuple[list[dict], set[str]]:
    """Load existing results and return (results_list, set of answered source_files)."""
    results = []
    answered = set()
    if not results_path.exists():
        return results, answered
    with open(results_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            # Skip summary line
            if record.get("type") == "summary":
                continue
            results.append(record)
            answered.add(record.get("source_file", ""))
    return results, answered


def main():
    parser = argparse.ArgumentParser(description="Run QA benchmark")
    parser.add_argument("--questions", type=str, default="qa_120.json", help="Questions file (default: qa_120.json)")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of questions")
    parser.add_argument("--resume", type=str, default=None, help="Resume from existing results file (e.g. results_xxx.jsonl)")
    parser.add_argument("--trace", action="store_true", help="Enable Phoenix telemetry tracing")
    parser.add_argument("--prompts", type=str, default="prompts.yaml", help="Prompts file (default: prompts.yaml, use prompts_single.yaml for baseline)")
    parser.add_argument("--retriever", type=str, choices=["bm25", "gemini"], help="Override retriever method from rag_config.yaml")
    args = parser.parse_args()

    if args.trace:
        os.environ["MLFF_ENABLE_TELEMETRY"] = "1"
        if setup_telemetry(project_name="qa-benchmark"):
            print("Telemetry enabled - traces at http://localhost:6006")

    # Config directory with all 3 config files
    config_dir = QA_DIR / "config"

    # Load configs
    llm_cfg = yaml.safe_load(open(config_dir / "llm_config.yaml"))
    rag_cfg = yaml.safe_load(open(config_dir / "rag_config.yaml"))
    max_steps = llm_cfg.get("agent", {}).get("max_steps", 3)

    # Load questions
    questions_file = args.questions
    with open(QA_DIR / questions_file) as f:
        questions = json.load(f)

    if args.limit:
        questions = questions[: args.limit]

    # Setup tools from config
    retriever_method = args.retriever  # None means use central config default
    tools = []
    if rag_cfg.get("enabled", True):
        tools.append(
            RagSearchTool(
                corpus=rag_cfg.get("corpus"),
                top_k=rag_cfg.get("top_k"),
                retriever_method=retriever_method,
            )
        )

    # Create workspace directory
    workspace_dir = QA_DIR / "workspace"
    workspace_dir.mkdir(exist_ok=True)

    # Create agent with QA-specific settings
    agent = create_agent(
        config_dir=config_dir,
        workspace_dir=workspace_dir,
        tools=tools,
        enable_step_logging=True,
        prompts_file=args.prompts,
    )

    # Output path and resume handling
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.resume:
        output_path = QA_DIR / args.resume
        results, answered_set = _get_answered_questions(output_path)
        correct_count = sum(1 for r in results if r.get("is_correct"))
        print(f"Resume: {len(answered_set)} questions already answered, {correct_count} correct")
        file_mode = "a"
    else:
        output_path = QA_DIR / f"results_{timestamp}.jsonl"
        results = []
        correct_count = 0
        answered_set = set()
        file_mode = "w"

    print(f"RAG enabled: {rag_cfg.get('enabled', True)}")
    print(f"Retriever: {retriever_method or '(from central config)'}")
    print(f"Questions: {len(questions)}")
    print(f"Max steps: {max_steps}")
    print(f"Output: {output_path}")
    print("-" * 40)

    with open(output_path, file_mode) as f:
        for i, question in enumerate(questions):
            # Skip already-answered questions (resume mode)
            if question["source_file"] in answered_set:
                continue

            if i > 0:
                time.sleep(DELAY_SECONDS)

            task = format_qa_task(question)
            start_time = time.time()

            try:
                result = agent.run(task)
                # Extract output from AgentResult
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
            predicted = extract_answer(output)
            correct = question["correct_answer"]
            is_correct = predicted == correct

            record = {
                "source_file": question["source_file"],
                "correct_answer": correct,
                "predicted_answer": predicted,
                "is_correct": is_correct,
                "raw_output": output,
                "error": error,
                "elapsed_seconds": elapsed,
                "steps": steps,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            }
            results.append(record)

            if is_correct:
                correct_count += 1

            # Write result immediately
            f.write(json.dumps(record) + "\n")
            f.flush()

            # Progress
            status = (
                "CORRECT"
                if is_correct
                else f"WRONG (expected {correct}, got {predicted})"
            )
            print(f"[{i + 1}/{len(questions)}] {status}")

    # Separate API errors (e.g. Gemini 500) from real attempts
    api_errors = [r for r in results if r["error"] and "InternalServerError" in r["error"]]
    answered = [r for r in results if r not in api_errors]
    n_answered = len(answered)

    # Summary
    accuracy = correct_count / n_answered if n_answered else 0
    print("-" * 40)
    if api_errors:
        print(f"API errors (excluded): {len(api_errors)}/{len(results)}")
    print(f"Accuracy: {correct_count}/{n_answered} ({accuracy:.1%})")

    # Compute averages for summary (excluding API errors)
    total_steps = sum(r["steps"] for r in answered)
    total_input = sum(r["input_tokens"] for r in answered)
    total_output = sum(r["output_tokens"] for r in answered)

    # Append summary as last line of JSONL
    summary = {
        "type": "summary",
        "rag_enabled": rag_cfg.get("enabled", True),
        "retriever": retriever_method,
        "questions_file": questions_file,
        "total_questions": len(results),
        "api_errors": len(api_errors),
        "answered": n_answered,
        "correct": correct_count,
        "accuracy": accuracy,
        "avg_steps": round(total_steps / n_answered, 2) if n_answered else 0,
        "avg_input_tokens": round(total_input / n_answered, 1) if n_answered else 0,
        "avg_output_tokens": round(total_output / n_answered, 1) if n_answered else 0,
        "timestamp": timestamp,
    }
    with open(output_path, "a") as f:
        f.write(json.dumps(summary) + "\n")
    print(f"Results: {output_path}")


if __name__ == "__main__":
    main()
