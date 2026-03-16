"""Core DeePMD training implementation (no decorators)."""

from __future__ import annotations

import gzip
import json
import os
import re
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Any


# Network architecture presets for DeePMD training
NET_SIZE_PRESETS = {
    # Pipeline validation / very fast iteration
    "sanity_check": {
        "descriptor_neuron": (5, 10, 20),
        "fitting_neuron": (20, 20, 20),
    },
    # Fast training (active-learning loops, frequent retrains)
    "fast": {
        "descriptor_neuron": (10, 20, 40),
        "fitting_neuron": (40, 40, 40),
    },
    # Recommended default (good accuracy, reasonable speed)
    "balanced": {
        "descriptor_neuron": (20, 40, 80),
        "fitting_neuron": (80, 80, 80),
    },
}


@contextmanager
def _cd(path: Path):
    """Context manager to temporarily change working directory."""
    old = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def _resolve_outcar_path(vasp_source: Any) -> Path:
    """Resolve OUTCAR path from TaskDoc output.

    Handles atomate2 dir_name format: "hostname:/path/to/vasp_run"
    """
    # Extract dir_name from TaskDoc
    if hasattr(vasp_source, "dir_name"):
        vasp_dir = vasp_source.dir_name
    elif isinstance(vasp_source, dict) and "dir_name" in vasp_source:
        vasp_dir = vasp_source["dir_name"]
    else:
        vasp_dir = str(vasp_source)

    # Strip hostname prefix (e.g., "nid001001:/path" -> "/path")
    if ":" in vasp_dir:
        vasp_dir = vasp_dir.split(":", 1)[1]

    outcar = Path(vasp_dir) / "OUTCAR"
    if outcar.exists():
        return outcar
    if (gz := Path(f"{outcar}.gz")).exists():
        return gz

    raise FileNotFoundError(f"Could not find OUTCAR at: {outcar}")


