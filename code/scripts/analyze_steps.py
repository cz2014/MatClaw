"""Analyze agent run logs from history.jsonl.

history.jsonl is written by MatClaw's history-writer step callback during execution: one JSON
record per message (role, content; assistant steps also carry phase, summary, timing, tokens,
error, code_action, images). It is the single run log this tool reads.

This tool provides 6 views into the run data:

  --summary     Quick overview: step counts, duration, tokens, errors, final answer
  --timeline    One line per step with number, duration, tokens, and summary
  --errors      Error steps with the code that caused the error and recovery status
  --step N      Full detail for step N: plan, code, summary, observations, tokens
  --tokens      Per-step and cumulative token usage with context growth rate

The structured output format ({plan, code, summary}) from Phase 0b means
each step has a one-line summary field, making --timeline especially useful
for understanding what the agent did at a glance.

Examples:
  python scripts/analyze_steps.py workspace/history.jsonl --summary
  python scripts/analyze_steps.py workspace/history.jsonl --timeline
  python scripts/analyze_steps.py workspace/history.jsonl --errors
  python scripts/analyze_steps.py workspace/history.jsonl --step 3
  python scripts/analyze_steps.py workspace/history.jsonl --tokens

Typical workflow after an agent run:
  1. --summary to check if the run succeeded and how many steps/tokens it used
  2. --timeline to scan what happened at each step
  3. --errors if there were failures, to see what went wrong
  4. --step N to drill into a specific step's full context
  5. --tokens to check for context growth issues (relevant for long runs)

Parser API (for programmatic use):
  from scripts.analyze_steps import parse, StepRecord
  steps = parse(Path("workspace/history.jsonl"))
  total_tokens = sum(s.input_tokens or 0 for s in steps)
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StepRecord:
    """Parsed agent step from history.jsonl (the messages sharing one step number)."""

    step_number: int | None
    duration: float | None
    input_tokens: int | None
    output_tokens: int | None
    code_action: str | None
    observations: str | None
    phase: str | None    # from structured output
    plan: str | None     # from structured output
    summary: str | None  # from structured output
    error: str | None
    is_final_answer: bool


def parse(path: Path) -> list[StepRecord]:
    """Parse a history.jsonl run log into StepRecords (one per agent step)."""
    by_step: dict[int, list[dict]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            by_step.setdefault(rec.get("step", 0), []).append(rec)

    records: list[StepRecord] = []
    for step_num in sorted(by_step):
        if step_num == 0:  # bootstrap (system/first-user) messages
            continue
        phase = plan = summary = code_action = observations = error = None
        timing_start = timing_end = token_usage = None
        is_final = False

        for msg in by_step[step_num]:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "assistant":
                phase = msg.get("phase")
                summary = msg.get("summary")
                try:
                    parsed = json.loads(content)
                    plan = parsed.get("plan")
                    code_action = parsed.get("code")
                except (json.JSONDecodeError, TypeError):
                    pass
                if msg.get("code_action") is not None:
                    code_action = msg["code_action"]
                if msg.get("timing"):
                    timing_start = msg["timing"].get("start_time")
                    timing_end = msg["timing"].get("end_time")
                if msg.get("error"):
                    error = str(msg["error"])
                if msg.get("token_usage"):
                    token_usage = msg["token_usage"]
                if msg.get("is_final_answer"):
                    is_final = True
            elif role in ("tool-response", "tool"):
                observations = content

        duration = (timing_end - timing_start) if (timing_start is not None and timing_end is not None) else None
        input_tokens = token_usage.get("input_tokens") if token_usage else None
        output_tokens = token_usage.get("output_tokens") if token_usage else None

        records.append(
            StepRecord(
                step_number=step_num,
                duration=duration,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                code_action=code_action,
                observations=observations,
                phase=phase,
                plan=plan,
                summary=summary,
                error=error,
                is_final_answer=is_final,
            )
        )
    return records


# ---------------------------------------------------------------------------
# CLI subcommands
# ---------------------------------------------------------------------------


def cmd_summary(steps: list[StepRecord]) -> None:
    """Print quick overview of the run."""
    if not steps:
        print("No steps found.")
        return

    total = len(steps)
    errors = sum(1 for s in steps if s.error)
    total_in = sum(s.input_tokens or 0 for s in steps)
    total_out = sum(s.output_tokens or 0 for s in steps)
    total_dur = sum(s.duration or 0.0 for s in steps)

    # Final answer
    final_steps = [s for s in steps if s.is_final_answer]
    final_val = None
    if final_steps:
        last = final_steps[-1]
        obs = last.observations or ""
        # Extract value after "Final answer: "
        for line in obs.splitlines():
            if line.startswith("Final answer:"):
                final_val = line[len("Final answer:"):].strip()
                break

    print(f"Steps:       {total} ({errors} errors)")
    print(f"Duration:    {total_dur:.1f}s")
    print(f"Tokens:      {total_in:,} in / {total_out:,} out / {total_in + total_out:,} total")
    if final_val is not None:
        print(f"Final answer: {final_val[:200]}")
    elif final_steps:
        print("Final answer: (returned, value not in observations)")
    else:
        print("Final answer: (none - agent did not call final_answer)")


def cmd_timeline(steps: list[StepRecord]) -> None:
    """Print one line per step."""
    if not steps:
        print("No steps found.")
        return

    # Header
    print(f"{'Step':>4}  {'Dur(s)':>6}  {'InTok':>6}  {'OutTok':>6}  Summary")
    print("-" * 80)

    for s in steps:
        sn = s.step_number if s.step_number is not None else "?"
        dur = f"{s.duration:.1f}" if s.duration is not None else "-"
        intok = str(s.input_tokens) if s.input_tokens is not None else "-"
        outtok = str(s.output_tokens) if s.output_tokens is not None else "-"

        # Summary: prefer structured output summary, fall back to code_action
        phase_str = f"[{s.phase}] " if s.phase else ""
        if s.summary:
            desc = phase_str + s.summary
            desc = desc[:70]
        elif s.code_action:
            desc = s.code_action.replace("\n", " ")[:60]
        else:
            desc = "(no output)"

        # Markers
        if s.error:
            desc = "[ERROR] " + desc[:62]
        if s.is_final_answer:
            desc = "[FINAL] " + desc[:62]

        print(f"{sn:>4}  {dur:>6}  {intok:>6}  {outtok:>6}  {desc}")


def cmd_errors(steps: list[StepRecord]) -> None:
    """Print error steps with context."""
    error_steps = [(i, s) for i, s in enumerate(steps) if s.error]

    if not error_steps:
        print("No errors found.")
        return

    print(f"Found {len(error_steps)} error(s):\n")

    for idx, (i, s) in enumerate(error_steps):
        recovered = i + 1 < len(steps) and not steps[i + 1].error
        status = "recovered" if recovered else "not recovered"

        print(f"--- Error {idx + 1} (step {s.step_number}, {status}) ---")
        # Error message (first 500 chars)
        err_text = str(s.error)[:500]
        print(f"Error: {err_text}")

        if s.code_action:
            print(f"\nCode:\n{s.code_action[:500]}")
        print()


def cmd_step(steps: list[StepRecord], step_num: int) -> None:
    """Print full detail for a specific step."""
    matches = [s for s in steps if s.step_number == step_num]
    if not matches:
        print(f"Step {step_num} not found. Available: {sorted(set(s.step_number for s in steps if s.step_number is not None))}")
        return

    s = matches[-1]  # last match if duplicates (multi-run files)

    print(f"=== Step {s.step_number} ===")
    dur = f"{s.duration:.1f}s" if s.duration is not None else "unknown"
    print(f"Duration:  {dur}")
    intok = s.input_tokens if s.input_tokens is not None else "?"
    outtok = s.output_tokens if s.output_tokens is not None else "?"
    print(f"Tokens:    {intok} in / {outtok} out")
    print()

    # Phase
    if s.phase:
        print(f"--- Phase ---")
        print(s.phase)
        print()

    # Plan
    print("--- Plan ---")
    print(s.plan if s.plan else "(none)")
    print()

    # Code
    print("--- Code ---")
    print(s.code_action if s.code_action else "(none)")
    print()

    # Summary
    print("--- Summary ---")
    print(s.summary if s.summary else "(none)")
    print()

    # Observations
    print("--- Observations ---")
    if s.observations:
        # Limit to 2000 chars to avoid flooding terminal
        obs = s.observations
        if len(obs) > 2000:
            print(obs[:2000])
            print(f"... ({len(obs) - 2000} more chars)")
        else:
            print(obs)
    else:
        print("(none)")
    print()

    # Error
    print("--- Error ---")
    print(s.error if s.error else "(none)")


def cmd_tokens(steps: list[StepRecord]) -> None:
    """Print per-step and cumulative token usage."""
    if not steps:
        print("No steps found.")
        return

    cum_in = 0
    cum_out = 0
    prev_in = 0

    print(f"{'Step':>4}  {'InTok':>7}  {'OutTok':>7}  {'CumIn':>8}  {'CumOut':>8}  {'Delta':>7}")
    print("-" * 55)

    for s in steps:
        in_tok = s.input_tokens or 0
        out_tok = s.output_tokens or 0
        cum_in += in_tok
        cum_out += out_tok
        delta = in_tok - prev_in if prev_in > 0 else 0
        prev_in = in_tok

        sn = s.step_number if s.step_number is not None else "?"
        print(f"{sn:>4}  {in_tok:>7}  {out_tok:>7}  {cum_in:>8}  {cum_out:>8}  {delta:>+7}")

    print("-" * 55)
    print(f"{'':>4}  {'':>7}  {'':>7}  {cum_in:>8}  {cum_out:>8}  Total: {cum_in + cum_out:,}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Analyze agent run logs from history.jsonl",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "path", type=Path, nargs="?", default=None,
        help="Path to history.jsonl. If omitted, uses workspace/history.jsonl.",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--summary", action="store_true", help="Quick overview (default)")
    group.add_argument("--timeline", action="store_true", help="One line per step")
    group.add_argument("--errors", action="store_true", help="Error steps with context")
    group.add_argument("--step", type=int, metavar="N", help="Full detail for step N")
    group.add_argument("--tokens", action="store_true", help="Per-step and cumulative token usage")

    args = parser.parse_args()

    # Resolve input path: explicit > workspace/history.jsonl
    path = args.path
    if path is None:
        ws = Path("workspace")
        if (ws / "history.jsonl").exists():
            path = ws / "history.jsonl"
        else:
            print("No history.jsonl found in workspace/", file=sys.stderr)
            sys.exit(1)

    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    steps = parse(path)

    if args.timeline:
        cmd_timeline(steps)
    elif args.errors:
        cmd_errors(steps)
    elif args.step is not None:
        cmd_step(steps, args.step)
    elif args.tokens:
        cmd_tokens(steps)
    else:
        # Default to summary
        cmd_summary(steps)


if __name__ == "__main__":
    main()
