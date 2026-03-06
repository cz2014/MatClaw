"""Analyze agent run logs from steps.jsonl.

steps.jsonl is written by the MLFF agent's step callback during execution.
Each line is a JSON record containing a timestamp, step type, and the full
step data (as a dict serialized from smolagents' ActionStep or PlanningStep).

This tool provides 6 views into the run data:

  --summary     Quick overview: step counts, duration, tokens, errors, final answer
  --timeline    One line per step with number, duration, tokens, and summary
  --errors      Error steps with the code that caused the error and recovery status
  --step N      Full detail for step N: plan, code, summary, observations, tokens
  --message N:M Extract message M from step N's model_input_messages (0=system prompt)
  --tokens      Per-step and cumulative token usage with context growth rate

The structured output format ({plan, code, summary}) from Phase 0b means
each step has a one-line summary field, making --timeline especially useful
for understanding what the agent did at a glance.

Examples:
  python scripts/analyze_steps.py workspace/steps.jsonl --summary
  python scripts/analyze_steps.py workspace/steps.jsonl --timeline
  python scripts/analyze_steps.py workspace/steps.jsonl --errors
  python scripts/analyze_steps.py workspace/steps.jsonl --step 3
  python scripts/analyze_steps.py workspace/steps.jsonl --message 3:0
  python scripts/analyze_steps.py workspace/steps.jsonl --tokens

Typical workflow after an agent run:
  1. --summary to check if the run succeeded and how many steps/tokens it used
  2. --timeline to scan what happened at each step
  3. --errors if there were failures, to see what went wrong
  4. --step N to drill into a specific step's full context
  5. --tokens to check for context growth issues (relevant for long runs)

Parser API (for programmatic use):
  from scripts.analyze_steps import parse_steps, StepRecord
  steps = parse_steps(Path("workspace/steps.jsonl"))
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
    """Parsed step from steps.jsonl."""

    ts: str
    step_type: str  # "ActionStep" or "PlanningStep"
    step_number: int | None
    duration: float | None
    input_tokens: int | None
    output_tokens: int | None
    code_action: str | None
    observations: str | None
    model_output: str | None  # raw model_output string (JSON)
    plan: str | None  # extracted from structured output
    summary: str | None  # extracted from structured output
    error: str | None
    is_final_answer: bool
    tool_calls: list[dict] | None
    raw: dict  # full record for --step and --message views


def parse_steps(path: Path) -> list[StepRecord]:
    """Parse steps.jsonl into list of StepRecord.

    Reads line-by-line, extracts fields from dict-format steps.
    Skips malformed records (non-dict step field) with a warning to stderr.
    Parses model_output as JSON to extract plan/summary from structured output.
    """
    records = []
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                print(f"WARNING: skipping malformed JSON on line {lineno}", file=sys.stderr)
                continue

            step = rec.get("step")
            if not isinstance(step, dict):
                print(f"WARNING: skipping non-dict step on line {lineno} (legacy format)", file=sys.stderr)
                continue

            # Extract token usage
            tu = step.get("token_usage") or {}
            input_tokens = tu.get("input_tokens")
            output_tokens = tu.get("output_tokens")

            # Extract duration from timing dict
            timing = step.get("timing") or {}
            duration = timing.get("duration")

            # Parse model_output as JSON for structured output fields
            model_output = step.get("model_output")
            plan = None
            summary = None
            if model_output:
                try:
                    parsed_mo = json.loads(model_output)
                    plan = parsed_mo.get("plan") or parsed_mo.get("thought")
                    summary = parsed_mo.get("summary")
                except (json.JSONDecodeError, TypeError):
                    pass

            # Detect final answer
            code_action = step.get("code_action")
            is_final = step.get("is_final_answer", False)

            records.append(
                StepRecord(
                    ts=rec.get("ts", ""),
                    step_type=rec.get("step_type", "unknown"),
                    step_number=step.get("step_number"),
                    duration=duration,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    code_action=code_action,
                    observations=step.get("observations"),
                    model_output=model_output,
                    plan=plan,
                    summary=summary,
                    error=step.get("error"),
                    is_final_answer=is_final,
                    tool_calls=step.get("tool_calls"),
                    raw=rec,
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

    # Tool usage from code_action
    rag_calls = sum(
        1 for s in steps if s.code_action and "rag_search(" in s.code_action
    )

    print(f"Steps:       {total} ({errors} errors)")
    print(f"Duration:    {total_dur:.1f}s")
    print(f"Tokens:      {total_in:,} in / {total_out:,} out / {total_in + total_out:,} total")
    if rag_calls:
        print(f"RAG calls:   {rag_calls}")
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
    print(f"{'Step':>4}  {'Type':<8}  {'Dur(s)':>6}  {'InTok':>6}  {'OutTok':>6}  Summary")
    print("-" * 80)

    for s in steps:
        sn = s.step_number if s.step_number is not None else "?"
        stype = "Action" if s.step_type == "ActionStep" else "Plan"
        dur = f"{s.duration:.1f}" if s.duration is not None else "-"
        intok = str(s.input_tokens) if s.input_tokens is not None else "-"
        outtok = str(s.output_tokens) if s.output_tokens is not None else "-"

        # Summary: prefer structured output summary, fall back to code_action
        if s.summary:
            desc = s.summary[:70]
        elif s.code_action:
            desc = s.code_action.replace("\n", " ")[:60]
        else:
            desc = "(no output)"

        # Markers
        if s.error:
            desc = "[ERROR] " + desc[:62]
        if s.is_final_answer:
            desc = "[FINAL] " + desc[:62]

        print(f"{sn:>4}  {stype:<8}  {dur:>6}  {intok:>6}  {outtok:>6}  {desc}")


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

    print(f"=== Step {s.step_number} ({s.step_type}) ===")
    print(f"Timestamp: {s.ts}")
    dur = f"{s.duration:.1f}s" if s.duration is not None else "unknown"
    print(f"Duration:  {dur}")
    intok = s.input_tokens if s.input_tokens is not None else "?"
    outtok = s.output_tokens if s.output_tokens is not None else "?"
    print(f"Tokens:    {intok} in / {outtok} out")
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


def cmd_message(steps: list[StepRecord], step_num: int, msg_idx: int) -> None:
    """Extract a specific message from a step's model_input_messages."""
    matches = [s for s in steps if s.step_number == step_num]
    if not matches:
        print(f"Step {step_num} not found.", file=sys.stderr)
        sys.exit(1)

    s = matches[-1]
    step_data = s.raw.get("step", {})
    messages = step_data.get("model_input_messages") or []

    if msg_idx >= len(messages):
        print(
            f"Message index {msg_idx} out of range (step {step_num} has {len(messages)} messages).",
            file=sys.stderr,
        )
        sys.exit(1)

    msg = messages[msg_idx]
    # Message can be a dict with 'role' and 'content'
    role = msg.get("role", "unknown")
    content = msg.get("content", "")

    # Content can be a string or a list of content blocks
    if isinstance(content, list):
        # Extract text from content blocks
        parts = []
        for block in content:
            if isinstance(block, dict) and "text" in block:
                parts.append(block["text"])
            elif isinstance(block, str):
                parts.append(block)
        text = "\n".join(parts)
    else:
        text = str(content)

    print(f"[Step {step_num}, Message {msg_idx}, Role: {role}]")
    print()
    print(text)


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
        description="Analyze agent run logs from steps.jsonl",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("path", type=Path, help="Path to steps.jsonl file")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--summary", action="store_true", help="Quick overview (default)")
    group.add_argument("--timeline", action="store_true", help="One line per step")
    group.add_argument("--errors", action="store_true", help="Error steps with context")
    group.add_argument("--step", type=int, metavar="N", help="Full detail for step N")
    group.add_argument("--message", type=str, metavar="N:M", help="Extract message M from step N")
    group.add_argument("--tokens", action="store_true", help="Per-step and cumulative token usage")

    args = parser.parse_args()

    if not args.path.exists():
        print(f"File not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    steps = parse_steps(args.path)

    if args.timeline:
        cmd_timeline(steps)
    elif args.errors:
        cmd_errors(steps)
    elif args.step is not None:
        cmd_step(steps, args.step)
    elif args.message:
        parts = args.message.split(":")
        if len(parts) != 2:
            print("--message format: N:M (step:message_index)", file=sys.stderr)
            sys.exit(1)
        cmd_message(steps, int(parts[0]), int(parts[1]))
    elif args.tokens:
        cmd_tokens(steps)
    else:
        # Default to summary
        cmd_summary(steps)


if __name__ == "__main__":
    main()
