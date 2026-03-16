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


## 6. Active learning for MLFF distillation (DP-GEN-style concurrent learning)

Lessons from previous failed active learning and literature:

Active learning iteration workflow:
1. Train 4 student models with DIFFERENT random seeds on the current
   training set (call train_deepmd N times with different seed= values).
2. Run exploration MD with ONE student model at diverse T/P conditions.
3. Evaluate ALL student models on the exploration frames (batch_static_eval
   with each model). Compute per-frame inter-model force variance:
   sigma = max_i sqrt(mean((F_i - F_mean)^2)) across models.
4. Filter out unphysical frames: reject frames with min interatomic
   distance < 1.5 A (student MD can generate atoms overlapping in early
   iterations -- this is expected, just filter them out).
5. Apply SELECTION BAND on sigma:
   - sigma < 0.05 eV/A: already well-described, skip
   - 0.05 < sigma < 0.15 eV/A: SELECT for labeling
   - sigma > 0.15 eV/A: likely unphysical/unconverged, skip
6. Label selected frames with the TEACHER model (batch_static_eval with
   teacher). The teacher replaces DFT as the labeling oracle.
7. Add teacher-labeled frames to the training set and retrain all students.

Key points:
- Start with ~500-2000 initial frames from diverse teacher MD, add
  ~200-700 per iteration.
- Exploration MDs should be SHORT: 1,000-16,000 steps at 1 fs timestep
  (1-16 ps per run). Save frames every 10-150 steps. Diversity comes from
  running MANY short probes at different T/P conditions, not from long
  trajectories. Use NPT ensemble for pressure exploration.
- Explore across many temperatures (50-1400K) and pressures (1-50,000 bar).
  Each iteration: 5-8 temperatures x 7-8 pressures x multiple starting
  structures. Early iterations use shorter runs (~1000 steps), later
  iterations can be longer (~10,000-16,000 steps).


## 7. Avoid globals() for sandbox state checks

The restricted sandbox may reject explicit globals() calls as forbidden evaluation. To test whether a cross-step variable exists, use a try/except NameError pattern instead, and reconstruct needed state from files if the variable is missing.


## 8. Avoid probing undefined sandbox variables; persist workflow state to files instead

In this sandbox, referencing an undefined variable can fail before a Python try/except NameError handler runs. For multi-step workflows, do not probe for state with bare variable references. Instead, recompute cheap local inputs and persist important workflow state (job UUIDs, specs, summaries) to workspace files using write_text so later steps can reconstruct state deterministically.


## 9. Avoid exhaustive all-frame pair-distance scans in one sandbox step

Computing O(N_atoms^2) minimum-distance checks across every frame of multiple trajectories can hit the sandbox operation limit even when each frame is modest. For phase inspection, sample a few representative frames (first/middle/last) and persist trajectory paths. Perform rigorous full-frame distance filtering later only on the exploration set you actually need to screen for selection.
