"""Unit tests for QueryJobstoreTool: whitelist enforcement, source introspection, serialization.

Offline -- no LLM, no MongoDB (the JobController is mocked). This fully covers the
MatClaw-owned logic; there is no separate live test, since query_jobstore is a thin
JobController wrapper and a real job/cluster would add queue wait but no coverage.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from core.tools import QueryJobstoreTool

UNIT_TESTS = []


def _unit(fn):
    UNIT_TESTS.append(fn)
    return fn


@_unit
def test_whitelist_enforcement():
    """Blocked methods raise ValueError."""
    tool = QueryJobstoreTool()
    try:
        tool.forward(project="x", method="delete_jobs", kwargs={})
        raise AssertionError("Expected ValueError for delete_jobs")
    except ValueError as e:
        assert "delete_jobs" in str(e)
        assert "not allowed" in str(e).lower()


@_unit
def test_show_source_all():
    """method='all' + show_source_code returns index of all whitelisted methods."""
    tool = QueryJobstoreTool()
    result = tool.forward(project="x", method="all", show_source_code=True)
    for name in QueryJobstoreTool._ALLOWED_METHODS:
        assert name in result, f"Expected {name} in show_source_code output"


@_unit
def test_show_source_single():
    """Specific method + show_source_code returns source code."""
    tool = QueryJobstoreTool()
    result = tool.forward(
        project="x", method="get_jobs_info", show_source_code=True
    )
    assert "def get_jobs_info" in result


@_unit
def test_serialization_cap():
    """Oversized results are truncated with marker."""
    tool = QueryJobstoreTool()

    class FakeResult:
        def model_dump(self):
            return {"data": "x" * 100_000}

    with patch(
        "jobflow_remote.jobs.jobcontroller.JobController.from_project_name"
    ) as mock_jc:
        mock_instance = MagicMock()
        mock_instance.get_jobs_info.return_value = [FakeResult()]
        mock_jc.return_value = mock_instance

        result = tool.forward(project="test", method="get_jobs_info")

    assert len(result) <= tool._MAX_RESULT_CHARS + 100  # marker overhead
    assert "[truncated" in result


@_unit
def test_serialization_pydantic():
    """Pydantic objects are serialized via model_dump()."""
    tool = QueryJobstoreTool()

    class FakeJobInfo:
        def model_dump(self):
            return {
                "uuid": "abc-123",
                "state": "COMPLETED",
                "worker": "perlmutter_debug",
            }

    with patch(
        "jobflow_remote.jobs.jobcontroller.JobController.from_project_name"
    ) as mock_jc:
        mock_instance = MagicMock()
        mock_instance.get_jobs_info.return_value = [FakeJobInfo(), FakeJobInfo()]
        mock_jc.return_value = mock_instance

        result = tool.forward(project="test", method="get_jobs_info")

    assert "abc-123" in result
    assert "COMPLETED" in result
    assert "perlmutter_debug" in result


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
