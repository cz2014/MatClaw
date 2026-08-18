"""create_agent injects the curated tool namespace.

The default toolset is the stable infra + agent-meta + final_answer set. After the P1 trim it
contains no domain-specific job wrappers (the agent reaches remote compute by composing standard
atomate2 Makers in code). This test guards that the curated set is present and complete.
"""

from __future__ import annotations

# Infra + agent-meta + final_answer -- the complete curated default toolset.
# P4: IO helpers renamed (write_text/read_text -> write_file/read_file) + the mainstream
# basic-primitive set added (edit_file/grep/glob/bash).
# P5c: rag_search removed -- the agent retrieves by grepping the installed package source.
_STABLE_TOOLS = {
    "wait_for_jobflow", "remote_put", "remote_get", "remote_ls", "query_jobstore",
    "fetch_history", "write_experience",
    "write_file", "read_file", "edit_file", "read_pdf",
    "grep", "glob", "bash", "wait_command", "kill_command", "final_answer",
}


def test_default_toolset_contains_stable_tools(make_agent):
    agent = make_agent(default_tools=True)
    names = set(agent.tools.keys())
    missing = _STABLE_TOOLS - names
    assert not missing, f"missing curated tools: {missing} (have {sorted(names)})"
