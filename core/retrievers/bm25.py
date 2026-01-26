"""BM25-based retriever implementation."""

from __future__ import annotations

import json
import re
from pathlib import Path

from core.rag import Chunk

from . import BaseRetriever


def _code_tokenize(text: str) -> list[str]:
    """Tokenize text with code-aware splitting.

    Splits on:
    - Whitespace
    - Underscores (snake_case)
    - Dots (module.paths)
    - CamelCase boundaries

    Examples:
        "monkhorst_automatic" -> ["monkhorst", "automatic"]
        "pymatgen.io.vasp" -> ["pymatgen", "io", "vasp"]
        "KPoints" -> ["k", "points"]
    """
    words = text.split()

    tokens = []
    for word in words:
        # Split on underscores and dots
        parts = re.split(r"[_.]", word)

        for part in parts:
            if not part:
                continue
            # Split CamelCase: "KPoints" -> ["K", "Points"] -> ["k", "points"]
            camel_split = re.sub(r"([a-z])([A-Z])", r"\1 \2", part).split()
            tokens.extend(t.lower() for t in camel_split if t)

    return tokens


class BM25Retriever(BaseRetriever):
    """BM25-based retrieval using bm25s library."""

    def __init__(
        self,
        chunks: list[Chunk] | None = None,
        use_code_tokenize: bool = True,
    ):
        """Initialize retriever with optional chunks.

        Args:
            chunks: List of chunks to index (can be added later via add_chunks).
            use_code_tokenize: If True, use code-aware tokenization (split snake_case,
                CamelCase, dotted.paths). If False, use default bm25s tokenization.
        """
        self._chunks: list[Chunk] = []
        self._retriever = None
        self._use_code_tokenize = use_code_tokenize

        if chunks:
            self.add_chunks(chunks)

    def add_chunks(self, chunks: list[Chunk]) -> None:
        """Add chunks to the index and rebuild."""
        self._chunks.extend(chunks)
        self._build_index()

    def _build_index(self) -> None:
        """Build BM25 index from current chunks."""
        if not self._chunks:
            return

        import bm25s

        corpus = [c.content for c in self._chunks]

        if self._use_code_tokenize:
            # Use code-aware tokenizer for better matching of snake_case, dots, CamelCase
            corpus_tokens = [_code_tokenize(doc) for doc in corpus]
        else:
            # Use default bm25s tokenization
            corpus_tokens = bm25s.tokenize(corpus, show_progress=False)

        self._retriever = bm25s.BM25()
        self._retriever.index(corpus_tokens, show_progress=False)

    def search(
        self,
        query: str,
        top_k: int = 5,
        software_filter: list[str] | None = None,
    ) -> list[tuple[Chunk, float]]:
        """Search for relevant chunks using BM25."""
        if not self._retriever or not self._chunks:
            return []

        import bm25s

        # Use same tokenizer as indexing
        if self._use_code_tokenize:
            query_tokens = [_code_tokenize(query)]
        else:
            query_tokens = bm25s.tokenize([query], show_progress=False)

        # Get more results if filtering
        fetch_k = top_k * 3 if software_filter else top_k
        results, scores = self._retriever.retrieve(
            query_tokens, k=min(fetch_k, len(self._chunks)), show_progress=False
        )

        # results shape: (1, k), scores shape: (1, k)
        results_flat = results[0]
        scores_flat = scores[0]

        output = []
        for idx, score in zip(results_flat, scores_flat):
            chunk = self._chunks[idx]

            # Apply software filter
            if software_filter and chunk.software not in software_filter:
                continue

            output.append((chunk, float(score)))

            if len(output) >= top_k:
                break

        return output

    def save(self, path: Path) -> None:
        """Save index to disk."""
        path.mkdir(parents=True, exist_ok=True)

        # Save chunks and settings as JSON
        data = {
            "use_code_tokenize": self._use_code_tokenize,
            "chunks": [
                {
                    "chunk_id": c.chunk_id,
                    "software": c.software,
                    "file_path": c.file_path,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "symbol": c.symbol,
                    "content": c.content,
                }
                for c in self._chunks
            ],
        }
        with (path / "chunks.json").open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        # Save BM25 index
        if self._retriever:
            self._retriever.save(str(path / "bm25"))

    @classmethod
    def load(cls, path: Path) -> BM25Retriever:
        """Load index from disk."""
        import bm25s

        with (path / "chunks.json").open("r", encoding="utf-8") as f:
            data = json.load(f)

        instance = cls(use_code_tokenize=data["use_code_tokenize"])

        instance._chunks = [
            Chunk(
                chunk_id=c["chunk_id"],
                software=c["software"],
                file_path=c["file_path"],
                start_line=c["start_line"],
                end_line=c["end_line"],
                symbol=c["symbol"],
                content=c["content"],
            )
            for c in data["chunks"]
        ]

        # Load BM25 index
        bm25_path = path / "bm25"
        if bm25_path.exists():
            instance._retriever = bm25s.BM25.load(str(bm25_path), load_corpus=False)

        return instance

    @property
    def chunk_count(self) -> int:
        """Number of indexed chunks."""
        return len(self._chunks)
