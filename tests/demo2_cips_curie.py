"""Test: CIPS Curie temperature investigation — broad research task.

Gives the agent an open-ended research question (determine the Curie temperature
of CuInP2S6) without prescribing methodology. The agent must design the
investigation, run MD at multiple temperatures, compute an order parameter,
produce figures, and write a summary report.

Uses image injection so the agent can see its own matplotlib plots and iterate
on figure quality.
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
    parser = argparse.ArgumentParser(description="CIPS Curie temperature investigation")
    parser.add_argument("--monitor", action="store_true", help="Launch health-check daemon alongside agent")
    parser.add_argument("--project", default="perlmutter",
                        help="HPC project name (default: perlmutter)")
    args = parser.parse_args()

    WORKSPACE_DIR = (PROJECT_ROOT / "workspace_curie").resolve()

    from main import main
    from scripts.analyze_steps import parse_steps
    from tests.utils import analyze_agent_errors

    task = """\
I have a monolayer CuInP2S6 (CIPS) structure in './CuInP2S6.cif' (10 atoms/cell).
A pre-trained DeePMD model is deployed on Perlmutter at:
  /pscratch/sd/c/cz2014/cips_distill/frozen_model.pb
This model was trained on 16,432 DFT frames and provides accurate energy/force
predictions from 100K to 600K.

CIPS is a van der Waals ferroelectric. Your task: investigate the ferroelectric
phase transition and determine the Curie temperature (Tc) of this material using
MLFF molecular dynamics.

Requirements:
1. Run MD simulations across a range of temperatures spanning the phase transition.
2. Compute an appropriate order parameter that captures the ferroelectric-to-
   paraelectric transition (e.g., Cu sublattice displacement, polarization).
3. Before the full temperature sweep, verify convergence: run a pilot MD near the
   expected transition temperature and confirm the order parameter has equilibrated.
4. Produce a publication-quality figure showing the order parameter vs. temperature
   (the Tc curve). Save it to the workspace as a PNG file.
5. Write a summary report (markdown) with your findings: estimated Tc, order
   parameter definition, methodology, and key observations.
6. Report in final_answer: estimated Tc, the order parameter definition you chose,
   and how many MD frames were used at each temperature.

Constraints:
- Type map: Cu, In, P, S (matching the model).
- Use the pre-trained model (.pb) directly for all MD — no training needed.
- Compute budget per MD job: n_atoms * n_steps should be under 20,000,000 to fit
  the debug queue's 25-minute usable wall time (~0.069 ms/step/atom on A100). For a
  6x6x1 supercell (360 atoms), this allows up to ~55,000 steps (55 ps).
- You have matplotlib available for plotting.
- Use `traj_file` to save MD trajectories to disk, then download them with
  `remote_get` for local analysis. This avoids MongoDB size limits for large
  trajectories.
- Prefer the perlmutter_debug queue for faster scheduling (<10 min wait, 27 min walltime).
"""

    print(f"Using project={args.project}")

    setup(WORKSPACE_DIR)

    monitor_proc = None
    if args.monitor:
        monitor_proc = subprocess.Popen(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "monitor.py"),
             "--workspace", str(WORKSPACE_DIR), "--interval", "30",
             "--agent-pattern", "test8_cips_curie",
             "--project", args.project],
            cwd=PROJECT_ROOT,
        )
        print(f"Monitor daemon started (pid={monitor_proc.pid})")

    try:
        main(task, workspace_dir=WORKSPACE_DIR, project=args.project,
             inject_images=True)
    finally:
        if monitor_proc is not None:
            monitor_proc.send_signal(signal.SIGTERM)
            try:
                monitor_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                monitor_proc.kill()
            print("Monitor daemon stopped")

    steps = parse_steps(WORKSPACE_DIR / "steps.jsonl")
    total = len(steps)
    errors = sum(1 for s in steps if s.error)
    rag_calls = sum(1 for s in steps if s.code_action and "rag_search(" in s.code_action)
    print(f"Step counts: {total} total, {errors} errors, {rag_calls} RAG calls")

    analyze_agent_errors(WORKSPACE_DIR)
