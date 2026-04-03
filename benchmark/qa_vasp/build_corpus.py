"""Build retrieval index for VASP wiki corpus.

Usage:
    python benchmark/qa_vasp/build_corpus.py
    python benchmark/qa_vasp/build_corpus.py --retriever gemini
    python benchmark/qa_vasp/build_corpus.py --method markdown
    python benchmark/qa_vasp/build_corpus.py --chunk-size 600
    python benchmark/qa_vasp/build_corpus.py --dry-run
"""

from __future__ import annotations

import argparse
from pathlib import Path

# Canonical paths (shared with scripts/build_corpus.py)
PROJECT_ROOT = Path(__file__).parent.parent.parent
CORPUS_DIR = PROJECT_ROOT / "data" / "docs" / "vasp"
DATA_DIR = PROJECT_ROOT / "data" / "corpus" / "vasp"


def build_corpus(
    method: str = "fixed",
    chunk_size: int = 800,
    overlap: int = 50,
    dry_run: bool = False,
    retriever_method: str = "bm25",
) -> None:
    """Build retrieval index from VASP wiki markdown files.

    Args:
        method: Chunking method ("fixed" or "markdown").
        chunk_size: Target tokens per chunk.
        overlap: Token overlap between chunks.
        dry_run: If True, print stats without saving.
        retriever_method: Retriever type ("bm25" or "gemini").
    """
    from core.rag import chunk_fixed_width, chunk_markdown_aware
    from core.retrievers import get_retriever

    # 1. Read all .md files
    md_files = sorted(CORPUS_DIR.glob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No .md files found in {CORPUS_DIR}")

    print(f"Found {len(md_files)} markdown files in {CORPUS_DIR}")
    print(f"Using chunking method: {method}")
    print(f"Using retriever: {retriever_method}")

    # 2. Chunk each file
    all_chunks = []
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8", errors="replace")
        if not content.strip():
            continue

        if method == "markdown":
            chunks = chunk_markdown_aware(
                content=content,
                file_path=md_file.name,
                software="vasp",
                max_tokens=chunk_size,
                overlap_lines=3,
            )
        else:
            chunks = chunk_fixed_width(
                content=content,
                file_path=md_file.name,
                software="vasp",
                chunk_size=chunk_size,
                overlap=overlap,
            )
        all_chunks.extend(chunks)

    print(f"Created {len(all_chunks)} chunks (chunk_size={chunk_size}, overlap={overlap})")

    if dry_run:
        print("Dry run - not saving index")
        # Print sample chunks
        if all_chunks:
            print(f"\nSample chunk from {all_chunks[0].file_path}:")
            print(f"  Lines: {all_chunks[0].start_line}-{all_chunks[0].end_line}")
            print(f"  Content preview: {all_chunks[0].content[:200]}...")
        return

    # 3. Build index
    print(f"Building {retriever_method} index...")
    if retriever_method == "bm25":
        retriever = get_retriever("bm25", use_code_tokenize=False)
    else:
        retriever = get_retriever(retriever_method)
    retriever.add_chunks(all_chunks)

    # 4. Save index
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    retriever.save(DATA_DIR)
    print(f"Saved index to {DATA_DIR}")
    print(f"  - chunks.json: {(DATA_DIR / 'chunks.json').stat().st_size / 1024:.1f} KB")
    if retriever_method == "bm25":
        print(f"  - bm25/: BM25 index files")
    else:
        print(f"  - embeddings.npy: embedding vectors")
        print(f"  - faiss.index: FAISS index file")


def main():
    parser = argparse.ArgumentParser(description="Build retrieval index for VASP wiki corpus")
    parser.add_argument(
        "--retriever",
        choices=["bm25", "gemini"],
        default="bm25",
        help="Retriever type: 'bm25' (sparse) or 'gemini' (dense embeddings)",
    )
    parser.add_argument(
        "--method",
        choices=["fixed", "markdown"],
        default="fixed",
        help="Chunking method: 'fixed' (token windows) or 'markdown' (header-aware)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=800,
        help="Tokens per chunk (default: 800)",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=50,
        help="Token overlap between chunks (default: 50)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stats without saving",
    )
    args = parser.parse_args()

    build_corpus(
        method=args.method,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        dry_run=args.dry_run,
        retriever_method=args.retriever,
    )


if __name__ == "__main__":
    main()
