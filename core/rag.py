"""RAG retrieval logic, indexer, and schemas for MatClaw.

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
ChunkMethod = Literal["fixed", "ast", "code-chunk", "cast", "markdown"]


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
# Chunking: Markdown-aware chunking (Method E)
# -----------------------------------------------------------------------------


@dataclass
class _MarkdownSection:
    """Internal helper for markdown section parsing."""

    header_path: str  # e.g., "IBRION/Molecular dynamics"
    header_level: int  # 1 for #, 2 for ##
    start_line: int  # 1-indexed
    lines: list[str]


def _match_header(line: str) -> tuple[int, str] | None:
    """Match a markdown header line.

    Args:
        line: A single line of text

    Returns:
        (level, text) tuple if line is a header, None otherwise.
        Level is 1 for #, 2 for ##, etc.
    """
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return None

    # Count leading hashes
    level = 0
    for ch in stripped:
        if ch == "#":
            level += 1
        else:
            break

    # Must have space after hashes (or be header-only like "##")
    rest = stripped[level:]
    if rest and not rest[0].isspace():
        return None

    header_text = rest.strip()
    return (level, header_text)


def _parse_markdown_sections(content: str) -> list[_MarkdownSection]:
    """Parse markdown content into sections based on headers.

    Tracks header stack to build hierarchical paths like "IBRION/Molecular dynamics".
    Preserves code fences (``` blocks) by ignoring headers inside them.

    Args:
        content: Full markdown content

    Returns:
        List of _MarkdownSection objects
    """
    lines = content.split("\n")
    sections: list[_MarkdownSection] = []
    header_stack: list[tuple[int, str]] = []  # (level, text)
    in_code_fence = False

    current_section_lines: list[str] = []
    current_header_path = ""
    current_header_level = 0
    current_start_line = 1

    for i, line in enumerate(lines):
        line_num = i + 1  # 1-indexed

        # Toggle code fence state
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            current_section_lines.append(line)
            continue

        # Inside code fence: just accumulate
        if in_code_fence:
            current_section_lines.append(line)
            continue

        # Check for header
        header_match = _match_header(line)
        if header_match:
            level, text = header_match

            # Save previous section if it has content
            if current_section_lines:
                sections.append(
                    _MarkdownSection(
                        header_path=current_header_path,
                        header_level=current_header_level,
                        start_line=current_start_line,
                        lines=current_section_lines,
                    )
                )

            # Update header stack: pop levels >= current, then push new
            while header_stack and header_stack[-1][0] >= level:
                header_stack.pop()
            header_stack.append((level, text))

            # Build header path from stack
            current_header_path = "/".join(h[1] for h in header_stack)
            current_header_level = level
            current_start_line = line_num
            current_section_lines = [line]
        else:
            current_section_lines.append(line)

    # Don't forget the last section
    if current_section_lines:
        sections.append(
            _MarkdownSection(
                header_path=current_header_path,
                header_level=current_header_level,
                start_line=current_start_line,
                lines=current_section_lines,
            )
        )

    return sections


def chunk_markdown_aware(
    content: str,
    file_path: str,
    software: str,
    max_tokens: int = 800,
    overlap_lines: int = 3,
) -> list[Chunk]:
    """Chunk markdown by accumulating sections until token budget is filled.

    Like code-chunk: combines small sections together, respects section boundaries,
    and adds context header showing which sections are included.

    Args:
        content: Markdown content
        file_path: Path for locator metadata
        software: Package name
        max_tokens: Maximum tokens per chunk
        overlap_lines: Line overlap for sub-chunking large sections

    Returns:
        List of Chunk objects
    """
    sections = _parse_markdown_sections(content)

    if not sections:
        return []

    tokenizer = _get_tokenizer()
    chunks: list[Chunk] = []
    chunk_idx = 0

    # Accumulator state
    acc_lines: list[str] = []
    acc_headers: list[str] = []
    acc_start_line: int = 1
    acc_tokens: int = 0

    def _flush_accumulator() -> None:
        """Emit accumulated content as a chunk."""
        nonlocal acc_lines, acc_headers, acc_start_line, acc_tokens, chunk_idx

        if not acc_lines:
            return

        # Build context header (like code-chunk's contextualizedText)
        context_header = f"# {file_path}\n"
        if acc_headers:
            context_header += f"# Sections: {', '.join(acc_headers)}\n"
        context_header += "\n"

        chunk_content = context_header + "\n".join(acc_lines)
        end_line = acc_start_line + len(acc_lines) - 1

        # Use first header as symbol (primary section)
        symbol = acc_headers[0] if acc_headers else None

        chunks.append(
            Chunk(
                chunk_id=_make_chunk_id(f"{file_path}:{chunk_idx}", chunk_idx),
                software=software,
                file_path=file_path,
                start_line=acc_start_line,
                end_line=end_line,
                symbol=symbol,
                content=chunk_content,
            )
        )
        chunk_idx += 1

        # Reset accumulator
        acc_lines = []
        acc_headers = []
        acc_start_line = 1
        acc_tokens = 0

    for section in sections:
        section_content = "\n".join(section.lines)
        section_tokens = len(tokenizer.encode(section_content))

        if section_tokens > max_tokens:
            # Large section: flush accumulator, then sub-chunk this section
            _flush_accumulator()

            sub_chunks = _chunk_lines_aligned(
                lines=section.lines,
                file_path=file_path,
                software=software,
                start_line_offset=section.start_line,
                symbol=section.header_path or "__section__",
                max_tokens=max_tokens,
                overlap_lines=overlap_lines,
            )
            for sub in sub_chunks:
                sub.chunk_id = _make_chunk_id(f"{file_path}:{chunk_idx}", chunk_idx)
                chunk_idx += 1
            chunks.extend(sub_chunks)

        elif acc_tokens + section_tokens > max_tokens:
            # Would exceed budget: flush, then start new accumulator
            _flush_accumulator()

            acc_lines = section.lines[:]
            acc_headers = [section.header_path] if section.header_path else []
            acc_start_line = section.start_line
            acc_tokens = section_tokens

        else:
            # Fits in current accumulator
            if not acc_lines:
                acc_start_line = section.start_line
            acc_lines.extend(section.lines)
            if section.header_path:
                acc_headers.append(section.header_path)
            acc_tokens += section_tokens

    # Flush any remaining content
    _flush_accumulator()

    return chunks


# -----------------------------------------------------------------------------
# Chunking: Line-aligned splitting for large AST nodes
# -----------------------------------------------------------------------------


def _chunk_lines_aligned(
    lines: list[str],
    file_path: str,
    software: str,
    start_line_offset: int,
    symbol: str,
    max_tokens: int,
    overlap_lines: int = 3,
) -> list[Chunk]:
    """Split source lines into chunks at line boundaries respecting token budget.

    Args:
        lines: Source code lines (already extracted for a node)
        file_path: Path for metadata
        software: Package name
        start_line_offset: 1-indexed line number where these lines start in original file
        symbol: Symbol name (function/class) for metadata
        max_tokens: Maximum tokens per chunk
        overlap_lines: Number of lines to overlap between chunks for context

    Returns:
        List of Chunk objects with line-aligned boundaries
    """
    if not lines:
        return []

    tokenizer = _get_tokenizer()
    chunks = []
    chunk_idx = 0
    lines_emitted = 0

    while lines_emitted < len(lines):
        # Start from current position (with overlap from previous chunk)
        start_idx = lines_emitted
        chunk_lines = []
        token_count = 0

        # Accumulate lines until we approach token budget
        idx = start_idx
        while idx < len(lines):
            line = lines[idx]
            line_tokens = len(tokenizer.encode(line + "\n"))

            # If adding this line exceeds budget and we have content, stop
            if token_count + line_tokens > max_tokens and chunk_lines:
                break

            chunk_lines.append(line)
            token_count += line_tokens
            idx += 1

        if chunk_lines:
            chunk_content = "\n".join(chunk_lines)
            chunk_start = start_line_offset + start_idx
            chunk_end = start_line_offset + start_idx + len(chunk_lines) - 1

            chunks.append(
                Chunk(
                    chunk_id=_make_chunk_id(f"{file_path}:{symbol}", chunk_idx),
                    software=software,
                    file_path=file_path,
                    start_line=chunk_start,
                    end_line=chunk_end,
                    symbol=symbol,
                    content=chunk_content,
                )
            )
            chunk_idx += 1

            # Move forward, but keep overlap_lines for context
            new_emitted = start_idx + len(chunk_lines)
            if new_emitted < len(lines):
                lines_emitted = new_emitted - overlap_lines
                lines_emitted = max(lines_emitted, start_idx + 1)  # Ensure progress
            else:
                lines_emitted = new_emitted
        else:
            break

    return chunks


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
        return chunk_fixed_width(content, file_path, software, chunk_size=max_tokens)

    lines = content.split("\n")
    chunks = []
    tokenizer = _get_tokenizer()

    # Extract top-level classes and functions only (not nested)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
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
                # Large node: split at line boundaries for readable chunks
                sub_chunks = _chunk_lines_aligned(
                    node_lines,
                    file_path,
                    software,
                    start_line_offset=start_line,
                    symbol=symbol,
                    max_tokens=max_tokens,
                )
                chunks.extend(sub_chunks)

    # Also capture module-level docstring if present (as raw source lines)
    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        doc_node = tree.body[0]
        doc_start = doc_node.lineno
        doc_end = doc_node.end_lineno or doc_start
        doc_content = "\n".join(lines[doc_start - 1 : doc_end])
        chunks.insert(
            0,
            Chunk(
                chunk_id=_make_chunk_id(f"{file_path}:module_doc", 0),
                software=software,
                file_path=file_path,
                start_line=doc_start,
                end_line=doc_end,
                symbol="__module__",
                content=doc_content,
            ),
        )

    # If no functions/classes found, fall back to fixed-width
    if not chunks:
        return chunk_fixed_width(content, file_path, software, chunk_size=max_tokens)

    return chunks


# -----------------------------------------------------------------------------
# Chunking: cAST / astchunk (Method D)
# -----------------------------------------------------------------------------

# Conversion factor: tokens to non-whitespace characters
# astchunk measures chunk size in non-whitespace chars, not tokens
# Empirically ~2.5 non-ws chars per token for Python code, using 3 conservatively
CAST_TOKENS_TO_NONWS_CHARS = 3


def chunk_cast(
    content: str,
    file_path: str,
    software: str,
    chunk_size: int = 800,
) -> list[Chunk]:
    """Chunk Python source using astchunk (cAST method).

    Uses chunk_expansion to prepend context headers (filepath, class/function ancestors)
    to each chunk for better retrieval.

    Args:
        content: Python source code
        file_path: Path for locator metadata
        software: Package name
        chunk_size: Maximum tokens per chunk (converted internally)

    Returns:
        List of Chunk objects
    """
    from astchunk import ASTChunkBuilder

    # Convert tokens to non-whitespace characters (astchunk's unit)
    max_nonws_chars = chunk_size * CAST_TOKENS_TO_NONWS_CHARS

    builder = ASTChunkBuilder(
        max_chunk_size=max_nonws_chars,
        language="python",
        metadata_template="default",
    )

    try:
        # Enable chunk_expansion for context headers (filepath, class/function path)
        result = builder.chunkify(
            content,
            chunk_expansion=True,
            chunk_overlap=1,
            repo_level_metadata={"filepath": file_path},
        )
    except Exception:
        # Fall back to fixed-width for unparseable files
        return chunk_fixed_width(content, file_path, software, chunk_size=chunk_size)

    if not result:
        return chunk_fixed_width(content, file_path, software, chunk_size=chunk_size)

    chunks = []
    for i, item in enumerate(result):
        # Content already includes context header from chunk_expansion
        chunk_content = item.get("content", "")
        metadata = item.get("metadata", {})

        # Extract line numbers from metadata
        start_line = metadata.get("start_line_no", 1)
        end_line = metadata.get("end_line_no", start_line)

        chunks.append(
            Chunk(
                chunk_id=_make_chunk_id(f"{file_path}:{i}", i),
                software=software,
                file_path=file_path,
                start_line=start_line,
                end_line=end_line,
                symbol=None,  # astchunk doesn't provide symbol name directly
                content=chunk_content,
            )
        )

    return chunks


# -----------------------------------------------------------------------------
# Chunking: code-chunk JSONL loader (Method C)
# -----------------------------------------------------------------------------


def load_chunks_from_jsonl(jsonl_path: str | Path) -> list[Chunk]:
    """Load chunks from code-chunk JSONL output.

    Uses contextualizedText as chunk content for better retrieval.
    The contextualizedText includes scope chain (e.g., "Scope: Kpoints")
    and entity definitions that help BM25 match class-method queries.

    Args:
        jsonl_path: Path to JSONL file from chunk_with_context.mjs

    Returns:
        List of Chunk objects
    """
    chunks = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)

            # Use contextualizedText (includes scope/entity headers)
            content = data.get("contextualizedText") or data.get("text", "")

            # Parse line range [start, end]
            line_range = data.get("lineRange", [1, 1])
            start_line = line_range[0] if isinstance(line_range, list) else 1
            end_line = line_range[1] if isinstance(line_range, list) else start_line

            # Extract symbol from context.entities[0].name
            symbol = None
            ctx = data.get("context", {})
            entities = ctx.get("entities", [])
            if entities:
                symbol = entities[0].get("name")

            chunk_id = _make_chunk_id(data["filepath"], data.get("index", 0))

            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    software=data["software"],
                    file_path=data["filepath"],
                    start_line=start_line,
                    end_line=end_line,
                    symbol=symbol,
                    content=content,
                )
            )

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
            # Single-file module: return parent directory
            return origin.parent

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
        method: Chunking method ("fixed", "ast", or "cast")
        chunk_size: Token size for fixed-width chunking

    Returns:
        List of all chunks.
    """
    chunks = []
    if method == "cast":
        chunk_fn = chunk_cast
    elif method == "ast":
        chunk_fn = chunk_ast
    else:
        chunk_fn = chunk_fixed_width

    for py_file in source_dir.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        if not content.strip():
            continue

        rel_path = str(py_file.relative_to(source_dir.parent))
        file_chunks = chunk_fn(content, rel_path, software, chunk_size)
        chunks.extend(file_chunks)

    return chunks


# -----------------------------------------------------------------------------
# Search API
# -----------------------------------------------------------------------------


def search(
    index,  # BaseRetriever or RagIndex (backward compat)
    query: str,
    top_k: int = 5,
    software: list[str] | None = None,
) -> list[SearchResult]:
    """Search the RAG index and return list of results.

    Args:
        index: Retriever instance (BaseRetriever or legacy RagIndex).
        query: Search query.
        top_k: Number of results.
        software: Optional package filter.

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


def _rrf_fuse(
    ranked_lists: list[list[tuple[Chunk, float]]],
    k: int = 60,
) -> list[tuple[Chunk, float]]:
    """Reciprocal Rank Fusion of multiple ranked lists.

    Combines multiple ranked result lists into a single fused ranking.
    RRF score = sum(1 / (k + rank)) across all lists where the chunk appears.

    Args:
        ranked_lists: List of ranked results, each is [(Chunk, score), ...].
        k: RRF constant (default 60, per original RRF paper).

    Returns:
        Fused ranked list sorted by RRF score descending.
    """
    scores: dict[str, float] = {}  # chunk_id -> accumulated RRF score
    chunks: dict[str, Chunk] = {}  # chunk_id -> Chunk

    for ranked_list in ranked_lists:
        for rank, (chunk, _) in enumerate(ranked_list, start=1):
            rrf_score = 1.0 / (k + rank)
            if chunk.chunk_id not in scores:
                scores[chunk.chunk_id] = 0.0
                chunks[chunk.chunk_id] = chunk
            scores[chunk.chunk_id] += rrf_score

    fused = [(chunks[cid], score) for cid, score in scores.items()]
    fused.sort(key=lambda x: x[1], reverse=True)
    return fused


def search_multi(
    index,  # BaseRetriever
    queries: list[str],
    top_k: int = 5,
    software: list[str] | None = None,
    per_query_k: int = 20,
    rrf_k: int = 60,
) -> list[SearchResult]:
    """Multi-query search with RRF fusion.

    Retrieves results for each query, then fuses with Reciprocal Rank Fusion.

    Args:
        index: Retriever instance.
        queries: List of search queries (paraphrases of the same question).
        top_k: Number of final results to return.
        software: Optional package filter.
        per_query_k: Results to retrieve per query before fusion.
        rrf_k: RRF constant (default 60).

    Returns:
        List of SearchResult with source location and code snippet.
    """
    # Retrieve for each query
    ranked_lists = []
    for q in queries:
        results = index.search(q, top_k=per_query_k, software_filter=software)
        ranked_lists.append(results)

    # Fuse with RRF
    fused = _rrf_fuse(ranked_lists, k=rrf_k)

    # Convert to SearchResult
    return [
        SearchResult(
            source=f"{c.file_path}:{c.start_line}-{c.end_line}",
            snippet=c.content,
        )
        for c, _ in fused[:top_k]
    ]
