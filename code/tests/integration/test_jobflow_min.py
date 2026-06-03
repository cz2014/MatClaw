"""Integration test: submit a minimal VASP relaxation to an HPC cluster and check the result.

Cluster-agnostic (via the ``hpc_target`` fixture). Submits an ions-only (ISIF=2) MoS2 relax,
waits for completion, and asserts a scalar energy + a parseable relaxed structure come back.
This is the real, expensive end-to-end (a live VASP job); it skips when no HPC project is
configured or the reference structure is missing.

Tier: integration. Run with:

    uv run --project code --extra dev pytest code/tests -m integration --hpc-project anvil
"""

from __future__ import annotations

from pathlib import Path

import pytest

# code/tests/integration -> code/tests -> code -> repo root -> ref/MoS2.cif
REF_MOS2 = Path(__file__).resolve().parents[3] / "ref" / "MoS2.cif"


def test_jobflow_min_relax(hpc_target):
    if not REF_MOS2.exists():
        pytest.skip(f"reference structure missing: {REF_MOS2}")

    from atomate2.vasp.jobs.core import RelaxMaker
    from atomate2.vasp.powerups import update_user_incar_settings
    from jobflow import Flow
    from jobflow_remote import submit_flow
    from pymatgen.core import Structure

    from core.tools import wait_for_jobflow

    project, worker = hpc_target
    structure = Structure.from_file(str(REF_MOS2))

    job = RelaxMaker().make(structure)
    job = update_user_incar_settings(job, {"ISIF": 2})  # ions only, fixed cell
    submit_flow(Flow([job], name="mos2_relax_min"), worker=worker, project=project)

    out = wait_for_jobflow(project, job.uuid)
    energy = out["output"]["energy"]
    relaxed = Structure.from_dict(out["output"]["structure"])
    assert isinstance(energy, (int, float)), f"no scalar energy in result: {out!r}"
    assert len(relaxed) == len(structure), "relaxed structure lost atoms"
