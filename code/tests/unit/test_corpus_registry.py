"""P5c: the doc-corpus registry (configs/corpus.yaml) replaces RAG.

create_agent resolves the registry, adds each corpus to grep/glob's search roots, points grep's
default at site-packages, and injects a corpus section (resolved paths + descriptions) into the
system prompt -- so the agent knows what reference docs exist and where to grep them now that
rag_search is gone.
"""

from __future__ import annotations

import sysconfig
from pathlib import Path

from core.agent import _corpus_instructions, _load_corpus_registry


def test_load_corpus_registry_resolves_and_skips_missing(tmp_path):
    corpus = tmp_path / "corpus"
    (corpus / "docs" / "vasp").mkdir(parents=True)
    cfg = tmp_path / "corpus.yaml"
    cfg.write_text(
        "corpus:\n"
        "  vasp:\n"
        "    path: docs/vasp\n"
        "    description: VASP wiki docs.\n"
        "  bogus:\n"
        "    path: docs/nope\n"          # missing dir -> skipped
        "    description: not present.\n"
    )
    got = _load_corpus_registry(cfg, corpus.resolve())
    assert [c["name"] for c in got] == ["vasp"]  # bogus skipped (dir missing)
    assert got[0]["path"] == (corpus / "docs" / "vasp").resolve()
    assert got[0]["description"] == "VASP wiki docs."


def test_load_corpus_registry_missing_file_is_empty(tmp_path):
    assert _load_corpus_registry(tmp_path / "nope.yaml", tmp_path) == []


def test_corpus_instructions_mentions_site_packages_and_each_corpus():
    sp = Path("/x/site-packages")
    text = _corpus_instructions(sp, [{"name": "vasp", "path": Path("/c/docs/vasp"), "description": "VASP docs."}])
    assert "/x/site-packages" in text          # code-search guidance points at site-packages
    assert "vasp" in text and "/c/docs/vasp" in text and "VASP docs." in text


def test_shipped_corpus_section_in_system_prompt(make_agent):
    """The production configs/corpus.yaml (vasp) is resolved + injected into the real agent's prompt."""
    sp = make_agent().system_prompt
    assert "site-packages" in sp                # the agent is told to grep installed source
    assert "vasp" in sp                         # the registered corpus
    assert "INCAR" in sp or "VASP wiki" in sp   # its description reached the prompt


def test_grep_roots_include_site_packages_and_vasp_corpus(make_agent):
    """grep/glob default to site-packages and also reach the registered vasp corpus."""
    agent = make_agent(default_tools=True)
    roots = [str(r) for r in agent.tools["grep"]._roots]
    site_packages = sysconfig.get_paths()["purelib"]
    assert any(site_packages in r for r in roots)
    assert any(r.endswith("corpus/docs/vasp") for r in roots)
