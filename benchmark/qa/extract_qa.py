"""Extract QA benchmark subsets from MatTools zip files.

Usage:
    python benchmark/qa/extract_qa.py               # code QA (default)
    python benchmark/qa/extract_qa.py --source doc   # doc QA

Generates (per source):
    - {prefix}_120.json: 120 QA pairs (seed=42)
    - {prefix}_300.json: 300 QA pairs (seed=123, no overlap with _120)
"""

import argparse
import json
import random
import zipfile
from pathlib import Path

RANDOM_SEED = 42
OUTPUT_DIR = Path(__file__).parent

_MATTOOLS_DIR = Path("/Users/cz/Work/MatTools_temp/qa_benchmark/generated_qa")

SOURCES = {
    "code": {
        "zip": _MATTOOLS_DIR / "generation_results_code.json.zip",
        "prefix": "qa",
    },
    "doc": {
        "zip": _MATTOOLS_DIR / "generation_results_doc.json.zip",
        "prefix": "qa_doc",
    },
}


def load_qa_from_zip(zip_path: Path) -> list[dict]:
    """Load and flatten QA data from zip file."""
    with zipfile.ZipFile(zip_path) as z:
        # Get the JSON filename inside the zip
        json_filename = [n for n in z.namelist() if n.endswith('.json')][0]
        data = json.loads(z.read(json_filename))

    # Flatten: each source may have multiple questions
    questions = []
    for item in data:
        source_file = item.get('source', {}).get('metadata', {}).get('code_source_file', '')
        for q in item.get('questions', []):
            questions.append({
                'source_file': source_file,
                'question': q['question'],
                'choices': q['choices'],
                'correct_answer': q['correct_answer']
            })
    return questions


def extract_subset(questions: list[dict], subset_size: int, seed: int = RANDOM_SEED) -> list[dict]:
    """Extract a random subset with fixed seed for reproducibility."""
    random.seed(seed)
    return random.sample(questions, min(subset_size, len(questions)))


def main():
    parser = argparse.ArgumentParser(description="Extract QA benchmark subsets from MatTools zip files.")
    parser.add_argument("--source", choices=SOURCES.keys(), default="code",
                        help="QA source type (default: code)")
    args = parser.parse_args()

    src = SOURCES[args.source]
    zip_path = src["zip"]
    prefix = src["prefix"]

    if not zip_path.exists():
        raise FileNotFoundError(f"MatTools zip not found: {zip_path}")

    print(f"Loading QA data from {zip_path}...")
    all_questions = load_qa_from_zip(zip_path)
    print(f"Total questions: {len(all_questions)}")

    # Extract _120 first (seed=42)
    qa_120 = extract_subset(all_questions, 120, seed=42)
    output_path = OUTPUT_DIR / f"{prefix}_120.json"
    with open(output_path, 'w') as f:
        json.dump(qa_120, f, indent=2)
    print(f"Wrote {len(qa_120)} questions to {output_path}")

    # Build set of _120 keys to exclude
    def get_key(q):
        return (q["source_file"], q["question"])

    qa_120_keys = set(get_key(q) for q in qa_120)

    # Filter out _120 questions from pool
    remaining = [q for q in all_questions if get_key(q) not in qa_120_keys]
    print(f"Remaining questions (excluding {prefix}_120): {len(remaining)}")

    # Extract _300 from remaining (seed=123, no overlap)
    qa_300 = extract_subset(remaining, 300, seed=123)
    output_path = OUTPUT_DIR / f"{prefix}_300.json"
    with open(output_path, 'w') as f:
        json.dump(qa_300, f, indent=2)
    print(f"Wrote {len(qa_300)} questions to {output_path}")


if __name__ == "__main__":
    main()
