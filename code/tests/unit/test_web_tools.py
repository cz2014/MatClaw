"""Unit tests for the web-access tools (web_fetch + web_search) and the config plumbing.

Fully offline -- no live HTTP, no live LLM, no API key. `requests.get` and
`litellm.completion` are mocked. Covers:
  A. web_fetch: URL normalization + fetch/markdown/truncation/headers/errors.
  B. web_search (WebSearchTool): the grounding call, source extraction + redirect
     resolution, capping, answer-only fallback, and fail-soft error reporting.
  C. _resolve_web_search: model/key fallbacks; key comes from the config template,
     NOT a hardcoded env-var name.
  D. _filter_disabled_tools: removal + fail-fast guards.

See docs/exec-plans/active/2026-06-05_web-access-tools.md S9.1-9.4.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from core.agent import _filter_disabled_tools, _resolve_web_search
from core.tools import (
    WebSearchTool,
    _normalize_fetch_url,
    web_fetch,
)

UNIT_TESTS = []


def _unit(fn):
    UNIT_TESTS.append(fn)
    return fn


# --- fixtures -------------------------------------------------------------


class _HttpResp:
    """A stand-in for a requests.Response."""

    def __init__(self, text="", content_type="text/html", status=200, url=None):
        self.text = text
        self.headers = {"Content-Type": content_type}
        self.url = url
        self._status = status

    def raise_for_status(self):
        if self._status >= 400:
            import requests

            raise requests.HTTPError(f"HTTP {self._status}")

    def close(self):
        pass


class _Grounded:
    """A stand-in for a litellm grounding ModelResponse."""

    def __init__(self, content, chunks=None):
        msg = MagicMock()
        msg.content = content
        choice = MagicMock()
        choice.message = msg
        self.choices = [choice]
        self._chunks = chunks or []  # list of (title, uri)
        self._hidden_params = {}

    def model_dump(self):
        return {
            "choices": [
                {
                    "message": {
                        "provider_specific_fields": {
                            "groundingMetadata": {
                                "groundingChunks": [
                                    {"web": {"uri": u, "title": t}} for (t, u) in self._chunks
                                ]
                            }
                        }
                    }
                }
            ]
        }


def _expect_value_error(fn, needle=None):
    try:
        fn()
    except ValueError as e:
        if needle is not None:
            assert needle in str(e), f"{needle!r} not in {e!r}"
        return
    raise AssertionError("expected ValueError")


# === Group A: web_fetch ===================================================


@_unit
def test_normalize_github_blob_to_raw():
    out = _normalize_fetch_url("https://github.com/microsoft/mattergen/blob/main/pyproject.toml")
    assert out == "https://raw.githubusercontent.com/microsoft/mattergen/main/pyproject.toml"
    out2 = _normalize_fetch_url("https://github.com/o/r/blob/abc123/src/x.py")
    assert out2 == "https://raw.githubusercontent.com/o/r/abc123/src/x.py"


@_unit
def test_normalize_github_bare_repo_to_readme_api():
    for u in ("https://github.com/microsoft/mattergen", "https://github.com/microsoft/mattergen/"):
        assert _normalize_fetch_url(u) == "https://api.github.com/repos/microsoft/mattergen/readme"


@_unit
def test_normalize_pypi_project_to_json():
    for u in ("https://pypi.org/project/mace-torch", "https://pypi.org/project/mace-torch/"):
        assert _normalize_fetch_url(u) == "https://pypi.org/pypi/mace-torch/json"


@_unit
def test_normalize_passthrough():
    u = "https://docs.example.com/install"
    assert _normalize_fetch_url(u) == u
    # an issue URL is NOT a bare repo -> left unchanged
    iss = "https://github.com/microsoft/mattergen/issues/83"
    assert _normalize_fetch_url(iss) == iss


@_unit
def test_web_fetch_html_to_markdown():
    html = '<p>see <a href="https://example.com/x">x</a></p>'
    with patch("requests.get", return_value=_HttpResp(html, "text/html")):
        out = web_fetch.forward(url="https://docs.example.com/p")
    assert "[x](https://example.com/x)" in out
    assert "<a" not in out  # tags were converted, not passed through


@_unit
def test_web_fetch_json_passthrough():
    body = '{"info": {"version": "1.2.3"}}'
    with patch("requests.get", return_value=_HttpResp(body, "application/json")):
        out = web_fetch.forward(url="https://pypi.org/project/foo")  # normalized to /json
    assert out == body  # JSON returned verbatim, not markdownified


@_unit
def test_web_fetch_truncation():
    big = "A" * 50_000
    with patch("requests.get", return_value=_HttpResp(big, "text/plain")):
        out = web_fetch.forward(url="https://raw.githubusercontent.com/o/r/main/f.txt", max_chars=100)
    assert out.startswith("A" * 100)
    assert "[truncated at 100 chars]" in out


@_unit
def test_web_fetch_github_token_header():
    import os

    mock = MagicMock(return_value=_HttpResp("# readme", "application/vnd.github.raw"))
    with patch("requests.get", mock), patch.dict(os.environ, {"GITHUB_TOKEN": "ght_abc"}, clear=False):
        web_fetch.forward(url="https://github.com/microsoft/mattergen")  # -> api.github.com
    headers = mock.call_args.kwargs["headers"]
    assert headers.get("Authorization") == "Bearer ght_abc"
    assert headers.get("Accept") == "application/vnd.github.raw+json"


@_unit
def test_web_fetch_no_token_no_auth_header():
    import os

    mock = MagicMock(return_value=_HttpResp("body", "text/html"))
    env = {k: v for k, v in os.environ.items() if k != "GITHUB_TOKEN"}
    with patch("requests.get", mock), patch.dict(os.environ, env, clear=True):
        web_fetch.forward(url="https://docs.example.com/p")
    headers = mock.call_args.kwargs["headers"]
    assert "Authorization" not in headers


@_unit
def test_web_fetch_404_raises():
    with patch("requests.get", return_value=_HttpResp("nope", "text/html", status=404)):
        try:
            web_fetch.forward(url="https://docs.example.com/missing")
        except Exception as e:  # noqa: BLE001
            assert "404" in str(e)
            return
    raise AssertionError("expected an HTTP error to propagate (fail-fast)")


# === Group B: web_search (WebSearchTool) ==================================


@_unit
def test_web_search_calls_gemini_grounding():
    cap = MagicMock(return_value=_Grounded("an answer", chunks=[]))
    with patch("litellm.completion", cap):
        out = WebSearchTool(model="gemini/gemini-3.5-flash", api_key="KEY123").forward(query="how to X")
    kwargs = cap.call_args.kwargs
    assert kwargs["model"] == "gemini/gemini-3.5-flash"
    assert kwargs["api_key"] == "KEY123"                 # resolved key passed explicitly
    assert kwargs["tools"] == [{"googleSearch": {}}]
    assert out == "an answer"                            # no chunks -> answer only


@_unit
def test_web_search_renders_answer_and_sources():
    chunks = [("github.com", "https://github.com/microsoft/mattergen")]
    grounded = _Grounded("install steps...", chunks=chunks)
    # resolve_redirect: identity (already-real URL)
    resolved = _HttpResp(url="https://github.com/microsoft/mattergen")
    with patch("litellm.completion", return_value=grounded), patch("requests.get", return_value=resolved):
        out = WebSearchTool(model="gemini/m", api_key="k").forward(query="q")
    assert "install steps..." in out
    assert "Sources:" in out
    assert "https://github.com/microsoft/mattergen" in out


@_unit
def test_web_search_resolves_redirect_and_dedups():
    # two different redirect URIs that resolve to the SAME real URL -> deduped to 1
    chunks = [
        ("github.com", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AAA"),
        ("github.com", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/BBB"),
    ]
    grounded = _Grounded("ans", chunks=chunks)
    real = _HttpResp(url="https://github.com/microsoft/mattergen")  # both resolve here
    with patch("litellm.completion", return_value=grounded), patch("requests.get", return_value=real):
        out = WebSearchTool(model="gemini/m", api_key="k").forward(query="q")
    assert out.count("https://github.com/microsoft/mattergen") == 1   # deduped
    assert "vertexaisearch" not in out                                # redirect resolved away


@_unit
def test_web_search_max_results_caps():
    chunks = [(f"s{i}", f"https://vertexaisearch.cloud.google.com/grounding-api-redirect/{i}") for i in range(5)]
    grounded = _Grounded("ans", chunks=chunks)
    # each redirect resolves to a distinct real URL
    def _get(uri, **_kw):
        return _HttpResp(url=uri.replace("vertexaisearch.cloud.google.com/grounding-api-redirect/", "real.example/"))
    with patch("litellm.completion", return_value=grounded), patch("requests.get", side_effect=_get):
        out = WebSearchTool(model="gemini/m", api_key="k").forward(query="q", max_results=2)
    assert out.count("real.example/") == 2


@_unit
def test_web_search_no_metadata_answer_only():
    with patch("litellm.completion", return_value=_Grounded("just the answer", chunks=[])):
        out = WebSearchTool(model="gemini/m", api_key="k").forward(query="q")
    assert out == "just the answer"
    assert "Sources:" not in out


@_unit
def test_web_search_error_returns_message():
    def _boom(**_kw):
        raise RuntimeError("no api key configured")
    with patch("litellm.completion", side_effect=_boom):
        out = WebSearchTool(model="gemini/m", api_key=None).forward(query="q")
    assert out.startswith("web_search unavailable")
    assert "RuntimeError" in out


# === Group C: _resolve_web_search =========================================


def _llm_cfg(**providers):
    return {"providers": providers}


@_unit
def test_resolve_key_from_template_not_hardcoded():
    import os

    llm = _llm_cfg(gemini={"model_id": "gemini/gemini-3.5-flash", "api_key": "${GEMINI_API_KEY}"})
    agent = {"web_search": {"api_key": "${CUSTOM_KEY}"}}
    with patch.dict(os.environ, {"CUSTOM_KEY": "abc", "GEMINI_API_KEY": "WRONG_SENTINEL"}, clear=False):
        model, key = _resolve_web_search(llm, agent)
    assert key == "abc"                 # the configured template, expanded
    assert key != "WRONG_SENTINEL"      # did NOT silently fall back to GEMINI_API_KEY
    assert model == "gemini/gemini-3.5-flash"


@_unit
def test_resolve_api_key_fallback_to_provider():
    import os

    llm = _llm_cfg(gemini={"model_id": "gemini/m", "api_key": "${GEMINI_API_KEY}"})
    with patch.dict(os.environ, {"GEMINI_API_KEY": "provkey"}, clear=False):
        _model, key = _resolve_web_search(llm, {"web_search": {}})  # no web_search.api_key
    assert key == "provkey"


@_unit
def test_resolve_no_key_is_none():
    llm = _llm_cfg(gemini={"model_id": "gemini/m"})  # provider has no api_key
    _model, key = _resolve_web_search(llm, {})
    assert key is None


@_unit
def test_resolve_model_fallback_chain():
    # override wins
    llm = _llm_cfg(gemini={"model_id": "gemini/provider-model"})
    m, _ = _resolve_web_search(llm, {"web_search": {"model": "gemini/override"}})
    assert m == "gemini/override"
    # else provider model_id
    m, _ = _resolve_web_search(llm, {"web_search": {}})
    assert m == "gemini/provider-model"
    # else hardcoded default
    m, _ = _resolve_web_search(_llm_cfg(gemini={}), {})
    assert m == "gemini/gemini-3.5-flash"


@_unit
def test_resolve_provider_selection():
    import os

    llm = _llm_cfg(
        gemini={"model_id": "gemini/g", "api_key": "${GEMINI_API_KEY}"},
        openai={"model_id": "gpt-x", "api_key": "${OPENAI_API_KEY}"},
    )
    with patch.dict(os.environ, {"OPENAI_API_KEY": "ok", "GEMINI_API_KEY": "gk"}, clear=False):
        m, key = _resolve_web_search(llm, {"web_search": {"provider": "openai"}})
    assert m == "gpt-x"
    assert key == "ok"  # resolved from providers.openai, not gemini


@_unit
def test_resolve_unresolved_var_raises():
    import os

    llm = _llm_cfg(gemini={"model_id": "gemini/m"})
    agent = {"web_search": {"api_key": "${DEFINITELY_NOT_SET_VAR_XYZ}"}}
    env = {k: v for k, v in os.environ.items() if k != "DEFINITELY_NOT_SET_VAR_XYZ"}
    with patch.dict(os.environ, env, clear=True):
        _expect_value_error(lambda: _resolve_web_search(llm, agent), needle="Unresolved env var")


# === Group D: _filter_disabled_tools ======================================


class _T:
    def __init__(self, name):
        self.name = name


def _toolset():
    return [_T("web_fetch"), _T("web_search"), _T("bash"), _T("grep")]


@_unit
def test_filter_removes_named():
    out = _filter_disabled_tools(_toolset(), {"web_fetch", "web_search"})
    assert {t.name for t in out} == {"bash", "grep"}


@_unit
def test_filter_empty_keeps_full_toolset():
    ts = _toolset()
    assert _filter_disabled_tools(ts, set()) == ts


@_unit
def test_filter_unknown_raises():
    _expect_value_error(lambda: _filter_disabled_tools(_toolset(), {"nope_tool"}), needle="nope_tool")


@_unit
def test_filter_final_answer_raises():
    _expect_value_error(
        lambda: _filter_disabled_tools(_toolset(), {"final_answer"}), needle="final_answer"
    )


if __name__ == "__main__":
    import traceback

    failed = 0
    for fn in UNIT_TESTS:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
        except Exception:
            print(f"  FAIL  {fn.__name__}")
            traceback.print_exc()
            failed += 1
    if failed:
        raise SystemExit(1)
    print(f"\nAll {len(UNIT_TESTS)} unit tests passed!")
