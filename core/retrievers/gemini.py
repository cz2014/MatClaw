"""Gemini embedding implementation."""

from __future__ import annotations

import os
import time

import numpy as np

from .vector import BaseEmbedder

# Environment variable for Gemini API key (users can modify this)
API_KEY_ENV_VAR = "GEMINI_API_KEY"


class GeminiEmbedder(BaseEmbedder):
    """Gemini embedding with rate limiting (3000 RPM, 1M TPM)."""

    MODEL = "gemini-embedding-001"
    BATCH_SIZE = 100
    RPM_LIMIT = 3000
    TPM_LIMIT = 1_000_000
    RATE_SAFETY_FACTOR = 0.7  # Use 70% of rate limits for safety buffer
    MAX_RETRIES = 5
    INITIAL_RETRY_DELAY = 30.0  # seconds

    def __init__(self, query_task_type: str = "RETRIEVAL_QUERY"):
        """Initialize Gemini embedder.

        Args:
            query_task_type: Task type for query embeddings.
                Options: RETRIEVAL_QUERY (for docs), CODE_RETRIEVAL_QUERY (for code).
        """
        self._query_task_type = query_task_type
        self._client = None
        self._last_request_time = 0.0
        self._tokenizer = None

    def _get_client(self):
        """Lazy-load Gemini client with API key from environment."""
        if self._client is None:
            from google import genai

            api_key = os.environ.get(API_KEY_ENV_VAR)
            if not api_key:
                raise ValueError(
                    f"{API_KEY_ENV_VAR} environment variable not set. "
                    "Required for Gemini embeddings."
                )
            self._client = genai.Client(api_key=api_key)
        return self._client

    def _get_tokenizer(self):
        """Lazy-load tiktoken tokenizer."""
        if self._tokenizer is None:
            import tiktoken

            self._tokenizer = tiktoken.get_encoding("cl100k_base")
        return self._tokenizer

    def _count_tokens(self, texts: list[str]) -> int:
        """Count tokens in a list of texts."""
        tokenizer = self._get_tokenizer()
        return sum(len(tokenizer.encode(t)) for t in texts)

    def _rate_limit(self, token_count: int) -> None:
        """Enforce rate limiting based on both RPM and TPM.

        Args:
            token_count: Number of tokens in the upcoming request.
        """
        # Apply safety factor to both limits
        safe_rpm = self.RPM_LIMIT * self.RATE_SAFETY_FACTOR
        safe_tpm = self.TPM_LIMIT * self.RATE_SAFETY_FACTOR

        # Calculate minimum intervals for both limits
        rpm_interval = 60.0 / safe_rpm
        tpm_interval = (token_count / safe_tpm) * 60.0  # seconds for this batch

        # Use the more restrictive limit
        min_interval = max(rpm_interval, tpm_interval)

        elapsed = time.time() - self._last_request_time
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self._last_request_time = time.time()

    def _embed_batch_with_retry(self, client, batch: list[str], batch_num: int, total_batches: int):
        """Embed a single batch with retry logic for rate limit errors."""
        from google.genai import types
        from google.genai.errors import ClientError

        token_count = self._count_tokens(batch)
        delay = self.INITIAL_RETRY_DELAY

        for attempt in range(self.MAX_RETRIES + 1):
            self._rate_limit(token_count)

            try:
                if attempt == 0:
                    print(f"  Embedding batch {batch_num}/{total_batches} ({token_count} tokens)...")
                else:
                    print(f"  Retry {attempt}/{self.MAX_RETRIES} for batch {batch_num}...")

                result = client.models.embed_content(
                    model=self.MODEL,
                    contents=batch,
                    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
                )
                return [np.array(e.values) for e in result.embeddings]

            except ClientError as e:
                if e.status_code == 429 and attempt < self.MAX_RETRIES:
                    print(f"  Rate limit hit, waiting {delay:.0f}s before retry...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    raise

    def embed(self, texts: list[str]) -> np.ndarray:
        """Embed texts using Gemini API with batching and rate limiting."""
        client = self._get_client()
        all_embeddings = []
        total_batches = (len(texts) + self.BATCH_SIZE - 1) // self.BATCH_SIZE

        for i in range(0, len(texts), self.BATCH_SIZE):
            batch = texts[i : i + self.BATCH_SIZE]
            batch_num = i // self.BATCH_SIZE + 1
            embeddings = self._embed_batch_with_retry(client, batch, batch_num, total_batches)
            all_embeddings.extend(embeddings)

        return np.array(all_embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        """Embed a single query using Gemini API."""
        from google.genai import types

        token_count = self._count_tokens([query])
        self._rate_limit(token_count)
        result = self._get_client().models.embed_content(
            model=self.MODEL,
            contents=[query],
            config=types.EmbedContentConfig(task_type=self._query_task_type),
        )
        return np.array(result.embeddings[0].values, dtype=np.float32).reshape(1, -1)
