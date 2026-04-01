"""Test: CIPS distillation -- multi-student ensemble with DP-GEN-style active learning.

Extended version of test6_cips_distill.py with key changes:
  1. Stopping condition: 5 iterations OR MAE_f < 0.10 eV/A (whichever first)
  2. Active learning strategy guided by experience.md (multi-student ensemble,
     inter-model variance selection, teacher labeling)
  3. Fast preset for rapid iteration cycles
"""

import argparse
import shutil
import signal
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

REF_DIR = PROJECT_ROOT / ".ref"


def setup(workspace_dir: Path):
    """Clean workspace and copy input files."""
    if workspace_dir.exists():
        shutil.rmtree(workspace_dir)
    workspace_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(REF_DIR / "CuInP2S6.cif", workspace_dir / "CuInP2S6.cif")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CIPS distillation stress test (long-running)")
    parser.add_argument("--monitor", action="store_true", help="Launch health-check daemon alongside agent")
    parser.add_argument("--project", default="perlmutter",
                        help="HPC project name (default: perlmutter)")
    parser.add_argument("--workspace", type=Path, default=None,
                        help="Workspace directory (default: workspace/)")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from existing workspace (skip setup, reload history)")
    args = parser.parse_args()

    WORKSPACE_DIR = (args.workspace or (PROJECT_ROOT / "workspace")).resolve()

    from main import main
    from scripts.analyze_steps import parse_steps
    from tests.utils import analyze_agent_errors

    task = """\
I have a monolayer CuInP2S6 (CIPS) structure in './CuInP2S6.cif' (10 atoms/cell).
CuInP2S6 is a van der Waals ferroelectric with a Curie temperature of ~330K.

Train a "student" DeePMD model for CIPS by distilling from a published teacher model.
The teacher model (a TensorFlow frozen graph, .pb format) is deployed on Perlmutter at:
  /pscratch/sd/c/cz2014/cips_distill/frozen_model.pb

Use the teacher model to generate initial training data by running MLFF MD at diverse
thermodynamic conditions, then train student models on the teacher's predictions.
Iterate with active distillation: explore new structures with student model MD,
evaluate by different student models, select high-variance frames from student models,
label with the teacher model, and retrain the students.

STOPPING CONDITION: Stop when EITHER:
  (a) You have completed 5 active distillation iterations, OR
  (b) The student model achieves MAE_f below 0.10 eV/A on a held-out test set
      that was never used for training.
Whichever condition is met first, stop and report the final results.

## Constraints

- Type map: Cu, In, P, S (matching the teacher model).
- Keep supercells < 200 atoms.
- Use the `fast` DeePMD network preset for student training.
- Initial teacher MDs: at least 20 ps per temperature; subsample to ~500 frames per trajectory. This overrides any shorter MD times from the paper or experience notes.
- Use the debug queue (perlmutter_debug worker) for all jobs.
- Break your work into phases. After each phase completes, inspect the results
  before proceeding. Do not write loops that run the entire workflow end-to-end.
- You have access to atomate2 (force field jobs), jobflow/jobflow-remote
  (workflow submission to remote HPC), dpdata (dataset handling),
  and numpy/scipy for local computation. deepmd-kit is installed on the remote HPC
  cluster but NOT locally.
- In your final_answer, include: total iterations completed, final MAE_f, total
  training frames, and which stopping condition was triggered.
"""

    print(f"Using project={args.project}")

    if not args.resume:
        setup(WORKSPACE_DIR)
    else:
        print(f"Resuming from existing workspace: {WORKSPACE_DIR}")

    # Optionally start monitor daemon
    monitor_proc = None
    if args.monitor:
        monitor_proc = subprocess.Popen(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "monitor.py"),
             "--workspace", str(WORKSPACE_DIR), "--interval", "30",
             "--agent-pattern", "test7_cips_distill",
             "--project", args.project],
            cwd=PROJECT_ROOT,
        )
        print(f"Monitor daemon started (pid={monitor_proc.pid})")

    try:
        main(task, workspace_dir=WORKSPACE_DIR, project=args.project, resume=args.resume)
    finally:
        if monitor_proc is not None:
            monitor_proc.send_signal(signal.SIGTERM)
            try:
                monitor_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                monitor_proc.kill()
            print("Monitor daemon stopped")

    # Parse steps and print summary
    steps = parse_steps(WORKSPACE_DIR / "steps.jsonl")
    total = len(steps)
    errors = sum(1 for s in steps if s.error)
    rag_calls = sum(1 for s in steps if s.code_action and "rag_search(" in s.code_action)
    print(f"Step counts: {total} total, {errors} errors, {rag_calls} RAG calls")

    # Analyze errors in the conversation
    analyze_agent_errors(WORKSPACE_DIR)
