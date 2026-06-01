"""Test utilities for MLFF agent."""

from __future__ import annotations

import re
from pathlib import Path

from scripts.analyze_steps import parse


def analyze_agent_errors(workspace_dir: Path) -> dict:
    """Analyze agent errors with code-based counting from history.jsonl.

    Args:
        workspace_dir: Directory containing history.jsonl

    Returns:
        Dict with 'total_steps', 'error_steps'.
    """
    file_path = workspace_dir / "history.jsonl"
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    steps = parse(file_path)
    return {
        "total_steps": len(steps),
        "error_steps": sum(1 for s in steps if s.error),
    }


# ---------------------------------------------------------------------------
# Benchmark report parsing (operates on markdown reports, not steps.jsonl)
# ---------------------------------------------------------------------------

_RUN_HEADER = re.compile(r"^## Run \d+", re.MULTILINE)
_STEP_COUNTS = re.compile(r"\*\*Step Counts\*\*: (\d+) total, (\d+) errors, (\d+) RAG")
_TOKEN_TOTAL = re.compile(r"Total=([\d,]+)")
_ERROR_CATEGORY = re.compile(r"\[Step \d+\] ([^:]+):")

CATEGORY_NAMES = [
    "API & Implementation Error",
    "Format & Protocol Violation",
    "Scientific Theory & Logic Error",
    "Contextual Decay",
]


def generate_benchmark_summary(report_path: Path) -> str:
    """Parse benchmark report and generate summary statistics.

    Args:
        report_path: Path to benchmark_report_*.md file

    Returns:
        Markdown string with summary statistics
    """
    content = report_path.read_text()

    # Count runs
    run_count = len(_RUN_HEADER.findall(content))

    # Extract step counts
    step_matches = _STEP_COUNTS.findall(content)
    total_steps = sum(int(m[0]) for m in step_matches)
    error_steps = sum(int(m[1]) for m in step_matches)

    # Extract token totals
    token_matches = _TOKEN_TOTAL.findall(content)
    total_tokens = sum(int(m.replace(",", "")) for m in token_matches)
    avg_tokens = total_tokens // run_count if run_count > 0 else 0

    # Calculate averages and rates
    avg_steps = total_steps / run_count if run_count > 0 else 0
    error_rate = (error_steps / total_steps * 100) if total_steps > 0 else 0

    # Count error categories
    category_matches = _ERROR_CATEGORY.findall(content)
    category_counts = {name: 0 for name in CATEGORY_NAMES}
    for match in category_matches:
        for name in CATEGORY_NAMES:
            if name in match:
                category_counts[name] += 1
                break

    # Build summary markdown
    lines = [
        "## Summary",
        "",
        f"**Runs**: {run_count}",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total Steps | {total_steps} |",
        f"| Error Steps | {error_steps} |",
        f"| Error Rate | {error_rate:.1f}% |",
        f"| Avg Steps/Run | {avg_steps:.1f} |",
        f"| Avg Tokens/Run | {avg_tokens:,} |",
        "",
        "**Error Classification**:",
        "| Category | Count | Percentage |",
        "|----------|-------|------------|",
    ]

    for name in CATEGORY_NAMES:
        count = category_counts[name]
        pct = (count / error_steps * 100) if error_steps > 0 else 0
        lines.append(f"| {name} | {count} | {pct:.1f}% |")

    return "\n".join(lines) + "\n"


def append_summary_to_report(report_path: Path) -> None:
    """Append summary statistics to existing benchmark report."""
    summary = generate_benchmark_summary(report_path)
    with open(report_path, "a") as f:
        f.write("\n---\n\n")
        f.write(summary)
