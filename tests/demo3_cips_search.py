"""Test: CIPS heuristic search for domino switching in (E, T) space.

Agent autonomously explores electric field and temperature to find conditions
where domain wall propagation (sequential domino-like Cu switching) is clearly
observable in a 1x25x1 CuInP2S6 supercell.

Two versions:
  A (broad)  -- agent must devise its own domino metric
  B (guided) -- metric (slope of <|dt(d)|> vs d) is explicitly provided

CLI flags:
  --version A|B    : select task description (default: A)
  --workspace DIR  : workspace directory (default: workspace_search)
  --monitor        : launch health-check daemon
  --project NAME   : HPC project (default: perlmutter)
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

TASK_A = """\
In prior E-field MD simulations of monolayer CuInP2S6 (CIPS), we applied a
negative E-field along c to flip Cu atoms from "up" to "down". In some
conditions, all Cu flip nearly simultaneously ("random flipping" -- each site
nucleates independently). But in an elongated supercell, there should exist
conditions where flipping propagates sequentially along the chain as a domain
wall ("domino switching"), with neighboring sites flipping one after another.
The model Tc is ~230 K from prior MD simulations.

Your task: perform a heuristic search through (E-field, Temperature) space
to find conditions where domain wall propagation is clearly observable.

Procedure:
- Build a 1x25x1 supercell from './cips_monolayer.cif' (500 atoms, 50 Cu
  along b-axis).
- Born effective charges for efield_md: Cu = +0.765, In = P = S = -0.085.
- DeePMD model: /pscratch/sd/c/cz2014/cips_distill/frozen_model.pb
- Start from E_z = -0.01 eV/A/e, T = 200 K. Run efield_md, download the
  trajectory, and analyze the Cu switching behavior.
- Search domain: E_z in [0, -0.3] eV/A/e, T in [0, 250] K.
- Devise a quantitative metric that distinguishes domino (sequential)
  switching from random (independent) switching. The metric should reflect
  the prevalence of domain wall propagation in the overall flipping process
  under the applied electric field.
- Based on your analysis, choose the next 1-2 (E, T) points to explore.
  Submit them, analyze, and repeat. Each iteration: submit -> analyze ->
  decide next direction.

Final deliverables:
- A figure showing all explored (E, T) points colored by your metric.
- The single best (E, T) condition with supporting evidence (space-time
  heatmap or equivalent visualization).
- A written report summarizing your search path and conclusions.

Constraints:
- Compute budget per job: n_atoms * n_steps < 20,000,000 (debug queue, 27 min).
  500 * 19,000 = 9.5M -- fits budget.
- Submit at most 2 jobs per iteration (to keep the search interactive).
- Prefer perlmutter_debug queue.
- Simulations are expensive. Minimize total wall time where possible --
  reasonable time-saving measures should not affect analysis quality.
- Aggressive E-field or temperature may cause Cu desorption from the 2D
  layer. After each MD run, verify all Cu remain within 5 A of the host
  monolayer midplane. If not, reduce E or T and retry.

Report in final_answer the paths to your figures and report.
"""

TASK_B = """\
In prior E-field MD simulations of monolayer CuInP2S6 (CIPS), we applied a
negative E-field along c to flip Cu atoms from "up" to "down". In some
conditions, all Cu flip nearly simultaneously ("random flipping" -- each site
nucleates independently). But in an elongated supercell, there should exist
conditions where flipping propagates sequentially along the chain as a domain
wall ("domino switching"), with neighboring sites flipping one after another.
The model Tc is ~230 K from prior MD simulations.

Your task: perform a heuristic search through (E-field, Temperature) space
to find conditions where domain wall propagation is clearly observable.

Procedure:
- Build a 1x25x1 supercell from './cips_monolayer.cif' (500 atoms, 50 Cu
  along b-axis).
- Born effective charges for efield_md: Cu = +0.765, In = P = S = -0.085.
- DeePMD model: /pscratch/sd/c/cz2014/cips_distill/frozen_model.pb
- Start from E_z = -0.01 eV/A/e, T = 200 K. Run efield_md, download the
  trajectory, and analyze the Cu switching behavior.
