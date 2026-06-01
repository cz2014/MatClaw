"""Test: MoS2 ions-only relaxation via jobflow-remote."""

import argparse
import shutil
import sys
from pathlib import Path

# code/: code/tests/demos/demo02_*.py -> demos -> tests -> code
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

WORKSPACE_DIR = PROJECT_ROOT.parent / "workspace"
REF_DIR = PROJECT_ROOT.parent / "ref"


def setup():
    """Clean workspace and copy input files."""
    if WORKSPACE_DIR.exists():
        shutil.rmtree(WORKSPACE_DIR)
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(REF_DIR / "MoS2.cif", WORKSPACE_DIR / "MoS2.cif")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MoS2 ions-only relaxation test")
    parser.add_argument("--project", default="anvil",
                        help="HPC project name (default: anvil)")
    args = parser.parse_args()

    from tests.demos._harness import main
    from scripts.analyze_steps import parse
    from tests.utils import analyze_agent_errors

    task = "I have a MoS2 structure in './MoS2.cif'. Please run an ions-only VASP relaxation on our remote cluster. When it finishes, save the relaxed structure to 'relaxed_min.cif' and tell me the final total energy."

    print(f"Using project={args.project}")

    setup()

    main(task, workspace_dir=WORKSPACE_DIR, project=args.project)

    # Parse steps and print summary
    steps = parse(WORKSPACE_DIR / "history.jsonl")
    total = len(steps)
    errors = sum(1 for s in steps if s.error)
    print(f"Step counts: {total} total, {errors} errors")

    # Analyze errors in the conversation (writes to workspace/error_analysis.md)
    analyze_agent_errors(WORKSPACE_DIR)
