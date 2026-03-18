"""Generate multiple-choice QA from VASP wiki .md pages using LLM structured output.

Usage:
    python benchmark/qa_vasp/generate_qa.py                    # Process all 846 pages
    python benchmark/qa_vasp/generate_qa.py --files ALGO.md    # Process specific pages
    python benchmark/qa_vasp/generate_qa.py --limit 10         # First 10 pages
    python benchmark/qa_vasp/generate_qa.py --resume           # Skip already-processed pages
    python benchmark/qa_vasp/generate_qa.py --model gemini/gemini-3-flash-preview

Outputs raw questions to benchmark/qa_vasp/raw/raw_questions.jsonl
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

QA_VASP_DIR = Path(__file__).parent


class MCQ(BaseModel):
    category: Literal[
        "Tag_Identification", "Tag_Dependency", "Error_Restart", "Physics_Recipe"
    ]
    question: str
    choices: list[str]  # exactly 4 options
    correct_answer_index: int  # 0-3
    explanation: str


class QuestionSet(BaseModel):
    questions: list[MCQ]  # empty list if page is non-informative


def _load_config() -> dict:
    config_path = QA_VASP_DIR / "config" / "generation_config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def _resolve_env(value: str) -> str:
    """Resolve ${VAR} references in config values."""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        return os.environ[value[2:-1]]
    return value


def _get_corpus_files(config: dict, args) -> list[Path]:
    """Return list of .md files to process based on CLI args."""
    corpus_path = QA_VASP_DIR / config["corpus_path"]
    if args.files:
        return [corpus_path / f for f in args.files]
    all_files = sorted(corpus_path.glob("*.md"))
    if args.limit:
        all_files = all_files[: args.limit]
    return all_files


def _get_processed_files(output_path: Path) -> set[str]:
    """Return set of already-processed source_file names from existing JSONL."""
    processed = set()
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


def generate_questions_for_page(
    page_path: Path,
    model: str,
    api_key: str,
    temperature: float,
    system_prompt: str,
) -> list[dict]:
    """Send a single .md page to the LLM and return list of MCQ dicts."""
    content = page_path.read_text()
    page_title = page_path.stem

    response = litellm.completion(
        model=model,
        api_key=api_key,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Page title: {page_title}\n\n"
                    f"---\n{content}\n---\n\n"
                    "Generate multiple-choice questions from this VASP wiki page. "
                    "Return a JSON object with a 'questions' array."
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
        record["source_file"] = page_path.name
        record["page_title"] = page_title
        results.append(record)
    return results


def main():
    parser = argparse.ArgumentParser(description="Generate VASP QA from wiki pages")
    parser.add_argument(
        "--files", nargs="+", help="Specific .md files to process (filenames only)"
    )
    parser.add_argument("--limit", type=int, help="Limit number of pages to process")
    parser.add_argument(
        "--model", type=str, help="Override model from config"
    )
    parser.add_argument(
        "--resume", action="store_true", help="Skip already-processed pages"
    )
    parser.add_argument(
        "--delay", type=float, help="Delay between API calls in seconds"
    )
    args = parser.parse_args()

    config = _load_config()
    model = args.model or config["model"]
    api_key = _resolve_env(config["api_key"])
    temperature = config.get("temperature", 1.0)
    delay_seconds = args.delay if args.delay is not None else config.get("delay_seconds", 1.0)
    system_prompt = config["system_prompt"]

    files = _get_corpus_files(config, args)
    output_path = QA_VASP_DIR / "raw" / "raw_questions.jsonl"
    output_path.parent.mkdir(exist_ok=True)

    # Resume support
    processed = set()
    if args.resume:
        processed = _get_processed_files(output_path)
        print(f"Resume: {len(processed)} pages already processed")

    total_questions = 0
    total_pages = 0
    skipped = 0

    with open(output_path, "a") as f:
        for i, page_path in enumerate(files):
            if not page_path.exists():
                print(f"WARNING: {page_path} not found, skipping")
                continue

            if page_path.name in processed:
                skipped += 1
                continue

            if i > 0 and delay_seconds > 0:
                time.sleep(delay_seconds)

            try:
                questions = generate_questions_for_page(
                    page_path, model, api_key, temperature, system_prompt
                )
            except Exception as e:
                print(f"[{i + 1}/{len(files)}] ERROR {page_path.name}: {e}")
                continue

            for q in questions:
                f.write(json.dumps(q) + "\n")
            f.flush()

            total_questions += len(questions)
            total_pages += 1

            print(
                f"[{i + 1}/{len(files)}] {page_path.name}: "
                f"{len(questions)} questions"
            )

    print("-" * 40)
    if skipped:
        print(f"Skipped (already processed): {skipped}")
    print(f"Pages processed: {total_pages}")
    print(f"Total questions generated: {total_questions}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
