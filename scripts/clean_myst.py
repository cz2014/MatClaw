#!/usr/bin/env python
"""Clean MyST-specific syntax from Markdown files for RAG ingestion.

Strips MyST substitutions, RST cross-references, and directive fences
so that the resulting .md files are plain markdown suitable for chunking.

Usage:
    python scripts/clean_myst.py data/docs/deepmd-kit/
    python scripts/clean_myst.py data/docs/dpgen/
    python scripts/clean_myst.py --dry-run data/docs/deepmd-kit/  # preview only
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

# MyST substitutions -> plain text labels
SUBSTITUTIONS = {
    "{{tf}}": "[TensorFlow]",
    "{{pt}}": "[PyTorch]",
    "{{dp}}": "[DeePMD-kit]",
    "{{jax}}": "[JAX]",
    "{{paddle}}": "[PaddlePaddle]",
    "{{numpy}}": "[NumPy]",
    "{{lammps}}": "[LAMMPS]",
    "{{i-pi}}": "[i-PI]",
    "{{ase}}": "[ASE]",
    "{{dpmodel}}": "[DP]",
    "{{ tf }}": "[TensorFlow]",
    "{{ pt }}": "[PyTorch]",
    "{{ dp }}": "[DeePMD-kit]",
    "{{ jax }}": "[JAX]",
    "{{ paddle }}": "[PaddlePaddle]",
    "{{ tensorflow_icon }}": "[TensorFlow]",
    "{{ pytorch_icon }}": "[PyTorch]",
    "{{ paddle_icon }}": "[PaddlePaddle]",
    "{{ jax_icon }}": "[JAX]",
    "{{ numpy_icon }}": "[NumPy]",
    "{{ dpmodel_icon }}": "[DP]",
}

# RST cross-reference patterns: :role:`text` -> text
# Matches :ref:`label`, :doc:`path`, :py:class:`name`, :py:func:`name`, etc.
RST_XREF_RE = re.compile(r":(?:[\w.]+:)*`([^`]*)`")

# MyST directive fences: :::{directive}\n...\n::: -> keep inner content
# Handles: ::::{tab-item}, :::: {.dargs ...}, {#cite}, ::::: note
DIRECTIVE_OPEN_RE = re.compile(r"^(:{3,})\s*(?:\{[^}]+\}|\w+).*$")
DIRECTIVE_CLOSE_RE = re.compile(r"^:{3,}\s*$")

# Catch-all for remaining {{...}} substitutions not in SUBSTITUTIONS dict
REMAINING_SUBST_RE = re.compile(r"\{\{(\w[\w\s-]*)\}\}")


def clean_content(text: str) -> str:
    """Clean MyST-specific syntax from markdown content."""
    # Step 1: Replace known substitutions
    for pattern, replacement in SUBSTITUTIONS.items():
        text = text.replace(pattern, replacement)

    # Step 2: Replace remaining {{...}} with [...]
    text = REMAINING_SUBST_RE.sub(lambda m: f"[{m.group(1).strip()}]", text)

    # Step 3: Strip RST cross-references
    text = RST_XREF_RE.sub(r"\1", text)

    # Step 4: Unwrap directive fences (keep inner content)
    # Uses a stack to handle nested directives (e.g., tab-set > tab-item)
    lines = text.split("\n")
    cleaned_lines = []
    directive_stack = []  # stack of colon counts for nested directives

    for line in lines:
        open_match = DIRECTIVE_OPEN_RE.match(line)
        if open_match:
            directive_stack.append(len(open_match.group(1)))
            continue
        elif directive_stack and DIRECTIVE_CLOSE_RE.match(line):
            colon_count = len(line.rstrip()) - len(line.rstrip().lstrip(":"))
            if colon_count >= directive_stack[-1]:
                directive_stack.pop()
                continue

        # Skip directive option lines (e.g., `:class: tip`)
        if directive_stack and line.strip().startswith(":") and ":" in line.strip()[1:]:
            option_match = re.match(r"^\s*:[\w-]+:", line)
            if option_match:
                continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def clean_directory(directory: Path, dry_run: bool = False) -> int:
    """Clean all .md files in a directory. Returns count of files processed."""
    md_files = sorted(directory.glob("**/*.md"))
    if not md_files:
        print(f"No .md files found in {directory}")
        return 0

    count = 0
    for md_file in md_files:
        original = md_file.read_text(encoding="utf-8", errors="replace")
        cleaned = clean_content(original)

        if original != cleaned:
            count += 1
            if dry_run:
                print(f"  [would clean] {md_file.name}")
            else:
                md_file.write_text(cleaned, encoding="utf-8")

    return count


def main():
    parser = argparse.ArgumentParser(description="Clean MyST syntax from markdown files")
    parser.add_argument("directory", type=Path, help="Directory containing .md files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    if not args.directory.exists():
        print(f"ERROR: Directory not found: {args.directory}")
        return

    md_count = len(list(args.directory.glob("**/*.md")))
    print(f"Processing {md_count} .md files in {args.directory}...")

    changed = clean_directory(args.directory, dry_run=args.dry_run)
    action = "would change" if args.dry_run else "cleaned"
    print(f"Done: {changed} files {action} out of {md_count} total")


if __name__ == "__main__":
    main()
