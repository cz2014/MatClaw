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


def train_deepmd_impl(
    vasp_source: Any,
    *,
    seed: int = 2026,
    type_map: tuple[str, ...] = ("C",),
    numb_steps: int = 2000,
    net_size_preset: str = "balanced",
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Train a DeePMD model from a VASP OUTCAR.

    This is the core implementation without any decorators.

    Args:
        vasp_source: TaskDoc output from MDMaker, or path to VASP run directory.
        seed: Random seed for shuffling and DP training.
        type_map: Element symbols in order of DeePMD types.
        numb_steps: Number of training steps.
        net_size_preset: Network architecture preset. One of:
            - 'sanity_check': ONLY to verify pipeline runs without errors.
            - 'fast': Rapid iterations, Active Learning loops, or limited compute.
            - 'balanced': Default recommended choice for production-quality force fields.
        overrides: Optional dict to deep-merge into the DeePMD input.json config.

    Returns:
        Dict with keys:
            mae_e: Energy MAE (eV/atom) or None
            rmse_e: Energy RMSE (eV/atom) or None
            mae_f: Force MAE (eV/A) or None
            rmse_f: Force RMSE (eV/A) or None
            model_path: Absolute path to frozen deepmd_model.pb model
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

    # Resolve and copy OUTCAR
    outcar_src = _resolve_outcar_path(vasp_source)
    run_dir = Path.cwd() / "deepmd_run"
    run_dir.mkdir(parents=True, exist_ok=True)
    outcar_local = run_dir / "OUTCAR"
    _maybe_decompress_to(outcar_src, outcar_local)

    # Load all frames with dpdata
    dsys = dpdata.LabeledSystem(str(outcar_local))

    n_total = len(dsys)
    if n_total < 2:
        raise ValueError(f"Need at least 2 frames for train/valid split; got {n_total}")

    # Shuffle + split (80/20)
    rng = np.random.default_rng(seed)
    order = rng.permutation(n_total)
    dsys = dsys[order]

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
        subprocess.run(["dp", "train", "input.json"], check=True)

        model_path = run_dir / f"{model_name}.pb"
        subprocess.run(["dp", "freeze", "-o", str(model_path)], check=True)

        # Test on validation set
        cp = subprocess.run(
            ["dp", "test", "-m", str(model_path), "-s", "data_valid", "-n", "0"],
            check=True,
            text=True,
            capture_output=True,
        )

    metrics = _parse_dp_test_metrics(cp.stderr)

    return {
        "mae_e": metrics.get("mae_e"),
        "rmse_e": metrics.get("rmse_e"),
        "mae_f": metrics.get("mae_f"),
        "rmse_f": metrics.get("rmse_f"),
        "model_path": str(model_path.resolve()),
    }
