"""Minimal jobflow-remote submission: submit MoS2 relaxation and wait for result."""

from __future__ import annotations

from pathlib import Path

from core.tools import wait_for_jobflow

# Constants
PROJECT = "anvil"
WORKER = "anvil_cpu"
TIMEOUT_S = 60 * 60  # 60 minutes
MOS2_CIF_PATH = Path(__file__).parent.parent.parent.parent / "ref" / "MoS2.cif"


def main():
    """Submit MoS2 relaxation and retrieve relaxed structure."""
    from jobflow import Flow
    from jobflow_remote import submit_flow
    from pymatgen.core import Structure
    from pymatgen.io.cif import CifWriter
    from atomate2.vasp.jobs.core import RelaxMaker
    from atomate2.vasp.powerups import update_user_incar_settings

    structure = Structure.from_file(str(MOS2_CIF_PATH))
    print(f"Structure: {structure.formula} ({len(structure)} atoms)")

    # Create relax job
    job = RelaxMaker().make(structure)
    # Force ions-only relaxation (fixed cell)
    job = update_user_incar_settings(job, {"ISIF": 2})

    flow = Flow([job], name="mos2_relax_min")
    submit_flow(flow, worker=WORKER, project=PROJECT)
    print(f"Submitted job: {job.uuid}")

    output = wait_for_jobflow(PROJECT, job.uuid, timeout_s=TIMEOUT_S)

    energy = output["output"]["energy"]
    relaxed = Structure.from_dict(output["output"]["structure"])

    # Save result
    out_path = Path(__file__).parent / "relaxed_min.cif"
    CifWriter(relaxed).write_file(str(out_path))
    print(f"Done! Energy: {energy} eV, saved to {out_path}")


if __name__ == "__main__":
    main()
