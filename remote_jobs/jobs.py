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
            - List of deepmd/npy path strings (merged automatically)

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
        Dict with keys: mae_e, rmse_e, mae_f, rmse_f, model_path.
    """
    return train_deepmd_impl(
        data_source,
        seed=seed,
        type_map=type_map,
        numb_steps=numb_steps,
        net_size_preset=net_size_preset,
        overrides=overrides,
    )
