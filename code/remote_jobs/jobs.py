"""Jobflow job definitions for remote execution."""

from __future__ import annotations

from jobflow import job


@job
def hello_anvil():
    """Trivial smoke test: returns hostname to verify remote execution works."""
    import socket
    return {"hostname": socket.gethostname(), "message": "Anvil connection works"}
