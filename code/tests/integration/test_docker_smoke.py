"""Docker smoke test for the MatClaw container runtime (P3).

Tier: integration (auto-marked by directory) + an explicit `docker` marker, so it is excluded
from the default unit run. It also skips cleanly when no Docker daemon is reachable, so a machine
without Docker stays green. Run it explicitly with:

    uv run --project code --extra dev pytest code/tests -m docker

Asserts the container contract (docs/references/docker-runtime.md):
  - the image builds from docker/Dockerfile (reproducibly, from the committed uv.lock);
  - `matclaw --help` exits 0 inside the container (real entrypoint -> matclaw);
  - the smolagents PyPI dependency is gone (vendored into core._smol);
  - the vendored core, kernel runtime dependencies, and scientific stack import;
  - a real ipykernel starts, executes a probe, and shuts down cleanly (kernel_probe.py, piped
    in on stdin so no Python is embedded in the command line);
  - the process runs non-root;
  - a file written to /work/workspace lands on the host bind mount;
  - the container is disposable: a write outside the mounts does not survive a re-run.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

# code/tests/integration -> code/tests -> code -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
IMAGE = "matclaw:smoketest"
# The kernel probe is a real file piped in on stdin, never an argument -- see kernel_probe.py.
KERNEL_PROBE = Path(__file__).with_name("kernel_probe.py")


def _docker_available() -> bool:
    if shutil.which("docker") is None:
        return False
    return subprocess.run(["docker", "info"], capture_output=True).returncode == 0


pytestmark = [
    pytest.mark.docker,
    pytest.mark.skipif(not _docker_available(), reason="Docker daemon not available"),
]


@pytest.fixture(scope="module")
def image() -> str:
    """Build the image once for the module, then remove it."""
    subprocess.run(
        [
            "docker", "build", "-f", "docker/Dockerfile",
            # match the host UID so the container user can read/write the bind mounts
            "--build-arg", f"UID={os.getuid()}", "--build-arg", f"GID={os.getgid()}",
            "-t", IMAGE, ".",
        ],
        cwd=REPO_ROOT,
        check=True,
    )
    yield IMAGE
    subprocess.run(["docker", "image", "rm", "-f", IMAGE], capture_output=True)


def _raw(image: str, *cmd: str) -> subprocess.CompletedProcess:
    """Run a raw command inside the container (bypassing the matclaw entrypoint)."""
    return subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", "", image, *cmd],
        capture_output=True, text=True,
    )


def _raw_stdin(image: str, program: str, *cmd: str) -> subprocess.CompletedProcess:
    """Run a raw command inside the container, feeding `program` to it on stdin.

    Used with `python -` so a multi-line Python program never appears on the command line:
    nothing to quote, nothing to escape, and the exact same bytes can be run on the host.
    """
    return subprocess.run(
        ["docker", "run", "--rm", "-i", "--entrypoint", "", image, *cmd],
        input=program, capture_output=True, text=True,
    )


def _mounted_workspace() -> Path:
    """A throwaway workspace under the repo `workspace/` -- the canonical mount location.

    NOT pytest's tmp_path: that lives under /private/tmp, which the Colima/Lima VM does not mount
    writable. docker/run.sh mounts `$PWD/workspace` (under $HOME, VM-mounted writable), so this
    mirrors real usage.
    """
    base = REPO_ROOT / "workspace"
    base.mkdir(exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=".smoketest-", dir=base))


def test_help_exits_zero(image: str):
    r = subprocess.run(
        ["docker", "run", "--rm", image, "--help"], capture_output=True, text=True
    )
    assert r.returncode == 0, r.stderr
    assert "matclaw" in (r.stdout + r.stderr).lower()


def test_smolagents_dependency_is_gone(image: str):
    r = _raw(image, "python", "-c", "import smolagents")
    assert r.returncode != 0, "smolagents must not be importable (it is vendored into core._smol)"


def test_vendored_core_and_stack_import(image: str):
    r = _raw(
        image,
        "python",
        "-c",
        "import core._smol, jupyter_client, ipykernel, psutil, pymatgen, ase, atomate2; print('ok')",
    )
    assert r.returncode == 0, r.stderr
    assert "ok" in r.stdout


def test_ipykernel_starts_and_executes(image: str):
    """The probe itself is validated against the host interpreter by the daemon-free
    counterpart, tests/unit/test_docker_wrapper.py::test_kernel_probe_runs_on_host, so a
    failure here is about the image, not about the probe being malformed.
    """
    r = _raw_stdin(image, KERNEL_PROBE.read_text(), "python", "-")
    assert r.returncode == 0, r.stderr
    assert "ok" in r.stdout


def test_runs_non_root(image: str):
    r = _raw(image, "id", "-u")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() != "0", "container must run as a non-root user"


def test_workspace_write_visible_on_host(image: str):
    ws = _mounted_workspace()
    try:
        subprocess.run(
            [
                "docker", "run", "--rm", "--entrypoint", "",
                "-v", f"{ws}:/work/workspace", image,
                "bash", "-c", "echo hi > /work/workspace/out.txt",
            ],
            check=True, capture_output=True, text=True,
        )
        assert (ws / "out.txt").read_text().strip() == "hi"
    finally:
        shutil.rmtree(ws, ignore_errors=True)


def test_disposable_root_fs(image: str):
    """A write outside the mounts must not persist into a fresh container."""
    subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", "", image,
         "bash", "-c", "echo x > /opt/marker"],
        capture_output=True,
    )
    r = _raw(image, "bash", "-c", "test -f /opt/marker && echo present || echo absent")
    assert "absent" in r.stdout


# End-to-end agent loop with a real LLM, run INSIDE the container. tools=[] (no RAG/corpus), so it
# confirms the whole vendored stack (core._smol + litellm + model + executor) runs in the image
# against a live model, without HPC/RAG wiring. Provider + key env var are pytest options
# (--llm-provider / --llm-key-env; default gemini / GEMINI_API_KEY): only the var NAME is used here;
# the key VALUE stays in the environment and is forwarded to the container via `docker -e NAME`.
def _llm_snippet(provider: str) -> str:
    return (
        "import os; from pathlib import Path; os.chdir('/work/workspace'); "
        "from core.agent import create_agent; "
        f"a=create_agent(config_dir=Path('/work/configs'), workspace_dir=Path('/work/workspace'), "
        f"provider_name={provider!r}, tools=[]); "
        "r=a.run('Do not write analysis or extra code. In your very first step immediately call "
        "final_answer with exactly the single word: DONE', max_steps=3); "
        "print('RESULT=' + str(r.output)); assert 'DONE' in str(r.output).upper()"
    )


@pytest.mark.llm
def test_live_agent_run_in_container(image: str, request):
    """Real agent loop + real LLM inside the container (docker + llm tiers).

    Provider/key are configurable (default gemini / GEMINI_API_KEY); only the env var NAME is used,
    so no secret is ever passed on a command line:
        pytest -m "docker and llm"                                              # gemini / GEMINI_API_KEY
        pytest -m "docker and llm" --llm-provider=claude --llm-key-env=CLAUDE_API_KEY
    The cheap build/smoke set (no token spend) is:  -m "docker and not llm"
    """
    provider = request.config.getoption("--llm-provider")
    key_env = request.config.getoption("--llm-key-env")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key_env):
        pytest.skip(f"--llm-key-env must be a valid env var name, got {key_env!r}")
    if key_env not in os.environ:
        pytest.skip(f"{key_env} not set")
    ws = _mounted_workspace()
    try:
        r = subprocess.run(
            [
                "docker", "run", "--rm", "--entrypoint", "",
                "-e", key_env,  # forward the host value BY NAME (the value is never on the command line)
                "-v", f"{ws}:/work/workspace",
                "-v", f"{REPO_ROOT}/configs:/work/configs:ro",
                image, "python", "-c", _llm_snippet(provider),
            ],
            capture_output=True, text=True, timeout=600,
        )
        assert r.returncode == 0, (r.stdout[-2000:] + "\n" + r.stderr[-2000:])
        assert "RESULT=" in r.stdout and "DONE" in r.stdout.upper()
    finally:
        shutil.rmtree(ws, ignore_errors=True)
