"""Harness-owned Unix-socket RPC for stateful local execution tools."""

from __future__ import annotations

import base64
import json
import os
import pickle
import shutil
import socket
import socketserver
import tempfile
import threading
from pathlib import Path
from typing import Any

import psutil

from core.tools import _LocalExecState


class FinalAnswerSignal(BaseException):
    """Kernel-local unwind raised after final_answer is recorded by the harness."""

    def __init__(self, value: Any, note: str | None = None):
        super().__init__()
        self.value = value
        self.note = note


def _safe_repr(value: Any) -> tuple[str, str | None]:
    try:
        return repr(value)[:30_000], None
    except Exception as exc:
        return (
            f"<unrepresentable {type(value).__name__}: {type(exc).__name__}: {exc}>",
            f"repr failed ({type(exc).__name__})",
        )


def _pack(value: Any, label: str = "final_answer") -> tuple[str | None, str, str | None]:
    fallback, repr_note = _safe_repr(value)
    try:
        raw = pickle.dumps(value)
        return base64.b64encode(raw).decode("ascii"), fallback, repr_note
    except Exception as exc:
        note = f"{label} was not picklable ({type(exc).__name__}); returned truncated repr"
        if repr_note:
            note += f"; {repr_note}"
        return None, fallback, note


def _unpack(payload: str) -> Any:
    return pickle.loads(base64.b64decode(payload.encode("ascii")))


def _is_pid_target(target: str | int) -> bool:
    """A numeric target is always a local process, never a kernel name."""
    try:
        int(str(target).removeprefix("bash:"))
        return True
    except ValueError:
        return False


class _ThreadingUnixServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True
    request_queue_size = 64


