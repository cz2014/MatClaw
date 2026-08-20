"""Provider usage calibrates the local context cap without persisted guesses."""

from __future__ import annotations

import logging
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from core._smol.models import ChatMessage, LiteLLMModel, MessageRole, TokenUsage
from core.context import (
    _IMAGE_TOKEN_RESERVE,
    _TokenRatioCalibrator,
    _count_tokens,
    wrap_model_with_context_management,
)


def _msg(text: str):
    return {"role": "user", "content": text}


def test_seed_and_effective_cap():
    calibrator = _TokenRatioCalibrator()
    assert calibrator.ratio == 1.60
    assert calibrator.effective_cap(200_000) == 125_000


def test_ratio_converges_to_paired_provider_usage(monkeypatch):
    calibrator = _TokenRatioCalibrator()
    monkeypatch.setattr("core.context._count_tokens", lambda *_args, **_kwargs: 100_000)
    for _ in range(20):
        calibrator.note_sent([_msg("sent")], "provider/model")
        calibrator.observe_actual(150_000)
    assert calibrator.ratio == pytest.approx(1.5, abs=0.001)
    assert calibrator.samples == 20


def test_feedback_is_paired_with_final_pruned_list(monkeypatch):
    counts = {"full": 180_000, "kept": 100_000}

    def count(messages, _model_id, **_kwargs):
        return counts[messages[-1]["content"]]

    monkeypatch.setattr("core.context._count_tokens", count)
    monkeypatch.setattr(
        "core.context.manage_context",
        lambda _messages, _cap, _model_id, counter=None: [_msg("kept")],
    )
    model = SimpleNamespace(context_manager=None, context_feedback=None)
    wrap_model_with_context_management(model, 200_000, "provider/model")
    # The 1.60 seed makes the effective cap 125k, so this controlled manager
    # returns a smaller list whose 100k count must be paired with 150k actual.
    sent = model.context_manager([_msg("full")])
    model.context_feedback(150_000)
    assert sent[-1]["content"] == "kept"
    assert model.context_calibrator.ratio == pytest.approx(1.57)


def test_retry_reuses_one_managed_prompt_and_reports_same_response(monkeypatch):
    with patch.object(LiteLLMModel, "__init__", lambda self, *args, **kwargs: None):
        model = LiteLLMModel.__new__(LiteLLMModel)
    managed = []
    requested = []
    feedback = []
    result = ChatMessage(
        role=MessageRole.ASSISTANT,
        content="ok",
        token_usage=TokenUsage(input_tokens=321, output_tokens=1),
    )

    def manage(messages):
        final = [*messages, _msg("managed")]
        managed.append(final)
        return final

    def request(messages, **_kwargs):
        requested.append(messages)
        if len(requested) == 1:
            raise RuntimeError("temporarily unavailable")
        return result

    model.context_manager = manage
    model.context_feedback = feedback.append
    model._generate_with_empty_retry = request
    model._pause_controller = None
    model.TRANSIENT_RETRIES = 1
    model.TRANSIENT_RETRY_WAIT = 0
    model.model_id = "provider/model"
    response = model.generate([_msg("raw")])

    assert response is result
    assert len(managed) == 1
    assert requested == [managed[0], managed[0]]
    assert feedback == [321]


def test_invalid_feedback_is_ignored_and_ratio_is_clamped(monkeypatch):
    calibrator = _TokenRatioCalibrator()
    monkeypatch.setattr("core.context._count_tokens", lambda *_args, **_kwargs: 100)
    for actual in (None, 0, -1, float("nan")):
        calibrator.note_sent([_msg("x")], "provider/model")
        calibrator.observe_actual(actual)
    assert calibrator.ratio == 1.60
    assert calibrator.samples == 0

    calibrator.note_sent([_msg("x")], "provider/model")
    calibrator.observe_actual(100_000)
    assert calibrator.ratio == 3.0
    calibrator.note_sent([_msg("x")], "provider/model")
    calibrator.observe_actual(1)
    assert 1.0 <= calibrator.ratio <= 3.0
    before = calibrator.ratio
    calibrator.observe_actual(100)
    assert calibrator.ratio == before


def test_fallback_chars_per_three_warns_once_per_calibrator(monkeypatch, caplog):
    monkeypatch.setattr(
        "litellm.token_counter", lambda **_kwargs: (_ for _ in ()).throw(ValueError("bad"))
    )
    calibrator = _TokenRatioCalibrator()
    with caplog.at_level(logging.WARNING, logger="core.context"):
        first = calibrator.count([_msg("abcdef")], "provider/model")
        second = calibrator.count([_msg("abcdef")], "provider/model")
    assert first == second == 2
    assert sum("using chars//3 fallback" in record.message for record in caplog.records) == 1


def test_images_reserve_two_thousand_tokens_each(monkeypatch):
    monkeypatch.setattr("litellm.token_counter", lambda **_kwargs: 10)
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "look"},
                {"type": "image", "image": object()},
                {"type": "image_url", "image_url": "data:image/png;base64,x"},
            ],
        }
    ]
    assert _count_tokens(messages, "provider/model") == 10 + 2 * _IMAGE_TOKEN_RESERVE


def test_calibrator_is_per_model_instance():
    first = SimpleNamespace(context_manager=None, context_feedback=None)
    second = SimpleNamespace(context_manager=None, context_feedback=None)
    wrap_model_with_context_management(first, 200_000, "provider/model")
    wrap_model_with_context_management(second, 200_000, "provider/model")
    assert first.context_calibrator is not second.context_calibrator
    first.context_calibrator._pending_count = 100
    first.context_feedback(300)
    assert first.context_calibrator.ratio != second.context_calibrator.ratio
    assert second.context_calibrator.ratio == 1.60
