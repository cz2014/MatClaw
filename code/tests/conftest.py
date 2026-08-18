"""Shared pytest configuration for the MatClaw test suite.

Tiers (see docs/exec-plans/active/2026-05-31_p0_test_scaffolding.md):
  unit         offline, deterministic, no LLM/cluster -- the gate (default run)
  llm          needs a real LLM (Gemini 3.5 Flash); the llm/ tier
  integration  needs a real HPC/SSH/Mongo cluster; the integration/ tier

The `unit` / `llm` / `integration` markers are auto-applied by directory below (one dir per
tier). Agent-run demo scripts under tests/demos/ are not collected.

Fixtures (fake_llm / tmp_workspace / agent_factory) are added in the P0b step.
"""

import json
import os
import time
from pathlib import Path

import psutil
import pytest

# Demo / agent-run scripts are reproducibility artifacts, not tests.
collect_ignore = ["demos"]

_TESTS_DIR = Path(__file__).parent
REPO_ROOT = _TESTS_DIR.parent.parent  # code/tests -> code -> repo root
CONFIGS_DIR = REPO_ROOT / "configs"
_DUMMY_KEYS = ("CLAUDE_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "DEEPSEEK_API_KEY")


def pytest_addoption(parser):
    """Options for the live LLM tests. Only the env var NAME is passed -- the key VALUE stays in the
    environment (never on a command line), so nothing leaks. Defaults match the repo's cheap model.
    """
    parser.addoption(
        "--llm-provider", action="store", default="gemini",
        help="Provider for the live LLM tests (a key in configs/llm_config.yaml). Default: gemini.",
    )
    parser.addoption(
        "--llm-key-env", action="store", default="GEMINI_API_KEY",
        help="NAME of the host env var holding the API key for --llm-provider (value is read from "
             "the environment, never passed as a value). Default: GEMINI_API_KEY.",
    )
    parser.addoption(
        "--hpc-project", action="store", default=os.environ.get("MATCLAW_TEST_PROJECT"),
        help="jobflow-remote project for the HPC integration tests (or $MATCLAW_TEST_PROJECT). "
             "Cluster-agnostic; the tests skip when it is unset or not configured on this host.",
    )
    parser.addoption(
        "--hpc-worker", action="store", default=os.environ.get("MATCLAW_TEST_WORKER"),
        help="Worker within --hpc-project (or $MATCLAW_TEST_WORKER). Defaults to the project's "
             "first configured worker.",
    )


def pytest_collection_modifyitems(config, items):
    """Auto-apply the tier marker (`unit` / `llm` / `integration`) based on directory."""
    _by_dir = {"unit": "unit", "llm": "llm", "integration": "integration"}
    for item in items:
        path = Path(str(item.fspath)).resolve()
        try:
            rel = path.relative_to(_TESTS_DIR)
        except ValueError:
            continue
        top = rel.parts[0] if rel.parts else ""
        marker = _by_dir.get(top)
        if marker:
            item.add_marker(getattr(pytest.mark, marker))


# --- P0b fixtures: drive the real CodeAgent loop with a scripted (fake) LLM ---


@pytest.fixture
def tmp_workspace(tmp_path):
    """A throwaway workspace directory for an agent run."""
    return tmp_path


@pytest.fixture(autouse=True)
def reap_children():
    """Fail tests that leave behind a new child process, after reaping it safely."""
    parent = psutil.Process()

    def snapshot():
        found = {}
        for child in parent.children(recursive=True):
            try:
                found[(child.pid, child.create_time())] = child
            except psutil.Error:
                pass
        return found

    before = set(snapshot())
    yield
    deadline = time.monotonic() + 0.3
    leaked = {}
    while time.monotonic() < deadline:
        leaked = {key: proc for key, proc in snapshot().items() if key not in before}
        if not leaked:
            return
        time.sleep(0.02)
    for process in leaked.values():
        try:
            process.terminate()
        except psutil.Error:
            pass
    _, alive = psutil.wait_procs(list(leaked.values()), timeout=0.5)
    for process in alive:
        try:
            process.kill()
        except psutil.Error:
            pass
    psutil.wait_procs(alive, timeout=0.5)
    pytest.fail(f"test leaked child process(es): {sorted(pid for pid, _ in leaked)}")


@pytest.fixture(scope="session")
def kernel_pool(tmp_path_factory):
    """Two real persistent kernels shared by non-destructive manager tests."""
    from core.kernel import KernelManager
    from core.tools import ToolSpec, _LocalExecState
    from core.toolserver import ToolServer

    workspace = tmp_path_factory.mktemp("kernel_pool")
    state = _LocalExecState(workspace, kill_grace_s=0.2)
    server = ToolServer(state)
    server.start()
    spec = ToolSpec(
        workspace=workspace,
        search_roots=(workspace,),
        site_packages=Path(__file__).resolve().parents[1] / ".venv" / "lib",
        disabled=("web_fetch", "web_search"),
    )
    manager = KernelManager(workspace, spec, server, grace_s=0.5)
    manager.execute("pass", kernel_name="probe", timeout=10)
    try:
        yield manager
    finally:
        manager.shutdown()
        server.stop()


@pytest.fixture
def fresh_manager(tmp_path):
    """Function-scoped real manager for restart/crash/destructive tests."""
    from core.kernel import KernelManager
    from core.tools import ToolSpec, _LocalExecState
    from core.toolserver import ToolServer

    state = _LocalExecState(tmp_path, kill_grace_s=0.2)
    server = ToolServer(state)
    server.start()
    spec = ToolSpec(
        workspace=tmp_path,
        search_roots=(tmp_path,),
        site_packages=Path(__file__).resolve().parents[1] / ".venv" / "lib",
        disabled=("web_fetch", "web_search"),
    )
    manager = KernelManager(tmp_path, spec, server, grace_s=0.5)
    try:
        yield manager
    finally:
        manager.shutdown()
        server.stop()


@pytest.fixture
def make_agent(monkeypatch, tmp_path):
    """Build a real CodeAgent (via create_agent) whose model is replaced by a scripted
    fake LLM, so agent.run() exercises the real loop offline (no network/API key).

    Usage:
        agent = make_agent(steps=[{"phase":.., "plan":.., "code":"x=1", "summary":..}, ...],
                           tools=[my_tool])
        result = agent.run("task")

    Each step's "code" is executed in the persistent interpreter; end a run with code that
    calls final_answer(...). When steps run out, a default final_answer step is returned so
    the loop always terminates. The message lists the model was called with are recorded on
    agent._fake_calls.
    """
    state = {"cwd": os.getcwd(), "agents": []}

    def _make(steps=None, tools=None, default_tools=False, **create_kwargs):
        for key in _DUMMY_KEYS:
            monkeypatch.setenv(key, "test-dummy")
        from core._smol.models import ChatMessage, MessageRole, TokenUsage

        from core.agent import create_agent

        if default_tools:
            tools = None  # let create_agent inject the full default toolset
        elif tools is None:
            tools = []  # minimal: skip the default scientific toolset (avoids RAG index load)
        agent = create_agent(
            config_dir=CONFIGS_DIR, workspace_dir=tmp_path, tools=tools, **create_kwargs
        )
        if hasattr(agent, "stream_outputs"):
            agent.stream_outputs = False

        queue = list(steps or [])
        calls = []
        default = {
            "phase": "end", "plan": "finish",
            "code": "final_answer('default')", "summary": "finish",
        }

        def fake_generate(messages, **kwargs):
            calls.append(messages)
            payload = queue.pop(0) if queue else default
            return ChatMessage(
                role=MessageRole.ASSISTANT,
                content=json.dumps(payload),
                token_usage=TokenUsage(input_tokens=1, output_tokens=1),
            )

        agent.model.generate = fake_generate
        agent._fake_calls = calls
        state["agents"].append(agent)
        return agent

    yield _make
    for agent in reversed(state["agents"]):
        agent.cleanup()
    os.chdir(state["cwd"])  # create_agent chdir's into the workspace; restore it


# --- HPC integration tier: cluster-agnostic target resolution ---


@pytest.fixture
def hpc_target(request):
    """(project, worker) for the HPC integration tests -- cluster-agnostic.

    Resolves from --hpc-project/--hpc-worker (or $MATCLAW_TEST_PROJECT/$MATCLAW_TEST_WORKER).
    SKIPS cleanly when no HPC project is configured on this host (so a machine without a
    cluster stays green); only a configured-but-unreachable cluster surfaces as a failure.
    Worker defaults to the project's first configured worker.
    """
    project = request.config.getoption("--hpc-project")
    if not project:
        pytest.skip("no HPC project (set --hpc-project or $MATCLAW_TEST_PROJECT)")
    try:
        from jobflow_remote.config.manager import ConfigManager

        proj = ConfigManager().get_project(project)
    except Exception as exc:  # project not defined in ~/.jfremote on this host
        pytest.skip(f"jobflow-remote project {project!r} not configured here: {exc}")
    workers = list(getattr(proj, "workers", {}) or {})
    worker = request.config.getoption("--hpc-worker") or (workers[0] if workers else None)
    if not worker:
        pytest.skip(f"project {project!r} has no workers configured")
    if worker not in workers:
        pytest.skip(f"worker {worker!r} not in project {project!r} (have: {workers})")
    return project, worker
