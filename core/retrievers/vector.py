"""Vector-based retrieval with FAISS.

This module provides the generic FAISS-based retriever that works with any embedder.
Specific embedder implementations (Gemini, OpenAI, etc.) are in separate files.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np

from core.rag import Chunk

from . import BaseRetriever


class BaseEmbedder(ABC):
    """Abstract base class for text embedders."""

    @abstractmethod
    def embed(self, texts: list[str]) -> np.ndarray:
        """Embed texts into vectors.

        Args:
            texts: List of text strings to embed.

        Returns:
            NumPy array of shape (N, dim) with embeddings.
        """
        ...

    @abstractmethod
    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single query.

        Args:
            query: Query string to embed.

        Returns:
            NumPy array of shape (1, dim) with query embedding.
        """
        ...


class VectorRetriever(BaseRetriever):
    """FAISS-based vector retriever that works with any embedder."""

    def __init__(self, embedder: BaseEmbedder):
        """Initialize vector retriever.

        Args:
            embedder: Embedder instance to use for encoding texts/queries.
        """
        self._embedder = embedder
        self._chunks: list[Chunk] = []
        self._embeddings: np.ndarray | None = None
        self._index = None

    def add_chunks(self, chunks: list[Chunk]) -> None:
        """Add chunks and compute embeddings."""
        self._chunks.extend(chunks)
        self._embeddings = self._embedder.embed([c.content for c in self._chunks])
        self._build_index()

    def _build_index(self) -> None:
        """Build FAISS index from embeddings."""
        import faiss

        # Normalize for cosine similarity via inner product
        faiss.normalize_L2(self._embeddings)
        self._index = faiss.IndexFlatIP(self._embeddings.shape[1])
        self._index.add(self._embeddings)

    def search(
        self,
        query: str,
        top_k: int = 5,
        software_filter: list[str] | None = None,
    ) -> list[tuple[Chunk, float]]:
        """Search for relevant chunks using vector similarity."""
        import faiss

        if self._index is None or not self._chunks:
            return []

        query_vec = self._embedder.embed_query(query)
        faiss.normalize_L2(query_vec)

        # Fetch more results if filtering
        fetch_k = top_k * 3 if software_filter else top_k
        scores, indices = self._index.search(query_vec, min(fetch_k, len(self._chunks)))

        output = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:  # FAISS returns -1 for empty slots
                continue
            chunk = self._chunks[idx]

            # Apply software filter
            if software_filter and chunk.software not in software_filter:
                continue

            output.append((chunk, float(score)))

            if len(output) >= top_k:
                break

        return output

    def save(self, path: Path) -> None:
        """Save retriever state to disk."""
        import faiss

        path.mkdir(parents=True, exist_ok=True)

        # Save embeddings
        np.save(path / "embeddings.npy", self._embeddings)

        # Save FAISS index
        faiss.write_index(self._index, str(path / "faiss.index"))

        # Save chunks as JSON
        chunks_data = [
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
        ]
        (path / "chunks.json").write_text(
            json.dumps(chunks_data, ensure_ascii=False), encoding="utf-8"
        )

    @classmethod
    def load(cls, path: Path, embedder: BaseEmbedder) -> VectorRetriever:
        """Load retriever from disk.

        Args:
            path: Directory containing saved index files.
            embedder: Embedder instance (needed for query embedding at search time).

        Returns:
            Loaded VectorRetriever instance.
        """
        import faiss

        instance = cls(embedder)

        # Load embeddings
        instance._embeddings = np.load(path / "embeddings.npy")

        # Load FAISS index
        instance._index = faiss.read_index(str(path / "faiss.index"))

        # Load chunks
        chunks_data = json.loads((path / "chunks.json").read_text(encoding="utf-8"))
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
            for c in chunks_data
        ]

        return instance

    @property
    def chunk_count(self) -> int:
        """Number of indexed chunks."""
        return len(self._chunks)
