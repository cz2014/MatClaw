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
import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.rag import (
    ChunkMethod,
    build_chunks_from_directory,
    copy_package_source,
)
from core.retrievers import BaseRetriever, get_retriever

DEFAULT_PACKAGES = ["pymatgen", "atomate2", "jobflow", "jobflow_remote"]
DEFAULT_SOURCES_DIR = PROJECT_ROOT / "data" / "sources"
DEFAULT_CORPUS_DIR = PROJECT_ROOT / "data" / "corpus"


def build_corpus(
    packages: list[str],
    sources_dir: Path,
    corpus_dir: Path,
    retriever_method: str = "bm25",
    method: ChunkMethod = "fixed",
    chunk_size: int = 400,
    skip_copy: bool = False,
) -> BaseRetriever:
    """Build RAG corpus from packages.

    Args:
        packages: List of package names to index
        sources_dir: Directory to copy source files to
        corpus_dir: Directory to save index
        retriever_method: Retriever backend ("bm25" or "gemini")
        method: Chunking method ("fixed" or "ast")
        chunk_size: Token size for chunks
        skip_copy: If True, use existing sources without copying

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

    # Step 2: Build chunks from each package
    print(f"\nChunking with method={method}, size={chunk_size}...")
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
        return get_retriever(retriever_method)

    # Step 3: Build retriever and add chunks
    print(f"\nBuilding {retriever_method} index with {len(all_chunks)} total chunks...")
    retriever = get_retriever(retriever_method)
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
  python scripts/build_corpus.py --skip-copy  # reindex existing sources
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
        choices=["fixed", "ast"],
        default="ast",
        help="Chunking method (default: ast)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=400,
        help="Token size for chunks (default: 400)",
    )
    parser.add_argument(
        "--skip-copy",
        action="store_true",
        help="Skip copying sources, use existing files",
    )

    args = parser.parse_args()

    print("RAG Corpus Builder")
    print(f"  Retriever: {args.retriever}")
    print(f"  Packages: {args.packages}")
    print(f"  Sources:  {args.sources_dir}")
    print(f"  Corpus:   {args.corpus_dir}")
    print(f"  Method:   {args.method}")
    print(f"  Chunk size: {args.chunk_size}")
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
        )
        print(f"\nDone. Total chunks indexed: {retriever.chunk_count}")
    except ImportError as e:
        print(f"\nERROR: Missing dependency: {e}")
        print("Install RAG dependencies with: pip install -e '.[rag]'")
        sys.exit(1)


if __name__ == "__main__":
    main()
