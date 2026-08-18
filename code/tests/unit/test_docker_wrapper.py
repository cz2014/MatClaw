"""Unit tests for the P3 Docker artifacts -- daemon-free.

These exercise the *logic* of the run wrapper + entrypoint (flag/mount assembly, the Mongo-host
rewrite) and lock in the security-relevant decisions, WITHOUT a Docker daemon. The daemon-requiring
end-to-end checks live in tests/integration/test_docker_smoke.py (the `docker` tier).

Strategy: stub `docker` on PATH (records the `run` argv) for the wrapper; run the entrypoint with
overridden staging paths (MATCLAW_JFREMOTE_SRC) + a stub `matclaw`, and assert the rewrite.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# code/tests/unit -> code/tests -> code -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
DOCKER_DIR = REPO_ROOT / "docker"
RUN_SH = DOCKER_DIR / "run.sh"
ENTRYPOINT = DOCKER_DIR / "entrypoint.sh"
KERNEL_PROBE = REPO_ROOT / "code" / "tests" / "integration" / "kernel_probe.py"

pytestmark = pytest.mark.skipif(shutil.which("bash") is None, reason="bash required")


def _write_exec(path: Path, body: str) -> None:
    path.write_text(body)
    path.chmod(0o755)


# --------------------------------------------------------------------------- static guards


def test_dockerignore_excludes_secrets():
    text = (REPO_ROOT / ".dockerignore").read_text()
    assert ".env" in text, ".env must be excluded from the build context (no secrets in the image)"


def test_pyproject_registers_docker_marker():
    text = (REPO_ROOT / "code" / "pyproject.toml").read_text()
    assert "docker:" in text, "the `docker` pytest marker must be registered"


def test_run_sh_does_not_use_read_only_or_privileged():
    """Locked decision: disposable container, NOT a frozen root FS; never privileged."""
    text = RUN_SH.read_text()
    assert "--read-only" not in text, "P3 deliberately does not use --read-only (see plan 6.4/6.5)"
    assert "--privileged" not in text
    assert "--network host" not in text


# --------------------------------------------------------------------------- run.sh argv assembly


@pytest.fixture
def stub_docker(tmp_path):
    """A fake `docker` on PATH that records the `run` argv and skips the build."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    argfile = tmp_path / "run_argv.txt"
    _write_exec(
        bindir / "docker",
        "#!/usr/bin/env bash\n"
        'if [ "$1" = "image" ]; then exit 0; fi\n'          # image inspect -> exists, skip build
        f'if [ "$1" = "run" ]; then shift; printf "%s\\n" "$@" > "{argfile}"; exit 0; fi\n'
        "exit 0\n",
    )
    env = dict(os.environ, PATH=f"{bindir}:{os.environ['PATH']}")
    return env, argfile


