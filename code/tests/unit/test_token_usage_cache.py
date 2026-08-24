"""Regression tests for the Anthropic prompt-cache breakdown in TokenUsage.

Anthropic bills a prompt-cache read at a fraction of the base input rate and a
cache write at a premium, so a run's cost cannot be reconstructed from
input_tokens alone. litellm folds both cache counts into prompt_tokens
(llms/anthropic/chat/transformation.py: `prompt_tokens += cache_*`), which makes
them a partition of input_tokens rather than an addition to it -- summing them
with input_tokens would double count. These tests pin both properties.
"""

import dataclasses
from types import SimpleNamespace
from unittest.mock import patch

from core._smol.models import LiteLLMModel, TokenUsage
from core._smol.monitoring import Monitor


def _usage(prompt, completion, read=0, creation=0):
    """A litellm-shaped usage object for an Anthropic response."""
    return SimpleNamespace(
        prompt_tokens=prompt,
        completion_tokens=completion,
        cache_read_input_tokens=read,
        cache_creation_input_tokens=creation,
    )


def _response(usage):
    message = SimpleNamespace(role="assistant", content="hi", tool_calls=None)
    return SimpleNamespace(choices=[SimpleNamespace(message=message)], usage=usage)


def _model_returning(response, model_id="anthropic/claude-opus-5"):
    """A LiteLLMModel wired to hand back one canned litellm response."""
    with patch.object(LiteLLMModel, "__init__", lambda self, *a, **kw: None):
        model = LiteLLMModel.__new__(LiteLLMModel)
    model.model_id = model_id
    model.api_base = None
    model.api_key = "test-key"
    model.custom_role_conversions = None
    model.kwargs = {}
    # short-circuit request building: these tests are about the response side
    model._prepare_completion_kwargs = lambda **kw: {}
    model.client = SimpleNamespace(completion=lambda **kw: response)
    model.retryer = lambda fn, **kw: fn(**kw)
    model._apply_rate_limit = lambda: None
    return model


def test_cache_fields_default_to_zero_and_do_not_inflate_total():
    u = TokenUsage(input_tokens=100, output_tokens=10)
    assert u.cache_read_input_tokens == 0
    assert u.cache_creation_input_tokens == 0
    assert u.total_tokens == 110


def test_cache_counts_partition_input_and_never_add_to_it():
    u = TokenUsage(
        input_tokens=1000, output_tokens=50,
        cache_read_input_tokens=900, cache_creation_input_tokens=60,
    )
    assert u.total_tokens == 1050, "cache counts must not be added on top of input_tokens"
    uncached = u.input_tokens - u.cache_read_input_tokens - u.cache_creation_input_tokens
    assert uncached == 40


def test_dict_and_asdict_carry_the_cache_fields():
    u = TokenUsage(
        input_tokens=7, output_tokens=3,
        cache_read_input_tokens=5, cache_creation_input_tokens=1,
    )
    for d in (u.dict(), dataclasses.asdict(u)):
        assert d["cache_read_input_tokens"] == 5
        assert d["cache_creation_input_tokens"] == 1


def test_addition_is_component_wise():
    a = TokenUsage(input_tokens=10, output_tokens=1, cache_read_input_tokens=6,
                   cache_creation_input_tokens=2)
    b = TokenUsage(input_tokens=20, output_tokens=2, cache_read_input_tokens=15,
                   cache_creation_input_tokens=3)
    total = a + b
    assert (total.input_tokens, total.output_tokens) == (30, 3)
    assert total.cache_read_input_tokens == 21
    assert total.cache_creation_input_tokens == 5
    assert total.total_tokens == 33


def test_generate_once_reads_the_cache_fields_off_the_response():
    model = _model_returning(_response(_usage(5000, 120, read=4500, creation=300)))
    msg = model._generate_once([{"role": "user", "content": "x"}])
    assert msg.token_usage.input_tokens == 5000
    assert msg.token_usage.cache_read_input_tokens == 4500
    assert msg.token_usage.cache_creation_input_tokens == 300


def test_a_provider_without_cache_fields_records_zeros():
    """Gemini/DeepSeek responses carry no cache counts; the fields must not blow up."""
    usage = SimpleNamespace(prompt_tokens=42, completion_tokens=7)
    model = _model_returning(_response(usage), model_id="gemini/gemini-3.5-flash")
    msg = model._generate_once([{"role": "user", "content": "x"}])
    assert msg.token_usage.cache_read_input_tokens == 0
    assert msg.token_usage.cache_creation_input_tokens == 0


def test_monitor_accumulates_cache_counts_and_reports_the_hit_rate():
    logged = []
    logger = SimpleNamespace(log=lambda text, level=1: logged.append(str(text)))
    monitor = Monitor(tracked_model=None, logger=logger)
    for _ in range(2):
        step = SimpleNamespace(
            timing=SimpleNamespace(duration=1.0),
            step_number=None,
            token_usage=TokenUsage(
                input_tokens=1000, output_tokens=10,
                cache_read_input_tokens=900, cache_creation_input_tokens=50,
            ),
        )
        monitor.update_metrics(step)
    total = monitor.get_total_token_counts()
    assert total.input_tokens == 2000
    assert total.cache_read_input_tokens == 1800
    assert total.cache_creation_input_tokens == 100
    assert "Cached: 90.0%" in logged[-1]
    monitor.reset()
    assert monitor.get_total_token_counts().cache_read_input_tokens == 0