class ToolServer:
    """Small JSON-RPC server; stateful processes stay in the harness process."""

    def __init__(self, state: _LocalExecState, kernel_manager=None):
        self.state = state
        self.kernel_manager = kernel_manager
        self._tmpdir: Path | None = None
        self.socket_path: Path | None = None
        self._server: _ThreadingUnixServer | None = None
        self._thread: threading.Thread | None = None
        self._final_answers: dict[str, tuple[Any, str | None]] = {}
        self._final_lock = threading.Lock()
        self._registered_processes: dict[str, dict[int, float]] = {}
        self._frozen_process_registration: set[str] = set()
        self._process_lock = threading.Lock()

    def start(self) -> Path:
        if self._server is not None:
            return self.socket_path  # type: ignore[return-value]
        self._tmpdir = Path(tempfile.mkdtemp(prefix="matclaw_", dir="/tmp"))
        self.socket_path = self._tmpdir / "tools.sock"
        owner = self

        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                for raw in self.rfile:
                    request_id = None
                    try:
                        request = json.loads(raw)
                        request_id = request.get("id")
                        if request.get("jsonrpc") != "2.0" or not isinstance(
                            request.get("method"), str
                        ):
                            raise ValueError("invalid JSON-RPC request")
                        result = owner.dispatch(request["method"], request.get("params") or {})
                        response = {"jsonrpc": "2.0", "id": request_id, "result": result}
                    except Exception as exc:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {"type": type(exc).__name__, "message": str(exc)},
                        }
                    self.wfile.write((json.dumps(response, default=str) + "\n").encode())
                    self.wfile.flush()

        self._server = _ThreadingUnixServer(str(self.socket_path), Handler)
        self._thread = threading.Thread(
            target=self._server.serve_forever, name="matclaw-toolserver", daemon=True
        )
        self._thread.start()
        return self.socket_path

    def set_kernel_manager(self, kernel_manager) -> None:
        self.kernel_manager = kernel_manager

    def dispatch(self, method: str, params: dict) -> Any:
        if method == "bash":
            return self.state.run_bash(**params)
        if method == "wait_command":
            target = params["target"]
            if self._is_local_target(target):
                return self.state.wait_command(target, params.get("timeout", 60))
            if self.kernel_manager is None or _is_pid_target(target):
                raise ValueError(f"unknown target: {target}")
            return self.kernel_manager.wait_command(target, params.get("timeout", 60))
        if method == "kill_command":
            target = params["target"]
            if self._is_local_target(target):
                return self.state.kill_command(target)
            if self.kernel_manager is None or _is_pid_target(target):
                raise ValueError(f"unknown target: {target}")
            return self.kernel_manager.kill_command(target)
        if method == "final_answer":
            note = params.get("note")
            try:
                value = _unpack(params["value"]) if params.get("value") is not None else params["repr"]
            except Exception as exc:
                value = params["repr"]
                note = (
                    f"final_answer could not be unpickled in the harness "
                    f"({type(exc).__name__}); returned truncated repr"
                )
            kernel = str(params.get("kernel", "default"))
            with self._final_lock:
                self._final_answers[kernel] = (value, note)
            return {"recorded": True, "note": note}
        if method == "pause_status":
            controller = self.state.pause_controller
            return {"paused": bool(controller is not None and controller.is_paused)}
        if method == "register_process":
            kernel = str(params["kernel"])
            pid = int(params["pid"])
            create_time = float(params["create_time"])
            with self._process_lock:
                frozen = kernel in self._frozen_process_registration
                if not frozen:
                    registry = self._registered_processes.setdefault(kernel, {})
                    # Opportunistic pruning: drop entries whose PID is gone or
                    # reused, so the registry cannot grow without bound in a run.
                    for known_pid, known_create in list(registry.items()):
                        try:
                            alive = psutil.Process(known_pid).create_time() == known_create
                        except psutil.Error:
                            alive = False
                        if not alive:
                            del registry[known_pid]
                    registry[pid] = create_time
            if frozen:
                self._kill_registered_process(pid, create_time)
                raise RuntimeError(f"kernel {kernel!r} is shutting down")
            return {"registered": True}
        raise ValueError(f"unknown RPC method: {method}")

    def _is_local_target(self, target: str | int) -> bool:
        return self.state.is_local_target(target)

    def take_final_answer(self, kernel: str) -> tuple[Any, str | None] | None:
        with self._final_lock:
            return self._final_answers.pop(kernel, None)

    def registered_processes(self, kernel: str) -> dict[int, float]:
        with self._process_lock:
            return dict(self._registered_processes.get(kernel, {}))

    def clear_registered_processes(self, kernel: str) -> None:
        with self._process_lock:
            self._registered_processes.pop(kernel, None)

    def freeze_process_registration(self, kernel: str) -> None:
        """Reject and kill children registered while a kernel is being stopped."""
        with self._process_lock:
            self._frozen_process_registration.add(kernel)

    def unfreeze_process_registration(self, kernel: str) -> None:
        with self._process_lock:
            self._frozen_process_registration.discard(kernel)

    @staticmethod
    def _kill_registered_process(pid: int, create_time: float) -> None:
        try:
            process = psutil.Process(pid)
            if abs(process.create_time() - create_time) >= 1e-6:
                return
            process.kill()
            process.wait(timeout=1)
        except psutil.Error:
            pass

    def stop(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        if self._thread is not None:
            self._thread.join(timeout=2)
            self._thread = None
        self.state.shutdown()
        if self._tmpdir is not None:
            shutil.rmtree(self._tmpdir, ignore_errors=True)
            self._tmpdir = None
            self.socket_path = None


class ToolClient:
    """One-request-per-connection client used by kernel-side stubs."""

    def __init__(self, socket_path: str | os.PathLike[str]):
        self.socket_path = str(socket_path)

    def call(self, method: str, params: dict | None = None) -> Any:
        request = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(self.socket_path)
            sock.sendall((json.dumps(request) + "\n").encode())
            stream = sock.makefile("rb")
            raw = stream.readline()
        if not raw:
            raise ConnectionError("tool server closed without a response")
        response = json.loads(raw)
        if "error" in response:
            error = response["error"]
            raise RuntimeError(f"{error['type']}: {error['message']}")
        return response["result"]


def build_stateful_stubs(
    socket_path: str,
    kernel_name: str = "default",
    disabled: set[str] | frozenset[str] | None = None,
) -> dict[str, Any]:
    """Return the four kernel callables backed by the harness ToolServer."""
    client = ToolClient(socket_path)

    def bash(
        command: str,
        timeout: int = 120,
        max_output_chars: int = 30_000,
        cwd: str | None = None,
        run_in_background: bool = False,
    ):
        return client.call(
            "bash",
            {
                "command": command,
                "timeout": timeout,
                "max_output_chars": max_output_chars,
                "cwd": cwd,
                "run_in_background": run_in_background,
            },
        )

    def wait_command(target: str, timeout: int = 60):
        return client.call("wait_command", {"target": target, "timeout": timeout})

    def kill_command(target: str):
        return client.call("kill_command", {"target": target})

    def final_answer(value=None, **kwargs):
        if value is None and kwargs:
            value = next(iter(kwargs.values()))
        payload, fallback, note = _pack(value)
        response = client.call(
            "final_answer",
            {
                "kernel": kernel_name,
                "value": payload,
                "repr": fallback,
                "note": note,
            },
        )
        raise FinalAnswerSignal(value if response.get("note") is None else fallback, response.get("note"))

    stubs = {
        "bash": bash,
        "wait_command": wait_command,
        "kill_command": kill_command,
        "final_answer": final_answer,
    }
    disabled = disabled or set()
    return {
        name: value
        for name, value in stubs.items()
        if name == "final_answer" or name not in disabled
    }
