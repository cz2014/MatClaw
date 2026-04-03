"""Agent runner: sets up workspace, telemetry, pause/resume, and runs the agent."""

import os
import sys
from pathlib import Path

from core.agent import PauseController, _make_pause_callback, create_agent, start_keyboard_listener
from core.tools import set_pause_controller
from smolagents import ActionStep, PlanningStep

PROJECT_ROOT = Path(__file__).parent.parent


class TeeWriter:
    """Write to both a file and original stdout."""

    def __init__(self, file_path: Path, original):
        self.file = open(file_path, "w")
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

    This is the core run logic shared by tests/main.py and core/cli.py.
    Provider and experience file are configured via llm_config.yaml, not here.
    """
    if workspace_dir is None:
        workspace_dir = PROJECT_ROOT / "workspace"
    workspace_dir = workspace_dir.resolve()

    if config_dir is None:
        config_dir = workspace_dir / "config"

    # Telemetry
    from core.telemetry import setup_telemetry

    if setup_telemetry(project_name="matclaw"):
        print("Telemetry enabled - traces at http://localhost:6006")

    workspace_dir.mkdir(parents=True, exist_ok=True)

    # stdout tee
    output_log = workspace_dir / "output.log"
    sys.stdout = TeeWriter(output_log, sys.stdout)

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

    result = agent.run(task)
    print("-" * 50)
    print(f"Result: {result.output}")
