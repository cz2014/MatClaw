"""Benchmark runner for agent tests."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

# code/: code/tests/demos/benchmark_runner.py -> demos -> tests -> code
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.analyze_steps import parse  # noqa: E402  (sys.path setup above)
from tests.utils import append_summary_to_report  # noqa: E402  (sys.path setup above)

WORKSPACE_DIR = PROJECT_ROOT.parent / "workspace"
RESULTS_DIR = Path(__file__).parent  # demos/ directory

# Configurable parameters (edit these)
TEST_FILE = "tests/demos/demo01_vasp_mos2_relax.py"
NUM_ITERATIONS = 40


def run_benchmark(test_file: str, iterations: int) -> Path:
    """Run test file N times and collect error analysis results.

    Writes results incrementally after each iteration to preserve partial
    results if terminated early.

    Args:
        test_file: Path to test file (relative to project root)
        iterations: Number of times to run the test

    Returns:
        Path to merged results file
    """
    # Create output file with header before loop starts
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = RESULTS_DIR / f"benchmark_report_{timestamp}.md"

    header = f"# Benchmark Results: {test_file}\n\n"
    header += f"- Iterations: {iterations}\n"
    header += f"- Timestamp: {timestamp}\n\n---\n\n"
    output_file.write_text(header)

    error_analysis_file = WORKSPACE_DIR / "error_analysis.md"

    for i in range(iterations):
        print(f"\n{'='*60}")
        print(f"Run {i+1}/{iterations}: {test_file}")
        print(f"{'='*60}\n")

        # Run test via subprocess
        subprocess.run(
            [sys.executable, PROJECT_ROOT / test_file],
            cwd=PROJECT_ROOT,
        )

        # Append result immediately after each run
        with open(output_file, "a") as f:
            f.write(f"## Run {i+1}\n\n")

            # Step counts and token usage from history.jsonl
            steps = parse(WORKSPACE_DIR / "history.jsonl")
            total_steps = len(steps)
            error_steps = sum(1 for s in steps if s.error)
            f.write(f"**Step Counts**: {total_steps} total, {error_steps} errors\n\n")

            total_in = sum(s.input_tokens or 0 for s in steps)
            total_out = sum(s.output_tokens or 0 for s in steps)
            f.write(f"**Token Usage**: Input={total_in:,}, Output={total_out:,}, Total={total_in + total_out:,}\n\n")

            # Error analysis
            if error_analysis_file.exists():
                content = error_analysis_file.read_text()
                f.write(f"{content}\n\n")
            else:
                f.write("*No error_analysis.md generated*\n\n")

            f.write("---\n\n")

    # Append summary statistics
    append_summary_to_report(output_file)

    return output_file


if __name__ == "__main__":
    output = run_benchmark(TEST_FILE, NUM_ITERATIONS)
    print(f"\nBenchmark complete! Results saved to: {output}")
