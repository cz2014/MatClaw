"""Generate multiple-choice QA from Python source files using LLM structured output.

Usage:
    python benchmark/qa_pylib/generate_qa.py                      # All files in corpus/
    python benchmark/qa_pylib/generate_qa.py --files jobcontroller.py
    python benchmark/qa_pylib/generate_qa.py --limit 5             # Quick test
    python benchmark/qa_pylib/generate_qa.py --resume
"""

import argparse
import json
import os
import time
from pathlib import Path
from typing import Literal

import litellm
import yaml
from pydantic import BaseModel

QA_DIR = Path(__file__).parent

QUESTIONS_PER_200_LINES = 4
MIN_QUESTIONS = 4
MIN_LINES = 50
MAX_QUESTIONS_PER_FILE = 40
MAX_FILE_LINES = 30_000


class MCQ(BaseModel):
    category: Literal[
        "API_Identification", "Parameter_Knowledge", "Return_Value", "Usage_Pattern"
    ]
    question: str
    choices: list[str]
    correct_answer_index: int
    explanation: str


class QuestionSet(BaseModel):
    questions: list[MCQ]


def _compute_n_questions(n_lines: int) -> int:
    if n_lines < MIN_LINES:
        return 0
    n = (n_lines // 200) * QUESTIONS_PER_200_LINES
    return min(max(n, MIN_QUESTIONS), MAX_QUESTIONS_PER_FILE)


def _load_config() -> dict:
    with open(QA_DIR / "config" / "generation_config.yaml") as f:
        return yaml.safe_load(f)


def _resolve_env(value: str) -> str:
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        return os.environ[value[2:-1]]
    return value


def _get_corpus_files(config: dict, args: argparse.Namespace) -> list[Path]:
    corpus_path = QA_DIR / config["corpus_path"]
    if args.files:
        found = []
        for name in args.files:
            matches = list(corpus_path.rglob(name))
            found.extend(matches)
        return found
    all_files = sorted(corpus_path.rglob("*.py"))
    if args.limit:
        all_files = all_files[: args.limit]
    return all_files


def _get_processed_files(output_path: Path) -> set[str]:
    processed: set[str] = set()
    if not output_path.exists():
        return processed
    with open(output_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            processed.add(record.get("source_file", ""))
    return processed


def generate_questions_for_file(
    file_path: Path,
    corpus_root: Path,
    model: str,
    api_key: str,
    temperature: float,
    system_prompt: str,
    package_name: str,
    n_questions: int,
) -> list[dict]:
    content = file_path.read_text()
    rel_path = file_path.relative_to(corpus_root)

    response = litellm.completion(
        model=model,
        api_key=api_key,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Package: {package_name}\n"
                    f"File: {rel_path}\n"
                    f"Generate exactly {n_questions} multiple-choice questions "
                    f"from this source file.\n\n"
                    f"---\n{content}\n---"
                ),
            },
        ],
        response_format=QuestionSet,
    )

    raw = response.choices[0].message.content
    question_set = QuestionSet.model_validate_json(raw)

    results = []
    for mcq in question_set.questions:
        record = mcq.model_dump()
        record["source_file"] = str(rel_path)
        record["package"] = package_name
        results.append(record)
    return results


def main():
    parser = argparse.ArgumentParser(description="Generate QA from Python source")
    parser.add_argument("--files", nargs="+", help="Specific files to process")
    parser.add_argument("--limit", type=int, help="Limit number of files")
    parser.add_argument("--model", type=str, help="Override model from config")
    parser.add_argument("--resume", action="store_true", help="Skip already-processed")
    parser.add_argument("--delay", type=float, help="Delay between API calls")
    args = parser.parse_args()

    config = _load_config()
    model = args.model or config["model"]
    api_key = _resolve_env(config["api_key"])
    temperature = config.get("temperature", 1.0)
    delay = args.delay if args.delay is not None else config.get("delay_seconds", 1.0)
    system_prompt = config["system_prompt"]
    package_name = config.get("package_name", "unknown")
    corpus_root = QA_DIR / config["corpus_path"]

    files = _get_corpus_files(config, args)
    output_path = QA_DIR / "raw" / "raw_questions.jsonl"
    output_path.parent.mkdir(exist_ok=True)

    processed: set[str] = set()
    if args.resume:
        processed = _get_processed_files(output_path)
        print(f"Resume: {len(processed)} files already processed")

    total_questions = 0
    total_files = 0
    skipped_short = 0
    skipped_long = 0

    with open(output_path, "a") as f:
        for i, file_path in enumerate(files):
            rel = str(file_path.relative_to(corpus_root))
            if rel in processed:
                continue

            content = file_path.read_text()
            n_lines = content.count("\n") + 1

            if n_lines < MIN_LINES:
                skipped_short += 1
                print(
                    f"[{i + 1}/{len(files)}] SKIP {rel}: "
                    f"{n_lines} lines (< {MIN_LINES})"
                )
                continue

            if n_lines > MAX_FILE_LINES:
                skipped_long += 1
                print(
                    f"[{i + 1}/{len(files)}] SKIP {rel}: "
                    f"{n_lines} lines (> {MAX_FILE_LINES})"
                )
                continue

            n_questions = _compute_n_questions(n_lines)

            if total_files > 0 and delay > 0:
                time.sleep(delay)

            try:
                questions = generate_questions_for_file(
                    file_path,
                    corpus_root,
                    model,
                    api_key,
                    temperature,
                    system_prompt,
                    package_name,
                    n_questions,
                )
            except Exception as e:
                print(f"[{i + 1}/{len(files)}] ERROR {rel}: {e}")
                continue

            for q in questions:
                f.write(json.dumps(q) + "\n")
            f.flush()

            total_questions += len(questions)
            total_files += 1
            print(
                f"[{i + 1}/{len(files)}] {rel}: "
                f"{n_lines} lines -> requested {n_questions}, got {len(questions)}"
            )

    print("-" * 40)
    print(f"Files processed: {total_files}")
    print(f"Skipped (too short): {skipped_short}")
    print(f"Skipped (too long): {skipped_long}")
    print(f"Total questions: {total_questions}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
