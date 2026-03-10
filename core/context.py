"""Unified zone-based context window management for long-running agent workflows.

Single mechanism that fires when total tokens exceed context_window (1.0x trigger).
Four zones measured from END (newest to oldest):
  Zone 1 (newest 30%):  Protected -- no modification
  Zone 2 (next 20%):    Soft-trim -- tool-responses trimmed to head+tail
  Zone 3 (next 25%):    Hard-clear -- tool-responses replaced with placeholder
  Zone 4 (oldest 25%):  Truncate -- all messages removed, single marker

Pruned-result caching in the wrapper provides hysteresis: ~8 stable turns
between triggers, preserving LLM provider cache hits.
"""

from __future__ import annotations

import logging
from copy import deepcopy

logger = logging.getLogger(__name__)

# --- Constants ---

_CHARS_PER_TOKEN = 4  # standard approximation for English/code text

_SOFT_TRIM_MAX_CHARS = 4_000
_SOFT_TRIM_HEAD_CHARS = 1_500
_SOFT_TRIM_TAIL_CHARS = 1_500
_HARD_CLEAR_PLACEHOLDER = "[Old tool result content cleared]"

# Zone boundaries (fraction of non-bootstrap message count, measured from END)
_ZONE_PROTECT = 0.30       # newest 30%: fully protected
_ZONE_SOFT_TRIM = 0.50     # next 20%: soft-trim tool-responses
_ZONE_HARD_CLEAR = 0.75    # next 25%: hard-clear tool-responses
# oldest 25%: removed entirely (truncation zone)

_MSG_SIZE_CAP_FRACTION = 0.20  # cap any single message exceeding 20% of context window

_TRUNCATION_MARKER = (
    "[Context truncated: {n} messages from earlier steps were removed "
    "to fit within the context window. Continue with the current task "
    "using the remaining context.]"
)


# --- Helpers ---

def _get_content_str(message) -> str:
    """Extract content as string from a ChatMessage or dict."""
    if isinstance(message, dict):
        content = message.get("content")
    else:
        content = getattr(message, "content", None)

    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "") for block in content if isinstance(block, dict)
        )
    return str(content)


def _set_content_str(message, new_content: str):
    """Set content string on a ChatMessage or dict."""
    if isinstance(message, dict):
        message["content"] = new_content
    elif hasattr(message, "content"):
        if isinstance(message.content, list):
            for block in message.content:
                if isinstance(block, dict) and block.get("type") == "text":
                    block["text"] = new_content
                    return
            message.content = new_content
        else:
            message.content = new_content


def _get_role(message) -> str:
    """Get role string from ChatMessage or dict."""
    if isinstance(message, dict):
        return message.get("role", "")
    role = getattr(message, "role", "")
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


def _make_marker(n: int) -> dict:
    """Create a truncation marker message compatible with smolagents.

    Uses list-format content so smolagents' get_clean_message_list() can merge
    it with adjacent same-role messages without assertion errors.
    """
    text = _TRUNCATION_MARKER.format(n=n)
    return {
        "role": "user",
        "content": [{"type": "text", "text": text}],
    }


def _count_tokens(messages: list, model_id: str) -> int:
    """Count tokens using litellm, with char/4 fallback."""
    try:
        import litellm
        msg_dicts = []
        for m in messages:
            role = _get_role(m)
            if role == "tool-response":
                role = "user"
            elif role == "tool-call":
                role = "assistant"
            msg_dicts.append({"role": role, "content": _get_content_str(m)})
        return litellm.token_counter(model=model_id, messages=msg_dicts)
    except Exception:
        total_chars = sum(len(_get_content_str(m)) for m in messages)
        return total_chars // _CHARS_PER_TOKEN


# --- Zone-based context management ---

def _cap_oversized_messages(messages: list, context_tokens: int, bootstrap_end: int) -> bool:
    """Truncate any single message exceeding 20% of context window.

    Skips bootstrap messages (system + first user). Returns True if any
    message was capped.
    """
    max_chars = int(context_tokens * _CHARS_PER_TOKEN * _MSG_SIZE_CAP_FRACTION)
    capped = False
    for i in range(bootstrap_end, len(messages)):
        content = _get_content_str(messages[i])
        if len(content) > max_chars:
            half = max_chars // 2
            new_content = (
                content[:half]
                + f"\n...[capped: {len(content):,} chars exceeded per-message limit]...\n"
                + content[-half:]
            )
            _set_content_str(messages[i], new_content)
            logger.info(
                "Context pruning: capped message %d from %d to %d chars",
                i, len(content), len(new_content),
            )
            capped = True
    return capped


