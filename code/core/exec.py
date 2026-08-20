"""Thin CodeAgent executor client for the supervised persistent kernels."""

from __future__ import annotations

import ast
from typing import Any

from core._smol.local_python_executor import CodeOutput, PythonExecutor
from core._smol.tools import Tool
from core._smol.utils import truncate_content
from core.kernel import parse_directives
from core.tools import build_stateless_tools

_STATEFUL_NAMES = {"bash", "wait_command", "kill_command", "final_answer"}
_STATUS_OUTPUT_KEYS = {
    "running",
    "refused",
    "kernel",
    "bash",
    "target",
    "pid",
    "elapsed",
    "vitals",
    "truncated",
    "log_file",
    "returncode",
    "error",
    "method",
    "namespace_preserved",
    "survivors",
}


def _bare_control_call(code: str) -> tuple[str, dict[str, Any]] | None:
    """Return a literal bare wait/kill call, or None for ordinary kernel code."""
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError:
        return None
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Expr):
        return None
    call = tree.body[0].value
    if (
        not isinstance(call, ast.Call)
        or not isinstance(call.func, ast.Name)
        or call.func.id not in {"wait_command", "kill_command"}
    ):
        return None
    if any(keyword.arg is None for keyword in call.keywords):
        return None
    keyword_names = [keyword.arg for keyword in call.keywords]
    if len(keyword_names) != len(set(keyword_names)):
        return None
    try:
        args = [ast.literal_eval(arg) for arg in call.args]
        kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in call.keywords}
    except (ValueError, TypeError):
        return None
    params: dict[str, Any] = {}
    if call.func.id == "wait_command":
        if len(args) > 2 or (args and "target" in kwargs) or (
            len(args) == 2 and "timeout" in kwargs
        ):
            return None
        target = args[0] if args else kwargs.pop("target", None)
        if target is None:
            return None
        params["target"] = target
        if len(args) == 2:
            params["timeout"] = args[1]
        if "timeout" in kwargs:
            params["timeout"] = kwargs.pop("timeout")
    else:
        if len(args) > 1 or (args and "target" in kwargs):
            return None
        target = args[0] if args else kwargs.pop("target", None)
        if target is None:
            return None
        params["target"] = target
    if kwargs:
        return None
    return call.func.id, params


class ExecPythonExecutor(PythonExecutor):
    """Map CodeAgent's executor contract onto a harness-owned KernelManager."""

    def __init__(self, kernel_manager, tool_server=None, **_ignored: Any):
        self.kernel_manager = kernel_manager
        self.tool_server = tool_server or kernel_manager.tool_server
        self.state: dict[str, Any] = {"_print_outputs": ""}
        self.static_tools: dict[str, Any] = {}
        self._closed = False

    def send_variables(self, variables: dict[str, Any]) -> None:
        """Pickle and inject CodeAgent state into every current/future kernel."""
        self._ensure_open()
        self.kernel_manager.send_variables(variables)
        self.state.update(variables)

    def send_tools(self, tools: dict[str, Tool]) -> None:
        """Validate tool values and inject only custom extras into kernels."""
        self._ensure_open()
        invalid = [name for name, value in tools.items() if not isinstance(value, Tool)]
        if invalid:
            raise TypeError(
                "managed_agents are not supported by the multi-kernel executor: "
                + ", ".join(sorted(invalid))
            )
        self.static_tools = dict(tools)
        self.state.update(tools)
        built = {tool.name for tool in build_stateless_tools(self.kernel_manager.tool_spec)}
        extras = {
            name: value
            for name, value in tools.items()
            if name not in built and name not in _STATEFUL_NAMES
        }
        if extras:
            # User-supplied Tool objects cannot be reconstructed inside a kernel,
            # and running them harness-side would put them outside all kernel
            # supervision (timeouts, vitals, kill ladder). Fail fast instead.
            raise ValueError(
                "user-supplied tools are not supported under the multi-kernel "
                "executor: " + ", ".join(sorted(extras))
            )

    def _status(self, result: dict[str, Any]) -> str:
        roster = result.get("roster") or self.kernel_manager.roster_line()
        local_lines = self.tool_server.state.status_lines().splitlines()
        bash = local_lines[0] if local_lines else "bash: idle"
        background = local_lines[1] if len(local_lines) > 1 else "background: none"
        if bash != "bash: idle":
            jobs = background.removeprefix("background: ")
            suffix = "" if jobs == "none" else f" | {jobs}"
            background = (
                f"background: foreground bash({bash.removeprefix('bash: ')}){suffix}"
            )
        return roster if background == "background: none" else roster + "\n" + background

    def _logs(self, result: dict[str, Any]) -> str:
        status = self._status(result)
        notes = list(result.get("completion_notes", []))
        # The bash slot drains its own notes only on bash-family calls, so a code
        # step would otherwise never surface a background job that finished under it.
        notes.extend(self.tool_server.state.take_completion_notes())
        parts = [f"[completed] {note}" for note in notes]
        if result.get("note"):
            parts.append(str(result["note"]))
        payload = result.get("logs") or result.get("stdout")
        if payload:
            parts.append(str(payload))
        body = truncate_content("\n".join(parts), max_length=30_000)
        return f"{body}\n{status}" if body else status

    def __call__(self, code_action: str) -> CodeOutput:
        """Route one code block and always refresh the shadow print-output state."""
        self._ensure_open()
        updated = False
        try:
            directives = parse_directives(code_action)
            control = _bare_control_call(code_action)
            if control is not None:
                method, params = control
                result = self.tool_server.dispatch(method, params)
            else:
                result = self.kernel_manager.execute(
                    code_action,
                    kernel_name=directives.kernel,
                    timeout=directives.timeout,
                )
            logs = self._logs(result)
            self.state["_print_outputs"] = logs
            updated = True
            error = result.get("error")
            if error and not result.get("refused") and not (
                control is not None and control[0] == "kill_command"
            ):
                if isinstance(error, dict):
                    message = f"{error.get('ename', 'ExecutionError')}: {error.get('evalue', '')}"
                else:
                    message = str(error)
                raise RuntimeError(message)
            if control is not None and control[0] == "kill_command":
                # A kill that collected an already-finished final_answer must end
                # the run with the computed value, not the ladder-report dict.
                output = result.get("output") if result.get("is_final_answer") else result
            elif "output" in result:
                output = result["output"]
            elif control is not None or result.get("running") or result.get("refused"):
                output = {
                    key: value for key, value in result.items() if key in _STATUS_OUTPUT_KEYS
                }
            else:
                output = None
            return CodeOutput(
                output=output,
                logs=logs,
                is_final_answer=bool(result.get("is_final_answer")),
            )
        except Exception:
            if not updated:
                self.state["_print_outputs"] = self._status({})
            raise

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("multi-kernel executor is closed")

    def cleanup(self) -> None:
        """Idempotently stop kernels, local processes, the RPC server, and socket."""
        if self._closed:
            return
        self._closed = True
        try:
            self.kernel_manager.shutdown()
        finally:
            self.tool_server.stop()
