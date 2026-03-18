"""Entry point for MatClaw."""

import os
import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load .env file (simple loader, no dependency)
_env_file = PROJECT_ROOT / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())

from core import create_agent
from core.agent import PauseController, start_keyboard_listener, _make_pause_callback
from core.telemetry import setup_telemetry
from core.tools import set_pause_controller
from smolagents import ActionStep, PlanningStep


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


def main(task: str = None, workspace_dir: Path = None,
         project: str | None = None, instructions_extra: str | None = None,
         inject_images: bool = False, resume: bool = False):
    """Run the agent with a task."""
    if task is None:
        task = "Calculate the least common multiple (LCM) of 3 and 7"
    if workspace_dir is None:
        workspace_dir = PROJECT_ROOT / "workspace"
    workspace_dir = workspace_dir.resolve()

    # Initialize telemetry BEFORE creating agent (instrumentation must be first)
    if setup_telemetry(project_name="matclaw"):
        print("Telemetry enabled - traces at http://localhost:6006")

    # Ensure workspace exists and change to it
    workspace_dir.mkdir(parents=True, exist_ok=True)

    # Set up stdout tee (both screen and file)
    output_log = workspace_dir / "output.log"
    sys.stdout = TeeWriter(output_log, sys.stdout)

    print(f"Working directory: {os.getcwd()}")
    print(f"Output log: {output_log}")

    print("Creating agent...")
    agent = create_agent(
        config_dir=PROJECT_ROOT / "config",
        workspace_dir=workspace_dir,
        project=project,
        instructions_extra=instructions_extra,
        inject_images=inject_images,
        resume=resume,
    )
    # Set up pause/resume
    pause_controller = PauseController()
    set_pause_controller(pause_controller)

    # Wire pause controller to model for auto-pause on connection errors
    if hasattr(agent.model, 'set_pause_controller'):
        agent.model.set_pause_controller(pause_controller)

    # Register pause callback AFTER existing callbacks (JSONL logger writes step first)
    pause_cb = _make_pause_callback(pause_controller)
    agent.step_callbacks.register(ActionStep, pause_cb)
    agent.step_callbacks.register(PlanningStep, pause_cb)

    listener = start_keyboard_listener(pause_controller)
    if listener:
        print("Press 'p' to pause, 'r' to resume")

    print(f"Task: {task}")
    print("-" * 50)

    result = agent.run(task)

    print("-" * 50)
    print(f"Result: {result.output}")


if __name__ == "__main__":
    main()
