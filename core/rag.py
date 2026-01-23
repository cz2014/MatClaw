"""RAG retrieval logic, indexer, and schemas for MLFF agent.

v0 implementation: BM25 + fixed-width/AST chunking over local source code.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

# Type aliases
ChunkMethod = Literal["fixed", "ast"]


@dataclass
class SearchResult:
    """A single search result with source location and code snippet."""

    source: str  # file path + line range (e.g., "pymatgen/core/structure.py:100-150")
    snippet: str  # verbatim code


@dataclass
class Chunk:
    """Internal representation of a text chunk for indexing."""

    chunk_id: str
    software: str
    file_path: str
    start_line: int
    end_line: int
    symbol: str | None
    content: str


# -----------------------------------------------------------------------------
# Chunking: Fixed-width token chunking (Method A)
# -----------------------------------------------------------------------------


def _get_tokenizer():
    """Get tiktoken tokenizer (lazy import)."""
    import tiktoken

    return tiktoken.get_encoding("cl100k_base")


def chunk_fixed_width(
    content: str,
    file_path: str,
    software: str,
    chunk_size: int = 400,
    overlap: int = 50,
) -> list[Chunk]:
    """Chunk text into fixed-width token windows.

    Args:
        content: Source code or text content
        file_path: Path for locator metadata
        software: Package name
        chunk_size: Target tokens per chunk (default 400)
        overlap: Token overlap between chunks (default 50)

    Returns:
        List of Chunk objects
    """
    tokenizer = _get_tokenizer()
    tokens = tokenizer.encode(content)

    if len(tokens) <= chunk_size:
        return [
            Chunk(
                chunk_id=_make_chunk_id(file_path, 0),
                software=software,
                file_path=file_path,
                start_line=1,
                end_line=content.count("\n") + 1,
                symbol=None,
                content=content,
            )
        ]

    chunks = []
    lines = content.split("\n")
    line_starts = _compute_line_starts(content)

    step = max(1, chunk_size - overlap)
    for i, start_tok in enumerate(range(0, len(tokens), step)):
        end_tok = min(start_tok + chunk_size, len(tokens))
        chunk_tokens = tokens[start_tok:end_tok]
        chunk_text = tokenizer.decode(chunk_tokens)

        # Compute line numbers from character offsets
        # Find approximate character positions
        prefix_text = tokenizer.decode(tokens[:start_tok]) if start_tok > 0 else ""
        start_char = len(prefix_text)
        start_line = _char_to_line(start_char, line_starts)
        end_line = min(start_line + chunk_text.count("\n") + 1, len(lines))

        chunks.append(
            Chunk(
                chunk_id=_make_chunk_id(file_path, i),
                software=software,
                file_path=file_path,
                start_line=start_line,
                end_line=end_line,
                symbol=None,
                content=chunk_text,
            )
        )

        if end_tok >= len(tokens):
            break

    return chunks


def _compute_line_starts(content: str) -> list[int]:
    """Compute character offset for start of each line."""
    starts = [0]
    for i, ch in enumerate(content):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def _char_to_line(char_offset: int, line_starts: list[int]) -> int:
    """Convert character offset to 1-indexed line number."""
    for i, start in enumerate(line_starts):
        if start > char_offset:
            return i  # 1-indexed
    return len(line_starts)


def _make_chunk_id(file_path: str, index: int) -> str:
    """Create a deterministic chunk ID."""
    h = hashlib.md5(f"{file_path}:{index}".encode()).hexdigest()[:8]
    return f"chunk_{h}"


# -----------------------------------------------------------------------------
# Chunking: AST-based chunking (Method B)
# -----------------------------------------------------------------------------


def chunk_ast(
    content: str,
    file_path: str,
    software: str,
    max_tokens: int = 800,
) -> list[Chunk]:
    """Chunk Python source using AST boundaries (functions/classes).

    Falls back to fixed-width chunking if parsing fails.

    Args:
        content: Python source code
        file_path: Path for locator metadata
        software: Package name
        max_tokens: Maximum tokens per chunk (default 800)

    Returns:
        List of Chunk objects
    """
    try:
        tree = ast.parse(content)
    except SyntaxError:
        # Fall back to fixed-width for unparseable files
        return chunk_fixed_width(content, file_path, software)

    lines = content.split("\n")
    chunks = []
    tokenizer = _get_tokenizer()

    # Extract top-level classes and functions
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # Get the symbol name
            if isinstance(node, ast.ClassDef):
                symbol = node.name
            else:
                symbol = node.name

            # Get line range (1-indexed in AST)
            start_line = node.lineno
            end_line = node.end_lineno or start_line

            # Extract source lines
            node_lines = lines[start_line - 1 : end_line]
            node_content = "\n".join(node_lines)

            # Check token count
            tokens = tokenizer.encode(node_content)
            if len(tokens) <= max_tokens:
                chunks.append(
                    Chunk(
                        chunk_id=_make_chunk_id(f"{file_path}:{symbol}", 0),
                        software=software,
                        file_path=file_path,
                        start_line=start_line,
                        end_line=end_line,
                        symbol=symbol,
                        content=node_content,
                    )
                )
            else:
                # Large node: split with fixed-width
                sub_chunks = chunk_fixed_width(
                    node_content,
                    file_path,
                    software,
                    chunk_size=max_tokens // 2,
                )
                for sc in sub_chunks:
                    sc.symbol = symbol
                    sc.start_line += start_line - 1
                    sc.end_line += start_line - 1
                chunks.extend(sub_chunks)

    # Also capture module-level docstring if present
    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        docstring = tree.body[0].value.value
        chunks.insert(
            0,
            Chunk(
                chunk_id=_make_chunk_id(f"{file_path}:module_doc", 0),
                software=software,
                file_path=file_path,
                start_line=1,
                end_line=tree.body[0].end_lineno or 1,
                symbol="__module__",
                content=docstring,
            ),
        )

    # If no functions/classes found, fall back to fixed-width
    if not chunks:
        return chunk_fixed_width(content, file_path, software)

    return chunks


# -----------------------------------------------------------------------------
# Corpus Builder
# -----------------------------------------------------------------------------


def get_package_source_path(package_name: str) -> Path | None:
    """Get the source path of an installed package.

    Args:
        package_name: Package name (e.g., "pymatgen")

    Returns:
        Path to package source directory, or None if not found.
    """
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            return None

        # Handle regular packages with __init__.py
        if spec.origin is not None:
            origin = Path(spec.origin)
            if origin.name == "__init__.py":
                return origin.parent
            return origin.parent / package_name

        # Handle namespace packages (spec.origin is None)
        if spec.submodule_search_locations:
            for loc in spec.submodule_search_locations:
                p = Path(loc)
                if p.exists():
                    return p

        return None
    except (ImportError, ModuleNotFoundError):
        return None


def copy_package_source(
    package_name: str,
    dest_dir: Path,
    extensions: tuple[str, ...] = (".py",),
) -> int:
    """Copy package source files to destination directory.

    Args:
        package_name: Package name to copy
        dest_dir: Destination directory (will be created)
        extensions: File extensions to copy (default: .py only)

    Returns:
        Number of files copied.
    """
    import shutil

    src_path = get_package_source_path(package_name)
    if src_path is None or not src_path.exists():
        return 0

    dest_pkg = dest_dir / package_name
    if dest_pkg.exists():
        shutil.rmtree(dest_pkg)

    copied = 0
    for src_file in src_path.rglob("*"):
        if src_file.is_file() and src_file.suffix in extensions:
            rel_path = src_file.relative_to(src_path)
            dest_file = dest_pkg / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dest_file)
            copied += 1

    return copied


def build_chunks_from_directory(
    source_dir: Path,
    software: str,
    method: ChunkMethod = "fixed",
    chunk_size: int = 400,
) -> list[Chunk]:
    """Build chunks from all Python files in a directory.

    Args:
        source_dir: Directory containing Python files
        software: Package name for metadata
        method: Chunking method ("fixed" or "ast")
        chunk_size: Token size for fixed-width chunking

    Returns:
        List of all chunks.
    """
    chunks = []
    chunk_fn = chunk_ast if method == "ast" else chunk_fixed_width

    for py_file in source_dir.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if not content.strip():
            continue

        rel_path = str(py_file.relative_to(source_dir.parent))
        file_chunks = chunk_fn(content, rel_path, software, chunk_size)
        chunks.extend(file_chunks)

    return chunks


# -----------------------------------------------------------------------------
# BM25 Index
# -----------------------------------------------------------------------------


class RagIndex:
    """BM25-based retrieval index for code chunks."""

    def __init__(self, chunks: list[Chunk] | None = None):
        """Initialize index with optional chunks.

        Args:
            chunks: List of chunks to index (can be added later)
        """
        self._chunks: list[Chunk] = []
        self._retriever = None

        if chunks:
            self.add_chunks(chunks)

    def add_chunks(self, chunks: list[Chunk]) -> None:
        """Add chunks to the index and rebuild.

        Args:
            chunks: Chunks to add
        """
        self._chunks.extend(chunks)
        self._build_index()

    def _build_index(self) -> None:
        """Build BM25 index from current chunks."""
        if not self._chunks:
            return

        import bm25s

        # Tokenize chunk content for BM25
        corpus = [c.content for c in self._chunks]
        corpus_tokens = bm25s.tokenize(corpus, show_progress=False)

        self._retriever = bm25s.BM25()
        self._retriever.index(corpus_tokens, show_progress=False)

    def search(
        self,
        query: str,
        top_k: int = 5,
        software_filter: list[str] | None = None,
    ) -> list[tuple[Chunk, float]]:
        """Search for relevant chunks.

        Args:
            query: Search query
            top_k: Number of results to return
            software_filter: Optional list of package names to filter by

        Returns:
            List of (chunk, score) tuples, sorted by relevance.
        """
        if not self._retriever or not self._chunks:
            return []

        import bm25s

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
        """Save index to disk.

        Args:
            path: Directory to save index files
        """
        path.mkdir(parents=True, exist_ok=True)

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
        with (path / "chunks.json").open("w", encoding="utf-8") as f:
            json.dump(chunks_data, f, ensure_ascii=False)

        # Save BM25 index
        if self._retriever:
            self._retriever.save(str(path / "bm25"))

    @classmethod
    def load(cls, path: Path) -> RagIndex:
        """Load index from disk.

        Args:
            path: Directory containing index files

        Returns:
            Loaded RagIndex instance.
        """
        import bm25s

        instance = cls()

        # Load chunks
        with (path / "chunks.json").open("r", encoding="utf-8") as f:
            chunks_data = json.load(f)

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

        # Load BM25 index
        bm25_path = path / "bm25"
        if bm25_path.exists():
            instance._retriever = bm25s.BM25.load(str(bm25_path), load_corpus=False)

        return instance

    @property
    def chunk_count(self) -> int:
        """Number of indexed chunks."""
        return len(self._chunks)


# -----------------------------------------------------------------------------
# Search API
# -----------------------------------------------------------------------------


def search(
    index: RagIndex,
    query: str,
    top_k: int = 5,
    software: list[str] | None = None,
) -> list[SearchResult]:
    """Search the RAG index and return list of results.

    Args:
        index: RagIndex instance
        query: Search query
        top_k: Number of results
        software: Optional package filter

    Returns:
        List of SearchResult with source location and code snippet.
    """
    results = index.search(query, top_k=top_k, software_filter=software)

    return [
        SearchResult(
            source=f"{chunk.file_path}:{chunk.start_line}-{chunk.end_line}",
            snippet=chunk.content,
        )
        for chunk, _ in results
    ]
