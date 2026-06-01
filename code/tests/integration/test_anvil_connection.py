"""Smoke test: submit a trivial job to Anvil and verify results come back."""
from jobflow import Flow
from jobflow_remote import submit_flow
from remote_jobs.jobs import hello_anvil
from core.tools import wait_for_jobflow

PROJECT = "anvil"
WORKER = "anvil_cpu"

if __name__ == "__main__":
    j = hello_anvil()
    flow = Flow([j], name="anvil_smoke_test")
    submit_flow(flow, worker=WORKER, project=PROJECT)
    print(f"Submitted job: {j.uuid}")

    out = wait_for_jobflow(PROJECT, j.uuid, timeout_s=600)
    print(f"Result: {out}")
