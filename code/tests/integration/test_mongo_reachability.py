"""Container -> host MongoDB reachability: the bind-regression guard.

Reproduces the failure where a mongod bound to 127.0.0.1 ONLY is invisible to the
containerized agent. On Linux a container reaches the host via host.docker.internal,
which resolves to the docker bridge gateway (e.g. 172.17.0.1), NOT loopback. When
mongod is loopback-only, every run silently hangs waiting for Mongo -- and nothing
in the unit tier or the host-side integration scripts can see it, because those
talk to Mongo from the host (127.0.0.1), never from inside a container.

This test runs a container with the EXACT networking docker/run.sh uses
(--add-host host.docker.internal:host-gateway) and asserts a pymongo ping succeeds.

Tier: integration (auto-marked by directory) + docker. Excluded from the default
unit gate. Run with:

    uv run --project code --extra dev pytest code/tests -m docker

It SKIPS cleanly when the integration environment is absent (no Docker daemon, no
matclaw:dev image, or no host mongod on :27017). It FAILS only when mongod IS up
but a container cannot reach it -- exactly the regression we want to catch. The
fix is docker/host_up.sh, which binds mongod to loopback + the bridge gateway.
"""

from __future__ import annotations

import shutil
import socket
import subprocess

import pytest

IMAGE = "matclaw:dev"
PORT = 27017

pytestmark = pytest.mark.docker


def _docker_ok() -> bool:
    return (
        shutil.which("docker") is not None
        and subprocess.run(["docker", "info"], capture_output=True).returncode == 0
    )


def _image_present() -> bool:
    return subprocess.run(
        ["docker", "image", "inspect", IMAGE], capture_output=True
    ).returncode == 0


def _bridge_gateway() -> str:
    r = subprocess.run(
        ["docker", "network", "inspect", "bridge",
         "--format", "{{range .IPAM.Config}}{{.Gateway}}{{end}}"],
        capture_output=True, text=True,
    )
    return r.stdout.strip()


def _host_mongod_up(gateway: str) -> bool:
    """mongod is part of the integration env only if something serves :27017 on the host."""
    for host in filter(None, ("127.0.0.1", gateway)):
        try:
            with socket.create_connection((host, PORT), timeout=2):
                return True
        except OSError:
            continue
    return False


@pytest.fixture(scope="module")
def integration_env() -> str:
    if not _docker_ok():
        pytest.skip("Docker daemon not available")
    if not _image_present():
        pytest.skip(f"image {IMAGE} not built")
    gateway = _bridge_gateway()
    if not gateway:
        pytest.skip("no docker bridge gateway")
    if not _host_mongod_up(gateway):
        pytest.skip("no host mongod on :27017 (integration env absent)")
    return gateway


def test_container_reaches_host_mongo(integration_env: str):
    """A matclaw container must reach the host mongod via host.docker.internal.

    If mongod is bound to 127.0.0.1 only, this FAILS -- the regression guard.
    Run docker/host_up.sh to rebind mongod to the bridge gateway.
    """
    ping = (
        "from pymongo import MongoClient; "
        f"MongoClient('host.docker.internal', {PORT}, serverSelectionTimeoutMS=4000)"
        ".admin.command('ping'); print('PING_OK')"
    )
    r = subprocess.run(
        ["docker", "run", "--rm",
         "--add-host", "host.docker.internal:host-gateway",
         "--entrypoint", "", IMAGE, "python", "-c", ping],
        capture_output=True, text=True, timeout=120,
    )
    assert "PING_OK" in r.stdout, (
        f"container could not reach host mongod via host.docker.internal:{PORT} -- "
        "mongod is likely bound to 127.0.0.1 only; run docker/host_up.sh to rebind.\n"
        f"stdout={r.stdout!r}\nstderr={r.stderr!r}"
    )
