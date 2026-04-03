"""Retriever abstractions and factory for RAG system.

Provides a unified interface for different retrieval methods (BM25, vector-based).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.rag import Chunk


class BaseRetriever(ABC):
    """Abstract base class for RAG retrievers."""

    @abstractmethod
    def add_chunks(self, chunks: list[Chunk]) -> None:
        """Add chunks to the retriever and build/update index.

        Args:
            chunks: List of Chunk objects to index.
        """
        ...

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 5,
        software_filter: list[str] | None = None,
    ) -> list[tuple[Chunk, float]]:
        """Search for relevant chunks.

        Args:
            query: Search query string.
            top_k: Number of results to return.
            software_filter: Optional list of package names to filter by.

        Returns:
            List of (chunk, score) tuples, sorted by relevance (highest first).
        """
        ...

    @abstractmethod
    def save(self, path: Path) -> None:
        """Save retriever state to disk.

        Args:
            path: Directory to save index files.
        """
        ...

    @classmethod
    @abstractmethod
    def load(cls, path: Path, **kwargs) -> BaseRetriever:
        """Load retriever from disk.

        Args:
            path: Directory containing index files.
            **kwargs: Additional arguments for specific retrievers.

        Returns:
            Loaded retriever instance.
        """
        ...

    @property
    @abstractmethod
    def chunk_count(self) -> int:
        """Number of indexed chunks."""
        ...


def get_retriever(method: str = "bm25", use_code_tokenize: bool = True) -> BaseRetriever:
    """Factory function to create a retriever by method name.

    Args:
        method: Retriever method ("bm25" or "gemini").
        use_code_tokenize: For BM25, whether to use code-aware tokenization.

    Returns:
        Configured retriever instance.

    Raises:
        ValueError: If method is not recognized.
    """
    if method == "bm25":
        from .bm25 import BM25Retriever

        return BM25Retriever(use_code_tokenize=use_code_tokenize)
    elif method == "gemini":
        from .gemini import GeminiEmbedder
        from .vector import VectorRetriever

        return VectorRetriever(GeminiEmbedder())
    else:
        raise ValueError(f"Unknown retriever method: {method}")


def load_retriever(
    method: str, path: Path, gemini_task_type: str = "RETRIEVAL_QUERY"
) -> BaseRetriever:
    """Load a pre-built retriever from disk.

    Args:
        method: Retriever method ("bm25" or "gemini").
        path: Directory containing index files.
        gemini_task_type: Task type for Gemini query embeddings.
            Options: RETRIEVAL_QUERY (for docs), CODE_RETRIEVAL_QUERY (for code).

    Returns:
        Loaded retriever instance.

    Raises:
        ValueError: If method is not recognized.
    """
    if method == "bm25":
        from .bm25 import BM25Retriever

        return BM25Retriever.load(path)
    elif method == "gemini":
        from .gemini import GeminiEmbedder
        from .vector import VectorRetriever

        return VectorRetriever.load(path, GeminiEmbedder(query_task_type=gemini_task_type))
    else:
        raise ValueError(f"Unknown retriever method: {method}")
