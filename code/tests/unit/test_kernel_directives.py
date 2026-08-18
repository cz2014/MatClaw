"""Leading-block kernel and timeout directive parsing."""

from __future__ import annotations

import pytest

from core.kernel import ExecutionDirectives, parse_directives


def test_defaults():
    assert parse_directives("x = 1") == ExecutionDirectives("default", 120)


def test_both_directives_in_either_order():
    assert parse_directives("# timeout: 30\n# kernel: probe\nx=1") == ExecutionDirectives(
        "probe", 30
    )
    assert parse_directives("# kernel: probe\n# timeout: 30\nx=1") == ExecutionDirectives(
        "probe", 30
    )


def test_other_comments_and_blanks_are_tolerated():
    code = "\n# explanation\n\n# kernel: analysis\n# another comment\n# timeout: 9\nx=1"
    assert parse_directives(code) == ExecutionDirectives("analysis", 9)


def test_scan_stops_at_first_code_line():
    assert parse_directives("x=1\n# kernel: ignored\n# timeout: 2") == ExecutionDirectives()


def test_string_literal_is_not_a_directive():
    assert parse_directives("text = '# kernel: ignored'") == ExecutionDirectives()


def test_timeout_is_capped_at_600():
    assert parse_directives("# timeout: 9999\nx=1").timeout == 600


def test_trailing_comment_on_directive_value_is_tolerated():
    assert parse_directives("# kernel: gpu  # hot MACE model\nx=1").kernel == "gpu"
    assert parse_directives("# timeout: 300  # five minutes\nx=1").timeout == 300


def test_kernel_names_are_case_insensitive():
    assert parse_directives("# Kernel: GPU\nx=1").kernel == "gpu"
    assert parse_directives("# kernel: Analysis\nx=1").kernel == "analysis"


def test_all_digit_kernel_name_is_rejected():
    # Numeric names would be ambiguous with background-PID targets in wait/kill.
    with pytest.raises(ValueError, match="kernel directive"):
        parse_directives("# kernel: 123\nx=1")


@pytest.mark.parametrize("value", ["", "abc", "0", "-1", "1.5"])
def test_malformed_timeout_names_offending_line(value):
    line = f"# timeout: {value}"
    with pytest.raises(ValueError, match="timeout directive") as raised:
        parse_directives(line + "\nx=1")
    assert line in str(raised.value)


@pytest.mark.parametrize("value", ["", "has space", "bad/name", "_leading"])
def test_malformed_kernel_names_offending_line(value):
    line = f"# kernel: {value}"
    with pytest.raises(ValueError, match="kernel directive") as raised:
        parse_directives(line + "\nx=1")
    assert line in str(raised.value)
