"""Curate raw VASP QA questions into balanced qa_120.json / qa_500.json.

Reads raw/raw_questions.jsonl, applies category-balanced selection,
converts to run_qa.py-compatible format, and outputs final JSON files.

Usage:
    python benchmark/qa_vasp/curate_qa.py                       # Default: 120 + 500
    python benchmark/qa_vasp/curate_qa.py --sizes 120 500       # Custom sizes
    python benchmark/qa_vasp/curate_qa.py --input raw/other.jsonl
    python benchmark/qa_vasp/curate_qa.py --dry-run             # Print stats only
"""

import argparse
import json
import random
from collections import Counter
from pathlib import Path

QA_VASP_DIR = Path(__file__).parent

# Target category distribution (equal weights)
CATEGORY_TARGETS = {
    "Tag_Identification": 0.25,
    "Tag_Dependency": 0.25,
    "Error_Restart": 0.25,
    "Physics_Recipe": 0.25,
}

LETTER_MAP = {0: "A", 1: "B", 2: "C", 3: "D"}


def _load_raw(input_path: Path) -> list[dict]:
    """Load all raw MCQ records from JSONL."""
    records = []
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def _validate(record: dict) -> bool:
    """Check that a raw record has valid structure."""
    if len(record.get("choices", [])) != 4:
        return False
    if record.get("correct_answer_index") not in (0, 1, 2, 3):
        return False
    if not record.get("question"):
        return False
    if record.get("category") not in CATEGORY_TARGETS:
        return False
    return True


def _convert_format(record: dict) -> dict:
    """Convert generation format to run_qa.py format.

    MCQ {choices: ["Normal","VeryFast","Damped","Fast"], correct_answer_index: 1}
      ->
    run_qa {choices: {"A":"A. Normal","B":"B. VeryFast","C":"C. Damped","D":"D. Fast"},
            correct_answer: "B"}
    """
    choices = {}
    for i, choice_text in enumerate(record["choices"]):
        letter = LETTER_MAP[i]
        choices[letter] = f"{letter}. {choice_text}"

    correct_letter = LETTER_MAP[record["correct_answer_index"]]

    return {
        "source_file": record.get("source_file", ""),
        "category": record["category"],
        "question": record["question"],
        "choices": choices,
        "correct_answer": correct_letter,
    }


def _balanced_select(
    records: list[dict], n: int, seed: int
) -> tuple[list[dict], list[dict]]:
    """Select n records with category-balanced distribution.

    Returns (selected, remaining).
    If a category is scarce, redistributes slack to other categories.
    """
    rng = random.Random(seed)

    # Group by category
    by_category: dict[str, list[dict]] = {}
    for cat in CATEGORY_TARGETS:
        by_category[cat] = []
    for r in records:
        cat = r["category"]
        if cat in by_category:
            by_category[cat].append(r)

    # Shuffle each category
    for cat in by_category:
        rng.shuffle(by_category[cat])

    # Compute target counts per category
    targets = {cat: int(n * pct) for cat, pct in CATEGORY_TARGETS.items()}
    # Distribute remainder to largest categories
    remainder = n - sum(targets.values())
    for cat in sorted(CATEGORY_TARGETS, key=CATEGORY_TARGETS.get, reverse=True):
        if remainder <= 0:
            break
        targets[cat] += 1
        remainder -= 1

    # First pass: take min(target, available) from each category
    selected = []
    slack = 0
    for cat in CATEGORY_TARGETS:
        available = len(by_category[cat])
        take = min(targets[cat], available)
        selected.extend(by_category[cat][:take])
        by_category[cat] = by_category[cat][take:]
        slack += targets[cat] - take

    # Second pass: redistribute slack from remaining pool
    if slack > 0:
        pool = []
        for cat in by_category:
            pool.extend(by_category[cat])
        rng.shuffle(pool)
        extra = pool[:slack]
        selected.extend(extra)
        # Remove extra from by_category
        extra_set = {id(r) for r in extra}
        for cat in by_category:
            by_category[cat] = [r for r in by_category[cat] if id(r) not in extra_set]

    # Build remaining
    remaining = []
    for cat in by_category:
        remaining.extend(by_category[cat])

    rng.shuffle(selected)
    return selected, remaining


def main():
    parser = argparse.ArgumentParser(description="Curate VASP QA questions")
    parser.add_argument(
        "--input",
        type=str,
        default="raw/raw_questions.jsonl",
        help="Input JSONL file (relative to qa_vasp/)",
    )
    parser.add_argument(
        "--sizes",
        type=int,
        nargs="+",
        default=[120, 500],
        help="Output sizes (default: 120 500)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print stats without writing files"
    )
    args = parser.parse_args()

    input_path = QA_VASP_DIR / args.input
    raw = _load_raw(input_path)
    print(f"Loaded {len(raw)} raw questions from {input_path}")

    # Validate
    valid = [r for r in raw if _validate(r)]
    invalid_count = len(raw) - len(valid)
    if invalid_count:
        print(f"Dropped {invalid_count} invalid records")
    print(f"Valid questions: {len(valid)}")

    # Category distribution
    cat_counts = Counter(r["category"] for r in valid)
    print("\nCategory distribution (raw):")
    for cat in CATEGORY_TARGETS:
        count = cat_counts.get(cat, 0)
        pct = count / len(valid) * 100 if valid else 0
        print(f"  {cat}: {count} ({pct:.1f}%)")

    if args.dry_run:
        print("\n[dry-run] No files written.")
        return

    # Select for each size (independent selection with different seeds)
    seeds = [42, 123, 456, 789]  # Different seed for each output file
    for i, size in enumerate(args.sizes):
        if size > len(valid):
            print(
                f"\nWARNING: requested {size} but only {len(valid)} available. "
                f"Taking all {len(valid)}."
            )
            size = len(valid)

        seed = seeds[i] if i < len(seeds) else 42 + i
        selected, _ = _balanced_select(valid, size, seed)

        # Convert format
        output = [_convert_format(r) for r in selected]
        output_path = QA_VASP_DIR / f"qa_{size}.json"
        with open(output_path, "w") as f:
            json.dump(output, f, indent=2)

        # Stats
        cat_dist = Counter(r["category"] for r in selected)
        print(f"\nqa_{size}.json: {len(output)} questions")
        for cat in CATEGORY_TARGETS:
            count = cat_dist.get(cat, 0)
            target_pct = CATEGORY_TARGETS[cat] * 100
            actual_pct = count / len(output) * 100 if output else 0
            print(f"  {cat}: {count} ({actual_pct:.1f}%, target {target_pct:.0f}%)")
        print(f"  Written to: {output_path}")


if __name__ == "__main__":
    main()
