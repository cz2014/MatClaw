#!/usr/bin/env python
"""CLI script to build RAG corpus from installed packages.

Supports multiple retriever backends (BM25, Gemini embeddings).

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
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.rag import (
    ChunkMethod,
    build_chunks_from_directory,
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
) -> BaseRetriever:
    """Build RAG corpus from packages.

    Args:
        packages: List of package names to index
        sources_dir: Directory to copy source files to
        corpus_dir: Directory to save index
        retriever_method: Retriever backend ("bm25" or "gemini")
        method: Chunking method ("fixed", "ast", or "code-chunk")
        chunk_size: Token size for chunks
        skip_copy: If True, use existing sources without copying
        use_code_tokenize: For BM25, use code-aware tokenization

    Returns:
        Built retriever instance
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
        return get_retriever(retriever_method, use_code_tokenize=use_code_tokenize)

    # Step 3: Build retriever and add chunks
    print(f"\nBuilding {retriever_method} index with {len(all_chunks)} total chunks...")
    retriever = get_retriever(retriever_method, use_code_tokenize=use_code_tokenize)
    retriever.add_chunks(all_chunks)

    # Step 4: Save index
    # BM25 saves to corpus_dir directly, vector retrievers save to subdirectory
    if retriever_method == "bm25":
        save_path = corpus_dir
    else:
        save_path = corpus_dir / retriever_method

    retriever.save(save_path)
    print(f"Index saved to: {save_path}")

    return retriever


def main():
    parser = argparse.ArgumentParser(
        description="Build RAG corpus from installed Python packages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/build_corpus.py
  python scripts/build_corpus.py --retriever gemini
  python scripts/build_corpus.py --packages pymatgen atomate2
  python scripts/build_corpus.py --method ast --chunk-size 600
  python scripts/build_corpus.py --method code-chunk --chunk-size 800
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

    args = parser.parse_args()

    use_code_tokenize = args.code_tokenize

    print("RAG Corpus Builder")
    print(f"  Retriever: {args.retriever}")
    print(f"  Packages: {args.packages}")
    print(f"  Sources:  {args.sources_dir}")
    print(f"  Corpus:   {args.corpus_dir}")
    print(f"  Method:   {args.method}")
    print(f"  Chunk size: {args.chunk_size}")
    print(f"  Code tokenize: {use_code_tokenize}")
    print()

    try:
        retriever = build_corpus(
            packages=args.packages,
            sources_dir=args.sources_dir,
            corpus_dir=args.corpus_dir,
            retriever_method=args.retriever,
            method=args.method,
            chunk_size=args.chunk_size,
            skip_copy=args.skip_copy,
            use_code_tokenize=use_code_tokenize,
        )
        print(f"\nDone. Total chunks indexed: {retriever.chunk_count}")
    except ImportError as e:
        print(f"\nERROR: Missing dependency: {e}")
        print("Install RAG dependencies with: pip install -e '.[rag]'")
        sys.exit(1)


if __name__ == "__main__":
    main()
