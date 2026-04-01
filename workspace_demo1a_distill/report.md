# Test 7: CIPS Distillation — Opus 4.6 Evaluation Report

## Experiment Setup

**Objective**: Evaluate Claude Opus 4.6's ability to autonomously execute a MLFF
knowledge distillation workflow (teacher -> student) with active learning, without
the detailed DP-GEN recipe (experience note #6 removed).

**Key change from prior runs**: The original experience note #6 provided a ~33-line
detailed recipe for DP-GEN-style concurrent learning (4 students, inter-model variance
selection bands, unphysical frame filtering, multi-T/P exploration). This was removed
to test whether Opus can design the workflow from scratch using only the task
description and general experience notes (sandbox pitfalls, MongoDB limits, etc.).

**Task**: Train student DeePMD models for CuInP2S6 (CIPS) by distilling from a
published teacher model. Stop when either (a) 5 active learning iterations complete
or (b) MAE_f < 0.10 eV/A on held-out test set.

**LLM**: Claude Opus 4.6 (with extended thinking)
**HPC**: Perlmutter debug queue (GPU)


## Run Summary

| Metric | Value |
|--------|-------|
| Total steps | 21 |
| Errors | 2 (both self-recovered) |
| Duration | 43.8 min (2626s) |
| Tokens | 501,629 in / 15,190 out / 516,819 total |
| RAG calls | 3 |
| Final MAE_f | 0.082 eV/A |
| Stopping condition | (b) MAE_f < 0.10 on iteration 0 |
| Active learning iterations | 0 (threshold met immediately) |


## Workflow Executed

```
Step  1:    Load CuInP2S6 (10 atoms/cell), evaluate supercell sizes
Steps 2-4:  RAG search for ForceFieldMDMaker API, inspect signature
Step  5:    [ERROR] Wrong MLFF enum "DeePMD" -> recovered via search
Steps 6-7:  Discover correct enum value
Step  8:    Submit 5 teacher MD jobs (4 train + 1 test)
Steps 9-10: Wait for all teacher MD jobs (1208s total)
Step  11:   [ERROR] MongoDB 16 MB limit (102 MB BSON) -> recovered
Steps 12-17: Convert to deepmd/npy, upload to remote, submit 2 student training jobs
Step  18:   Wait for training (581s)
Step  19:   Submit batch_static_eval for both students on test set
Step  20:   Compute MAE_f, detect stopping condition met
Step  21:   Final report and answer
```


## Teacher MD Parameters

| Parameter | Training MDs | Test MD |
|-----------|-------------|---------|
| Temperatures | 200K, 300K, 400K, 500K | 350K |
| Steps | 500 | 300 |
| Timestep | 2 fs | 2 fs |
| Simulation time | **1.0 ps each** | **0.6 ps** |
| Ensemble | NVT | NVT |
| Frames saved | 501 each (every step) | 301 |
| Supercell | 3x3x1 (90 atoms) | 3x3x1 (90 atoms) |
| Total training frames | 2004 | — |


## Student Training Results

| Metric | Student 1 (seed=42) | Student 2 (seed=137) |
|--------|---------------------|----------------------|
| Training MAE_e (eV/atom) | 0.00133 | 0.00095 |
| Training RMSE_e (eV/atom) | 0.00182 | 0.00132 |
| Training MAE_f (eV/A) | 0.0861 | 0.0859 |
| Training RMSE_f (eV/A) | 0.1127 | 0.1134 |
| **Test MAE_f (eV/A)** | **0.08265** | **0.08239** |
| Test RMSE_f (eV/A) | 0.10682 | 0.10734 |
| Net preset | fast | fast |
| Training steps | 2000 | 2000 |


## Error Recovery

**Error 1 (step 5)**: Used `force_field_name="DeePMD"` but the correct atomate2
enum value differs. Agent searched the codebase, found the correct value, and
resubmitted. Standard API discovery — not specific to this task.

**Error 2 (step 11)**: Passed 4 teacher MD output dicts (~102 MB) inline to
`train_deepmd`, exceeding MongoDB's 16 MB BSON limit. Agent recovered by:
1. Extracting data from ionic_steps into numpy arrays
2. Saving as deepmd/npy format locally
3. Uploading to Perlmutter via `remote_put`
4. Passing remote path strings to `train_deepmd`

This recovery matches experience note #2 (MongoDB 16 MB limit) — the note told
the agent *what* to do, and Opus figured out *how* autonomously.


## Comparison with Original DP-GEN Recipe (Removed Note #6)

| Aspect | Original Note #6 | Opus Autonomous |
|--------|-------------------|-----------------|
| Number of students | 4 | 2 |
| Ensemble diversity | Different random seeds | Different random seeds (42, 137) |
| Ensemble metric | Inter-model force variance (sigma) | Direct MAE_f vs teacher |
| Selection band | 0.05 < sigma < 0.15 eV/A | N/A (not reached) |
| Unphysical filter | Min distance < 1.5 A | N/A (not reached) |
| Exploration MD | Many short probes, NPT, wide T/P | N/A (not reached) |
| Temperature range | 50-1400K | 200-500K (training) |
| Pressure exploration | 1-50,000 bar, NPT | None (NVT only) |
| Separate test set | Yes | Yes (350K, separate trajectory) |
| State persistence | Write UUIDs to files | Write UUIDs to files |


## Critical Assessment

### What Opus did well

1. **Correct workflow structure**: Teacher MD -> data conversion -> student training
   -> held-out evaluation -> stopping condition check. Textbook distillation pipeline.
2. **Separate test trajectory**: Used a distinct temperature (350K) not in the
   training set. Follows experience note #3 correctly.
3. **Multi-student ensemble**: Trained 2 models with different seeds for diversity,
   even without the recipe telling it to.
4. **State persistence**: Saved all UUIDs and remote paths to JSON files.
5. **Autonomous error recovery**: Both the enum name and MongoDB limit were handled
   without human intervention.
6. **Efficient execution**: 21 steps with only 3 RAG calls and 517K tokens.

### Concerns about sampling adequacy

The teacher MD simulations are **very short** (1 ps per trajectory):

- **1 ps covers ~10-100 lattice vibration cycles** — sufficient for harmonic
  sampling near equilibrium, but inadequate for:
  - Cu ion hopping (characteristic timescale ~10-1000 ps in CIPS)
  - Structural phase transitions
  - Anharmonic distortions far from equilibrium
- **NVT only** — no pressure exploration means the model has never seen volume
  changes, making it unreliable for NPT simulations.
- **Narrow temperature range (200-500K)** — CIPS has a Curie temperature of ~330K.
  The training data does not cover low-temperature ferroelectric or high-temperature
  paraelectric regimes adequately. The original recipe suggested 50-1400K.
- **No diversity from structural perturbations** — all MDs start from the same
  relaxed supercell. Different starting configurations (e.g., rattled atoms,
  strained cells) would improve coverage.

### Why MAE_f still looks good

The test set (350K, 0.6 ps) is drawn from the **same distribution** as the training
data — short NVT trajectories near equilibrium at similar temperatures. The student
models are essentially learning to interpolate the teacher's potential energy surface
in a small region of configuration space. This is not a rigorous test of
generalization:

- A proper test would include configurations the model hasn't seen: different
  temperatures, pressures, defects, or long-timescale rare events.
- The near-identical MAE_f between training (0.086) and test (0.082) suggests the
  test set is not significantly out-of-distribution.
- Both students have nearly identical performance (0.08265 vs 0.08239 eV/A),
  which is consistent with a well-sampled, easy-to-learn distribution.

### Active learning was never tested

Because the stopping condition was met on iteration 0, the core active learning
loop — the main challenge of this task — was never exercised:

- No exploration MD with student models
- No inter-model variance computation
- No frame selection based on uncertainty
- No teacher re-labeling of uncertain frames
- No iterative retraining

The test effectively became a **single-shot distillation** rather than an active
learning benchmark. To truly test Opus's ability to design the AL loop, the stopping
threshold should be tighter (e.g., MAE_f < 0.05 eV/A) or the initial data should be
deliberately sparse.


## Recommendations for Future Runs

1. **Lower the MAE_f threshold** to 0.05 eV/A to force active learning iterations.
2. **Reduce initial training data** (e.g., 1 temperature, 200 frames) to make
   iteration 0 insufficient.
3. **Use a harder test set**: longer MD at extreme temperatures (50K, 800K),
   NPT at various pressures, or structures with Cu defects.
4. **Evaluate long-timescale stability**: run a 100 ps student MD and check if it
   stays physically reasonable (no atom overlap, energy conservation).
5. **Compare with the recipe-guided run**: run test7 again WITH note #6 and compare
   the quality of the final model, not just MAE_f on an easy test set.


## Verdict

Opus 4.6 successfully completed a single-shot distillation pipeline in 21 steps
with full autonomous error recovery. The workflow structure is correct and the code
quality is high. However, the experiment design (short MDs, narrow T range, easy
test set) means the stopping condition was trivially met, and the active learning
capability — the core challenge — was never tested. The result demonstrates Opus's
competence at composing computational workflows, but does not validate its ability
to design a robust active learning strategy.
