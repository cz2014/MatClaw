"""Context window management for long-running agent workflows.

Two-layer defense against context overflow:
  Layer 1: OpenClaw-style pruning (char-based soft-trim + hard-clear)
  Layer 2: Hard token cap using litellm.token_counter() for accuracy

See plan_e.md for design rationale and OpenClaw verification.
"""

from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any

logger = logging.getLogger(__name__)

# --- Constants ---

_CHARS_PER_TOKEN = 4  # standard approximation for English/code text

# OpenClaw default settings (from settings.ts)
_SOFT_TRIM_RATIO = 0.30
_HARD_CLEAR_RATIO = 0.50
_MIN_PRUNABLE_TOOL_CHARS = 50_000
_KEEP_LAST_ASSISTANTS = 3
_SOFT_TRIM_MAX_CHARS = 4_000
_SOFT_TRIM_HEAD_CHARS = 1_500
_SOFT_TRIM_TAIL_CHARS = 1_500
_HARD_CLEAR_PLACEHOLDER = "[Old tool result content cleared]"

# Layer 2 headroom (match OpenClaw CONTEXT_INPUT_HEADROOM_RATIO)
_HEADROOM_RATIO = 0.75


# --- Helpers ---

def _get_content_str(message) -> str:
    """Extract content as string from a ChatMessage or dict.

    ChatMessage.content can be str, list[dict], or None.
    For list content (multimodal), concatenate text elements.
    """
    if isinstance(message, dict):
        content = message.get("content")
    else:
        content = getattr(message, "content", None)

    if content is None:
        return ""
    if isinstance(content, str):
        return content
    # list of dicts (multimodal content blocks)
    if isinstance(content, list):
        return "".join(
            block.get("text", "") for block in content if isinstance(block, dict)
        )
    return str(content)


def _set_content_str(message, new_content: str):
    """Set content string on a ChatMessage or dict.

    For ChatMessage with list content, replaces the first text block.
    """
    if isinstance(message, dict):
        message["content"] = new_content
    elif hasattr(message, "content"):
        if isinstance(message.content, list):
            # Replace text in first text block, keep other blocks
            for block in message.content:
                if isinstance(block, dict) and block.get("type") == "text":
                    block["text"] = new_content
                    return
            # No text block found, replace entire content
            message.content = new_content
        else:
            message.content = new_content


def _get_role(message) -> str:
    """Get role string from ChatMessage or dict."""
    if isinstance(message, dict):
        return message.get("role", "")
    role = getattr(message, "role", "")
    # MessageRole enum has .value
    return role.value if hasattr(role, "value") else str(role)


def _total_chars(messages) -> int:
    """Sum of all message content lengths."""
    return sum(len(_get_content_str(m)) for m in messages)


def _find_first_user_idx(messages) -> int:
    """Find index of first user message (bootstrap boundary)."""
    for i, m in enumerate(messages):
        if _get_role(m) == "user":
            return i
    return 0


def _find_protect_from(messages) -> int:
    """Find the index from which messages are protected (last N assistants).

    Returns the index of the (N-th from last) assistant message.
    Messages at this index and beyond are protected from pruning.
    """
    assistant_indices = [
        i for i, m in enumerate(messages) if _get_role(m) == "assistant"
    ]
    if len(assistant_indices) >= _KEEP_LAST_ASSISTANTS:
        return assistant_indices[-_KEEP_LAST_ASSISTANTS]
    return len(messages)


def _find_prunable_tool_indices(
    messages, first_user_idx: int, protect_from: int
) -> list[int]:
    """Return indices of tool result messages in the prunable zone.

    Prunable zone: after first user message, before the protected tail.
    Only tool-response / tool role messages are prunable.
    """
    tool_roles = {"tool", "tool-response"}
    return [
        i
        for i in range(first_user_idx + 1, min(protect_from, len(messages)))
        if _get_role(messages[i]) in tool_roles
    ]


# --- Layer 1: OpenClaw-style pruning ---

