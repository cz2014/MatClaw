"""Run paired significance test: BM25 vs Gemini (both with 3-query fusion).

Runs each (retriever, question_file) combination 3 times and compares accuracy.

Usage:
    python benchmark/qa_vasp/run_paired_test.py
    python benchmark/qa_vasp/run_paired_test.py --dry-run  # Show commands without running
"""

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

QA_DIR = Path(__file__).parent
REPEATS = 3
RETRIEVERS = ["bm25", "gemini"]
QUESTION_FILES = ["qa_bm25_fail.json", "qa_gemini_fail.json"]


def run_test(retriever: str, questions: str, run_id: int, dry_run: bool = False) -> dict | None:
    """Run single test and return summary from results file."""
    cmd = [
        sys.executable,
        str(QA_DIR / "run_qa.py"),
        "--questions", questions,
        "--retriever", retriever,
    ]

    print(f"\n{'='*60}")
    print(f"Run {run_id+1}/{REPEATS}: {retriever} on {questions}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)

    if dry_run:
        return None

    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode != 0:
        print(f"ERROR: Command failed with return code {result.returncode}")
        return None

    # Find the most recent results file
    results_files = sorted(QA_DIR.glob("results_*.jsonl"), key=lambda p: p.stat().st_mtime)
    if not results_files:
        print("ERROR: No results file found")
        return None

    latest = results_files[-1]
    print(f"Results file: {latest}")

    # Parse summary from last line
    with open(latest) as f:
        lines = f.readlines()
        for line in reversed(lines):
            record = json.loads(line.strip())
            if record.get("type") == "summary":
                return {
                    "retriever": retriever,
                    "questions_file": questions,
                    "run_id": run_id,
                    "results_file": str(latest),
                    **record,
                }

    print("ERROR: No summary found in results file")
    return None


def compute_statistics(results: list[dict]) -> dict:
    """Compute paired statistics from all results."""
    # Group by (retriever, questions_file)
    groups = defaultdict(list)
    for r in results:
        key = (r["retriever"], r["questions_file"])
        groups[key].append(r)

    # Compute stats per group
    stats = {}
    for (retriever, qfile), runs in groups.items():
        accuracies = [r["accuracy"] for r in runs]
        correct_counts = [r["correct"] for r in runs]
        total_counts = [r["answered"] for r in runs]

        stats[(retriever, qfile)] = {
            "runs": len(runs),
            "accuracies": accuracies,
            "mean_accuracy": sum(accuracies) / len(accuracies),
            "correct_counts": correct_counts,
            "total_counts": total_counts,
            "total_correct": sum(correct_counts),
            "total_answered": sum(total_counts),
        }

    return stats


def print_summary(stats: dict):
    """Print summary table."""
    print("\n" + "=" * 70)
    print("PAIRED TEST SUMMARY")
    print("=" * 70)

    # Header
    print(f"\n{'Retriever':<10} {'Questions':<20} {'Runs':>5} {'Mean Acc':>10} {'Total':>12}")
    print("-" * 70)

    for (retriever, qfile), s in sorted(stats.items()):
        total = f"{s['total_correct']}/{s['total_answered']}"
        print(f"{retriever:<10} {qfile:<20} {s['runs']:>5} {s['mean_accuracy']:>9.1%} {total:>12}")

    # Comparison by question file
    print("\n" + "-" * 70)
    print("COMPARISON BY QUESTION SET:")

    for qfile in QUESTION_FILES:
        bm25_key = ("bm25", qfile)
        gemini_key = ("gemini", qfile)

        if bm25_key in stats and gemini_key in stats:
            bm25_acc = stats[bm25_key]["mean_accuracy"]
            gemini_acc = stats[gemini_key]["mean_accuracy"]
            diff = gemini_acc - bm25_acc

            print(f"\n{qfile}:")
            print(f"  BM25:   {bm25_acc:.1%}")
            print(f"  Gemini: {gemini_acc:.1%}")
            print(f"  Diff:   {diff:+.1%} ({'Gemini' if diff > 0 else 'BM25'} better)")


def main():
    parser = argparse.ArgumentParser(description="Run paired significance test")
    parser.add_argument("--dry-run", action="store_true", help="Show commands without running")
    parser.add_argument("--repeats", type=int, default=REPEATS, help=f"Number of repeats (default: {REPEATS})")
    args = parser.parse_args()

    print(f"Paired Significance Test: BM25 vs Gemini (3-query fusion)")
    print(f"Question files: {QUESTION_FILES}")
    print(f"Repeats per condition: {args.repeats}")
    print(f"Total runs: {len(RETRIEVERS) * len(QUESTION_FILES) * args.repeats}")

    if args.dry_run:
        print("\n[DRY RUN - Commands will be shown but not executed]")

    results = []
    for retriever in RETRIEVERS:
        for qfile in QUESTION_FILES:
            for run_id in range(args.repeats):
                result = run_test(retriever, qfile, run_id, dry_run=args.dry_run)
                if result:
                    results.append(result)

    if args.dry_run:
        print("\n[DRY RUN COMPLETE]")
        return

    if not results:
        print("\nNo results collected!")
        return

    # Compute and print statistics
    stats = compute_statistics(results)
    print_summary(stats)

    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = QA_DIR / f"paired_test_{timestamp}.json"
    with open(output_path, "w") as f:
        json.dump({
            "timestamp": timestamp,
            "repeats": args.repeats,
            "results": results,
            "stats": {f"{k[0]}_{k[1]}": v for k, v in stats.items()},
        }, f, indent=2)
    print(f"\nDetailed results saved to: {output_path}")


if __name__ == "__main__":
    main()
