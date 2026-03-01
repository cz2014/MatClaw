"""Jobflow job definitions for remote execution."""

from __future__ import annotations

from typing import Any

from jobflow import job

from remote_jobs._deepmd import train_deepmd_impl


@job
def hello_anvil():
    """Trivial smoke test: returns hostname to verify remote execution works."""
    import socket
    return {"hostname": socket.gethostname(), "message": "Anvil connection works"}


@job
def train_deepmd(
    vasp_source: Any,
    *,
    seed: int = 2026,
    type_map: tuple[str, ...] = ("C",),
    numb_steps: int = 2000,
    net_size_preset: str = "balanced",
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Train a DeePMD model from a VASP OUTCAR.

    Reads VASP MD trajectory (all frames), prepares training/validation data (80/20 split),
    trains the model, and returns accuracy metrics.

    Args:
        vasp_source: TaskDoc output from MDMaker, or path to VASP run directory.
        seed: Random seed for shuffling and DP training.
        type_map: Element symbols in order of DeePMD types.
        numb_steps: Number of training steps.
        net_size_preset: Network architecture preset:
            - 'sanity_check': ONLY to verify pipeline runs without errors.
            - 'fast': Rapid iterations, Active Learning loops, or limited compute.
            - 'balanced': Default recommended choice for production-quality force fields.

            Mapping (descriptor_neuron, fitting_neuron):
            - sanity_check -> ([5, 10, 20], [20, 20, 20])
            - fast         -> ([10, 20, 40], [40, 40, 40])
            - balanced     -> ([20, 40, 80], [80, 80, 80])

            Note: Descriptor width impacts accuracy more than fitting width beyond 80.
        overrides: Optional dict to override any DeePMD input.json parameters.

    Returns:
        Dict with keys: mae_e, rmse_e, mae_f, rmse_f, model_path.
    """
    return train_deepmd_impl(
        vasp_source,
        seed=seed,
        type_map=type_map,
        numb_steps=numb_steps,
        net_size_preset=net_size_preset,
        overrides=overrides,
    )
