# Experience Notes

Operational lessons learned from past runs. Auto-injected into every prompt.
Both humans and the agent (via write_experience tool) can add notes.

## 1. Do NOT define custom @job functions in the agent sandbox

The @job decorator transforms a function into a jobflow Job factory -- calling
it returns an OutputReference placeholder, not a computed result. The function
body never executes locally; it would only run on the remote worker, where
sandbox-defined functions don't exist. Instead, use the provided tools
(train_deepmd, batch_static_eval, wait_for_jobflow) which are pre-registered
as remote jobs. For data merging, pass a list of sources to train_deepmd's
data_source parameter.

## 2. MongoDB has a 16 MB document size limit

train_deepmd pre-check rejects inline dicts above ~10 MB (~800 frames of
90-atom structures). To bypass: write data locally, use remote_put to upload,
and pass the remote path string instead of inline data. Both train_deepmd and
batch_static_eval accept remote path strings.

Default upload directory: /pscratch/sd/c/cz2014/agent_tmp_dir
(avoid /tmp -- node-local and periodically cleaned).

## 3. Use a separate MD trajectory for held-out evaluation

When constructing a held-out test set from MD trajectories, generate a SEPARATE
MD trajectory for evaluation. Do NOT split frames from the training trajectories
(e.g., every Nth frame). Adjacent frames in an MD trajectory are highly
correlated and do not constitute an independent test.


## 4. Avoid explicit repr() calls in sandbox code

The restricted interpreter may reject explicit repr(...) as a forbidden function call, especially inside exception handlers. Prefer f-strings like f'{exc}' or just print the object directly instead of calling repr explicitly.


## 5. Avoid accessing dunder attributes directly in sandbox inspection

The restricted interpreter may block direct access to dunder attributes like __init__. When inspecting classes, prefer inspect.signature(ClassName) for the constructor signature, inspect.signature(ClassName.make) for regular methods, and inspect.getsource(ClassName) instead of referencing ClassName.__init__.


## 6. Avoid globals() for sandbox state checks

The restricted sandbox may reject explicit globals() calls as forbidden evaluation. To test whether a cross-step variable exists, use a try/except NameError pattern instead, and reconstruct needed state from files if the variable is missing.


## 7. Avoid probing undefined sandbox variables; persist workflow state to files instead

In this sandbox, referencing an undefined variable can fail before a Python try/except NameError handler runs. For multi-step workflows, do not probe for state with bare variable references. Instead, recompute cheap local inputs and persist important workflow state (job UUIDs, specs, summaries) to workspace files using write_text so later steps can reconstruct state deterministically.


## 8. Avoid exhaustive all-frame pair-distance scans in one sandbox step

Computing O(N_atoms^2) minimum-distance checks across every frame of multiple trajectories can hit the sandbox operation limit even when each frame is modest. For phase inspection, sample a few representative frames (first/middle/last) and persist trajectory paths. Perform rigorous full-frame distance filtering later only on the exploration set you actually need to screen for selection.


## 9. Avoid string state filters in query_jobstore count_jobs/get_jobs_info

Passing states as plain strings such as {"states": ["COMPLETED"]} to query_jobstore can fail inside jobflow-remote because the underlying methods expect JobState/FlowState enum objects. In the agent sandbox, prefer queries without states, use name patterns, or use custom_query if a state-based Mongo filter is truly needed.


## 10. Avoid Python @ matrix-multiplication syntax in sandbox trajectory analysis

The restricted sandbox can raise NotImplementedError for the MatMult AST node even when NumPy arrays support @ normally. In analysis code, replace expressions like positions @ c_hat with np.sum(positions * c_hat.reshape((1, 3)), axis=1) or np.dot(...) to stay compatible.


## 11. Avoid recursive full-dict traversal on large atomate2 TaskDocs in sandbox

A completed MD TaskDoc can be large enough that a generic recursive search over the whole nested object hits the sandbox operation limit. When a needed field is already known to exist at the top level (for example out['dir_name'] in ForceFieldMDMaker/EFieldMDMaker outputs), access it directly instead of walking the entire document.


## 12. Only set ionic_step_data when per-step data will be consumed downstream

Setting ionic_step_data to any non-None value (even just ("energy",)) causes atomate2
to serialize the full Structure for every saved frame into additional_store_data.json.
For long MD runs with many atoms, this JSON blob can grow to hundreds of megabytes,
which jobflow-remote must download via paramiko SFTP -- a slow, unreliable transfer
that frequently fails on large files.

Leave ionic_step_data as None (default, produces empty ionic_steps) unless the per-step
data will actually be consumed by a downstream job (e.g., train_deepmd). For post-hoc
trajectory analysis, download the .traj file via remote_get instead -- it is compact
binary and transfers reliably.


## 13. Create workspace directories with write_text before saving matplotlib figures

In this sandbox, matplotlib savefig() will fail with FileNotFoundError if parent directories do not exist. Because open()/os.makedirs() are not available, create output directories first by calling write_text() on a placeholder file such as 'path/.keep'; write_text creates parent directories automatically.


## 14. CIPS DP-GEN methodology from He et al. PRB 2023

Key parameters from He et al. for CuInP2S6 DP model training:
- 4 independent DP models trained (ensemble of 4)
- Concurrent learning: train -> explore (NPT MD) -> select -> label -> retrain
- Exploration: NPT MD at various temperatures (50K-1400K) and pressures (1-50000 bar)
- Selection criterion: max deviation of 4 model forces σ = max|Fi - <Fi>|
  - σ < 0.05 eV/A: well described, skip
  - 0.05 < σ < 0.15 eV/A: label with DFT and add to training set
  - σ > 0.15 eV/A: too distorted, skip
- Convergence: all explored configs have σ < 0.05
- 23 iterations produced 11,260 training configurations
- Network size: (240, 240, 240) fitting networks
- Starting structures: 1x1x1 and 1x2x2 supercells of FE, AFE1, AFE2, AFE3
- Also included mono-, bi-, triple-, quadruple-layer configs
- Born effective charges (out-of-plane): Z*_Cu=0.6, Z*_In=1.8, Z*_P2S6=-2.4
- Time step: 0.001 ps = 1 fs for MD
- Final model accuracy: MAE energy 1.10 meV/atom, MAE force 0.70 eV/A
- Curie temperature: ~315K experimental, ~340K predicted
