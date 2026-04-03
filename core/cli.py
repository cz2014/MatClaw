"""MatClaw CLI entry point."""

import argparse
import os
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(prog="matclaw", description="MatClaw agent")
    sub = parser.add_subparsers(dest="command")

    run_p = sub.add_parser("run", help="Run the agent")
    run_p.add_argument("--task", type=Path, help="Path to task .txt file")
    run_p.add_argument("--workspace", type=Path, default=None,
                       help="Workspace directory (default: current dir)")
    run_p.add_argument("--config", type=Path, default=None,
                       help="Config directory (default: <workspace>/config)")
    run_p.add_argument("--setup", type=Path,
                       help="Directory of files to copy into workspace before starting")
    run_p.add_argument("--project", type=str, help="HPC project name (anvil, perlmutter)")
    run_p.add_argument("--monitor", action="store_true",
                       help="(Deprecated) Use Claude Code monitor-agent skill instead")
    run_p.add_argument("--resume", action="store_true",
                       help="Resume a crashed run from existing workspace")
    run_p.add_argument("--inject-images", action="store_true",
                       help="Auto-inject workspace images into agent observations")

    args = parser.parse_args()

    if args.command == "run":
        _run(args, run_p)
    else:
        parser.print_help()


def _run(args, parser):
    # Load .env from package root (API keys)
    _env_file = Path(__file__).parent.parent / ".env"
    if _env_file.exists():
        for line in _env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

    # Workspace defaults to cwd
    workspace_dir = (args.workspace or Path.cwd()).resolve()

    # Config defaults to <workspace>/config
    config_dir = (args.config or workspace_dir / "config").resolve()

    # Read task from file (default: task.txt in workspace)
    task_file = args.task or workspace_dir / "task.txt"
    if task_file.exists():
        task = task_file.read_text().strip()
    elif args.resume:
        task = None
    else:
        parser.error(f"No task file found at {task_file}. Use --task or create task.txt in the workspace.")

    # Copy setup files if provided
    if args.setup:
        import shutil

        if not args.setup.is_dir():
            print(f"ERROR: --setup path is not a directory: {args.setup}", file=sys.stderr)
            sys.exit(1)
        for f in args.setup.iterdir():
            if f.is_file():
                shutil.copy2(f, workspace_dir / f.name)

    if args.monitor:
        raise NotImplementedError(
            "--monitor is deprecated. Use the Claude Code monitor-agent skill instead."
        )

    # Delegate to run_agent (extracted from main.py)
    from core.runner import run_agent

    run_agent(
        task=task,
        workspace_dir=workspace_dir,
        config_dir=config_dir,
        project=args.project,
        inject_images=args.inject_images,
        resume=args.resume,
    )
