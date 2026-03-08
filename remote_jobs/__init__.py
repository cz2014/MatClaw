"""Remote jobs package for jobflow-remote execution.

Applies monkey-patches that must run on the remote worker before any
atomate2 force field jobs execute.
"""

from remote_jobs._patches import patch_ase_relaxer_stale_arrays
from remote_jobs.jobs import train_deepmd

patch_ase_relaxer_stale_arrays()

__all__ = ["train_deepmd"]
