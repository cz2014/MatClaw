"""Named persistent ipykernels with bounded check-ins and harness supervision."""

from __future__ import annotations

import base64
import os
import pickle
import queue
import re
import subprocess
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import psutil
from jupyter_client import KernelManager as JupyterKernelManager

from core.tools import ToolSpec, _collapse_cr, _fmt_duration
from core.toolserver import FinalAnswerSignal

# The execution contract these three numbers describe is rendered into the system
# prompt, so they are public: the prompt-parity test imports them and fails when a
# change here is not carried into the prompt text.
DEFAULT_STEP_TIMEOUT_S = 120
MAX_STEP_TIMEOUT_S = 600
MAX_KERNELS = 3

# Names must start with a letter so a kernel name can never be confused with a
# numeric background-PID target in wait_command/kill_command routing.
_KERNEL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,31}$")
_DIRECTIVE_RE = re.compile(r"^#\s*(kernel|timeout)\s*:\s*(.*?)\s*$", re.IGNORECASE)
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


class KernelCapacityError(RuntimeError):
    """All kernel slots are taken; the refusal return doubles as a check-in."""


@dataclass(frozen=True)
class ExecutionDirectives:
    kernel: str = "default"
    timeout: int = DEFAULT_STEP_TIMEOUT_S


def parse_directives(code: str) -> ExecutionDirectives:
    """Parse routing directives from the leading blank/comment block only."""
    kernel = "default"
    timeout = DEFAULT_STEP_TIMEOUT_S
    for line in code.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("#"):
            break
        match = _DIRECTIVE_RE.match(stripped)
        if match is None:
            continue
        key, value = match.groups()
        # Tolerate an explanatory trailing comment ("# kernel: gpu  # hot model").
        value = value.split("#", 1)[0].strip()
        if key.lower() == "kernel":
            if not _KERNEL_RE.fullmatch(value):
                raise ValueError(f"Malformed kernel directive: {line}")
            kernel = value.lower()
        else:
            try:
                parsed = int(value)
            except ValueError:
                raise ValueError(f"Malformed timeout directive: {line}") from None
            if parsed <= 0:
                raise ValueError(f"Malformed timeout directive: {line}")
            timeout = min(parsed, MAX_STEP_TIMEOUT_S)
    return ExecutionDirectives(kernel=kernel, timeout=timeout)


def _sanitize_traceback(frames: list, source_name: str) -> list[str]:
    """Strip ANSI escapes and drop harness wrapper frames from an IPython traceback.

    Keeps the banner and exception lines plus every frame that belongs to the
    step's own source file; drops the wrapper cell and ``_matclaw_execute``
    internals. Falls back to the full (ANSI-stripped) traceback if filtering
    would remove everything.
    """
    cleaned = [_ANSI_RE.sub("", str(frame)) for frame in frames]
    kept = [
        frame
        for frame in cleaned
        # "<file>:<line>" only appears in a real frame header for the step file;
        # the wrapper cell merely quotes the path as a call argument.
        if f"{source_name}:" in frame
        or not ("_matclaw_execute" in frame or "Cell In[" in frame or "<ipython-input" in frame)
    ]
    return kept or cleaned


@dataclass
class _KernelExecution:
    msg_id: str
    log_path: Path
    result_path: Path
    source_path: Path
    started_at: float
    deadline: float | None = None
    done: threading.Event = field(default_factory=threading.Event)
    cancelled: threading.Event = field(default_factory=threading.Event)
    reader: threading.Thread | None = None
    error: dict | None = None
    output: Any = None
    output_note: str | None = None
    is_final_answer: bool = False
    namespace_preserved: bool = True


@dataclass
class _Kernel:
    name: str
    manager: JupyterKernelManager
    client: Any
    pid: int
    token: str
    started_at: float
    current: _KernelExecution | None = None
    completed: dict | None = None
    completed_note: str | None = None
    sample_stop: threading.Event = field(default_factory=threading.Event)
    sample_ready: threading.Event = field(default_factory=threading.Event)
    sampler: threading.Thread | None = None
    latest_vitals: dict = field(default_factory=dict)
    sample_rss: int = 0
    sample_log_size: int = 0
    needs_restart: bool = False


