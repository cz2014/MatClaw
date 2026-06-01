"""Shared entry point for the demo scripts (demo01, demo02).

Loads .env, builds the agent, and runs a task -- the common harness the
`tests/demos/demo*.py` scripts import. New standalone code should prefer
`core.runner.run_agent()` or the `matclaw` CLI directly.
"""

import os
import sys
from pathlib import Path

# repo root: code/tests/demos/_harness.py -> demos -> tests -> code -> repo root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# .env loader (test scripts rely on this for API keys)
_env_file = PROJECT_ROOT / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def main(task: str = None, workspace_dir: Path = None,
         config_dir: Path = None,
         project: str | None = None, instructions_extra: str | None = None,
         inject_images: bool = False, resume: bool = False):
    """Run the agent (backward-compatible entry point for old test scripts)."""
    from core.runner import run_agent
    run_agent(
        task=task,
        workspace_dir=workspace_dir,
        config_dir=config_dir or PROJECT_ROOT / "configs",
        project=project,
        instructions_extra=instructions_extra,
        inject_images=inject_images,
        resume=resume,
    )


if __name__ == "__main__":
    main()
