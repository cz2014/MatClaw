"""Regression tests for the cache_control marker sweep in _inject_cache_control.

Message objects outlive a single call: core/context.py's pruning snapshot retains
them across steps, so a marker set on step N's last message is still attached at
step N+1. Anthropic rejects requests with more than 4 cache_control blocks, so
without the sweep the run dies 3 steps after the first prune (observed in
production 2026-08-19: prune at step 174, crash at step 177 with "A maximum of
4 blocks with cache_control may be provided. Found 5.").
"""

from unittest.mock import patch

from core._smol.models import LiteLLMModel


def _make_model(model_id="anthropic/claude-opus-5"):
    """Create a LiteLLMModel with mocked LiteLLM internals."""
    with patch.object(LiteLLMModel, "__init__", lambda self, *a, **kw: None):
        model = LiteLLMModel.__new__(LiteLLMModel)
        model.model_id = model_id
    return model


def _count_markers(messages):
    n = 0
    for msg in messages:
        content = msg.get("content")
        if isinstance(content, list):
            n += sum(1 for b in content if isinstance(b, dict) and "cache_control" in b)
    return n


def _system_message():
    return {"role": "system", "content": [{"type": "text", "text": "sys prompt"}]}


def test_marker_count_bounded_under_message_reuse():
    """Same message objects re-sent across steps (the pruning-snapshot pattern):
    exactly 2 markers per call, never growing."""
    model = _make_model()
    messages = [_system_message()]
    counts = []
    for step in range(8):
        messages.append({"role": "user", "content": [{"type": "text", "text": f"obs {step}"}]})
        model._inject_cache_control(messages)
        counts.append(_count_markers(messages))
        messages.append({"role": "assistant", "content": [{"type": "text", "text": f"act {step}"}]})
    assert counts == [2] * 8, f"Expected 2 markers every step, got {counts}"
    print("PASS: test_marker_count_bounded_under_message_reuse")


def test_marker_placement():
    """System message's last block and the last message's last block are marked."""
    model = _make_model()
    messages = [
        _system_message(),
        {"role": "user", "content": [{"type": "text", "text": "a"}, {"type": "text", "text": "b"}]},
    ]
    model._inject_cache_control(messages)
    assert "cache_control" in messages[0]["content"][-1]
    assert "cache_control" in messages[1]["content"][-1]
    assert "cache_control" not in messages[1]["content"][0]
    print("PASS: test_marker_placement")


def test_string_content_converted_then_swept_on_reuse():
    """A str-content last message is converted to a marked list; when that same
    object is re-sent later (no longer last), its marker is swept."""
    model = _make_model()
    messages = [_system_message(), {"role": "user", "content": "plain string"}]
    model._inject_cache_control(messages)
    assert isinstance(messages[1]["content"], list)
    assert "cache_control" in messages[1]["content"][-1]

    messages.append({"role": "user", "content": [{"type": "text", "text": "next"}]})
    model._inject_cache_control(messages)
    assert "cache_control" not in messages[1]["content"][-1]
    assert _count_markers(messages) == 2
    print("PASS: test_string_content_converted_then_swept_on_reuse")


def test_non_anthropic_untouched():
    """Non-Anthropic providers get no markers at all."""
    model = _make_model(model_id="gemini/gemini-3.5-flash")
    messages = [_system_message(), {"role": "user", "content": [{"type": "text", "text": "x"}]}]
    model._inject_cache_control(messages)
    assert _count_markers(messages) == 0
    print("PASS: test_non_anthropic_untouched")


def test_anthropic_block_limit_never_exceeded():
    """The API invariant itself: at most 4 cache_control blocks per request,
    even after many calls over a long-lived message list."""
    model = _make_model()
    messages = [_system_message()]
    for step in range(50):
        messages.append({"role": "user", "content": [{"type": "text", "text": f"obs {step}"}]})
        model._inject_cache_control(messages)
        assert _count_markers(messages) <= 4, f"step {step}: {_count_markers(messages)} markers"
    print("PASS: test_anthropic_block_limit_never_exceeded")


if __name__ == "__main__":
    test_marker_count_bounded_under_message_reuse()
    test_marker_placement()
    test_string_content_converted_then_swept_on_reuse()
    test_non_anthropic_untouched()
    test_anthropic_block_limit_never_exceeded()
    print("\nAll tests passed.")
