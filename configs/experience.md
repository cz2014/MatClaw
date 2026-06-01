# Experience Notes

Operational lessons learned from past runs. Auto-injected into every prompt.
Both humans and the agent (via write_experience tool) can add notes. Keep this short:
only a handful of high-value, non-obvious gotchas. Prune obsolete notes aggressively --
do NOT add notes about interpreter/sandbox restrictions (the runtime is open: full
builtins, all imports, no operation limit).

## 1. Do NOT define custom @job functions in the agent sandbox

The @job decorator transforms a function into a jobflow Job factory -- calling
it returns an OutputReference placeholder, not a computed result. The function
body never executes locally; it would only run on the remote worker, where
sandbox-defined functions don't exist. For remote computation, compose
pre-installed atomate2 Makers (e.g. RelaxMaker, StaticMaker, MDMaker,
ForceFieldMDMaker) into a Flow, submit with submit_flow(), and block on
wait_for_jobflow(). The Makers and their dependencies already exist on the
workers, so the jobs deserialize and run correctly there.

## 2. MongoDB has a 16 MB document size limit

jobflow-remote stores job inputs/outputs in MongoDB, which rejects documents
above 16 MB. Do not pass large arrays (trajectories, many structures, datasets)
inline. Instead write the data to a file locally, upload it with remote_put to a
scratch directory (e.g. `$SCRATCH/agent_tmp_dir` -- avoid `/tmp`, which is node-local
and periodically cleaned), and pass the remote path string to the job.

## 3. Only set ionic_step_data when per-step data will be consumed downstream

Setting ionic_step_data to any non-None value (even just ("energy",)) causes atomate2
to serialize the full Structure for every saved frame into additional_store_data.json.
For long MD runs with many atoms, this JSON blob can grow to hundreds of megabytes,
which jobflow-remote must download via paramiko SFTP -- a slow, unreliable transfer
that frequently fails on large files.

Leave ionic_step_data as None (default, produces empty ionic_steps) unless the per-step
data will actually be consumed by a downstream job. For post-hoc trajectory analysis,
download the .traj file via remote_get instead -- it is compact binary and transfers reliably.