_BOOTSTRAP = r'''
import ast as _matclaw_ast
import base64 as _matclaw_base64
import pickle as _matclaw_pickle
from core.tools import build_stateless_tools as _matclaw_build_tools
from core.toolserver import build_stateful_stubs as _matclaw_build_stubs
from core.toolserver import ToolClient as _MatclawToolClient

_matclaw_spec = _matclaw_pickle.loads(_matclaw_base64.b64decode("__SPEC__"))
for _matclaw_tool in _matclaw_build_tools(_matclaw_spec):
    globals()[_matclaw_tool.name] = _matclaw_tool
globals().update(
    _matclaw_build_stubs(
        "__SOCKET__", "__KERNEL__", disabled=set(_matclaw_spec.disabled)
    )
)
globals().update(_matclaw_pickle.loads(_matclaw_base64.b64decode("__VARIABLES__")))

# Register subprocess children synchronously with the harness before returning
# from Popen, so even a subsequent os._exit cannot orphan a detached child.
import os as _matclaw_os
import signal as _matclaw_signal
import subprocess as _matclaw_subprocess
import psutil as _matclaw_psutil
_matclaw_original_popen = _matclaw_subprocess.Popen
class _MatclawPopen(_matclaw_original_popen):
    _rpc = _MatclawToolClient("__SOCKET__")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self._rpc.call(
                "register_process",
                {
                    "kernel": "__KERNEL__",
                    "pid": self.pid,
                    "create_time": _matclaw_psutil.Process(self.pid).create_time(),
                },
            )
        except Exception as _exc:
            # An unregistered child would be unsupervised; kill it and fail fast
            # with a message that names the real cause (harness unreachable).
            try:
                if kwargs.get("start_new_session"):
                    _matclaw_os.killpg(self.pid, _matclaw_signal.SIGKILL)
                else:
                    self.kill()
            except Exception:
                pass
            raise RuntimeError(
                "matclaw harness tool server unreachable (shutting down?); "
                f"subprocess registration failed: {type(_exc).__name__}: {_exc}"
            ) from _exc
_matclaw_subprocess.Popen = _MatclawPopen

def _matclaw_execute(_source_path, _result_path):
    # The step source lives in a real file and is compiled under that filename,
    # so tracebacks show the agent's own code with correct line numbers.
    with open(_source_path, "r", encoding="utf-8") as _stream:
        _source = _stream.read()
    _tree = _matclaw_ast.parse(_source, _source_path, mode="exec")
    _value = None
    if _tree.body and isinstance(_tree.body[-1], _matclaw_ast.Expr):
        _last = _matclaw_ast.Expression(_tree.body.pop().value)
        _matclaw_ast.fix_missing_locations(_last)
        exec(compile(_tree, _source_path, "exec"), globals())
        _value = eval(compile(_last, _source_path, "eval"), globals())
    else:
        exec(compile(_tree, _source_path, "exec"), globals())
    _note = None
    try:
        _fallback = repr(_value)[:30000]
    except Exception as _repr_exc:
        _fallback = (
            f"<unrepresentable {type(_value).__name__}: "
            f"{type(_repr_exc).__name__}: {_repr_exc}>"
        )
        _note = f"repr failed ({type(_repr_exc).__name__})"
    try:
        _payload = _matclaw_pickle.dumps(_value)
    except Exception as _exc:
        _payload = None
        _pickle_note = f"output was not picklable ({type(_exc).__name__}); returned truncated repr"
        _note = f"{_pickle_note}; {_note}" if _note else _pickle_note
    with open(_result_path, "wb") as _stream:
        _matclaw_pickle.dump(
            {"payload": _payload, "repr": _fallback, "note": _note}, _stream
        )
'''