- Search domain: E_z in [0, -0.3] eV/A/e, T in [0, 250] K.
- Use the following quantitative metric for domino detection:
  1. Sort Cu atoms by their b-fractional coordinate (position along the chain).
  2. For each Cu site i, compute the displacement dz(i, t) from the host
     (non-Cu) midplane along c. Smooth with a 0.5 ps Gaussian in time.
  3. Define first-flip time t_flip(i) as the first frame where smoothed
     dz crosses zero (positive-to-negative for negative E-field).
  4. Compute the mean absolute flip-time delay for site separation d:
       <|dt(d)|> = < |t_flip(i+d) - t_flip(i)| >
     averaged over all sites i with periodic boundary conditions (PBC):
     i.e., site (i+d) wraps around using modular arithmetic.
  5. Fit a line to <|dt(d)|> vs d for d = 1..10. The slope (ps/site)
     is the domino metric:
     - slope > 0.3 ps/site: clear domain wall propagation
     - slope ~ 0: random or simultaneous flipping (no domino)
- Based on the slope, choose the next 1-2 (E, T) points to explore.
  Submit them, analyze, and repeat. Each iteration: submit -> analyze ->
  decide next direction.

Final deliverables:
- A figure showing all explored (E, T) points colored by slope.
- The single best (E, T) condition with supporting evidence (space-time
  heatmap or equivalent visualization).
- A written report summarizing your search path and conclusions.

Constraints:
- Compute budget per job: n_atoms * n_steps < 20,000,000 (debug queue, 27 min).
  500 * 19,000 = 9.5M -- fits budget.
- Submit at most 2 jobs per iteration (to keep the search interactive).
- Prefer perlmutter_debug queue.
- Simulations are expensive. Minimize total wall time where possible --
  reasonable time-saving measures should not affect analysis quality.
- Aggressive E-field or temperature may cause Cu desorption from the 2D
  layer. After each MD run, verify all Cu remain within 5 A of the host
  monolayer midplane. If not, reduce E or T and retry.

Report in final_answer the paths to your figures and report.
"""

TASKS = {"A": TASK_A, "B": TASK_B}


def setup(workspace_dir: Path):
    """Clean workspace and copy input files."""
    if workspace_dir.exists():
        shutil.rmtree(workspace_dir)
    workspace_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(REF_DIR / "cips_monolayer.cif", workspace_dir / "cips_monolayer.cif")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CIPS heuristic search for domino switching"
    )
    parser.add_argument("--version", choices=["A", "B"], default="A",
                        help="Task version: A (broad) or B (guided) (default: A)")
    parser.add_argument("--monitor", action="store_true",
                        help="Launch health-check daemon alongside agent")
    parser.add_argument("--project", default="perlmutter",
                        help="HPC project name (default: perlmutter)")
    parser.add_argument("--workspace", default=None,
                        help="Workspace directory (default: workspace_search)")
    args = parser.parse_args()

    if args.workspace:
        WORKSPACE_DIR = Path(args.workspace).resolve()
    else:
        WORKSPACE_DIR = (PROJECT_ROOT / "workspace_search").resolve()

    from main import main
    from scripts.analyze_steps import parse_steps
    from tests.utils import analyze_agent_errors

    task = TASKS[args.version]

    print(f"Using version={args.version}, project={args.project}")
    setup(WORKSPACE_DIR)

    monitor_proc = None
    if args.monitor:
        monitor_proc = subprocess.Popen(
            [sys.executable, str(PROJECT_ROOT / "scripts" / "monitor.py"),
             "--workspace", str(WORKSPACE_DIR), "--interval", "30",
             "--agent-pattern", "test9_cips_search",
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
    rag_calls = sum(
        1 for s in steps if s.code_action and "rag_search(" in s.code_action
    )
    print(f"Step counts: {total} total, {errors} errors, {rag_calls} RAG calls")
    analyze_agent_errors(WORKSPACE_DIR)
