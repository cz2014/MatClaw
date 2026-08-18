#!/usr/bin/env python3
"""Tests for unified zone-based context management (core/context.py).

Unit tests only: synthetic messages testing zone-based pruning and caching (no LLM, fast).

Usage: python tests/test_context_pruning.py   (or: pytest)
"""

from __future__ import annotations

import sys
from pathlib import Path

from core.context import (
    _HARD_CLEAR_PLACEHOLDER,
    _enforce_token_cap,
    _get_content_str,
    _get_role,
    wrap_model_with_context_management,
)

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

def _msg(role: str, content: str) -> dict:
    """Create a simple message dict."""
    return {"role": role, "content": content}


def _build_conversation(
    n_tool_assistant_pairs: int,
    tool_content_size: int = 20_000,
    system_size: int = 2000,
) -> list[dict]:
    """Build a synthetic conversation with system + user + N tool/assistant pairs."""
    messages = [
        _msg("system", "System prompt " + "S" * system_size),
        _msg("user", "Task description for testing"),
    ]
    for i in range(n_tool_assistant_pairs):
        messages.append(
            _msg("tool-response", f"RAG result {i}: " + "x" * tool_content_size)
        )
        messages.append(
            _msg("assistant", f"Step {i} reasoning about the results")
        )
    return messages


def _count_role(messages, role: str) -> int:
    """Count messages with given role."""
    return sum(1 for m in messages if m.get("role") == role)


# ---------------------------------------------------------------------------
# Zone-based unit tests
# ---------------------------------------------------------------------------

def test_zone_truncation_removes_oldest():
    """Zone 4 (oldest 25%) is removed entirely."""
    msgs = _build_conversation(20, tool_content_size=10_000)
    result = _enforce_token_cap(msgs, context_tokens=20_000, model_id="unknown-model")

    assert len(result) < len(msgs)
    marker_msgs = [m for m in result if "Context truncated" in _get_content_str(m)]
    assert len(marker_msgs) == 1
    print("  PASS: test_zone_truncation_removes_oldest")


def test_zone_hard_clear_applied():
    """Zone 3 tool-responses are hard-cleared."""
    msgs = _build_conversation(20, tool_content_size=10_000)
    result = _enforce_token_cap(msgs, context_tokens=20_000, model_id="unknown-model")

    cleared = [m for m in result if _get_content_str(m) == _HARD_CLEAR_PLACEHOLDER]
    assert len(cleared) > 0
    print("  PASS: test_zone_hard_clear_applied")


def test_zone_soft_trim_applied():
    """Zone 2 tool-responses are soft-trimmed."""
    msgs = _build_conversation(20, tool_content_size=10_000)
    result = _enforce_token_cap(msgs, context_tokens=20_000, model_id="unknown-model")

    trimmed = [m for m in result if "...[trimmed]..." in _get_content_str(m)]
    assert len(trimmed) > 0
    print("  PASS: test_zone_soft_trim_applied")


def test_zone_protected_tail_intact():
    """Zone 1 (newest 30%) is fully intact."""
    msgs = _build_conversation(20, tool_content_size=10_000)
    original_last_tool = _get_content_str(msgs[-2])  # last tool-response (second to last msg)
    result = _enforce_token_cap(msgs, context_tokens=20_000, model_id="unknown-model")

    result_last_tool = _get_content_str(result[-2])
    assert result_last_tool == original_last_tool
    print("  PASS: test_zone_protected_tail_intact")


def test_zone_single_marker():
    """Only one truncation marker, regardless of how many messages removed."""
    msgs = _build_conversation(20, tool_content_size=10_000)
    result = _enforce_token_cap(msgs, context_tokens=20_000, model_id="unknown-model")

    markers = [m for m in result if "Context truncated" in _get_content_str(m)]
    assert len(markers) == 1
    print("  PASS: test_zone_single_marker")


def test_zone_preserves_message_order():
    """Bootstrap comes first, then marker, then zones 3->2->1."""
    msgs = _build_conversation(20, tool_content_size=10_000)
    result = _enforce_token_cap(msgs, context_tokens=20_000, model_id="unknown-model")

    assert _get_role(result[0]) == "system"
    assert _get_role(result[1]) == "user"
    assert "Context truncated" not in _get_content_str(result[1])
    assert _get_role(result[2]) == "user"
    assert "Context truncated" in _get_content_str(result[2])
    # After marker, conversation continues with tool-response/assistant pairs
    assert _get_role(result[3]) in ("tool-response", "assistant")
    print("  PASS: test_zone_preserves_message_order")


