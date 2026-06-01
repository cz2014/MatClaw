"""Thin ``exec()``-namespace Python executor for the opened runtime (P4).

This is the load-bearing change of framework-migration P4: it replaces the
vendored AST interpreter (:class:`core._smol.local_python_executor.LocalPythonExecutor`)
with a minimal executor that runs the agent's code via the builtin :func:`exec`
in a persistent namespace. The three guardrails of the AST interpreter -- the
import allow-list, the missing ``open`` builtin, and the ~10M elementary-operation
cap (``MAX_OPERATIONS = 10_000_000``) -- were MatClaw's largest run-failure class,
and they protect nothing the P3 container does not already protect. A real
``exec()`` has none of them by construction: the namespace inherits the real
``__builtins__`` (so ``open``, ``__import__``, ``eval``, ... all work) and there
is no AST walk to count operations on.

It honors the same :class:`core._smol.local_python_executor.PythonExecutor`
contract the vendored ``CodeAgent`` drives (``send_tools`` / ``send_variables``
once per run, ``__call__`` -> :class:`CodeOutput` every step), so it is a drop-in
swap selected by the ``agent.executor`` config flag. The AST executor is kept
in-tree for instant rollback (``agent.executor: ast``).

See ``docs/exec-plans/completed/2026-05-31_p4_open_runtime.md`` (section 3).
"""

from __future__ import annotations

import ast
import contextlib
import io
import logging
import signal
import threading
from typing import Any

from core._smol.local_python_executor import (
    DEFAULT_MAX_LEN_OUTPUT,
    CodeOutput,
    PythonExecutor,
)
from core._smol.utils import truncate_content

logger = logging.getLogger(__name__)


class _FinalAnswer(BaseException):
    """Sentinel raised by the injected ``final_answer`` to unwind the code block.

    Mirrors the AST executor's ``FinalAnswerException``. It derives from
    ``BaseException`` (not ``Exception``) so the agent's own ``try/except Exception``
    cannot accidentally swallow a final answer. It is always caught inside
    :meth:`ExecPythonExecutor.__call__`, so it never reaches the agent loop.
    """

    def __init__(self, value: Any):
        super().__init__()
        self.value = value


class _ExecTimeout(BaseException):
    """Raised from the SIGALRM handler when a single step exceeds the deadline.

    ``BaseException`` so a hot loop wrapped in ``try/except Exception`` can still
    be interrupted (same reasoning as :class:`_FinalAnswer`). It is converted to a
    normal :class:`TimeoutError` at the executor boundary so the agent loop handles
    it as a recoverable step failure rather than crashing the whole run.
    """


class ExecPythonExecutor(PythonExecutor):
    """A minimal ``exec()``-namespace executor with full Python access.

    Args:
        max_print_outputs_length: cap on captured stdout per step (defaults to
            ``DEFAULT_MAX_LEN_OUTPUT``), matching the AST executor.
        exec_timeout_s: optional per-step wall-clock deadline (seconds). ``None``
            or ``<= 0`` disables the watchdog (the default). Best-effort: only armed
            on the main thread on platforms with ``signal.SIGALRM`` (every supported
            runtime), and -- like any Python signal -- it can only interrupt between
            bytecode ops, so a long C-extension call is bounded only when it returns
            to Python. The always-on backstop is the P3 container's
            ``--memory``/``--cpus``/``--pids-limit`` plus ``max_steps``.
    """

    def __init__(
        self,
        max_print_outputs_length: int | None = None,
        exec_timeout_s: float | None = None,
        **_ignored: Any,
    ):
        # _ignored absorbs additional_authorized_imports / additional_functions etc.:
        # this executor enforces no import policy, so it has nothing to do with them.
        self.state: dict[str, Any] = {"__name__": "__main__", "_print_outputs": ""}
        self.static_tools: dict[str, Any] = {}
        self.max_print_outputs_length = max_print_outputs_length or DEFAULT_MAX_LEN_OUTPUT
        self.exec_timeout_s = exec_timeout_s
        self._warned_no_watchdog = False

    # -- PythonExecutor contract ------------------------------------------------

    def send_variables(self, variables: dict[str, Any]) -> None:
        """Inject variables into the persistent namespace (once per run)."""
        self.state.update(variables)

    def send_tools(self, tools: dict[str, Any]) -> None:
        """Expose tools as plain callables in the namespace (once per run).

        Overrides any ``final_answer`` the agent supplies (its ``FinalAnswerTool``)
        with the sentinel-raising version, exactly as the AST executor does.
        """

        def final_answer(*args: Any, **kwargs: Any):
            value = args[0] if args else next(iter(kwargs.values()), None)
            raise _FinalAnswer(value)

        self.static_tools = {**tools, "final_answer": final_answer}
        # Tools are just names in the exec namespace.
        self.state.update(self.static_tools)

    def __call__(self, code_action: str) -> CodeOutput:
        """Execute one code block; return its CodeOutput (every step)."""
        buf = io.StringIO()
        output: Any = None
        is_final = False
        try:
            with contextlib.redirect_stdout(buf), self._deadline():
                tree = ast.parse(code_action, mode="exec")
                # IPython-style: eval a trailing bare expression so CodeOutput.output
                # carries the last value (preserves the "Out: ..." observation).
                if tree.body and isinstance(tree.body[-1], ast.Expr):
                    last = ast.Expression(tree.body.pop().value)
                    ast.fix_missing_locations(last)
                    exec(compile(tree, "<agent>", "exec"), self.state)
                    output = eval(compile(last, "<agent>", "eval"), self.state)
                else:
                    exec(compile(tree, "<agent>", "exec"), self.state)
        except _FinalAnswer as fa:
            output, is_final = fa.value, True
        except _ExecTimeout as te:
            # Surface as a normal error so the loop's `except Exception` catches it
            # (-> AgentExecutionError -> recoverable step failure, not a crash).
            raise TimeoutError(str(te) or "code execution timed out") from None
        finally:
            # Write captured stdout BEFORE any real exception propagates, so the
            # loop's error path (agents.py: reads state["_print_outputs"]) recovers
            # partial logs identically to the AST executor.
            self.state["_print_outputs"] = buf.getvalue()
        logs = truncate_content(buf.getvalue(), self.max_print_outputs_length)
        return CodeOutput(output=output, logs=logs, is_final_answer=is_final)

    def cleanup(self) -> None:  # optional in the contract; nothing to release.
        pass

    # -- optional wall-clock watchdog (opt-in, off by default) ------------------

    @contextlib.contextmanager
    def _deadline(self):
        """Arm a SIGALRM deadline for the duration of one exec, if configured."""
        if not self._can_arm():
            yield
            return

        def _on_alarm(_signum, _frame):
            raise _ExecTimeout(
                f"Code execution exceeded {self.exec_timeout_s}s (agent.exec_timeout_s)"
            )

        previous = signal.signal(signal.SIGALRM, _on_alarm)
        signal.setitimer(signal.ITIMER_REAL, float(self.exec_timeout_s))
        try:
            yield
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)

    def _can_arm(self) -> bool:
        if not self.exec_timeout_s or self.exec_timeout_s <= 0:
            return False
        on_main_thread = threading.current_thread() is threading.main_thread()
        if not hasattr(signal, "SIGALRM") or not on_main_thread:
            if not self._warned_no_watchdog:
                logger.warning(
                    "agent.exec_timeout_s set but the SIGALRM watchdog cannot be armed "
                    "(no SIGALRM or not on the main thread); relying on container limits "
                    "+ max_steps instead."
                )
                self._warned_no_watchdog = True
            return False
        return True
