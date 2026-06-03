"""Jobflow job definitions for remote execution."""

from __future__ import annotations

from jobflow import job


@job
def hello_hpc():
    """Trivial smoke test: returns the worker hostname to verify remote execution works."""
    import socket
    return {"hostname": socket.gethostname(), "message": "HPC connection works"}