def _soft_trim(messages, prunable_indices: list[int]) -> list[int]:
    """Soft-trim oversized tool results to head+tail.

    Modifies messages in place. Returns list of indices that were trimmed.
    """
    trimmed = []
    for i in prunable_indices:
        content = _get_content_str(messages[i])
        if len(content) <= _SOFT_TRIM_MAX_CHARS:
            continue
        head = content[:_SOFT_TRIM_HEAD_CHARS]
        tail = content[-_SOFT_TRIM_TAIL_CHARS:]
        new_content = head + "\n...[trimmed]...\n" + tail
        _set_content_str(messages[i], new_content)
        trimmed.append(i)
    return trimmed


def _hard_clear(
    messages, prunable_indices: list[int], char_window: int
) -> list[int]:
    """Hard-clear oldest tool results one by one until ratio < hard_clear_ratio.

    Greedy: stops immediately when ratio drops below threshold.
    Precondition: at least _MIN_PRUNABLE_TOOL_CHARS of prunable content.
    """
    # Check precondition: enough prunable content
    prunable_chars = sum(
        len(_get_content_str(messages[i])) for i in prunable_indices
    )
    if prunable_chars < _MIN_PRUNABLE_TOOL_CHARS:
        return []

    cleared = []
    total = _total_chars(messages)

    # Iterate oldest to newest
    for i in prunable_indices:
        ratio = total / char_window if char_window > 0 else 0
        if ratio < _HARD_CLEAR_RATIO:
            break

        content = _get_content_str(messages[i])
        # Skip already-cleared messages
        if content == _HARD_CLEAR_PLACEHOLDER:
            continue

        old_len = len(content)
        _set_content_str(messages[i], _HARD_CLEAR_PLACEHOLDER)
        total -= old_len - len(_HARD_CLEAR_PLACEHOLDER)
        cleared.append(i)

    return cleared


def prune_messages(messages: list, char_window: int) -> list:
    """Prune old tool results based on context pressure (Layer 1).

    Follows OpenClaw's two-stage approach:
    1. Soft-trim (ratio >= 0.30): trim oversized tool results to head+tail
    2. Hard-clear (ratio >= 0.50 after soft-trim): replace oldest one by one

    Protected: last 3 assistant messages, messages before first user message.
    Only modifies tool result messages.

    Args:
        messages: List of ChatMessage objects or dicts.
        char_window: Context window size in characters.

    Returns:
        Modified copy of messages list.
    """
    if not messages or char_window <= 0:
        return messages

    # Work on a deep copy to avoid mutating the original
    messages = deepcopy(messages)

    total = _total_chars(messages)
    ratio = total / char_window

    if ratio < _SOFT_TRIM_RATIO:
        return messages

    # Determine protection boundaries
    first_user_idx = _find_first_user_idx(messages)
    protect_from = _find_protect_from(messages)
    prunable = _find_prunable_tool_indices(messages, first_user_idx, protect_from)

    if not prunable:
        return messages

    # Stage 1: Soft-trim
    trimmed = _soft_trim(messages, prunable)
    if trimmed:
        logger.debug(
            "Context pruning: soft-trimmed %d tool results (ratio was %.2f)",
            len(trimmed), ratio,
        )

    # Recalculate ratio after soft-trim
    total = _total_chars(messages)
    ratio = total / char_window

    if ratio < _HARD_CLEAR_RATIO:
        return messages

    # Stage 2: Hard-clear
    cleared = _hard_clear(messages, prunable, char_window)
    if cleared:
        logger.debug(
            "Context pruning: hard-cleared %d tool results (ratio was %.2f)",
            len(cleared), ratio,
        )

    return messages


# --- Layer 2: Hard token cap ---