def _enforce_token_cap(
    messages: list, context_tokens: int, model_id: str
) -> list:
    """Zone-based context truncation.

    Trigger: total_tokens > context_tokens (1.0x).

    Returns input unchanged (same reference) when under window.
    Returns deepcopy-based result when pruning fires.
    """
    total_tokens = _count_tokens(messages, model_id)
    if total_tokens <= context_tokens:
        return messages

    logger.info(
        "Context pruning: %d tokens exceeds window %d, applying zone-based pruning",
        total_tokens, context_tokens,
    )

    messages = deepcopy(messages)

    first_user_idx = _find_first_user_idx(messages)
    bootstrap_end = first_user_idx + 1

    # Cap oversized individual messages before zone processing
    if _cap_oversized_messages(messages, context_tokens, bootstrap_end):
        total_tokens = _count_tokens(messages, model_id)
        if total_tokens <= context_tokens:
            logger.info(
                "Context pruning: message capping sufficient (%d tokens), "
                "skipping zone pruning", total_tokens,
            )
            return messages

    n_prunable = len(messages) - bootstrap_end
    if n_prunable <= 0:
        return messages

    zone4_end = bootstrap_end + max(int(n_prunable * (1.0 - _ZONE_HARD_CLEAR)), 1)
    zone3_end = bootstrap_end + max(int(n_prunable * (1.0 - _ZONE_SOFT_TRIM)), 1)
    zone2_end = bootstrap_end + max(int(n_prunable * (1.0 - _ZONE_PROTECT)), 1)

    tool_roles = {"tool", "tool-response"}

    # Zone 3: hard-clear tool-responses
    for i in range(zone4_end, zone3_end):
        if _get_role(messages[i]) in tool_roles:
            content = _get_content_str(messages[i])
            if content != _HARD_CLEAR_PLACEHOLDER:
                _set_content_str(messages[i], _HARD_CLEAR_PLACEHOLDER)

    # Zone 2: soft-trim tool-responses
    for i in range(zone3_end, zone2_end):
        if _get_role(messages[i]) in tool_roles:
            content = _get_content_str(messages[i])
            if len(content) > _SOFT_TRIM_MAX_CHARS:
                head = content[:_SOFT_TRIM_HEAD_CHARS]
                tail = content[-_SOFT_TRIM_TAIL_CHARS:]
                _set_content_str(
                    messages[i], head + "\n...[trimmed]...\n" + tail
                )

    # Zone 4: truncate oldest messages
    removed_count = zone4_end - bootstrap_end
    if removed_count > 0:
        result = messages[:bootstrap_end] + [_make_marker(removed_count)] + messages[zone4_end:]
    else:
        result = messages

    result_tokens = _count_tokens(result, model_id)

    if result_tokens <= context_tokens:
        logger.info(
            "Context pruning: zone-based complete (%d -> %d tokens, "
            "removed %d messages, headroom %d tokens)",
            total_tokens, result_tokens, removed_count,
            context_tokens - result_tokens,
        )
        return result

    # Fallback: expand truncation zone progressively
    logger.warning(
        "Context pruning: zone-based insufficient (%d tokens > %d), "
        "expanding truncation zone",
        result_tokens, context_tokens,
    )

    remaining = messages[zone4_end:]
    assistant_indices = [
        i for i, m in enumerate(remaining) if _get_role(m) == "assistant"
    ]

    for keep_count in range(len(assistant_indices) - 1, 0, -1):
        tail_start_in_remaining = assistant_indices[-keep_count]
        expanded_removed = zone4_end - bootstrap_end + tail_start_in_remaining
        candidate = (
            messages[:bootstrap_end]
            + [_make_marker(expanded_removed)]
            + remaining[tail_start_in_remaining:]
        )
        candidate_tokens = _count_tokens(candidate, model_id)
        if candidate_tokens <= context_tokens:
            logger.info(
                "Context pruning: expanded truncation (%d -> %d tokens, "
                "keeping last %d turns)",
                total_tokens, candidate_tokens, keep_count,
            )
            return candidate

    # Last resort: bootstrap + marker only
    removed_count = len(messages) - bootstrap_end
    candidate = messages[:bootstrap_end] + [_make_marker(removed_count)]
    logger.warning(
        "Context pruning: removed all %d non-bootstrap messages", removed_count
    )
    return candidate


# --- Public API ---

def manage_context(
    messages: list, context_tokens: int, model_id: str
) -> list:
    """Zone-based context management.

    Single unified mechanism: fires when total tokens exceed context_window.
    No-op when total tokens <= context_window, preserving cache hits.
    """
    return _enforce_token_cap(messages, context_tokens, model_id)


def wrap_model_with_context_management(model, context_tokens: int, model_id: str):
    """Wrap model.generate with zone-based context management + caching.

    Caching ensures hysteresis: after pruning creates ~40% headroom,
    subsequent calls build from the cached pruned result + new messages,
    staying under the window for ~8 turns without re-pruning.
    """
    original_generate = model.generate
    _state: dict = {"snapshot": None, "seen_count": 0}

    def managed_generate(messages, **kwargs):
        snapshot = _state["snapshot"]
        seen = _state["seen_count"]

        if snapshot is not None and len(messages) >= seen:
            candidate = snapshot + list(messages[seen:])
        else:
            candidate = messages

        result = manage_context(candidate, context_tokens, model_id)

        if result is not candidate:
            _state["snapshot"] = result
            _state["seen_count"] = len(messages)
        elif snapshot is not None:
            _state["snapshot"] = candidate
            _state["seen_count"] = len(messages)

        return original_generate(result, **kwargs)

    model.generate = managed_generate
    logger.info(
        "Context management enabled: context_window=%d tokens, "
        "zones=[protect=%.0f%%, soft-trim=%.0f%%, hard-clear=%.0f%%, truncate=%.0f%%]",
        context_tokens,
        _ZONE_PROTECT * 100,
        (_ZONE_SOFT_TRIM - _ZONE_PROTECT) * 100,
        (_ZONE_HARD_CLEAR - _ZONE_SOFT_TRIM) * 100,
        (1.0 - _ZONE_HARD_CLEAR) * 100,
    )
    return model
