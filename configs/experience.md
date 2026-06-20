# Experience Notes

Operational lessons learned from past runs. Auto-injected into every prompt.
Both humans and the agent (via write_experience tool) can add notes. Keep this short:
only a handful of high-value, non-obvious gotchas. Prune obsolete notes aggressively --
do NOT add notes about interpreter/sandbox restrictions (the runtime is open: full
builtins, all imports, no operation limit).

## 1. Do NOT define custom @job functions; use the pre-installed remote paths

The @job decorator turns a function into a jobflow Job factory -- calling it returns an
OutputReference placeholder, and the body would only run on the remote worker, where a
sandbox-defined function does not exist. So never DEFINE a @job here. For remote compute,
use one of the two pre-installed paths (their code already lives on the workers):

- atomate2 Makers (RelaxMaker, StaticMaker, MDMaker, ForceFieldMDMaker, ...) composed into a
  Flow -- for VASP and force-field workflows.
- remote_jobs.jobs.run_command -- a GENERIC raw-deck runner for any external code (ABACUS,
  LAMMPS, ...). Import it, never redefine it; you write the input files yourself:

    from remote_jobs.jobs import run_command
    job = run_command(
        input_files={"INPUT": "...", "STRU": "...", "KPT": "..."},  # raw deck, as strings
        command="srun abacus",                                       # launcher is part of the command
        env={"OMP_NUM_THREADS": "1"},                                # merged into the subprocess env
        setup="export PATH=/opt/abacus/bin:$PATH",                   # export, NOT `module load` (stripped)
        output_globs=["OUT.*/**"],                                   # files/dirs to report back
    )
    submit_flow(Flow([job]), worker=WORKER, project=PROJECT)
    out = wait_for_jobflow(PROJECT, job.uuid)

  run_command RETURNS, never raises, on a nonzero exit or timeout -- inspect out["returncode"],
  out["timed_out"], out["stdout_tail"], fix the deck, resubmit (you are the recovery loop;
  there is no custodian). Results are raw: out["run_dir"] + out["produced_files"] say what to
  remote_get and parse yourself (no typed schema). Keep decks small (note 2); pre-stage bulky
  data (pseudopotentials, potentials) on the cluster and reference by absolute path. Chain a
  follow-on step by passing a prior out["run_dir"] as a path argument.

Boundary: run_command/Makers are only for heavy engines that MUST run on HPC. Light Python
post-processing (parsing, analytic solvers, structure analysis) runs locally in this executor.

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
