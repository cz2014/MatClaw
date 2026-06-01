"""Tests for the vendored LiteLLMModel retry / pause logic.

Folded from the former LiteLLMModel subclass into core/_smol/models.py (P2/V3):
generate() wraps _generate_with_empty_retry() with a transient/connection retry + auto-pause loop.
"""

import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core._smol.models import LiteLLMModel


def _make_model():
    """Create a LiteLLMModel with mocked LiteLLM internals."""
    with patch.object(LiteLLMModel, "__init__", lambda self, *a, **kw: None):
        model = LiteLLMModel.__new__(LiteLLMModel)
        model._pause_controller = None
        model.context_manager = None
        model.model_id = "test-model"
        model.EMPTY_RETRIES = 3
        model.EMPTY_RETRY_WAIT = 1.0
        model.TRANSIENT_RETRIES = 3
        model.TRANSIENT_RETRY_WAIT = 0.01  # fast for tests
    return model


def _make_content_policy_error():
    """Create a ContentPolicyViolationError-like exception."""
    return Exception(
        "litellm.ContentPolicyViolationError: OpenAIException - "
        "Invalid prompt: your prompt was flagged as potentially "
        "violating our usage policy."
    )


def _make_connection_error():
    return Exception("Connection timeout: server did not respond")


def _make_auth_error():
    return Exception("AuthenticationError: invalid API key")


def _make_success_response():
    resp = MagicMock()
    resp.content = "test response"
    return resp


def test_transient_error_retry_then_succeed():
    """ContentPolicyViolationError on first call, success on second -- no crash."""
    model = _make_model()
    error = _make_content_policy_error()
    success = _make_success_response()

    call_count = 0

    def mock_generate(messages, stop_sequences=None, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise error
        return success

    model._generate_with_empty_retry = mock_generate

    result = model.generate([], stop_sequences=None)
    assert result.content == "test response"
    assert call_count == 2, f"Expected 2 calls, got {call_count}"
    print("PASS: test_transient_error_retry_then_succeed")


def test_transient_error_exhausts_retries_no_pause():
    """ContentPolicyViolationError on all calls, no pause controller -- raises."""
    model = _make_model()
    error = _make_content_policy_error()
    call_count = 0

    def mock_generate(messages, stop_sequences=None, **kwargs):
        nonlocal call_count
        call_count += 1
        raise error

    model._generate_with_empty_retry = mock_generate

    try:
        model.generate([], stop_sequences=None)
        assert False, "Should have raised"
    except Exception as e:
        assert "usage policy" in str(e)
    # 1 initial + 3 retries = 4 total calls
    assert call_count == 4, f"Expected 4 calls (1 + 3 retries), got {call_count}"
    print("PASS: test_transient_error_exhausts_retries_no_pause")


def test_transient_error_exhausts_retries_then_pauses():
    """ContentPolicyViolationError on all calls, pause controller set -- pauses."""
    model = _make_model()
    error = _make_content_policy_error()
    success = _make_success_response()
    call_count = 0
    pause_called = False

    def mock_generate(messages, stop_sequences=None, **kwargs):
        nonlocal call_count
        call_count += 1
        # Fail for first 4 calls (1 + 3 retries), succeed after pause+resume
        if call_count <= 4:
            raise error
        return success

    model._generate_with_empty_retry = mock_generate

    # Mock pause controller
    pc = MagicMock()

    def mock_request_pause(reason=""):
        nonlocal pause_called
        pause_called = True

    pc.request_pause = mock_request_pause
    pc.wait_if_paused = MagicMock()
    model._pause_controller = pc
    model.set_pause_controller(pc)

    result = model.generate([], stop_sequences=None)
    assert result.content == "test response"
    assert pause_called, "Pause controller should have been called"
    assert call_count == 5, f"Expected 5 calls (4 failed + 1 after resume), got {call_count}"
    print("PASS: test_transient_error_exhausts_retries_then_pauses")


def test_auth_error_raises_immediately():
    """AuthenticationError should raise immediately, no retry."""
    model = _make_model()
    error = _make_auth_error()
    call_count = 0

    def mock_generate(messages, stop_sequences=None, **kwargs):
        nonlocal call_count
        call_count += 1
        raise error

    model._generate_with_empty_retry = mock_generate

    try:
        model.generate([], stop_sequences=None)
        assert False, "Should have raised"
    except Exception as e:
        assert "invalid API key" in str(e)
    assert call_count == 1, f"Expected 1 call (no retry), got {call_count}"
    print("PASS: test_auth_error_raises_immediately")


def test_connection_error_pauses():
    """Connection error should auto-pause (existing behavior)."""
    model = _make_model()
    conn_error = _make_connection_error()
    success = _make_success_response()
    call_count = 0
    pause_called = False

    def mock_generate(messages, stop_sequences=None, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise conn_error
        return success

    model._generate_with_empty_retry = mock_generate

    pc = MagicMock()

    def mock_request_pause(reason=""):
        nonlocal pause_called
        pause_called = True

    pc.request_pause = mock_request_pause
    pc.wait_if_paused = MagicMock()
    model._pause_controller = pc
    model.set_pause_controller(pc)

    result = model.generate([], stop_sequences=None)
    assert result.content == "test response"
    assert pause_called, "Should have paused on connection error"
    assert call_count == 2
    print("PASS: test_connection_error_pauses")


if __name__ == "__main__":
    test_transient_error_retry_then_succeed()
    test_transient_error_exhausts_retries_no_pause()
    test_transient_error_exhausts_retries_then_pauses()
    test_auth_error_raises_immediately()
    test_connection_error_pauses()
    print("\nAll tests passed.")
