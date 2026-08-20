"""Agent runner: sets up workspace, pause/resume, and runs the agent."""

import logging
import os
import signal
import sys
import traceback
from datetime import datetime
from pathlib import Path

from core.agent import PauseController, _make_pause_callback, create_agent, start_keyboard_listener
from core.tools import set_pause_controller
from core._smol import ActionStep, PlanningStep

# repo root: code/core/runner.py -> core -> code -> repo root
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TeeWriter:
    """Write to both one shared log handle and an original Python stream."""

    def __init__(self, file_path: Path, original, *, handle=None, mode: str = "w"):
        self.file = handle if handle is not None else open(file_path, mode, encoding="utf-8")
        self._owns_file = handle is None
        self.original = original

    def write(self, data):
        self.file.write(data)
        self.file.flush()
        self.original.write(data)

    def flush(self):
        self.file.flush()
        self.original.flush()

    def isatty(self):
        """Return True if original stdout is a TTY (enables Rich colors)."""
        return self.original.isatty()

    def fileno(self):
        """Return file descriptor of original stdout (needed by some libraries)."""
        return self.original.fileno()

    def close(self):
        if self._owns_file and not self.file.closed:
            self.file.close()


def _setup_logging(stream):
    """Attach one run-scoped handler to MatClaw loggers and return prior state."""
    logger = logging.getLogger("core")
    previous = (logger.level, logger.propagate)
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger, handler, previous


def _sigterm_exit(signum, frame):
    """Turn SIGTERM into SystemExit so the teardown paths (finally, atexit) still run.

    Only the run entry point installs this: a plain `kill` of the harness would otherwise
    leave the agent's kernel processes and their children orphaned.
    """
    raise SystemExit(128 + signum)


def run_agent(
    task: str | None = None,
    workspace_dir: Path | None = None,
    config_dir: Path | None = None,
    project: str | None = None,
    instructions_extra: str | None = None,
    inject_images: bool = False,
    resume: bool = False,
    enable_step_logging: bool = False,
):
    """Set up workspace, create agent, and run the task.

    This is the core run logic shared by code/tests/examples/_harness.py and core/cli.py.
    Provider and experience file are configured via llm_config.yaml, not here.
    """
    if workspace_dir is None:
        workspace_dir = PROJECT_ROOT / "workspace"
    workspace_dir = workspace_dir.resolve()

    if config_dir is None:
        config_dir = workspace_dir / "config"

    workspace_dir.mkdir(parents=True, exist_ok=True)

    output_log = workspace_dir / "output.log"
    previous_stdout, previous_stderr = sys.stdout, sys.stderr
    stdout_tee = TeeWriter(
        output_log, previous_stdout, mode="a" if resume else "w"
    )
    stderr_tee = TeeWriter(output_log, previous_stderr, handle=stdout_tee.file)
    sys.stdout, sys.stderr = stdout_tee, stderr_tee
    core_logger = log_handler = logger_state = None
    previous_sigterm = None
    agent = None
    try:
        core_logger, log_handler, logger_state = _setup_logging(sys.stdout)
        previous_sigterm = signal.signal(signal.SIGTERM, _sigterm_exit)
        print(
            "\n===== matclaw "
            f"{'resume' if resume else 'run'} start "
            f"{datetime.now().isoformat(timespec='seconds')} (pid {os.getpid()}) ====="
        )
        print(f"Working directory: {os.getcwd()}")
        print(f"Config directory: {config_dir}")
        print(f"Output log: {output_log}")
        print("Creating agent...")
        agent = create_agent(
            config_dir=config_dir,
            workspace_dir=workspace_dir,
            project=project,
            instructions_extra=instructions_extra,
            inject_images=inject_images,
            resume=resume,
            enable_step_logging=enable_step_logging,
        )

        # Pause/resume
        pause_controller = PauseController()
        set_pause_controller(pause_controller)
        agent.python_executor.tool_server.state.pause_controller = pause_controller
        if hasattr(agent.model, "set_pause_controller"):
            agent.model.set_pause_controller(pause_controller)
        pause_cb = _make_pause_callback(pause_controller)
        agent.step_callbacks.register(ActionStep, pause_cb)
        agent.step_callbacks.register(PlanningStep, pause_cb)
        listener = start_keyboard_listener(pause_controller)
        if listener:
            print("Press 'p' to pause, 'r' to resume")

        if task:
            print(f"Task: {task[:200]}{'...' if len(task) > 200 else ''}")
        print("-" * 50)

        # reset=False on resume: create_agent(resume=True) reconstructed agent.memory
        # from history; agent.run() defaults to reset=True, which would wipe it and
        # restart the task fresh. Pass reset=not resume so a resumed run continues.
        result = agent.run(task, reset=not resume)
        print("-" * 50)
        print(f"Result: {result.output}")
    except Exception:
        # The process may be running in a disposable container.  Persist the fatal
        # traceback before restoring stderr so output.log remains a complete record.
        traceback.print_exc(file=sys.stderr)
        raise
    finally:
        try:
            if agent is not None:
                try:
                    agent.cleanup()
                finally:
                    set_pause_controller(None)
            else:
                set_pause_controller(None)
        finally:
            try:
                if previous_sigterm is not None:
                    signal.signal(signal.SIGTERM, previous_sigterm)
            finally:
                if core_logger is not None and log_handler is not None and logger_state is not None:
                    core_logger.removeHandler(log_handler)
                    log_handler.close()
                    core_logger.setLevel(logger_state[0])
                    core_logger.propagate = logger_state[1]
                sys.stdout, sys.stderr = previous_stdout, previous_stderr
                stdout_tee.close()
