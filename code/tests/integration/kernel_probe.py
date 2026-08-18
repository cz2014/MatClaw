"""Standalone probe: a real ipykernel starts, executes, and shuts down cleanly.

This is a program, not a test module (pytest does not collect it). It exists as a file rather
than as an embedded string so that:
  - the container check pipes it in on stdin (`docker run -i ... python -`), leaving no Python
    on the command line and therefore no nested quoting to get wrong;
  - the same bytes can be run against the host interpreter without Docker, which is what
    tests/unit/test_docker_wrapper.py::test_kernel_probe_runs_on_host does.

Contract: exit 0 and "ok" on stdout means the kernel round-trip worked. Anything else raises.
"""

from jupyter_client.manager import start_new_kernel

TIMEOUT_S = 60


def main() -> None:
    km, kc = start_new_kernel()
    try:
        msg_id = kc.execute("print(6 * 7)")
        seen = False
        while True:
            reply = kc.get_iopub_msg(timeout=TIMEOUT_S)
            if reply.get("parent_header", {}).get("msg_id") != msg_id:
                continue
            content = reply["content"]
            if reply["msg_type"] == "stream" and "42" in content.get("text", ""):
                seen = True
            if reply["msg_type"] == "status" and content.get("execution_state") == "idle":
                break
        if not seen:
            raise SystemExit("kernel never streamed the expected '42' output")
    finally:
        kc.stop_channels()
        km.shutdown_kernel(now=True)
    print("ok")


if __name__ == "__main__":
    main()
