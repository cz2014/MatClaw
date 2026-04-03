#!/usr/bin/env python3
"""Health-check daemon for MatClaw long-running workflows.

Runs periodic health checks alongside a long-running agent process:
  - Agent process alive (pgrep)
  - jobflow-remote runner alive (foreground or daemon mode)
  - MongoDB accessible (pymongo ping)
  - Agent error rate (parse recent steps)

On failure: sends macOS notification and logs to <workspace>/monitor.log.
State is persisted to <workspace>/monitor_state.json for external
monitoring tools to read.

Usage:
  python scripts/monitor.py --workspace workspace --interval 30
  python scripts/monitor.py --workspace workspace --interval 10 --project perlmutter
  python scripts/monitor.py --workspace workspace --interval 10 --agent-pattern "python main.py"
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.analyze_steps import parse_steps

# ---------------------------------------------------------------------------
# Health check functions
# ---------------------------------------------------------------------------

_MAX_HISTORY = 10  # keep last N results per check in state file
_MAX_INTERVAL = 1200  # 20 minutes cap for exponential backoff


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _result(name: str, status: str, message: str) -> dict:
    return {"name": name, "status": status, "message": message, "ts": _now_iso()}


def check_agent_alive(pattern: str) -> dict:
    """Check if the agent process is running.

    Uses ``ps ax`` piped through ``grep`` instead of ``pgrep -f`` because
    macOS ``pgrep`` cannot find ancestor processes -- when the daemon is
    launched as a subprocess of the agent, ``pgrep`` will never match the
    agent's PID.
    """
    try:
        # ps ax lists all processes; grep filters by pattern.
        # Two-grep idiom avoids matching the grep process itself.
        proc = subprocess.run(
            ["bash", "-c", f"ps ax -o pid,command | grep -F '{pattern}' | grep -v grep | grep -v 'agent-pattern'"],
            capture_output=True, text=True, timeout=5,
        )
        lines = [ln.strip() for ln in proc.stdout.strip().split("\n") if ln.strip()]
        if lines:
            pids = [ln.split()[0] for ln in lines]
            return _result("agent_alive", "OK", f"pid={','.join(pids)}")
        return _result("agent_alive", "FAIL", "process not found")
    except Exception as e:
        return _result("agent_alive", "FAIL", str(e))


def check_runner_alive(project: str = "anvil") -> dict:
    """Check if the jobflow-remote runner is alive (foreground or daemon).

    1. Check for foreground runner process (jf runner run)
    2. Fallback: jf runner status (daemon mode)
    """
    # Check foreground process: look for 'jf' commands containing 'runner run'
    # and the project name
    try:
        proc = subprocess.run(
            ["bash", "-c",
             f"ps ax -o pid,command | grep -F 'runner' | grep -F '{project}' | grep -v grep"],
            capture_output=True, text=True, timeout=5,
        )
        lines = [ln.strip() for ln in proc.stdout.strip().split("\n") if ln.strip()]
        # Look for 'runner run' (foreground mode only, not 'runner start' which is daemon)
        for ln in lines:
            if "runner run" in ln:
                pid = ln.split()[0]
                return _result(
                    "runner_alive", "OK",
                    f"runner alive (foreground, project={project}, pid={pid})",
                )
    except Exception:
        pass

    # Fallback: daemon mode via jf runner status
    try:
        env = {**os.environ, "JFREMOTE_PROJECT": project}
        proc = subprocess.run(
            ["jf", "runner", "status"],
            capture_output=True, text=True, timeout=15, env=env,
        )
        output = proc.stdout.strip().lower() + proc.stderr.strip().lower()
        if "running" in output and "not running" not in output:
            return _result(
                "runner_alive", "OK",
                f"runner alive (daemon, project={project})",
            )
    except FileNotFoundError:
        return _result("runner_alive", "FAIL", "jf command not found")
    except Exception:
        pass

    return _result("runner_alive", "FAIL", f"runner not detected (project={project})")


def check_mongodb() -> dict:
    """Ping MongoDB on localhost:27017."""
    try:
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

        client = MongoClient("127.0.0.1", 27017, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        client.close()
        return _result("mongodb", "OK", "ping successful")
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        return _result("mongodb", "FAIL", str(e))
    except ImportError:
        return _result("mongodb", "FAIL", "pymongo not installed")
    except Exception as e:
        return _result("mongodb", "FAIL", str(e))



def check_error_rate(workspace: Path) -> dict:
    """Check error rate over last 10 steps."""
    steps_file = workspace / "steps.jsonl"
    if not steps_file.exists():
        return _result("error_rate", "OK", "no steps.jsonl yet")

    steps = parse_steps(steps_file)
    if not steps:
        return _result("error_rate", "OK", "no steps parsed")

    recent = steps[-10:]
    errors = sum(1 for s in recent if s.error)
    rate = errors / len(recent)
    total = len(steps)

    if rate > 0.5:
        return _result(
            "error_rate", "FAIL",
            f"{errors}/{len(recent)} errors in last {len(recent)} steps "
            f"({rate:.0%}), {total} total steps. "
            f"Run: /analyze-agent {steps_file}",
        )
    return _result("error_rate", "OK", f"{errors}/{len(recent)} errors ({rate:.0%}), {total} total steps")


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------

def send_notification(title: str, message: str) -> None:
    """Send a macOS notification via osascript."""
    # Escape double quotes and backslashes for AppleScript
    safe_msg = message.replace("\\", "\\\\").replace('"', '\\"')
    safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
    script = f'display notification "{safe_msg}" with title "{safe_title}" sound name "Glass"'
    try:
        subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
    except Exception:
        pass  # notification is best-effort


# ---------------------------------------------------------------------------
# Daemon loop
# ---------------------------------------------------------------------------

def _run_all_checks(agent_pattern: str, workspace: Path, project: str = "anvil") -> list[dict]:
    """Run all health checks and return results."""
    return [
        check_agent_alive(agent_pattern),
        check_runner_alive(project),
        check_mongodb(),
        check_error_rate(workspace),
    ]


def _load_state(state_path: Path) -> dict:
    """Load previous state from JSON file."""
    if state_path.exists():
        return json.loads(state_path.read_text())
    return {}


def _save_state(state_path: Path, state: dict) -> None:
    """Save state to JSON file."""
    state_path.write_text(json.dumps(state, indent=2))


def _update_state(state: dict, results: list[dict]) -> dict:
    """Update state with new results, keeping history."""
    for r in results:
        name = r["name"]
        if name not in state:
            state[name] = {"latest": r, "history": []}
        else:
            state[name]["history"].append(state[name]["latest"])
            # Trim history
            state[name]["history"] = state[name]["history"][-_MAX_HISTORY:]
            state[name]["latest"] = r
    return state


def main_loop(workspace: Path, interval: int, agent_pattern: str, project: str = "anvil") -> None:
    """Main daemon loop."""
    workspace.mkdir(parents=True, exist_ok=True)

    log_path = workspace / "monitor.log"
    state_path = workspace / "monitor_state.json"

    # Set up logging
    logger = logging.getLogger("monitor")
    logger.setLevel(logging.INFO)
    # File handler
    fh = logging.FileHandler(log_path)
    fh.setFormatter(logging.Formatter("%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(fh)
    # Stdout handler
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("%(asctime)s %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(sh)

    # Startup log
    logger.info("monitor started: workspace=%s initial_interval=%ds agent_pattern='%s' project='%s'",
                workspace, interval, agent_pattern, project)
    logger.info("checks: agent_alive, runner_alive, mongodb, error_rate")
    logger.info("backoff: %ds -> %ds (2x, reset on new FAIL)", interval, _MAX_INTERVAL)

    # Load previous state
    state = _load_state(state_path)
    prev_statuses: dict[str, str] = {}
    for name, data in state.items():
        prev_statuses[name] = data.get("latest", {}).get("status", "OK")

    # Graceful exit
    running = True

    def _handle_signal(signum, frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    current_interval = interval  # exponential backoff state

    while running:
        results = _run_all_checks(agent_pattern, workspace, project)

        # Log and check for transitions
        has_new_fail = False
        for r in results:
            status_str = f"{r['name']}={r['status']}"
            prev = prev_statuses.get(r["name"], "OK")

            if r["status"] == "FAIL":
                if prev != "FAIL":
                    # OK -> FAIL transition: notify and reset backoff
                    logger.info("[ALERT] %s: %s", status_str, r["message"])
                    send_notification(
                        f"MLFF Monitor: {r['name']}",
                        r["message"],
                    )
                    has_new_fail = True
                else:
                    # FAIL -> FAIL: log but don't re-notify
                    logger.info("[still] %s: %s", status_str, r["message"])
            elif prev == "FAIL":
                # FAIL -> OK transition: log recovery
                logger.info("[RECOVERED] %s: %s", status_str, r["message"])
                send_notification(
                    f"MLFF Monitor: {r['name']} recovered",
                    r["message"],
                )
            else:
                logger.info("%s: %s", status_str, r["message"])

            prev_statuses[r["name"]] = r["status"]

        # Update and save state
        state = _update_state(state, results)
        _save_state(state_path, state)

        # Exponential backoff: reset on new failure, otherwise double up to cap
        if has_new_fail:
            current_interval = interval
            logger.info("backoff reset to %ds (new failure detected)", current_interval)
        else:
            next_interval = min(current_interval * 2, _MAX_INTERVAL)
            if next_interval != current_interval:
                current_interval = next_interval
                logger.info("backoff increased to %ds", current_interval)

        # Sleep in small increments so SIGTERM is responsive
        for _ in range(current_interval):
            if not running:
                break
            time.sleep(1)

    # Final state write
    _save_state(state_path, state)
    logger.info("monitor stopped")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Health-check daemon for MatClaw workflows",
    )
    parser.add_argument(
        "workspace", type=Path, nargs="?", default=None,
        help="Workspace directory (contains steps.jsonl, writes monitor.log + monitor_state.json)",
    )
    parser.add_argument(
        "--workspace", type=Path, dest="workspace_flag", default=None,
        help="Workspace directory (alias for positional argument)",
    )
    parser.add_argument(
        "--interval", type=int, default=60,
        help="Check interval in seconds (default: 60)",
    )
    parser.add_argument(
        "--agent-pattern", type=str, default="matclaw",
        help="Process pattern to check agent liveness (default: 'matclaw')",
    )
    parser.add_argument(
        "--project", type=str, default="anvil",
        help="jobflow-remote project name for runner/SSH checks (default: 'anvil')",
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Run all checks once, print JSON to stdout, and exit",
    )

    args = parser.parse_args()
    workspace = args.workspace or args.workspace_flag
    if workspace is None:
        parser.error("workspace is required (positional or --workspace)")

    if args.once:
        results = _run_all_checks(args.agent_pattern, workspace, args.project)
        print(json.dumps(results, indent=2))
    else:
        main_loop(workspace, args.interval, args.agent_pattern, args.project)


if __name__ == "__main__":
    main()