def test_run_sh_assembles_hardening_flags_and_mounts(stub_docker):
    env, argfile = stub_docker
    r = subprocess.run(
        ["bash", str(RUN_SH), "run", "--task", "t"],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    argv = argfile.read_text().splitlines()

    # hardening flags (locked)
    for flag in ("--rm", "-it", "--init", "--cap-drop", "--security-opt", "--user",
                 "--memory", "--cpus", "--pids-limit"):
        assert flag in argv, f"missing {flag} in: {argv}"
    assert "ALL" in argv                      # --cap-drop ALL
    assert "no-new-privileges" in argv        # --security-opt no-new-privileges
    assert "--read-only" not in argv          # disposable, not frozen

    # mounts: corpus + ssh + jfremote ro; workspace + config rw. config is rw so the
    # agent can append to experience.md, which lives INSIDE the config dir (no separate
    # experience.md mount).
    assert any("/work/corpus:ro" in a for a in argv)
    assert any("/opt/ssh-host:ro" in a for a in argv)
    assert any("/opt/jfremote-host:ro" in a for a in argv)
    assert any(a.endswith("/work/workspace") for a in argv)
    # config mounted rw (NOT :ro), and no nested experience.md mount
    assert any(a.endswith("/work/configs") and ":" in a for a in argv), "config dir must be mounted"
    assert not any("/work/configs:ro" in a for a in argv), "config is now rw (experience.md writable)"
    assert not any("experience.md" in a for a in argv), \
        "experience.md lives in the rw config dir, not a separate mount"

    # run defaults --config to the mounted repo configs
    assert "--config" in argv and "/work/configs" in argv

    # Mongo host alias passed in
    assert any("MATCLAW_MONGO_HOST=" in a for a in argv)

    # Config-driven secret forwarding (no hardcoded key name): every env var the configs reference
    # via ${VAR} that is also set in the host shell must be forwarded by name. Derived from configs/,
    # mirroring run.sh's scan -- so this adapts to whatever keys the project's config declares.
    referenced = set()
    for _p in (REPO_ROOT / "configs").rglob("*.yaml"):
        for _line in _p.read_text().splitlines():
            if not _line.lstrip().startswith("#"):
                referenced.update(re.findall(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", _line))
    for _v in sorted(referenced & set(os.environ)):
        assert _v in argv, f"config-referenced env var {_v} (set in the shell) must be forwarded with -e"

    # platform-conditional host-gateway
    if os.uname().sysname == "Linux":
        assert any("host.docker.internal:host-gateway" in a for a in argv)


def test_run_sh_respects_explicit_config(stub_docker):
    env, argfile = stub_docker
    subprocess.run(
        ["bash", str(RUN_SH), "run", "--config", "/custom/cfg", "--task", "t"],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=True,
    )
    argv = argfile.read_text().splitlines()
    assert "/custom/cfg" in argv
    assert "/work/configs" not in argv, "must not inject the default when --config is given"


# --------------------------------------------------------------------------- entrypoint rewrite


def test_entrypoint_rewrites_mongo_host(tmp_path):
    """The entrypoint copies the ro-staged jfremote config and rewrites 127.0.0.1 -> host alias."""
    home = tmp_path / "home"
    home.mkdir()
    jfsrc = tmp_path / "jfsrc"
    jfsrc.mkdir()
    # queue store on loopback (rewritten) + an SSH host (must be preserved). The hostname is
    # invented fixture data, not a real cluster.
    (jfsrc / "project.yaml").write_text(
        "queue:\n  store:\n    host: 127.0.0.1\n    port: 27017\n"
        "worker:\n  host: login.example.com\n"
    )
    bindir = tmp_path / "bin"
    bindir.mkdir()
    _write_exec(bindir / "matclaw", "#!/usr/bin/env bash\nexit 0\n")  # stub for `exec matclaw`

    env = dict(
        os.environ,
        HOME=str(home),
        PATH=f"{bindir}:{os.environ['PATH']}",
        MATCLAW_JFREMOTE_SRC=str(jfsrc),
        MATCLAW_SSH_SRC=str(tmp_path / "nonexistent"),   # skip the SSH/ssh-keyscan block
    )
    # leave MATCLAW_MONGO_HOST unset -> default host.docker.internal
    env.pop("MATCLAW_MONGO_HOST", None)

    r = subprocess.run(["bash", str(ENTRYPOINT)], env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr

    out = (home / ".jfremote" / "project.yaml").read_text()
    assert "host.docker.internal" in out
    assert "127.0.0.1" not in out
    assert "login.example.com" in out, "SSH host must be preserved (only the Mongo loopback rewritten)"


# --------------------------------------------------------------------------- kernel probe


def test_kernel_probe_runs_on_host():
    """Validate the ipykernel probe itself, daemon-free.

    tests/integration/test_docker_smoke.py pipes kernel_probe.py into the container on stdin
    (`python -`). Whether the *image* satisfies it is only knowable after a build, but whether
    the probe is a correct program is knowable here: run the identical bytes through the local
    interpreter the same way (stdin, not an argument), against the uv env's own ipykernel.
    """
    r = subprocess.run(
        [sys.executable, "-"],
        input=KERNEL_PROBE.read_text(), capture_output=True, text=True, timeout=180,
    )
    assert r.returncode == 0, r.stderr
    assert "ok" in r.stdout
