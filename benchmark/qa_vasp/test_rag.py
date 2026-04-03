"""RAG retrieval quality test for VASP wiki corpus.

Tests whether the RAG system retrieves the correct documentation chunks
for queries that failed during the QA benchmark.

Run:
    python benchmark/qa_vasp/test_rag.py
    python benchmark/qa_vasp/test_rag.py --retriever gemini
    pytest benchmark/qa_vasp/test_rag.py -v
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from core.retrievers import load_retriever

DATA_DIR = Path(__file__).parent / "data"
REPORT_DIR = Path(__file__).parent

# Ground truth queries derived from QA benchmark failure analysis
# Each entry maps a query to the expected file that should be retrieved
#
# Categories:
# 1. WRONG_ANSWER: Query from question agent answered incorrectly
# 2. RETRY_FAILED: First RAG query that didn't return useful results (agent retried)
# 3. RETRY_SUCCESS: The query that succeeded after retry (for comparison)

EVAL_QUERIES = [
    # =========================================================================
    # WRONG ANSWER: Agent got this question wrong due to RAG ranking issue
    # Question: "Which IBRION value must be set for IRC calculation?"
    # Expected: C (IBRION=40), Got: D (IBRION=44)
    # =========================================================================
    {
        "query": "IBRION IRC Intrinsic Reaction Coordinate",
        "expected_file": "IBRION.md",
        "description": "[WRONG_ANSWER] IBRION.md ranked 6th, outside top-5",
        "category": "wrong_answer",
    },

    # =========================================================================
    # RETRY CASES: Queries that failed on first attempt, succeeded on retry
    # These reveal BM25 keyword matching weaknesses
    # =========================================================================

    # Case 1: QPOINTS (phonon dispersion q-points input file)
    {
        "query": "VASP internal phonon code q-points input file",
        "expected_file": "QPOINTS.md",
        "description": "[RETRY_FAILED] First query didn't find QPOINTS.md",
        "category": "retry_failed",
    },
    {
        "query": "VASP internal phonon dispersion q-points QPOINTS KPOINTS",
        "expected_file": "QPOINTS.md",
        "description": "[RETRY_SUCCESS] Adding 'QPOINTS' keyword helped",
        "category": "retry_success",
    },

    # Case 2: LSELFENERGY (GW frequency points)
    {
        "query": "LSELFENERGY frequency points range",
        "expected_file": "LSELFENERGY.md",
        "description": "[RETRY_FAILED] First query - too generic",
        "category": "retry_failed",
    },
    {
        "query": "LSELFENERGY default 100 points -50 50",
        "expected_file": "LSELFENERGY.md",
        "description": "[RETRY_FAILED] Second query - wrong numbers",
        "category": "retry_failed",
    },
    {
        "query": "LSELFENERGY default frequency points range 100 -50 50",
        "expected_file": "LSELFENERGY.md",
        "description": "[RETRY_SUCCESS] Third query succeeded",
        "category": "retry_success",
    },

    # Case 3: VRijkl (Coulomb integrals ALGO setting)
    {
        "query": "VRijkl off-centre Coulomb integrals ALGO",
        "expected_file": "VRijkl.md",
        "description": "[RETRY_FAILED] Word order affected BM25 matching",
        "category": "retry_failed",
    },
    {
        "query": "VRijkl ALGO off-centre Coulomb integrals",
        "expected_file": "VRijkl.md",
        "description": "[RETRY_SUCCESS] Reordered query succeeded",
        "category": "retry_success",
    },

    # Case 4: I_CONSTRAINED_M (magnetic moment constraints)
    {
        "query": "I_CONSTRAINED_M magnetic moment constraint size and direction",
        "expected_file": "I_CONSTRAINED_M.md",
        "description": "[RETRY_FAILED] Too many keywords diluted relevance",
        "category": "retry_failed",
    },
    {
        "query": "I_CONSTRAINED_M VASP",
        "expected_file": "I_CONSTRAINED_M.md",
        "description": "[RETRY_SUCCESS] Simpler query worked better",
        "category": "retry_success",
    },

    # Case 5: LTRIPLET (BSE triplet state)
    {
        "query": "LTRIPLET BSE ISPIN=1 LSORBIT=.FALSE.",
        "expected_file": "LTRIPLET.md",
        "description": "[RETRY_FAILED] Equality syntax hurt BM25 matching",
        "category": "retry_failed",
    },
    {
        "query": "LTRIPLET tag BSE ISPIN=1",
        "expected_file": "LTRIPLET.md",
        "description": "[RETRY_SUCCESS] Simplified query worked",
        "category": "retry_success",
    },

    # Case 6: LALL_IN_ONE / NBANDSEXACT
    {
        "query": "LALL_IN_ONE automatic enablement NBANDS",
        "expected_file": "NBANDSEXACT.md",
        "description": "[RETRY_FAILED] Answer is in NBANDSEXACT.md, not LALL_IN_ONE.md",
        "category": "retry_failed",
    },
    {
        "query": "LALL_IN_ONE automatically enabled NBANDS",
        "expected_file": "NBANDSEXACT.md",
        "description": "[RETRY_SUCCESS] Slightly different phrasing worked",
        "category": "retry_success",
    },
]


def test_rag_retrieval():
    """Test that RAG retrieves correct chunks for known queries.

    Only checks if the expected SOURCE FILE appears in top-5 results,
    since QA questions are derived from specific source files.
    """
    retriever = load_retriever("bm25", DATA_DIR)

    results_by_category = {
        "wrong_answer": {"total": 0, "passed": 0},
        "retry_failed": {"total": 0, "passed": 0},
        "retry_success": {"total": 0, "passed": 0},
    }
    failures = []

    for q in EVAL_QUERIES:
        results = retriever.search(q["query"], top_k=5)
        files_returned = [chunk.file_path for chunk, _ in results]

        # Check if expected file is in top-5 results
        found = q["expected_file"] in files_returned

        category = q.get("category", "unknown")
        if category in results_by_category:
            results_by_category[category]["total"] += 1

        if found and category in results_by_category:
            results_by_category[category]["passed"] += 1

        if not found:
            failures.append({
                "query": q["query"],
                "description": q["description"],
                "expected_file": q["expected_file"],
                "got_files": files_returned,
                "category": category,
            })

    # Report by category
    print("\n=== RAG RETRIEVAL RESULTS BY CATEGORY (file match in top-5) ===")
    for cat, stats in results_by_category.items():
        if stats["total"] > 0:
            pct = 100 * stats["passed"] / stats["total"]
            print(f"  {cat}: {stats['passed']}/{stats['total']} ({pct:.0f}%)")

    # Report failures
    if failures:
        print("\n=== FAILURES (expected file not in top-5) ===")
        for f in failures:
            print(f"\n[{f['category']}] Query: '{f['query']}'")
            print(f"  Expected: {f['expected_file']}")
            print(f"  Got: {f['got_files']}")

    # Summary
    total = len(EVAL_QUERIES)
    successes = total - len(failures)
    print(f"\n=== Overall: {successes}/{total} queries found expected file in top-5 ===")

    # Soft assertion: retry_success queries should mostly work
    retry_success = results_by_category["retry_success"]
    assert retry_success["passed"] >= retry_success["total"] // 2, \
        "Most retry_success queries should find expected file"


def compute_metrics(evaluations: list[dict]) -> dict:
    """Compute retrieval quality metrics."""
    ranks = [e["match_rank"] for e in evaluations if e["match_rank"] is not None]
    total = len(evaluations)
    found = len(ranks)

    # Mean Reciprocal Rank (MRR) - average of 1/rank, higher is better
    mrr = sum(1.0 / r for r in ranks) / total if ranks else 0.0

    # Average rank of found items (lower is better)
    avg_rank = sum(ranks) / found if found else float('inf')

    # Recall@K
    recall_at_5 = sum(1 for r in ranks if r <= 5) / total
    recall_at_10 = found / total

    return {
        "mrr": mrr,
        "avg_rank": avg_rank,
        "recall@5": recall_at_5,
        "recall@10": recall_at_10,
        "found": found,
        "total": total,
    }


def generate_report(evaluations: list[dict], retriever_method: str = "bm25") -> str:
    """Generate markdown report from evaluations."""
    lines = [
        "# VASP Wiki RAG Quality Evaluation Report",
        "",
        f"Generated: {datetime.now().isoformat()}",
        "",
        "## Evaluation Context",
        "",
        "**Purpose**: Evaluate RAG retrieval quality for VASP wiki documentation",
        "**Corpus**: VASP wiki markdown files",
        f"**Retriever**: {retriever_method}",
        "**Success criteria**: Expected file in top-5 results",
        "",
        "---",
        "",
    ]

    # Group by category
    by_category = {}
    for e in evaluations:
        cat = e["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(e)

    for cat_name, evals in by_category.items():
        lines.extend([
            f"## Category: {cat_name.upper()}",
            "",
        ])

        for e in evals:
            in_top5 = e["match_rank"] is not None and e["match_rank"] <= 5
            verdict = "PASS" if in_top5 else "FAIL"

            lines.extend([
                f"### Query: `{e['query']}`",
                "",
                f"**Expected file**: `{e['expected_file']}`",
                f"**Note**: {e['description']}",
                "",
                "| Rank | File | Score | Match |",
                "|------|------|-------|-------|",
            ])

            for r in e["results"][:10]:
                match = "**YES**" if r["is_match"] else ""
                lines.append(f"| {r['rank']} | {r['file']}:{r['lines']} | {r['score']:.4f} | {match} |")

            lines.append("")

            if e["match_rank"]:
                lines.append(f"**Result**: {verdict} - Found at rank {e['match_rank']} (in top-5: {'YES' if in_top5 else 'NO'})")
            else:
                lines.append(f"**Result**: {verdict} - Expected file not in top-10")

            lines.extend(["", "---", ""])

    # Summary table
    lines.extend([
        "## Summary",
        "",
        "| Category | Passed | Failed | Rate |",
        "|----------|--------|--------|------|",
    ])

    for cat_name, evals in by_category.items():
        passed = sum(1 for e in evals if e["match_rank"] and e["match_rank"] <= 5)
        failed = len(evals) - passed
        rate = 100 * passed / len(evals) if evals else 0
        lines.append(f"| {cat_name} | {passed} | {failed} | {rate:.0f}% |")

    total_passed = sum(1 for e in evaluations if e["match_rank"] and e["match_rank"] <= 5)
    total = len(evaluations)
    lines.extend([
        f"| **Total** | **{total_passed}** | **{total - total_passed}** | **{100*total_passed/total:.0f}%** |",
        "",
    ])

    return "\n".join(lines)


def run_evaluation(write_report: bool = True, retriever_method: str = "bm25") -> list[dict]:
    """Run evaluation and optionally write report."""
    retriever = load_retriever(retriever_method, DATA_DIR)

    print(f"\nLoaded {retriever.chunk_count} chunks from {DATA_DIR} (retriever: {retriever_method})")

    evaluations = []

    for q in EVAL_QUERIES:
        results = retriever.search(q["query"], top_k=10)

        match_rank = None
        ranked_results = []

        for rank, (chunk, score) in enumerate(results, 1):
            is_match = q["expected_file"] in chunk.file_path

            if is_match and match_rank is None:
                match_rank = rank

            ranked_results.append({
                "rank": rank,
                "file": chunk.file_path,
                "lines": f"{chunk.start_line}-{chunk.end_line}",
                "score": score,
                "is_match": is_match,
            })

        evaluations.append({
            "query": q["query"],
            "expected_file": q["expected_file"],
            "description": q["description"],
            "category": q.get("category", "unknown"),
            "match_rank": match_rank,
            "results": ranked_results,
        })

    if write_report:
        report = generate_report(evaluations, retriever_method)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = REPORT_DIR / f"rag_eval_report_{retriever_method}_{timestamp}.md"
        report_path.write_text(report)
        print(f"Report written to: {report_path}")

    return evaluations


def test_rag_detailed():
    """Detailed test with full output for debugging RAG issues.

    Only checks if the expected SOURCE FILE appears in results,
    since QA questions are derived from specific source files.
    """
    retriever = load_retriever("bm25", DATA_DIR)

    print(f"\nLoaded {retriever.chunk_count} chunks from {DATA_DIR}")

    # Group queries by category for clearer output
    categories = {}
    for q in EVAL_QUERIES:
        cat = q.get("category", "unknown")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(q)

    summary = {"pass": 0, "fail": 0}

    for cat_name, queries in categories.items():
        print(f"\n{'#'*60}")
        print(f"# Category: {cat_name.upper()}")
        print(f"{'#'*60}")

        for q in queries:
            print(f"\n{'='*60}")
            print(f"Query: '{q['query']}'")
            print(f"Expected file: {q['expected_file']}")
            print(f"Note: {q['description']}")
            print("-" * 60)

            results = retriever.search(q["query"], top_k=10)

            match_rank = None

            for rank, (chunk, score) in enumerate(results, 1):
                is_expected_file = q["expected_file"] in chunk.file_path

                if is_expected_file and match_rank is None:
                    match_rank = rank

                marker = " [FILE MATCH]" if is_expected_file else ""

                print(f"  {rank}. {chunk.file_path}:{chunk.start_line}-{chunk.end_line} "
                      f"(score={score:.4f}){marker}")

            if match_rank:
                in_top5 = "YES" if match_rank <= 5 else "NO"
                print(f"  RESULT: FOUND at rank {match_rank} (in top-5: {in_top5})")
                summary["pass"] += 1
            else:
                print("  RESULT: FAIL - expected file not in top 10")
                summary["fail"] += 1

    print(f"\n{'='*60}")
    print(f"SUMMARY: {summary['pass']} passed, {summary['fail']} failed")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="RAG retrieval quality test for VASP wiki corpus")
    parser.add_argument(
        "--retriever",
        choices=["bm25", "gemini"],
        default="bm25",
        help="Retriever type: 'bm25' (sparse) or 'gemini' (dense embeddings)",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip writing the markdown report",
    )
    args = parser.parse_args()

    # Run evaluation and write report
    evaluations = run_evaluation(
        write_report=not args.no_report,
        retriever_method=args.retriever,
    )

    # Print metrics
    metrics = compute_metrics(evaluations)
    print(f"\nMETRICS:")
    print(f"  MRR: {metrics['mrr']:.3f}")
    print(f"  Avg Rank: {metrics['avg_rank']:.2f}")
    print(f"  Recall@5: {metrics['recall@5']:.1%}")
    print(f"  Recall@10: {metrics['recall@10']:.1%}")

    # Print summary
    total = len(evaluations)
    passed = sum(1 for e in evaluations if e["match_rank"] and e["match_rank"] <= 5)
    print(f"\nSUMMARY: {passed}/{total} queries found expected file in top-5")


if __name__ == "__main__":
    main()