def test_zone_fallback_expands_truncation():
    """When zone-based pruning is insufficient, truncation zone expands."""
    msgs = _build_conversation(5, tool_content_size=50_000)
    result = _enforce_token_cap(msgs, context_tokens=15_000, model_id="unknown-model")

    assistant_count = sum(1 for m in result if _get_role(m) == "assistant")
    assert assistant_count >= 1
    print("  PASS: test_zone_fallback_expands_truncation")


def test_zone_bootstrap_only_fallback():
    """When even 1 turn doesn't fit, return bootstrap + marker only."""
    msgs = _build_conversation(5, tool_content_size=50_000)
    # 600 tokens: too small for even 1 turn (assistant ~9 tokens + tool-response ~12500 tokens)
    result = _enforce_token_cap(msgs, context_tokens=600, model_id="unknown-model")

    assert len(result) <= 3  # system + user + marker
    assert _get_role(result[0]) == "system"
    assert "Context truncated" in _get_content_str(result[-1])
    print("  PASS: test_zone_bootstrap_only_fallback")


def test_no_truncation_when_under_window():
    """No changes when total tokens are under context_tokens."""
    msgs = _build_conversation(2, tool_content_size=1_000)
    result = _enforce_token_cap(msgs, context_tokens=100_000, model_id="unknown-model")
    assert result is msgs  # same reference -- no copy made
    assert len(result) == len(msgs)
    print("  PASS: test_no_truncation_when_under_window")


# ---------------------------------------------------------------------------
# Per-message size cap tests
# ---------------------------------------------------------------------------

def test_oversized_message_capped():
    """A single huge message is capped before zone processing."""
    msgs = _build_conversation(5, tool_content_size=1_000)
    # Insert a 100K-char message in the protected zone (last position)
    # With context_tokens=10000, 20% cap = 2000 tokens = 8000 chars
    msgs.append(_msg("tool-response", "huge: " + "X" * 100_000))
    msgs.append(_msg("assistant", "final reasoning"))
    result = _enforce_token_cap(msgs, context_tokens=10_000, model_id="unknown-model")
    # The huge message should be capped, not cause last-resort fallback
    last_tool = [m for m in result if "huge:" in _get_content_str(m)]
    assert len(last_tool) == 1
    content = _get_content_str(last_tool[0])
    assert "capped" in content
    assert len(content) < 10_000  # capped, not original 100K
    # Other messages should survive (not bootstrap-only fallback)
    assistant_msgs = [m for m in result if _get_role(m) == "assistant"]
    assert len(assistant_msgs) >= 1
    print("  PASS: test_oversized_message_capped")


def test_oversized_message_cap_sufficient_skips_zones():
    """When message capping alone brings context under window, skip zones."""
    msgs = [
        _msg("system", "S" * 2000),
        _msg("user", "task"),
        _msg("assistant", "step 1"),
        _msg("tool-response", "big: " + "B" * 50_000),  # ~12.5K tokens via chars/4
        _msg("assistant", "step 2"),
        _msg("tool-response", "small result"),
        _msg("assistant", "step 3"),
    ]
    # Window = 20K tokens. The 50K-char message = ~12.5K tokens (>20% cap).
    # After capping to 20% (4K tokens = 16K chars), total should fit.
    result = _enforce_token_cap(msgs, context_tokens=20_000, model_id="unknown-model")
    # All messages should survive (no truncation marker)
    markers = [m for m in result if "Context truncated" in _get_content_str(m)]
    assert len(markers) == 0
    assert len(result) == len(msgs)
    print("  PASS: test_oversized_message_cap_sufficient_skips_zones")


# ---------------------------------------------------------------------------
# Caching wrapper tests
# ---------------------------------------------------------------------------

class _MockModel:
    """Mock model for testing wrap_model_with_context_management."""

    def __init__(self):
        self.call_count = 0
        self.last_messages = None
        self.context_manager = None  # set by wrap_model_with_context_management (P2/V3 hook)

    def generate(self, messages, **kwargs):
        # Mirror the vendored LiteLLMModel.generate: apply the context hook first.
        if self.context_manager is not None:
            messages = self.context_manager(messages)
        self.call_count += 1
        self.last_messages = messages
        return "mock response"