def _enforce_token_cap(
    messages: list, max_input_tokens: int, model_id: str
) -> list:
    """Drop oldest unprotected tool results if total tokens exceed cap.

    Uses litellm.token_counter() for accurate model-specific counting.
    Falls back to char/4 estimate if token counting fails.

    Args:
        messages: List of ChatMessage objects or dicts.
        max_input_tokens: Maximum allowed input tokens.
        model_id: LiteLLM model ID for accurate token counting.

    Returns:
        Modified copy of messages (only copies if changes needed).
    """
    # Count tokens
    try:
        import litellm
        # token_counter expects dicts with "role" and "content" keys
        msg_dicts = []
        for m in messages:
            role = _get_role(m)
            # Map tool-response to user for token counting (matches LiteLLM convention)
            if role == "tool-response":
                role = "user"
            elif role == "tool-call":
                role = "assistant"
            msg_dicts.append({"role": role, "content": _get_content_str(m)})
        total_tokens = litellm.token_counter(model=model_id, messages=msg_dicts)
    except Exception:
        # Fallback: char-based estimate
        total_chars = sum(len(_get_content_str(m)) for m in messages)
        total_tokens = total_chars // _CHARS_PER_TOKEN

    if total_tokens <= max_input_tokens:
        return messages

    logger.debug(
        "Token cap: %d tokens exceeds cap %d, dropping old tool results",
        total_tokens, max_input_tokens,
    )

    # Work on a deep copy
    messages = deepcopy(messages)

    # Protection boundaries (same rules as Layer 1)
    first_user_idx = _find_first_user_idx(messages)
    protect_from = _find_protect_from(messages)
    prunable = _find_prunable_tool_indices(messages, first_user_idx, protect_from)

    # Drop oldest tool results until under cap
    for i in prunable:
        if total_tokens <= max_input_tokens:
            break

        content = _get_content_str(messages[i])
        placeholder = "[dropped: context cap exceeded]"
        if content == placeholder:
            continue

        # Estimate tokens saved (char-based, since re-counting is expensive)
        saved_chars = len(content) - len(placeholder)
        saved_tokens = max(saved_chars // _CHARS_PER_TOKEN, 0)

        _set_content_str(messages[i], placeholder)
        total_tokens -= saved_tokens

    return messages


# --- Public API ---

def manage_context(
    messages: list, context_tokens: int, model_id: str
) -> list:
    """Two-layer context management.

    Layer 1: OpenClaw-style pruning (char-based ratios, soft-trim + hard-clear).
    Layer 2: Hard token cap using litellm.token_counter() for accuracy.

    Args:
        messages: List of ChatMessage objects or dicts.
        context_tokens: Effective context window in tokens (may be < model limit).
        model_id: LiteLLM model ID for accurate token counting.

    Returns:
        Pruned/capped copy of messages.
    """
    char_window = context_tokens * _CHARS_PER_TOKEN

    # Layer 1: char-based pruning (soft-trim + hard-clear)
    messages = prune_messages(messages, char_window)

    # Layer 2: accurate token cap
    max_input_tokens = int(context_tokens * _HEADROOM_RATIO)
    messages = _enforce_token_cap(messages, max_input_tokens, model_id)

    return messages


def wrap_model_with_context_management(model, context_tokens: int, model_id: str):
    """Wrap model.generate with two-layer context management.

    Args:
        model: smolagents Model instance (LiteLLMModel or subclass).
        context_tokens: Effective context window in tokens.
        model_id: LiteLLM model ID for token counting.

    Returns:
        The same model instance with generate() monkey-patched.
    """
    original_generate = model.generate

    def managed_generate(messages, **kwargs):
        managed = manage_context(messages, context_tokens, model_id)
        return original_generate(managed, **kwargs)

    model.generate = managed_generate
    logger.info(
        "Context management enabled: context_window=%d tokens, "
        "pruning char_window=%d chars, token cap=%d tokens (%.0f%% headroom)",
        context_tokens,
        context_tokens * _CHARS_PER_TOKEN,
        int(context_tokens * _HEADROOM_RATIO),
        _HEADROOM_RATIO * 100,
    )
    return model
