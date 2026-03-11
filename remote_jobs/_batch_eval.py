"""Batch static evaluation for active distillation."""

from __future__ import annotations

from typing import Any


def batch_static_eval_impl(
    structures: list[dict] | str,
    force_field_name: str,
    calculator_kwargs: dict[str, Any],
    type_map: tuple[str, ...],
) -> dict[str, Any]:
    """Run N static evaluations in one call. Returns energies + forces.

    Args:
        structures: One of:
            - list[dict]: pymatgen Structure dicts (monty-serialized, inline)
            - str: remote path to a trajectory file (.traj, .xyz, .extxyz)
              containing structures. The file is read directly by ASE on the
              remote cluster, bypassing MongoDB entirely.
        force_field_name: Calculator name, e.g. "DeepMD" (matches atomate2).
        calculator_kwargs: Kwargs for calculator. For DeePMD: {"model": "/path/to/model.pth"}.
        type_map: Element symbols in DeePMD type order.

    Returns:
        {"output": {"energies": [...], "forces": [...], "n_frames": int}}
        energies: list of float (eV)
        forces: list of list-of-list (eV/A), shape [N][n_atoms][3]
    """
    if force_field_name == "DeepMD":
        from deepmd.calculator import DP
        calc = DP(**(calculator_kwargs or {}))
    else:
        raise ValueError(f"Unsupported force_field_name: {force_field_name}")

    if isinstance(structures, str):
        from ase.io import read
        atoms_list = read(structures, index=":")
    else:
        from pymatgen.core import Structure
        from pymatgen.io.ase import AseAtomsAdaptor
        adaptor = AseAtomsAdaptor()
        atoms_list = []
        for s in structures:
            if isinstance(s, Structure):
                atoms_list.append(adaptor.get_atoms(s))
            else:
                atoms_list.append(adaptor.get_atoms(Structure.from_dict(s)))


    energies = []
    forces = []
    for atoms in atoms_list:
        atoms.calc = calc
        energies.append(float(atoms.get_potential_energy()))
        forces.append(atoms.get_forces().tolist())

    return {
        "output": {
            "energies": energies,
            "forces": forces,
            "n_frames": len(atoms_list),
        }
    }