class KernelManager:
    """Own up to three named persistent kernels and all execution state."""

    def __init__(
        self,
        workspace: Path,
        tool_spec: ToolSpec,
        tool_server,
        max_kernels: int = MAX_KERNELS,
        grace_s: float = 15.0,
        inline_limit: int = 30_000,
    ):
        self.workspace = workspace.resolve()
        self.tool_spec = tool_spec
        self.tool_server = tool_server
        self.max_kernels = max_kernels
        self.grace_s = grace_s
        self.inline_limit = inline_limit
        self.kernels: dict[str, _Kernel] = {}
        self.variables: dict[str, Any] = {}
        self._step = 0
        self._notes: list[str] = []
        self._lock = threading.RLock()
        self._closed = False
        self.tool_server.set_kernel_manager(self)
        self._start_kernel("default")

    @staticmethod
    def _b64_pickle(value: Any, label: str) -> str:
        try:
            return base64.b64encode(pickle.dumps(value)).decode("ascii")
        except Exception as exc:
            raise TypeError(f"{label} is not picklable: {type(exc).__name__}: {exc}") from exc

    def send_variables(self, variables: dict[str, Any]) -> None:
        if self._closed:
            raise RuntimeError("kernel manager is shut down")
        payload = self._b64_pickle(variables, "send_variables value")
        for kernel in self.kernels.values():
            if kernel.current is not None and not kernel.current.done.is_set():
                raise RuntimeError(f"cannot send variables while kernel {kernel.name!r} is busy")
        self.variables.update(variables)
        code = (
            "import base64 as _b64, pickle as _pickle\n"
            f"globals().update(_pickle.loads(_b64.b64decode({payload!r})))"
        )
        for kernel in self.kernels.values():
            self._execute_internal(kernel, code)

    def _start_kernel(self, name: str) -> _Kernel:
        if name in self.kernels:
            return self.kernels[name]
        if len(self.kernels) >= self.max_kernels:
            raise KernelCapacityError(f"kernel cap {self.max_kernels} reached")
        env = os.environ.copy()
        env["MATCLAW_TOOL_SOCKET"] = str(self.tool_server.socket_path)
        token = f"{name}-{uuid.uuid4().hex}"
        env["MATCLAW_KERNEL_TOKEN"] = token
        manager = JupyterKernelManager(kernel_name="python3")
        manager.start_kernel(cwd=str(self.workspace), env=env)
        client = manager.blocking_client()
        client.start_channels()
        try:
            client.wait_for_ready(timeout=30)
            pid = int(manager.provisioner.pid)
            kernel = _Kernel(name, manager, client, pid, token, time.monotonic())
            self.kernels[name] = kernel
            self._bootstrap(kernel)
            self._start_sampler(kernel)
            return kernel
        except Exception:
            client.stop_channels()
            manager.shutdown_kernel(now=True)
            raise

    def _bootstrap(self, kernel: _Kernel) -> None:
        code = (
            _BOOTSTRAP.replace("__SPEC__", self._b64_pickle(self.tool_spec, "ToolSpec"))
            .replace("__VARIABLES__", self._b64_pickle(self.variables, "kernel variables"))
            .replace(
                "__SOCKET__",
                str(self.tool_server.socket_path).replace("\\", "\\\\").replace('"', '\\"'),
            )
            .replace("__KERNEL__", kernel.name.replace("\\", "\\\\").replace('"', '\\"'))
        )
        self._execute_internal(kernel, code)

    @staticmethod
    def _execute_internal(kernel: _Kernel, code: str, timeout: float = 30) -> None:
        msg_id = kernel.client.execute(code, store_history=False, allow_stdin=False)
        deadline = time.monotonic() + timeout
        errors = []
        reached_idle = False
        while time.monotonic() < deadline:
            try:
                message = kernel.client.get_iopub_msg(timeout=0.2)
            except queue.Empty:
                continue
            if message.get("parent_header", {}).get("msg_id") != msg_id:
                continue
            msg_type = message.get("header", {}).get("msg_type")
            if msg_type == "error":
                errors.append(message["content"])
            if msg_type == "status" and message["content"].get("execution_state") == "idle":
                reached_idle = True
                break
        if not reached_idle:
            raise TimeoutError("kernel bootstrap timed out")
        KernelManager._drain_shell_reply(kernel, msg_id, max(0.1, deadline - time.monotonic()))
        if errors:
            error = errors[-1]
            raise RuntimeError(
                f"kernel bootstrap failed: {error.get('ename')}: {error.get('evalue')}"
            )

    @staticmethod
    def _drain_shell_reply(kernel: _Kernel, msg_id: str, timeout: float = 5.0) -> dict:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                message = kernel.client.get_shell_msg(
                    timeout=min(0.2, max(0.01, deadline - time.monotonic()))
                )
            except queue.Empty:
                continue
            if message.get("parent_header", {}).get("msg_id") == msg_id:
                return message.get("content", {})
        raise TimeoutError(f"missing execute_reply for {msg_id}")

    def execute(
        self, code: str, kernel_name: str = "default", timeout: int = DEFAULT_STEP_TIMEOUT_S
    ) -> dict:
        timeout = min(max(1, int(timeout)), MAX_STEP_TIMEOUT_S)
        with self._lock:
            try:
                kernel = self._ensure_kernel(kernel_name)
            except KernelCapacityError as exc:
                # Only the cap refusal gets the refused shape; a kernel that fails
                # to start or restart propagates as a real error to the agent.
                return self._with_notes(
                    {
                        "running": False,
                        "refused": True,
                        "error": str(exc),
                        "roster": self.roster_line(),
                    }
                )
            self._lazy_reap(kernel)
            if kernel.current is not None:
                return self._running_result(kernel, refused=True)
            # A new step supersedes the previous one's collectable result, never
            # its note: the note stays queued until a return announces it.
            kernel.completed = None
            kernel.completed_note = None
            # This counter only advances for steps that reach a kernel, so the
            # on-disk .kernel_* numbering trails the agent's step numbering
            # whenever a step was handled harness-side (bare wait/kill calls).
            self._step += 1
            safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", kernel.name)
            log_path = self.workspace / f".kernel_{safe_name}_step_{self._step}.log"
            result_path = self.workspace / f".kernel_{safe_name}_step_{self._step}.result"
            source_path = self.workspace / f".kernel_{safe_name}_step_{self._step}.py"
            source_path.write_text(code, encoding="utf-8")
            # A prior cell may have deliberately caught BaseException after the
            # final-answer RPC, or crashed before emitting its error message.
            # Never let that stale record turn a later unrelated error into a
            # final answer.
            self.tool_server.take_final_answer(kernel.name)
            wrapper = f"_matclaw_execute({str(source_path)!r}, {str(result_path)!r})"
            msg_id = kernel.client.execute(wrapper, store_history=False, allow_stdin=False)
            execution = _KernelExecution(
                msg_id, log_path, result_path, source_path, time.monotonic()
            )
            execution.deadline = execution.started_at + timeout
            kernel.current = execution
            execution.reader = threading.Thread(
                target=self._read_execution,
                args=(kernel, execution),
                name=f"matclaw-iopub-{kernel.name}-{self._step}",
                daemon=True,
            )
            execution.reader.start()
        if execution.done.wait(timeout):
            with self._lock:
                return self._with_notes(self._collect(kernel, execution))
        with self._lock:
            return self._running_result(kernel)

    def dispatch(self, code: str) -> dict:
        directives = parse_directives(code)
        return self.execute(code, directives.kernel, directives.timeout)

    def remaining_step_time(self, name: str) -> float | None:
        """Seconds left on the named kernel's current step deadline, if busy."""
        with self._lock:
            kernel = self.kernels.get(str(name))
            if kernel is None or kernel.current is None or kernel.current.done.is_set():
                return None
            deadline = kernel.current.deadline
        return None if deadline is None else max(0.0, deadline - time.monotonic())

    def _read_execution(self, kernel: _Kernel, execution: _KernelExecution) -> None:
        execution.log_path.touch()
        try:
            with execution.log_path.open("a", encoding="utf-8") as log:
                while not execution.cancelled.is_set():
                    try:
                        message = kernel.client.get_iopub_msg(timeout=0.2)
                    except queue.Empty:
                        if not kernel.manager.is_alive():
                            execution.error = {
                                "ename": "KernelDied",
                                "evalue": f"kernel {kernel.name!r} exited",
                                "traceback": [],
                            }
                            execution.namespace_preserved = False
                            kernel.needs_restart = True
                            break
                        continue
                    if message.get("parent_header", {}).get("msg_id") != execution.msg_id:
                        continue
                    content = message.get("content", {})
                    msg_type = message.get("header", {}).get("msg_type")
                    if msg_type == "stream":
                        log.write(content.get("text", ""))
                        log.flush()
                    elif msg_type == "error":
                        # Only the final-answer unwind itself may claim the
                        # recorded value: a cell that catches it and then raises
                        # a real error must be reported as that error, and the
                        # stale record is dropped with the cell.
                        recorded = self.tool_server.take_final_answer(kernel.name)
                        final = (
                            recorded
                            if content.get("ename") == FinalAnswerSignal.__name__
                            else None
                        )
                        if final is not None:
                            execution.output, execution.output_note = final
                            execution.is_final_answer = True
                        else:
                            execution.error = {
                                "ename": content.get("ename"),
                                "evalue": content.get("evalue"),
                                "traceback": _sanitize_traceback(
                                    content.get("traceback") or [],
                                    execution.source_path.name,
                                ),
                            }
                            if execution.error["traceback"]:
                                log.write("\n".join(execution.error["traceback"]) + "\n")
                                log.flush()
                    elif msg_type == "status" and content.get("execution_state") == "idle":
                        break
            if not execution.cancelled.is_set() and kernel.manager.is_alive():
                self._drain_shell_reply(kernel, execution.msg_id)
            if not execution.is_final_answer and execution.error is None:
                try:
                    with execution.result_path.open("rb") as stream:
                        result = pickle.load(stream)
                    try:
                        execution.output = (
                            pickle.loads(result["payload"])
                            if result.get("payload") is not None
                            else result["repr"]
                        )
                        execution.output_note = result.get("note")
                    except Exception as exc:
                        execution.output = result["repr"]
                        execution.output_note = (
                            f"output could not be unpickled in the harness "
                            f"({type(exc).__name__}); returned truncated repr"
                        )
                except FileNotFoundError:
                    execution.output = None
        except Exception as exc:
            if not execution.cancelled.is_set():
                execution.error = {
                    "ename": type(exc).__name__,
                    "evalue": str(exc),
                    "traceback": [],
                }
        finally:
            execution.result_path.unlink(missing_ok=True)
            execution.done.set()

    def _ensure_kernel(self, name: str) -> _Kernel:
        if self._closed:
            raise RuntimeError("kernel manager is shut down")
        kernel = self.kernels.get(name)
        if kernel is None:
            return self._start_kernel(name)
        if kernel.manager.is_alive() and not kernel.needs_restart:
            return kernel
        self._restart(kernel)
        self._notes.append(f"kernel {name} restarted after exit; namespace lost")
        return kernel

    def _lazy_reap(self, kernel: _Kernel) -> None:
        execution = kernel.current
        if execution is not None and execution.done.is_set():
            result = self._collect(kernel, execution)
            kernel.completed = result
            kernel.completed_note = self._completion_note(kernel.name, result)
            self._notes.append(kernel.completed_note)

    def _with_notes(self, result: dict) -> dict:
        """Attach the pending completion notes to a return and clear the queue.

        The queue is the only home of a background completion's note, so no
        return can bury one and a superseded stash cannot take one with it.
        A completion is announced once: delivering its note here retires the
        stashed result that ``wait_command`` would otherwise hand out again.
        """
        notes, self._notes = self._notes, []
        if not notes:
            return result
        result["completion_notes"] = notes
        for kernel in self.kernels.values():
            if kernel.completed_note in notes:
                kernel.completed = None
                kernel.completed_note = None
        return result

    @staticmethod
    def _completion_note(name: str, result: dict) -> str:
        try:
            rendered_output = repr(result.get("output"))[:4000]
        except Exception as exc:
            rendered_output = f"<repr failed: {type(exc).__name__}: {exc}>"
        note = f"kernel {name} step completed; output={rendered_output}"
        if result.get("error"):
            error = result["error"]
            note += f"; error={error.get('ename')}: {error.get('evalue')}"
        logs = str(result.get("logs") or "")
        if logs:
            note += f"; log_tail={logs[-4000:]}"
        if result.get("log_file"):
            note += f"; log_file={result['log_file']}"
        return note

    def _log_output(self, execution: _KernelExecution) -> tuple[str, bool]:
        try:
            size = execution.log_path.stat().st_size
        except FileNotFoundError:
            return "", False
        if size <= self.inline_limit:
            return (
                _collapse_cr(execution.log_path.read_text(encoding="utf-8", errors="replace")),
                False,
            )
        half = max(1, self.inline_limit // 2)
        with execution.log_path.open("rb") as stream:
            head = stream.read(half).decode("utf-8", errors="replace")
            stream.seek(max(0, size - half))
            tail = stream.read(half).decode("utf-8", errors="replace")
        return (
            _collapse_cr(head)
            + f"\n..._This content has been truncated to stay below {self.inline_limit} characters_...\n"
            + _collapse_cr(tail),
            True,
        )

    def _collect(self, kernel: _Kernel, execution: _KernelExecution) -> dict:
        logs, truncated = self._log_output(execution)
        result = {
            "running": False,
            "kernel": kernel.name,
            "output": execution.output,
            "logs": logs,
            "truncated": truncated,
            "log_file": os.path.relpath(execution.log_path, self.workspace),
            "is_final_answer": execution.is_final_answer,
            "namespace_preserved": execution.namespace_preserved,
        }
        if execution.output_note:
            result["note"] = execution.output_note
        if execution.error:
            result["error"] = execution.error
        if kernel.current is execution:
            kernel.current = None
        return result

    def _running_result(self, kernel: _Kernel, refused: bool = False) -> dict:
        execution = kernel.current
        if execution is None:
            return self._with_notes({"running": False, "kernel": kernel.name})
        if execution.done.is_set():
            return self._with_notes(self._collect(kernel, execution))
        logs, truncated = self._log_output(execution)
        vitals = self.vitals(kernel.name)
        if execution.done.is_set():
            return self._with_notes(self._collect(kernel, execution))
        result = {
            "running": True,
            "kernel": kernel.name,
            "elapsed": time.monotonic() - execution.started_at,
            "logs": logs,
            "tail": logs[-4000:],
            "truncated": truncated,
            "log_file": os.path.relpath(execution.log_path, self.workspace),
            "vitals": vitals,
            "roster": self.roster_line(skip_reap={kernel.name}),
        }
        if refused:
            result["refused"] = True
        return self._with_notes(result)

    def wait_command(self, target: str, timeout: int = 60) -> dict:
        with self._lock:
            kernel = self.kernels.get(str(target))
            if kernel is None:
                raise ValueError(f"unknown kernel: {target}")
            execution = kernel.current
            if execution is None:
                if kernel.completed is not None:
                    # Handing out the stashed result announces this completion,
                    # so its queued note must not announce it a second time.
                    result, kernel.completed = kernel.completed, None
                    self._notes.remove(kernel.completed_note)
                    kernel.completed_note = None
                    return self._with_notes(result)
                return self._with_notes(
                    {"running": False, "kernel": kernel.name, "roster": self.roster_line()}
                )
            if execution.done.is_set():
                return self._with_notes(self._collect(kernel, execution))
        if execution.done.wait(min(max(0, int(timeout or 60)), MAX_STEP_TIMEOUT_S)):
            with self._lock:
                return self._with_notes(self._collect(kernel, execution))
        with self._lock:
            return self._running_result(kernel)

    def kill_command(self, target: str) -> dict:
        with self._lock:
            kernel = self.kernels.get(str(target))
            if kernel is None:
                raise ValueError(f"unknown kernel: {target}")
            execution = kernel.current
            if execution is None:
                return self._with_notes(
                    {
                        "running": False,
                        "kernel": kernel.name,
                        "method": "noop",
                        "namespace_preserved": True,
                    }
                )
            if execution.done.is_set():
                return self._with_notes(
                    self._collect_after_kill(kernel, execution, method="noop")
                )
            kernel.manager.interrupt_kernel()
        if execution.done.wait(self.grace_s):
            with self._lock:
                return self._with_notes(
                    self._collect_after_kill(kernel, execution, method="interrupt")
                )
        with self._lock:
            logs, truncated = self._log_output(execution)
            if logs:
                # Replaying the killed step's stdout unlabeled reads as if the
                # workload had just started again.
                logs = "[output before kill]\n" + logs
            execution.cancelled.set()
            survivors = self._restart(kernel)
            kernel.current = None
            result = {
                "running": False,
                "kernel": kernel.name,
                "method": "restart",
                "namespace_preserved": False,
                "logs": logs,
                "truncated": truncated,
                "log_file": os.path.relpath(execution.log_path, self.workspace),
            }
            if survivors:
                result["survivors"] = survivors
            return self._with_notes(result)

    def _collect_after_kill(
        self, kernel: _Kernel, execution: _KernelExecution, method: str
    ) -> dict:
        result = self._collect(kernel, execution)
        if not execution.namespace_preserved or not kernel.manager.is_alive():
            survivors = self._restart(kernel)
            result.update(method="restart", namespace_preserved=False)
            if survivors:
                result["survivors"] = survivors
        else:
            result.update(method=method, namespace_preserved=True)
        return result

    def _restart(self, kernel: _Kernel) -> list[int]:
        """Rebuild the kernel; return the swept pids that outlived the sweep."""
        # A failed restart must never leave the kernel frozen for registration:
        # frozen means every later subprocess.Popen in it is killed on arrival.
        self.tool_server.freeze_process_registration(kernel.name)
        try:
            kernel.sample_stop.set()
            if kernel.sampler is not None:
                kernel.sampler.join(timeout=1)
            if kernel.current is not None:
                kernel.current.cancelled.set()
                if kernel.current.reader is not None:
                    kernel.current.reader.join(timeout=1)
            try:
                kernel.client.stop_channels()
            except Exception:
                pass
            self._kill_kernel_process(kernel)
            survivors = self._terminate_owned_processes(kernel)
            kernel.manager.restart_kernel(now=True)
            client = kernel.manager.blocking_client()
            client.start_channels()
            client.wait_for_ready(timeout=30)
            kernel.client = client
            kernel.pid = int(kernel.manager.provisioner.pid)
            kernel.started_at = time.monotonic()
            kernel.current = None
            kernel.completed = None
            kernel.completed_note = None
            kernel.sample_stop = threading.Event()
            kernel.sample_ready = threading.Event()
            kernel.latest_vitals = {}
            kernel.sample_rss = 0
            kernel.sample_log_size = 0
            kernel.needs_restart = False
            self._bootstrap(kernel)
            self._start_sampler(kernel)
            return survivors
        finally:
            self.tool_server.unfreeze_process_registration(kernel.name)

    @staticmethod
    def _kill_kernel_process(kernel: _Kernel) -> None:
        """Quiesce the old kernel before the final owned-process sweep."""
        try:
            process = psutil.Process(kernel.pid)
            process.kill()
            process.wait(timeout=2)
        except psutil.Error:
            pass

    @staticmethod
    def _kernel_resources(kernel: _Kernel) -> tuple[float, int, int]:
        process = psutil.Process(kernel.pid)
        processes = [process, *process.children(recursive=True)]
        cpu = sum(sum(proc.cpu_times()[:2]) for proc in processes if proc.is_running())
        rss = sum(proc.memory_info().rss for proc in processes if proc.is_running())
        return cpu, rss, max(0, len(processes) - 1)

    def _start_sampler(self, kernel: _Kernel, window_s: float = 1.0, tick_s: float = 0.2) -> None:
        def sample() -> None:
            try:
                cpu, rss, _ = self._kernel_resources(kernel)
                kernel.sample_rss = rss
            except psutil.Error:
                cpu = 0.0
            history = [(time.monotonic(), cpu)]
            while not kernel.sample_stop.wait(tick_s):
                try:
                    cpu, rss, children = self._kernel_resources(kernel)
                    now = time.monotonic()
                    history.append((now, cpu))
                    cutoff = now - window_s
                    while len(history) > 2 and history[1][0] <= cutoff:
                        history.pop(0)
                    old_at, old_cpu = history[0]
                    kernel.latest_vitals = {
                        "pid": kernel.pid,
                        "elapsed_s": now - kernel.started_at,
                        "cpu_time_s": cpu,
                        "cpu_over_wall": max(0.0, cpu - old_cpu) / max(1e-9, now - old_at),
                        "rss_bytes": rss,
                        "children": children,
                    }
                    kernel.sample_ready.set()
                except psutil.Error:
                    if not kernel.manager.is_alive():
                        return

        kernel.sampler = threading.Thread(
            target=sample, name=f"matclaw-kernel-vitals-{kernel.name}", daemon=True
        )
        kernel.sampler.start()

    def _vram_bytes(self, pid: int) -> int | None:
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-compute-apps=pid,used_memory",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
        except (FileNotFoundError, subprocess.SubprocessError):
            return None
        total_mib = 0
        for line in result.stdout.splitlines():
            fields = [field.strip() for field in line.split(",")]
            if len(fields) == 2 and fields[0] == str(pid):
                try:
                    total_mib += int(fields[1])
                except ValueError:
                    continue
        return total_mib * 1024 * 1024 if total_mib else None

    @staticmethod
    def _owned_processes(kernel: _Kernel) -> list[psutil.Process]:
        owned = []
        for process in psutil.process_iter():
            if process.pid == kernel.pid:
                continue
            try:
                if process.environ().get("MATCLAW_KERNEL_TOKEN") == kernel.token:
                    owned.append(process)
            except (psutil.Error, OSError):
                continue
        return owned

    @staticmethod
    def _is_live(process: psutil.Process) -> bool:
        """A reaped-but-unwaited zombie is gone for supervision purposes."""
        try:
            return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
        except psutil.Error:
            return False

    def _terminate_owned_processes(self, kernel: _Kernel) -> list[int]:
        """Kill the kernel's process forest; return the pids still alive after it."""
        by_pid = {process.pid: process for process in self._owned_processes(kernel)}
        for pid, create_time in self.tool_server.registered_processes(kernel.name).items():
            try:
                process = psutil.Process(pid)
                if abs(process.create_time() - create_time) < 1e-6:
                    by_pid[pid] = process
            except psutil.Error:
                continue

        # Preserve ancestry while freezing the complete process forest. Killing
        # a root first would reparent detached grandchildren and make them
        # undiscoverable on platforms where reading another process's environ
        # is restricted. Once every discovered node is suspended, the forest
        # is stable and can be killed without a spawn-between-snapshot race.
        pending = list(by_pid.values())
        frozen: dict[tuple[int, float], psutil.Process] = {}
        while pending:
            process = pending.pop()
            try:
                key = (process.pid, process.create_time())
                if key in frozen:
                    continue
                process.suspend()
                frozen[key] = process
                pending.extend(process.children(recursive=False))
            except psutil.Error:
                pass

        processes = list(frozen.values())
        for process in reversed(processes):
            try:
                process.kill()
            except psutil.Error:
                pass
        _, alive = psutil.wait_procs(processes, timeout=2)
        self.tool_server.clear_registered_processes(kernel.name)

        # Descendants that re-setsid out of the forest can outlive the ladder.
        # The leak class is accepted; reporting the kill as a clean sweep is not,
        # so re-check everything the harness knows about for this kernel.
        survivors = {process.pid for process in alive if self._is_live(process)}
        survivors.update(process.pid for process in self._owned_processes(kernel))
        return sorted(survivors)

    def vitals(self, name: str) -> dict:
        kernel = self.kernels[name]
        kernel.sample_ready.wait(timeout=0.05)
        result = dict(kernel.latest_vitals)
        if not result:
            try:
                cpu, rss, children = self._kernel_resources(kernel)
                result = {
                    "pid": kernel.pid,
                    "elapsed_s": time.monotonic() - kernel.started_at,
                    "cpu_time_s": cpu,
                    "cpu_over_wall": 0.0,
                    "rss_bytes": rss,
                    "children": children,
                }
            except psutil.Error:
                result = {"pid": kernel.pid, "elapsed_s": time.monotonic() - kernel.started_at}
        execution = kernel.current
        log_size = (
            execution.log_path.stat().st_size
            if execution is not None and execution.log_path.exists()
            else 0
        )
        result["rss_delta"] = result.get("rss_bytes", 0) - kernel.sample_rss
        result["log_bytes"] = log_size
        result["log_growth_bytes"] = log_size - kernel.sample_log_size
        kernel.sample_rss = result.get("rss_bytes", 0)
        kernel.sample_log_size = log_size
        vram = self._vram_bytes(kernel.pid)
        if vram is not None:
            result["vram_bytes"] = vram
        return result

    def roster_line(self, skip_reap: set[str] | None = None) -> str:
        skip_reap = skip_reap or set()
        rows = []
        # _lazy_reap mutates kernel/completed state, and RPC handler threads enter
        # wait/kill under the same lock -- roster rendering must hold it too.
        with self._lock:
            for name, kernel in self.kernels.items():
                if name not in skip_reap:
                    self._lazy_reap(kernel)
                vitals = self.vitals(name)
                # Idle rows carry the same memory columns as busy ones: a kernel
                # holding a hot model is idle, and that is exactly when the model
                # has to see the memory it is still paying for.
                if kernel.current is None:
                    row = f"{name}(idle"
                else:
                    row = (
                        f"{name}(busy "
                        f"{_fmt_duration(time.monotonic() - kernel.current.started_at)}, "
                        f"cpu {vitals.get('cpu_over_wall', 0) * 100:.0f}%"
                    )
                row += f", rss {vitals.get('rss_bytes', 0) / (1024 ** 3):.1f}G"
                if "vram_bytes" in vitals:
                    row += f", vram {vitals['vram_bytes'] / (1024 ** 3):.1f}G"
                rows.append(row + ")")
        return "kernels: " + " | ".join(rows)

    def shutdown(self) -> None:
        with self._lock:
            self._closed = True
            kernels = list(self.kernels.values())
            self.kernels = {}
        for kernel in kernels:
            self.tool_server.freeze_process_registration(kernel.name)
            kernel.sample_stop.set()
            if kernel.current is not None:
                kernel.current.cancelled.set()
            if kernel.sampler is not None:
                kernel.sampler.join(timeout=1)
            if kernel.current is not None and kernel.current.reader is not None:
                kernel.current.reader.join(timeout=1)
            try:
                kernel.client.stop_channels()
            except Exception:
                pass
            self._kill_kernel_process(kernel)
            try:
                self._terminate_owned_processes(kernel)
                kernel.manager.shutdown_kernel(now=True)
            except Exception:
                pass