def _maybe_decompress_to(outcar_like: Path, dest_outcar: Path) -> Path:
    """Copy OUTCAR (or OUTCAR.gz) to dest_outcar, decompressing if needed."""
    dest_outcar.parent.mkdir(parents=True, exist_ok=True)
    if outcar_like.suffix == ".gz":
        with gzip.open(outcar_like, "rb") as f_in, open(dest_outcar, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    else:
        shutil.copy2(outcar_like, dest_outcar)
    return dest_outcar


def _parse_dp_test_metrics(output: str) -> dict[str, float | None]:
    """Parse dp test stderr for energy/force MAE/RMSE.

    DeePMD outputs metrics to stderr. Expects format like:
        Energy MAE/Natoms  : 8.300762e-03 eV
        Force  MAE         : 5.839027e-01 eV/Å
    """

    def grab(pattern: str) -> float | None:
        m = re.search(rf"{pattern}\s*:\s*([0-9eE.+\-]+)", output)
        return float(m.group(1)) if m else None

    return {
        "mae_e": grab(r"Energy MAE/Natoms"),  # eV/atom
        "rmse_e": grab(r"Energy RMSE/Natoms"),  # eV/atom
        "mae_f": grab(r"Force\s+MAE"),  # eV/Å
        "rmse_f": grab(r"Force\s+RMSE"),  # eV/Å
    }


def _deep_merge(base: dict, overrides: dict) -> dict:
    """Recursively merge overrides into base dict (in-place)."""
    for key, value in overrides.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def _get_step_field(step: Any, *keys: str) -> Any:
    """Get a field from an ionic step (dict or pydantic model)."""
    for key in keys:
        val = step.get(key) if isinstance(step, dict) else getattr(step, key, None)
        if val is not None:
            return val
    return None


def _to_structure(val: Any) -> Any:
    """Convert a structure value to pymatgen Structure.

    Handles: pymatgen Structure (passthrough), dict (from_dict), monty-serialized.
    """
    from pymatgen.core import Structure

    if isinstance(val, Structure):
        return val
    if isinstance(val, dict):
        return Structure.from_dict(val)
    # Pydantic model with .as_dict() or similar
    if hasattr(val, "as_dict"):
        return Structure.from_dict(val.as_dict())
    raise TypeError(f"Cannot convert {type(val).__name__} to Structure")


def _extract_from_ionic_steps(
    ionic_steps: list, type_map: tuple[str, ...]
) -> Any:
    """Convert ForceFieldMDMaker ionic_steps to dpdata LabeledSystem.

    Each ionic step has: structure (pymatgen Structure or dict), energy (float),
    forces (list of [fx, fy, fz]).
    Units: eV for energy, eV/A for forces (matches deepmd/npy convention).
    Handles both plain dicts and pydantic IonicStep models.
    """
    import dpdata
    import numpy as np

    first_step = ionic_steps[0]
    first_struct = _to_structure(
        _get_step_field(first_step, "structure", "mol_or_struct")
    )

    species_list = [str(s) for s in first_struct.species]
    atom_types = np.array([list(type_map).index(s) for s in species_list])
    atom_numbs = [species_list.count(elem) for elem in type_map]
    n_atoms = len(species_list)

    coords_all, cells_all, energies, forces_all = [], [], [], []
    for step in ionic_steps:
        struct = _to_structure(
            _get_step_field(step, "structure", "mol_or_struct")
        )
        coords_all.append(struct.cart_coords)
        cells_all.append(struct.lattice.matrix)
        energies.append(_get_step_field(step, "energy"))
        forces_all.append(np.array(_get_step_field(step, "forces")))

    n_frames = len(energies)
    ls = dpdata.LabeledSystem()
    ls.data = {
        "atom_names": list(type_map),
        "atom_numbs": atom_numbs,
        "atom_types": atom_types,
        "cells": np.array(cells_all).reshape(n_frames, 3, 3),
        "coords": np.array(coords_all).reshape(n_frames, n_atoms, 3),
        "energies": np.array(energies),
        "forces": np.array(forces_all).reshape(n_frames, n_atoms, 3),
        "orig": np.zeros(3),
        "nopbc": False,
    }
    return ls


def _harmonize_optional_fields(systems: list) -> list:
    """Strip optional frame-dependent fields that aren't present in ALL systems.

    dpdata's LabeledSystem.append() requires that optional fields like 'virials'
    are either present in both systems or absent from both. When merging data from
    heterogeneous sources (e.g., deepmd/npy with virials + raw dict without),
    this function drops fields that would cause merge failures.

    Only frame-dependent optional fields are affected (virials, atom_pref,
    real_atom_types). Core fields (cells, coords, energies, forces) are never
    touched.
    """
    if len(systems) <= 1:
        return systems

    # Frame-dependent optional fields that dpdata checks during append
    _OPTIONAL_FRAME_FIELDS = ("virials", "atom_pref", "real_atom_types")

    # Find fields present in ALL systems
    common = set(_OPTIONAL_FRAME_FIELDS)
    for sys in systems:
        present = {f for f in _OPTIONAL_FRAME_FIELDS if f in sys.data}
        common &= present

    # Strip fields not in the common set
    for sys in systems:
        for field in _OPTIONAL_FRAME_FIELDS:
            if field in sys.data and field not in common:
                del sys.data[field]

    return systems


def _load_labeled_data(data_source: Any, type_map: tuple[str, ...], run_dir: Path) -> Any:
    """Load training data from various sources.

    Dispatches on input type:
    1. deepmd/npy directory path (has type_map.raw + set.*/) -> load directly
    1.1. Trajectory file path (.traj, .extxyz) -> load via dpdata format readers
    2. List of any supported type -> recursively load each + merge
    1.5. Raw dpdata-compatible dict (has "cells" key) -> load directly
    3. ForcefieldTaskDocument dict/model (has output.ionic_steps) -> extract inline data
    4. VASP TaskDoc / OUTCAR path -> existing behavior (resolve OUTCAR, parse)
    """
    import dpdata

    # Case 1: deepmd/npy directory
    if isinstance(data_source, str):
        p = Path(data_source)
        if p.is_dir() and (p / "type_map.raw").exists():
            return dpdata.LabeledSystem(str(p), fmt="deepmd/npy")

        # Case 1.1: trajectory file (.traj or .extxyz) on remote filesystem
        _TRAJ_FMTS = {".traj": "ase/traj", ".extxyz": "extxyz"}
        fmt = _TRAJ_FMTS.get(p.suffix.lower())
        if fmt is not None and p.is_file():
            return dpdata.LabeledSystem(str(p), fmt=fmt)

    # Case 2: list of data sources (recursive dispatch -- supports mixed types)
    if isinstance(data_source, (list, tuple)) and len(data_source) > 0:
        systems = []
        for item in data_source:
            sub = _load_labeled_data(item, type_map, run_dir)
            systems.append(sub)
        systems = _harmonize_optional_fields(systems)
        merged = systems[0]
        for s in systems[1:]:
            merged += s
        return merged

    # Case 1.5: raw dpdata-compatible dict (cells, coords, energies, forces)
    # MongoDB serializes numpy arrays to lists, so convert back before loading.
    if isinstance(data_source, dict) and "cells" in data_source:
        import numpy as np

        data = dict(data_source)
        for key in ("cells", "coords", "energies", "forces", "atom_types", "orig"):
            if key in data and not isinstance(data[key], np.ndarray):
                data[key] = np.array(data[key])

        # Auto-populate derivable fields that dpdata requires but the agent
        # may omit (atom_numbs, orig, nopbc).
        if "atom_numbs" not in data and "atom_types" in data and "atom_names" in data:
            data["atom_numbs"] = [
                int(np.sum(data["atom_types"] == i))
                for i in range(len(data["atom_names"]))
            ]
        if "orig" not in data:
            data["orig"] = np.zeros(3)
        if "nopbc" not in data:
            data["nopbc"] = False

        ls = dpdata.LabeledSystem()
        ls.data = data
        return ls

    # Case 3: ForcefieldTaskDocument (from ForceFieldMDMaker)
    # Handles both plain dicts (JSON-deserialized) and pydantic models (monty-deserialized)
    if isinstance(data_source, dict):
        output = data_source.get("output")
    elif hasattr(data_source, "output"):
        output = data_source.output
    else:
        output = None

    if output is not None:
        ionic_steps = (
            output.get("ionic_steps") if isinstance(output, dict)
            else getattr(output, "ionic_steps", None)
        )
        # ionic_steps can be: list (normal), Trajectory object, or None (blob unresolved)
        if ionic_steps is not None:
            # Convert non-list iterables (e.g. Trajectory) to list
            if not isinstance(ionic_steps, list):
                try:
                    ionic_steps = list(ionic_steps)
                except (TypeError, ValueError):
                    ionic_steps = None
            if ionic_steps:
                return _extract_from_ionic_steps(ionic_steps, type_map)

    # Case 4: VASP OUTCAR -- only if path actually exists on this machine
    if isinstance(data_source, str) and not Path(data_source).exists():
        raise FileNotFoundError(
            f"Path '{data_source}' not found on the remote HPC cluster. "
            "Note: train_deepmd runs on the remote HPC, not on your local machine. "
            "Local paths (e.g., /Users/...) do not exist here. "
            "Accepted data_source formats: "
            "(1) Chain with MD job in a Flow: dp_job = train_deepmd(md_job.output, ...); "
            "(2) Pass a raw dict with keys: cells, coords, energies, forces, atom_types, atom_names; "
            "(3) Path to a deepmd/npy directory on the remote HPC (e.g., /scratch/...); "
            "(4) Path to a trajectory file (.traj, .extxyz) on the remote HPC."
        )
    if not isinstance(data_source, str):
        raise TypeError(
            f"_load_labeled_data: unsupported data_source type "
            f"{type(data_source).__name__}. If passing ForceFieldMDMaker output, "
            "ensure ionic_step_data=('energy', 'forces', 'mol_or_struct') is set "
            "on the ForceFieldMDMaker (default is None, producing empty ionic_steps)."
        )
    outcar_src = _resolve_outcar_path(data_source)
    outcar_local = run_dir / "OUTCAR"
    _maybe_decompress_to(outcar_src, outcar_local)
    return dpdata.LabeledSystem(str(outcar_local))


def train_deepmd_impl(
    data_source: Any,
    *,
    seed: int = 2026,
    type_map: tuple[str, ...] = ("C",),
    numb_steps: int = 2000,
    net_size_preset: str = "balanced",
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Train a DeePMD model from MD output or pre-prepared training data.

    This is the core implementation without any decorators.

    Args:
        data_source: Training data. Accepts:
            - VASP TaskDoc (from MDMaker) -- resolves OUTCAR from dir_name
            - ForcefieldTaskDoc (from ForceFieldMDMaker) -- extracts from ionic_steps
            - Path string to deepmd/npy directory on remote filesystem
            - Path string to trajectory file (.traj, .extxyz) on remote filesystem
            - Raw dpdata-compatible dict with cells, coords, energies, forces keys
            - List of any of the above (recursively loaded and merged)
        seed: Random seed for shuffling and DP training.
        type_map: Element symbols in order of DeePMD types.
        numb_steps: Number of training steps.
        net_size_preset: Network architecture preset. One of:
            - 'sanity_check': ONLY to verify pipeline runs without errors.
            - 'fast': Rapid iterations, Active Learning loops, or limited compute.
            - 'balanced': Default recommended choice for production-quality force fields.
        overrides: Optional dict to deep-merge into the DeePMD input.json config.

    Returns:
        Dict with atomate2-compatible structure:
            {
                "output": {
                    "model_path": str,           # Absolute path to frozen model (.pth)
                    "data_total_path": str,      # All input frames (deepmd/npy), pre-split
                    "data_train_path": str,      # 80% training split (deepmd/npy)
                    "data_valid_path": str,      # 20% validation split (deepmd/npy)
                    "n_total_frames": int,       # Total frames before split
                    "n_train_frames": int,       # Frames in training split (80%)
                    "n_valid_frames": int,       # Frames in validation split (20%)
                    "mae_e": float or None,      # Energy MAE (eV/atom)
                    "rmse_e": float or None,     # Energy RMSE (eV/atom)
                    "mae_f": float or None,      # Force MAE (eV/Angstrom)
                    "rmse_f": float or None,     # Force RMSE (eV/Angstrom)
                }
            }

        For multi-iteration active learning: pass `data_total_path` (not
        `data_train_path`) as input to the next iteration to preserve all
        frames. `data_train_path` contains only the 80% training split and
        will cause cumulative data loss if reused as the sole data source.
    """
    import dpdata
    import numpy as np

    # Validate preset
    if net_size_preset not in NET_SIZE_PRESETS:
        raise ValueError(
            f"Unknown preset: {net_size_preset}. Choose from {list(NET_SIZE_PRESETS)}"
        )
    preset = NET_SIZE_PRESETS[net_size_preset]
    descriptor_neuron = preset["descriptor_neuron"]
    fitting_neuron = preset["fitting_neuron"]

    # Training defaults
    train_frac = 0.8  # 80/20 train/validation split
    model_name = "deepmd_model"

    # Descriptor defaults
    rcut = 6.0       # Cutoff radius (Angstroms)
    rcut_smth = 0.5  # Smoothing distance
    sel = 80         # Max neighbors per atom

    # Load training data (dispatches on source type)
    run_dir = Path.cwd() / "deepmd_run"
    run_dir.mkdir(parents=True, exist_ok=True)
    dsys = _load_labeled_data(data_source, type_map, run_dir)

    n_total = len(dsys)
    if n_total < 2:
        raise ValueError(f"Need at least 2 frames for train/valid split; got {n_total}")

    # Shuffle + split (80/20)
    rng = np.random.default_rng(seed)
    order = rng.permutation(n_total)
    dsys = dsys[order]

    # Save full dataset (pre-split) for multi-iteration accumulation
    data_total = run_dir / "data_total"
    dsys.to("deepmd/npy", str(data_total), set_size=min(2000, n_total))

    n_train = int(round(train_frac * n_total))
    n_train = max(1, min(n_total - 1, n_train))

    train_sys = dsys[:n_train]
    valid_sys = dsys[n_train:]

    # Compute set_size based on training data
    set_size = min(2000, n_train)

    data_train = run_dir / "data_train"
    data_valid = run_dir / "data_valid"
    train_sys.to("deepmd/npy", str(data_train), set_size=set_size)
    valid_sys.to("deepmd/npy", str(data_valid), set_size=set_size)

    # Build input.json
    input_config = {
        "model": {
            "type_map": list(type_map),
            "descriptor": {
                "type": "se_e2_a",
                "rcut": rcut,
                "rcut_smth": rcut_smth,
                "sel": [int(sel)] * len(type_map),
                "neuron": list(descriptor_neuron),
                "axis_neuron": 16,
                "resnet_dt": False,
                "seed": seed,
            },
            "fitting_net": {
                "neuron": list(fitting_neuron),
                "resnet_dt": False,
                "seed": seed,
            },
        },
        "learning_rate": {
            "type": "exp",
            "start_lr": 1e-3,
            "decay_steps": max(1000, numb_steps // 2),
            "stop_lr": 3.51e-8,
        },
        "loss": {
            "type": "ener",
            "start_pref_e": 0.02,
            "limit_pref_e": 1.0,
            "start_pref_f": 1000.0,
            "limit_pref_f": 1.0,
            "start_pref_v": 0.0,
            "limit_pref_v": 0.0,
        },
        "training": {
            "training_data": {"systems": ["data_train"], "batch_size": "auto"},
            "validation_data": {"systems": ["data_valid"], "batch_size": "auto"},
            "numb_steps": numb_steps,
            "seed": seed,
            "disp_file": "lcurve.out",
            "disp_freq": 100,
            "save_freq": 1000,
        },
    }

    # Apply user overrides (deep merge)
    if overrides:
        _deep_merge(input_config, overrides)

    input_json = run_dir / "input.json"
    input_json.write_text(json.dumps(input_config, indent=2))

    # Run dp train / freeze / test
    with _cd(run_dir):
        subprocess.run(["dp", "--pt", "train", "input.json"], check=True)

        model_path = run_dir / f"{model_name}.pth"
        subprocess.run(["dp", "--pt", "freeze", "-o", str(model_path)], check=True)

        # Test on validation set
        cp = subprocess.run(
            ["dp", "--pt", "test", "-m", str(model_path), "-s", "data_valid", "-n", "0"],
            check=True,
            text=True,
            capture_output=True,
        )

    metrics = _parse_dp_test_metrics(cp.stderr)

    # Return in atomate2-compatible structure: {"output": {...}}
    return {
        "output": {
            "mae_e": metrics.get("mae_e"),
            "rmse_e": metrics.get("rmse_e"),
            "mae_f": metrics.get("mae_f"),
            "rmse_f": metrics.get("rmse_f"),
            "model_path": str(model_path.resolve()),
            "data_total_path": str(data_total.resolve()),
            "data_train_path": str(data_train.resolve()),
            "data_valid_path": str(data_valid.resolve()),
            "n_total_frames": n_total,
            "n_train_frames": n_train,
            "n_valid_frames": n_total - n_train,
        }
    }
