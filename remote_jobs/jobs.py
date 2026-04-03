"""Jobflow job definitions for remote execution."""

from __future__ import annotations

from typing import Any

from jobflow import job

from remote_jobs._batch_eval import batch_static_eval_impl
from remote_jobs._deepmd import train_deepmd_impl


@job
def hello_anvil():
    """Trivial smoke test: returns hostname to verify remote execution works."""
    import socket
    return {"hostname": socket.gethostname(), "message": "Anvil connection works"}


@job
def train_deepmd(
    data_source: Any,
    *,
    seed: int = 2026,
    type_map: tuple[str, ...] = ("C",),
    numb_steps: int = 2000,
    net_size_preset: str = "balanced",
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Train a DeePMD model from MD output or pre-prepared training data.

    Prepares training/validation data (80/20 split), trains the model,
    and returns accuracy metrics.

    Args:
        data_source: Training data. Accepts:
            - VASP TaskDoc (from MDMaker) -- resolves OUTCAR from dir_name
            - ForcefieldTaskDoc (from ForceFieldMDMaker) -- extracts from ionic_steps
            - Path string to deepmd/npy directory on remote filesystem
            - Raw dpdata-compatible dict (keys: cells, coords, energies, forces)
            - List of any of the above (recursively loaded and merged)

            Chain with an MD job in a Flow for automatic data passing:
                md_job = MDMaker(...).make(struct)           # VASP
                md_job = ForceFieldMDMaker(...).make(struct)  # or MLFF
                dp_job = train_deepmd(md_job.output, type_map=["Cu","In","P","S"])
                flow = Flow([md_job, dp_job])
                submit_flow(flow, ...)
        seed: Random seed for shuffling and DP training.
        type_map: Element symbols in order of DeePMD types.
        numb_steps: Number of training steps.
        net_size_preset: Network architecture preset:
            - 'sanity_check': ONLY to verify pipeline runs without errors.
            - 'fast': Rapid iterations, Active Learning loops, or limited compute.
            - 'balanced': Default recommended choice for production-quality force fields.
        overrides: Optional dict to override any DeePMD input.json parameters.

    Returns:
        Dict with output structure:
            out["output"]["model_path"]      # Absolute path to frozen model (.pth)
            out["output"]["data_total_path"] # All input frames (deepmd/npy), pre-split
            out["output"]["data_train_path"] # 80% training split (deepmd/npy)
            out["output"]["data_valid_path"] # 20% validation split (deepmd/npy)
            out["output"]["n_total_frames"]  # Total frames before split
            out["output"]["n_train_frames"]  # Frames in training split (80%)
            out["output"]["n_valid_frames"]  # Frames in validation split (20%)
            out["output"]["mae_e"]           # Energy MAE (eV/atom) on validation set
            out["output"]["rmse_e"]          # Energy RMSE (eV/atom) on validation set
            out["output"]["mae_f"]           # Force MAE (eV/Angstrom) on validation set
            out["output"]["rmse_f"]          # Force RMSE (eV/Angstrom) on validation set

        For multi-iteration active learning: pass `data_total_path` (not
        `data_train_path`) as input to the next iteration to preserve all
        frames. `data_train_path` contains only the 80% training split and
        will cause cumulative data loss if reused as the sole data source.
    """
    return train_deepmd_impl(
        data_source,
        seed=seed,
        type_map=type_map,
        numb_steps=numb_steps,
        net_size_preset=net_size_preset,
        overrides=overrides,
    )


@job(data=["output"])
def batch_static_eval(
    structures: list[dict] | str,
    force_field_name: str = "DeepMD",
    calculator_kwargs: dict[str, Any] | None = None,
    type_map: tuple[str, ...] = ("C",),
) -> dict[str, Any]:
    """Run N static evaluations in one SLURM job.

    Args:
        structures: List of pymatgen Structure dicts (via struct.as_dict()),
            or a remote path to a trajectory file (.traj, .xyz, .extxyz).
        force_field_name: Calculator name, e.g. "DeepMD" (atomate2 convention).
        calculator_kwargs: Kwargs for calculator, e.g. {"model": "/path/model.pth"}.
        type_map: Element symbols in DeePMD type order.

    Returns:
        {"output": {"energies": [float, ...], "forces": [[[float]]], "n_frames": int}}
        output dict is offloaded to GridFS (no 16 MB limit).
    """
    return batch_static_eval_impl(
        structures, force_field_name, calculator_kwargs or {}, type_map
    )