def test_caching_no_reprune_within_headroom():
    """After pruning, subsequent calls with new messages don't re-prune."""
    model = _MockModel()
    context_tokens = 5_000
    wrap_model_with_context_management(model, context_tokens, "unknown-model")

    # First call: build a conversation that exceeds context_tokens
    msgs = _build_conversation(10, tool_content_size=5_000)
    model.generate(msgs)
    first_result_len = len(model.last_messages)
    assert first_result_len < len(msgs), "Pruning should have fired on first call"

    # Second call: add 1 more pair (simulating smolagents appending)
    msgs_extended = msgs + [
        _msg("tool-response", "new result " + "x" * 1_000),
        _msg("assistant", "new reasoning"),
    ]
    model.generate(msgs_extended)
    second_result_len = len(model.last_messages)

    # Result should be first_result + 2 new messages (no re-pruning)
    assert second_result_len == first_result_len + 2, (
        f"Expected {first_result_len + 2} messages (cached + 2 new), got {second_result_len}"
    )
    print("  PASS: test_caching_no_reprune_within_headroom")


def test_caching_reprune_when_headroom_exhausted():
    """After enough new messages exhaust headroom, re-pruning fires."""
    model = _MockModel()
    context_tokens = 5_000
    wrap_model_with_context_management(model, context_tokens, "unknown-model")

    # First call: triggers pruning
    msgs = _build_conversation(10, tool_content_size=5_000)
    model.generate(msgs)
    first_result_len = len(model.last_messages)

    # Add many large messages to exhaust headroom
    extended = msgs
    for i in range(10):
        extended = extended + [
            _msg("tool-response", f"big result {i}: " + "x" * 5_000),
            _msg("assistant", f"reasoning {i}"),
        ]
    model.generate(extended)

    # Re-pruning should have fired -- result should be shorter than cached + all new
    expected_no_reprune = first_result_len + 20  # 10 pairs = 20 messages
    actual = len(model.last_messages)
    assert actual < expected_no_reprune, (
        f"Expected re-pruning (result {actual} should be < {expected_no_reprune})"
    )
    print("  PASS: test_caching_reprune_when_headroom_exhausted")


def test_caching_prefix_stability():
    """Between triggers, the prefix (cached snapshot) is identical across calls."""
    model = _MockModel()
    context_tokens = 5_000
    wrap_model_with_context_management(model, context_tokens, "unknown-model")

    # First call: triggers pruning
    msgs = _build_conversation(10, tool_content_size=5_000)
    model.generate(msgs)
    first_result = [_get_content_str(m) for m in model.last_messages]

    # Second call: add 1 small pair
    msgs2 = msgs + [
        _msg("tool-response", "small result"),
        _msg("assistant", "small reasoning"),
    ]
    model.generate(msgs2)
    second_result = [_get_content_str(m) for m in model.last_messages]

    # Prefix (all messages except last 2) should be identical
    prefix_len = len(first_result)
    assert second_result[:prefix_len] == first_result, (
        "Prefix should be identical between non-triggering calls"
    )
    print("  PASS: test_caching_prefix_stability")


def test_caching_no_cache_before_first_trigger():
    """Before first trigger, full messages are passed through unchanged."""
    model = _MockModel()
    context_tokens = 100_000  # large enough that pruning won't trigger
    wrap_model_with_context_management(model, context_tokens, "unknown-model")

    msgs = _build_conversation(2, tool_content_size=1_000)
    model.generate(msgs)

    # All messages should be present, unchanged
    assert len(model.last_messages) == len(msgs)
    for i, m in enumerate(msgs):
        assert _get_content_str(model.last_messages[i]) == _get_content_str(m)
    print("  PASS: test_caching_no_cache_before_first_trigger")


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

def run_unit_tests():
    """Run all unit tests."""
    print("Running zone-based unit tests...")
    test_zone_truncation_removes_oldest()
    test_zone_hard_clear_applied()
    test_zone_soft_trim_applied()
    test_zone_protected_tail_intact()
    test_zone_single_marker()
    test_zone_preserves_message_order()
    test_zone_fallback_expands_truncation()
    test_zone_bootstrap_only_fallback()
    test_no_truncation_when_under_window()

    print("\nRunning per-message size cap tests...")
    test_oversized_message_capped()
    test_oversized_message_cap_sufficient_skips_zones()

    print("\nRunning caching wrapper tests...")
    test_caching_no_reprune_within_headroom()
    test_caching_reprune_when_headroom_exhausted()
    test_caching_prefix_stability()
    test_caching_no_cache_before_first_trigger()

    print("\nAll 15 unit tests passed!")


if __name__ == "__main__":
    run_unit_tests()
