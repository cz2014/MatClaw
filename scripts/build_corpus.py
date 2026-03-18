#!/usr/bin/env python
"""CLI script to build RAG corpus from installed packages.

Outputs per-package subdirs under data/corpus/{package}/, each with
chunks.json + bm25/ index. Supports multiple retriever backends.

Usage:
    python scripts/build_corpus.py
    python scripts/build_corpus.py --retriever gemini
    python scripts/build_corpus.py --packages pymatgen atomate2
    python scripts/build_corpus.py --method ast --chunk-size 600
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.rag import (
    ChunkMethod,
    build_chunks_from_directory,
    chunk_markdown_aware,
    copy_package_source,
    load_chunks_from_jsonl,
)
from core.retrievers import BaseRetriever, get_retriever

DEFAULT_PACKAGES = ["pymatgen", "atomate2", "jobflow", "jobflow_remote"]
DEFAULT_SOURCES_DIR = PROJECT_ROOT / "data" / "sources"
DEFAULT_CORPUS_DIR = PROJECT_ROOT / "data" / "corpus"

# Approximate conversion: 1 token ~ 3 bytes for code (same as cast method)
# This gives consistent chunk sizes across methods
TOKENS_TO_BYTES = 3


def run_code_chunk(
    sources_dir: Path, corpus_dir: Path, packages: list[str], chunk_size: int
) -> Path:
    """Run code-chunk Node.js script and return path to JSONL output.

    Args:
        sources_dir: Directory containing copied package sources
        corpus_dir: Directory to write JSONL output
        packages: List of package names to chunk
        chunk_size: Chunk size in tokens (converted to bytes internally)

    Returns:
        Path to generated JSONL file

    Raises:
        FileNotFoundError: If Node.js script not found
        RuntimeError: If node_modules missing or chunking fails
    """
    script_dir = Path(__file__).parent
    script_path = script_dir / "chunk_with_context.mjs"

    if not script_path.exists():
        raise FileNotFoundError(f"Node.js script not found: {script_path}")

    if not (script_dir / "node_modules").exists():
        raise RuntimeError(
            f"node_modules not found. Run: cd {script_dir} && npm install"
        )

    jsonl_path = corpus_dir / "code_chunk_output.jsonl"
    corpus_dir.mkdir(parents=True, exist_ok=True)

    # Convert tokens to bytes
    max_bytes = chunk_size * TOKENS_TO_BYTES

    cmd = [
        "node",
        str(script_path),
        str(sources_dir),
        str(jsonl_path),
        str(max_bytes),
        *packages,
    ]

    print(f"Running code-chunk (max {max_bytes} bytes per chunk)...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"code-chunk failed:\n{result.stderr}")

    if result.stdout:
        print(result.stdout.rstrip())

    return jsonl_path


def build_corpus(
    packages: list[str],
    sources_dir: Path,
    corpus_dir: Path,
    retriever_method: str = "bm25",
    method: ChunkMethod = "fixed",
    chunk_size: int = 400,
    skip_copy: bool = False,
    use_code_tokenize: bool = True,
) -> int:
    """Build RAG corpus from packages, saving per-package subdirs.

    Output layout:
        corpus_dir/{package}/chunks.json + bm25/  (for each package)

    Args:
        packages: List of package names to index
        sources_dir: Directory to copy source files to
        corpus_dir: Base directory for per-package output
        retriever_method: Retriever backend ("bm25" or "gemini")
        method: Chunking method ("fixed", "ast", or "code-chunk")
        chunk_size: Token size for chunks
        skip_copy: If True, use existing sources without copying
        use_code_tokenize: For BM25, use code-aware tokenization

    Returns:
        Total number of chunks indexed across all packages.
    """
    sources_dir.mkdir(parents=True, exist_ok=True)
    corpus_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Copy package sources
    if not skip_copy:
        print("Copying package sources...")
        for pkg in packages:
            count = copy_package_source(pkg, sources_dir)
            if count > 0:
                print(f"  {pkg}: {count} files")
            else:
                print(f"  {pkg}: not found or empty (skipped)")

    # Step 2: Build chunks
    print(f"\nChunking with method={method}, size={chunk_size}...")

    if method == "code-chunk":
        # Use Node.js code-chunk for tree-sitter based chunking with context
        jsonl_path = run_code_chunk(sources_dir, corpus_dir, packages, chunk_size)
        all_chunks = load_chunks_from_jsonl(jsonl_path)
        print(f"Loaded {len(all_chunks)} chunks from code-chunk")
    else:
        # Use Python-based chunking (fixed or ast)
        all_chunks = []
        for pkg in packages:
            pkg_dir = sources_dir / pkg
            if not pkg_dir.exists():
                continue

            chunks = build_chunks_from_directory(
                pkg_dir,
                software=pkg,
                method=method,
                chunk_size=chunk_size,
            )
            print(f"  {pkg}: {len(chunks)} chunks")
            all_chunks.extend(chunks)

    if not all_chunks:
        print("\nWARNING: No chunks created. Check that packages are installed.")
        return 0

    # Step 3: Group chunks by software and save per-package
    groups: dict[str, list] = defaultdict(list)
    for chunk in all_chunks:
        groups[chunk.software].append(chunk)

    print(f"\nSaving per-package indices ({len(all_chunks)} total chunks)...")
    total = 0
    for pkg_name, pkg_chunks in sorted(groups.items()):
        pkg_dir = corpus_dir / pkg_name
        retriever = get_retriever(retriever_method, use_code_tokenize=use_code_tokenize)
        retriever.add_chunks(pkg_chunks)
        retriever.save(pkg_dir)
        print(f"  {pkg_name}: {len(pkg_chunks)} chunks -> {pkg_dir}")
        total += len(pkg_chunks)

    # Clean up code-chunk JSONL intermediate file if it exists
    jsonl_intermediate = corpus_dir / "code_chunk_output.jsonl"
    if jsonl_intermediate.exists():
        jsonl_intermediate.unlink()

    return total


def build_docs_corpus(
    docs_dir: Path,
    software: str,
    corpus_dir: Path,
    retriever_method: str = "bm25",
    chunk_size: int = 800,
) -> int:
    """Build RAG corpus from markdown documentation files.

    Reads all .md files from docs_dir, chunks with markdown-aware method,
    and saves to corpus_dir/{software}/.

    Args:
        docs_dir: Directory containing .md files
        software: Software name for tagging chunks (e.g., "deepmd", "dpgen_docs")
        corpus_dir: Base directory for per-package output
        retriever_method: Retriever backend ("bm25" or "gemini")
        chunk_size: Token size for chunks

    Returns:
        Number of chunks indexed.
    """
    md_files = sorted(docs_dir.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {docs_dir}")
        return 0

    print(f"Found {len(md_files)} markdown files in {docs_dir}")

    all_chunks = []
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8", errors="replace")
        if not content.strip():
            continue
        chunks = chunk_markdown_aware(
            content=content,
            file_path=md_file.name,
            software=software,
            max_tokens=chunk_size,
            overlap_lines=3,
        )
        all_chunks.extend(chunks)

    if not all_chunks:
        print("WARNING: No chunks created from documentation files.")
        return 0

    print(f"Created {len(all_chunks)} chunks (method=markdown, size={chunk_size})")

    pkg_dir = corpus_dir / software
    retriever = get_retriever(retriever_method, use_code_tokenize=False)
    retriever.add_chunks(all_chunks)
    retriever.save(pkg_dir)
    print(f"Saved {len(all_chunks)} chunks -> {pkg_dir}")

    return len(all_chunks)


def main():
    parser = argparse.ArgumentParser(
        description="Build RAG corpus from installed Python packages or documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Source code packages (code-chunk method)
  python scripts/build_corpus.py
  python scripts/build_corpus.py --packages pymatgen atomate2
  python scripts/build_corpus.py --packages dpdata dpgen

  # Documentation (markdown method)
  python scripts/build_corpus.py --docs-dir data/docs/deepmd-kit --software deepmd
  python scripts/build_corpus.py --docs-dir data/docs/dpgen --software dpgen_docs

  # Options
  python scripts/build_corpus.py --retriever gemini
  python scripts/build_corpus.py --method ast --chunk-size 600
  python scripts/build_corpus.py --skip-copy  # reindex existing sources

For code-chunk method, first run: cd scripts && npm install
""",
    )
    parser.add_argument(
        "--retriever",
        choices=["bm25", "gemini"],
        default="bm25",
        help="Retriever backend to use (default: bm25)",
    )
    parser.add_argument(
        "--packages",
        nargs="+",
        default=DEFAULT_PACKAGES,
        help=f"Packages to index (default: {DEFAULT_PACKAGES})",
    )
    parser.add_argument(
        "--sources-dir",
        type=Path,
        default=DEFAULT_SOURCES_DIR,
        help=f"Directory for copied sources (default: {DEFAULT_SOURCES_DIR})",
    )
    parser.add_argument(
        "--corpus-dir",
        type=Path,
        default=DEFAULT_CORPUS_DIR,
        help=f"Directory for index output (default: {DEFAULT_CORPUS_DIR})",
    )
    parser.add_argument(
        "--method",
        choices=["fixed", "ast", "code-chunk", "cast"],
        default="code-chunk",
        help="Chunking method: fixed (token windows), ast (Python AST), code-chunk (tree-sitter with context), cast (astchunk)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=800,
        help="Token size for chunks (default: 800)",
    )
    parser.add_argument(
        "--skip-copy",
        action="store_true",
        help="Skip copying sources, use existing files",
    )
    parser.add_argument(
        "--code-tokenize",
        action="store_true",
        help="Enable code-aware tokenization (split snake_case, CamelCase). Default uses bm25s tokenizer.",
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        help="Directory containing .md documentation files (uses markdown chunking method)",
    )
    parser.add_argument(
        "--software",
        type=str,
        help="Software name for documentation corpus (required with --docs-dir, e.g., 'deepmd')",
    )

    args = parser.parse_args()

    use_code_tokenize = args.code_tokenize

    # Documentation mode: --docs-dir
    if args.docs_dir:
        if not args.software:
            parser.error("--software is required when using --docs-dir")
        if not args.docs_dir.exists():
            parser.error(f"Directory not found: {args.docs_dir}")

        print("RAG Corpus Builder (documentation mode)")
        print(f"  Docs dir:  {args.docs_dir}")
        print(f"  Software:  {args.software}")
        print(f"  Corpus:    {args.corpus_dir}")
        print(f"  Retriever: {args.retriever}")
        print(f"  Chunk size: {args.chunk_size}")
        print()

        total = build_docs_corpus(
            docs_dir=args.docs_dir,
            software=args.software,
            corpus_dir=args.corpus_dir,
            retriever_method=args.retriever,
            chunk_size=args.chunk_size,
        )
        print(f"\nDone. Total chunks indexed: {total}")
        return

    # Source code mode (default)
    print("RAG Corpus Builder (source code mode)")
    print(f"  Retriever: {args.retriever}")
    print(f"  Packages: {args.packages}")
    print(f"  Sources:  {args.sources_dir}")
    print(f"  Corpus:   {args.corpus_dir}")
    print(f"  Method:   {args.method}")
    print(f"  Chunk size: {args.chunk_size}")
    print(f"  Code tokenize: {use_code_tokenize}")
    print()

    try:
        total = build_corpus(
            packages=args.packages,
            sources_dir=args.sources_dir,
            corpus_dir=args.corpus_dir,
            retriever_method=args.retriever,
            method=args.method,
            chunk_size=args.chunk_size,
            skip_copy=args.skip_copy,
            use_code_tokenize=use_code_tokenize,
        )
        print(f"\nDone. Total chunks indexed: {total}")
    except ImportError as e:
        print(f"\nERROR: Missing dependency: {e}")
        print("Install RAG dependencies with: pip install -e '.[rag]'")
        sys.exit(1)


if __name__ == "__main__":
    main()
