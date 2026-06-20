"""Jobflow job definitions for remote execution.

These functions are reconstructed on the HPC worker by jobflow-remote via their module
path (e.g. ``remote_jobs.jobs.run_command``), so do not rename this package. They stay
deliberately generic: ``run_command`` is a single code-agnostic primitive -- it knows
nothing about any specific simulation code. All code-specific knowledge lives in the
agent-written decks and the reference corpora, never here.
"""

from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path

from jobflow import job


@job
def hello_hpc():
    """Trivial smoke test: returns the worker hostname to verify remote execution works."""
    import socket
    return {"hostname": socket.gethostname(), "message": "HPC connection works"}


# -- generic raw-command runner -----------------------------------------------

_HARNESS_FILES = {"run.sh"}  # written by the helper; excluded from produced_files


def _tail(path: Path, n_lines: int) -> str:
    """Last ``n_lines`` lines of a text file (empty string if missing)."""
    if not path.exists():
        return ""
    return "\n".join(path.read_text(errors="replace").splitlines()[-n_lines:])


def _collect_produced(output_globs: list[str] | None) -> list[dict]:
    """Files in the run dir to report back as ``{path, size}``, matched recursively.

    With ``output_globs`` given, each pattern is globbed recursively; a pattern that
    matches a directory (e.g. ``OUT.*`` or ``OUT.*/**``) expands to every file under it,
    so a whole output directory is captured regardless of how the deck-author wrote the
    glob. Otherwise every file in the run-dir tree is listed. Harness scratch (``run.sh``)
    is excluded. Paths are relative POSIX.
    """
    root = Path(".")
    if output_globs:
        matches: set[Path] = set()
        for pattern in output_globs:
            for p in root.glob(pattern):
                if p.is_file():
                    matches.add(p)
                elif p.is_dir():
                    matches.update(f for f in p.rglob("*") if f.is_file())
        files = sorted(matches)
    else:
        files = sorted(p for p in root.rglob("*") if p.is_file())
    produced = []
    for p in files:
        rel = p.as_posix()
        if rel in _HARNESS_FILES:
            continue
        produced.append({"path": rel, "size": p.stat().st_size})
    return produced


def _run_command_impl(
    input_files: dict[str, str],
    command: str,
    env: dict[str, str] | None = None,
    setup: str | None = None,
    output_globs: list[str] | None = None,
    stdout_tail_lines: int = 200,
    timeout_s: int | None = None,
) -> dict:
    """Run an arbitrary command in the current directory and return a small result dict.

    Generic and code-agnostic. The current working directory is the per-job run dir that
    jobflow-remote creates (the job body runs inside it), so input files are written with
    plain relative names and the command runs there.

    Behavior: stdout/stderr are redirected to files on disk and only a bounded tail is
    returned, so the result dict stays tiny regardless of run length; a nonzero exit or a
    timeout is returned as data (``returncode`` / ``timed_out``), never raised, so the
    caller can diagnose and recover; large outputs stay on disk and are listed (path +
    size) for separate retrieval. Only a failure to spawn the shell raises.

    Args:
        input_files: ``{filename: text_content}`` decks written into the run dir.
        command: the literal invocation, including any launcher prefix (e.g. ``srun abacus``).
        env: extra environment variables merged over ``os.environ`` for the subprocess.
        setup: shell lines run before ``command`` in the same shell (use ``export``;
            ``module load`` is stripped by jobflow-remote).
        output_globs: which files/dirs to report (recursive); defaults to the whole run dir.
        stdout_tail_lines: number of trailing lines of stdout/stderr to return.
        timeout_s: kill the command (whole process group) after this many seconds; ``None``
            waits indefinitely.

    Returns:
        ``{returncode, timed_out, stdout_tail, stderr_tail, produced_files, run_dir, command}``.
    """
    for name, content in input_files.items():
        Path(name).write_text(content)

    Path("run.sh").write_text((setup + "\n" if setup else "") + command)

    run_env = {**os.environ, **(env or {})}
    out_path, err_path = Path("stdout.log"), Path("stderr.log")
    timed_out = False
    with out_path.open("w") as out_f, err_path.open("w") as err_f:
        # start_new_session puts the child in its own process group so a timeout can kill
        # the whole tree (e.g. srun-launched ranks), not just the bash wrapper.
        proc = subprocess.Popen(
            ["bash", "run.sh"], stdout=out_f, stderr=err_f, env=run_env,
            start_new_session=True,
        )
        try:
            returncode = proc.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            timed_out = True
            returncode = None
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
            proc.wait()

    return {
        "returncode": returncode,
        "timed_out": timed_out,
        "stdout_tail": _tail(out_path, stdout_tail_lines),
        "stderr_tail": _tail(err_path, stdout_tail_lines),
        "produced_files": _collect_produced(output_globs),
        "run_dir": os.getcwd(),
        "command": command,
    }


@job
def run_command(
    input_files: dict[str, str],
    command: str,
    env: dict[str, str] | None = None,
    setup: str | None = None,
    output_globs: list[str] | None = None,
    stdout_tail_lines: int = 200,
    timeout_s: int | None = None,
) -> dict:
    """Generic raw-deck runner (jobflow ``@job`` wrapper around ``_run_command_impl``).

    Write hand-authored input files into the SLURM run dir, run an arbitrary executable,
    and return a small raw result dict. The thin wrapper exists so the implementation can
    be unit-tested locally without a cluster.
    """
    return _run_command_impl(
        input_files, command, env, setup, output_globs, stdout_tail_lines, timeout_s
    )
