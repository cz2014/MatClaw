"""Test: VASP SCF calculation for MoS2 monolayer."""

import shutil
import sys
from pathlib import Path

# code/: code/tests/demos/demo01_*.py -> demos -> tests -> code
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
    from tests.demos._harness import main

    task = "I want to obtain the relaxed structure of a Sulfur vacancy in a 5x5 supercell of MoS2, using VASP. (MoS2 unit cell structure is in file './MoS2.cif'). I have several requirements: (a) make the Sulfur vacancy close to the center of supercell; (b) add a random displacement ~ 0.1 Ang on each atom to lower the symmetry for better geometry optimization; (c) use parameters that lead to high precision calculations. (d) only help me generate these input files for VASP: INCAR, KPOINTS, POSCAR. "

    from scripts.analyze_steps import parse
    from tests.utils import analyze_agent_errors

    setup()
    main(task, workspace_dir=WORKSPACE_DIR)

    # Parse steps and print summary
    steps = parse(WORKSPACE_DIR / "history.jsonl")
    total = len(steps)
    errors = sum(1 for s in steps if s.error)
    print(f"Step counts: {total} total, {errors} errors")

    # Analyze errors in the conversation (writes to workspace/error_analysis.md)
    analyze_agent_errors(WORKSPACE_DIR)
