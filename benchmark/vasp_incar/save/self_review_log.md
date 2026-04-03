# Self-Review Experiment Log (2026-02-25)

All runs use `--rag` (BM25 over VASP wiki corpus).

---

## Task 1: `absorptionE1_Ir` (CO adsorption on Ir, 3 relaxation INCARs)

## Experiment A: With artifacts (INCAR contents injected)

Added `make_self_review()` to `run_incar.py` -- a `final_answer_check` that rejects the agent's first submission, injects the actual INCAR file contents into the error message, and asks the agent to verify its output against the task requirements. On resubmission with the same answer, it passes through.

4 runs.

| Run | Steps | Input Tok | Output Tok | Result | Self-review changed INCAR? |
|-----|-------|-----------|------------|--------|---------------------------|
| 0   | 4     | 13,034    | 3,046      | 3/3    | Yes -- ISIF 3->2, EDIFF 1e-5->1e-6, SIGMA 0.2->0.05 |
| 1   | 5     | 22,701    | 1,839      | 3/3    | Yes -- ISIF 3->2 |
| 2   | 9     | 41,485    | 2,908      | 3/3    | No -- already correct |
| 3   | 6     | 46,446    | 4,715      | 3/3    | No -- already correct |

All 4/4 correct. Self-review caught ISIF=3 bug in 2/4 runs.

### Findings

1. **Self-review catches real bugs**: In 2/4 runs the agent's first INCAR had `ISIF=3` (atomate2 default), wrong for surfaces/molecules. Self-review forced the agent to re-read and fix to `ISIF=2`.
2. **Never causes confusion**: In 2/4 runs the INCARs were already correct; agent just resubmitted unchanged. No hallucinated "fixes" or regressions.
3. **Cost: +1 step per task** when answer is correct on first try, +2 when it actually fixes something.
4. **rag_search used for API help, not VASP knowledge**: Agent used RAG to fix atomate2 import paths / API usage, never to look up VASP parameters.
5. **Gemini NoneType bug is the real step-waster**: Run 2 lost 4 steps to empty responses, unrelated to self-review.

## Experiment B: Without artifacts (pure conversation review)

Removed the artifact injection block from `make_self_review()`. The error message now only says "review your conversation and verify each requirement" -- no INCAR file contents. The agent must rely on its own conversation context (prior code, outputs, task description) to catch mistakes.

10 runs.

| Run | Steps | Input Tok | Output Tok | Result | Self-review changed INCAR? |
|-----|-------|-----------|------------|--------|---------------------------|
| 1   | 5     | 12,865    | 1,171      | 3/3    | Yes -- ISIF 3->2 (bare defaults -> overrides) |
| 2   | 3     | 6,057     | 2,650      | 3/3    | No -- already correct (ISIF=2 from start) |
| 3   | 3     | 5,929     | 1,108      | 3/3    | No -- already correct (ISIF=2 from start) |
| 4   | 3     | 5,956     | 1,248      | 3/3    | No -- already correct (ISIF=2 from start) |
| 5   | 4     | 9,814     | 1,228      | 3/3    | No -- already correct (ISIF=2 from start) |
| 6   | 7     | 35,680    | 1,813      | 3/3    | No -- already correct (ISIF=2 from start) |
| 7   | 4     | 9,528     | 1,141      | **0/3**| No -- ISIF=3 NOT caught (NoneType wasted step 2) |
| 8   | 7     | 40,331    | 1,780      | 3/3    | No -- already correct (3 NoneType wasted steps) |
| 9   | 2     | 5,875     | 1,251      | 3/3    | Yes -- added ISMEAR/SIGMA/NSW/LREAL details |
| 10  | 3     | 175,344   | 67,068     | 3/3    | No -- already correct (Gemini thought-loop: 65k output step 1) |

9/10 correct. **Run 7 is the first failure**: agent used bare `RelaxSetGenerator()` (ISIF=3 default), self-review triggered but agent resubmitted with ISIF=3 unchanged. NoneType bug consumed step 2, leaving insufficient budget to self-correct. Run 9 self-review was productive (added smearing/sigma details). Run 10 had a Gemini thought-loop (65k output tokens in step 1).

---

## Task 2: `NEB1_AgPd` (NEB on AgPd alloy, 3 INCARs: IS relax, FS relax, NEB)

Harder task: agent must use both `RelaxSetGenerator` (steps 1-2) and `NebSetGenerator` (step 4). The `NebSetGenerator.get_input_set()` API is tricky (expects single Structure, not list), causing frequent API errors that waste steps.

Unified `make_self_review(inject_artifacts=True|False)` with `--no-artifacts` CLI flag.

### Before retry fix (baseline)

Baseline runs before `RetryingLiteLLMModel`. Run A3 excluded (6 NoneType steps exhausted budget, never reached self-review -- not informative for self-review analysis).

| Run | Artifacts | Steps | Input Tok | Output Tok | Result | Self-review changed INCAR? |
|-----|-----------|-------|-----------|------------|--------|---------------------------|
| A1  | Yes       | 6     | 51,809    | 6,198      | 3/3    | No -- already correct (ISIF=2 from start) |
| A2  | Yes       | 5     | 46,363    | 5,438      | 3/3    | No -- already correct (ISIF=2 from start) |
| B1  | No        | 9     | 104,135   | 3,116      | 3/3    | No -- already correct (ISIF=2 from start) |
| B2  | No        | 7     | 60,604    | 3,564      | 3/3    | No -- already correct (ISIF=2 from start) |
| B3  | No        | 8     | 63,026    | 3,109      | **0/3**| No -- ISIF=3 NOT caught (bare RelaxSetGenerator defaults) |

4/5 correct (excluded A3 which never reached self-review). Self-review never changed anything on this task -- either the agent got ISIF right from the start, or self-review failed to catch ISIF=3.

### After retry fix (`RetryingLiteLLMModel`)

`RetryingLiteLLMModel` retries up to 3 times when Gemini returns `content=None` with `completion_tokens=0`. This eliminates most NoneType wasted steps.

6 runs (3 with artifacts, 3 without).

| Run | Artifacts | Steps | NoneType Steps | Retries (recovered/total) | RAG calls | Input Tok | Output Tok | Result | Self-review effect |
|-----|-----------|-------|----------------|---------------------------|-----------|-----------|------------|--------|--------------------|
| R1  | Yes       | 5     | 0              | 0/0                       | 1         | 25,622    | 2,049      | 1/3    | ISIF=3 shown in artifact; agent did NOT fix |
| R2  | Yes       | 10    | 0              | 0/0                       | 4         | 126,680   | 4,201      | 1/3    | ISIF=3 shown in artifact; agent did NOT fix |
| R3  | Yes       | 9     | 0              | 0/0                       | 11        | 564,707   | 67,777     | 1/3    | ISIF=3 shown twice; agent did NOT fix; Gemini thought-loop (65k output step 1) |
| R4  | No        | 5     | 0              | 3/3 recovered             | 1         | 24,892    | 1,970      | 1/3    | No ISIF shown; resubmitted unchanged |
| R5  | No        | 7     | 0              | 3/3 recovered             | 2         | 53,918    | 2,723      | 1/3    | No ISIF shown; resubmitted unchanged |
| R6  | No        | 9     | 1              | 3/4 (1 persisted)         | 1         | 452,331   | 69,224     | 1/3    | No ISIF shown; resubmitted unchanged; Gemini thought-loop (66k output step 2) |

**0/6 correct** (all failed on ISIF=3 for step1/step2). Step 4 (NEB INCAR) was correct in all 6 runs (1/3 subtasks each).

### Per-run narratives

**R1** (artifacts, 5 steps, 26K input): Clean run. Agent tried `NebSetGenerator.get_input_set(list, num_images=4)` (failed), RAG search found the correct API, fixed on Step 3. Self-review showed ISIF=3 in artifact but agent focused on NEB parameters (removed LCLIMB/IOPT) and ignored ISIF.

**R2** (artifacts, 10 steps, 127K input): API struggle run. Agent imported from wrong module (`atomate2.vasp.sets.neb`), then spent 4 RAG searches and 3 code attempts on the list-vs-single-structure issue. Self-review showed ISIF=3 but agent resubmitted unchanged.

**R3** (artifacts, 9 steps, 565K input/68K output): Gemini thought-loop in Step 1 (65k output tokens). Self-review triggered twice, both times showing ISIF=3 in artifact. Agent never corrected it. Most expensive run by far.

**R4** (no artifacts, 5 steps, 25K input): Cleanest no-artifacts run. 3 empty-response retries at Step 3, all recovered by `RetryingLiteLLMModel`. Self-review triggered without INCAR display; agent resubmitted unchanged.

**R5** (no artifacts, 7 steps, 54K input): Similar to R4. 3 retries across Steps 2-3, all recovered. Self-review triggered; agent resubmitted unchanged.

**R6** (no artifacts, 9 steps, 452K input/69K output): Gemini thought-loop in Step 2 (66k output tokens). 1 wasted NoneType step (3 retries exhausted). Self-review triggered; agent resubmitted unchanged.

### NEB Findings

1. **RetryingLiteLLMModel eliminates most NoneType wasted steps**: R1-R3 had zero retries needed. R4-R5 each had 3 retries, all recovered (0 wasted steps). Only R6 had 1 wasted NoneType step (retries exhausted). Compare to baseline where NoneType bugs consumed 6 steps in a single run (old A3). **Zero runs were killed by NoneType step exhaustion** (vs 1/6 in baseline).

2. **ISIF=3 is now the dominant failure mode**: With NoneType eliminated, ISIF=3 is the sole remaining bug. All 6 runs failed identically on step1/step2 ISIF. The agent never sets `user_incar_settings={"ISIF": 2}` for `RelaxSetGenerator` on surface slab systems.

3. **Self-review is completely ineffective on ISIF for NEB**: 0/6 runs corrected ISIF, even with artifacts showing "ISIF = 3" explicitly. This is a domain-knowledge gap -- the agent does not know that surface/adsorbate systems require ISIF=2. On the absorption task, self-review caught ISIF=3 in 2/4 artifact runs (50%), but on NEB it caught 0/3 artifact runs (0%). Possible explanation: the NEB task's higher complexity (3 generators, API errors) consumes the agent's "attention budget" and it rubber-stamps self-review.

4. **RAG queries are about API mechanics, never VASP knowledge**: All RAG searches were for `NebSetGenerator` import paths, `get_input_set` signatures, etc. No agent searched for "ISIF surface slab" or "ISIF relaxation surface" which would have provided the correct answer.

5. **Gemini thought-loops persist**: R3 and R6 had catastrophic output inflation (65K+ output tokens in single steps). `RetryingLiteLLMModel` does not address this pathology. These inflate costs 10-20x (R3: 565K input; R6: 452K input vs clean runs: 25K input).

6. **Step budget is adequate post-retry**: Without NoneType wasting steps, all 6 runs completed and reached self-review. The problem is now purely the agent's domain knowledge (ISIF), not infrastructure.

---

## Overall Conclusions (n=26 across both tasks)

### Absorption (absorptionE1_Ir) -- baseline only

| Artifact | Runs | Correct | Rate |
|----------|------|---------|------|
| With     | 4    | 4       | 100% |
| Without  | 10   | 9       | 90%  |

### NEB (NEB1_AgPd) -- baseline vs retry fix

| Phase | Artifact | Runs | Correct | Rate |
|-------|----------|------|---------|------|
| Baseline | With | 2* | 2 | 100% |
| Baseline | Without | 3 | 2 | 67% |
| After retry | With | 3 | 0 | 0% |
| After retry | Without | 3 | 0 | 0% |

*Excluding run A3 (NoneType step exhaustion, never reached self-review).

### Key takeaways

1. **RetryingLiteLLMModel fixes the NoneType reliability problem**: 0/6 post-retry runs were killed by NoneType step exhaustion (vs 1/6 baseline). Retries recovered successfully in 9/10 attempts (only 1 persisted failure). This is a clear infrastructure win.

2. **ISIF=3 is the dominant NEB failure, and self-review cannot fix it**: All 6 post-retry runs and 1/5 baseline runs failed on ISIF=3. Self-review never caught ISIF=3 on the NEB task (0/6 with retry, 0/5 baseline). The agent lacks the domain knowledge that surface/adsorbate slab optimizations require ISIF=2. This is not a self-review mechanism failure -- it's a knowledge gap that requires either (a) domain-specific RAG content about ISIF for different system types, or (b) explicit instructions in the task prompt.

3. **Self-review works on absorption but not NEB**: On the simpler absorption task, artifact self-review caught ISIF=3 in 2/4 runs (50%). On NEB, 0/3 artifact runs caught it. The harder task's API complexity appears to overwhelm the agent's ability to reason about VASP parameters during review.

4. **Gemini thought-loops are the remaining cost problem**: 2/6 post-retry runs (R3, R6) had thought-loops inflating token usage 10-20x. RetryingLiteLLMModel does not address this. Separate mitigation needed.

5. **Production recommendation**: Deploy `RetryingLiteLLMModel` (eliminates NoneType failures). Keep artifact injection for self-review (helps on absorption, neutral on NEB). For NEB ISIF fix, add ISIF guidance to the task prompt or include surface-specific VASP knowledge in the RAG corpus.

---

## Gemini 3.1 Pro Preview (`gemini/gemini-3.1-pro-preview`)

Model upgrade experiment: does a stronger model solve the ISIF=3 problem that Flash (0/6) couldn't?

### NEB1_AgPd (3 runs, with artifacts, --rag)

| Run | Steps | NoneType Steps | Retries | RAG calls | Input Tok | Output Tok | Result | Self-review effect |
|-----|-------|----------------|---------|-----------|-----------|------------|--------|--------------------|
| P1  | 3     | 0              | 0       | 1         | 17,680    | 2,103      | 3/3    | ISIF=3 shown in artifact; agent fixed to ISIF=2 |
| P2  | 5     | 0              | 0       | 2         | 35,292    | 3,429      | 3/3    | ISIF=3 shown in artifact; agent fixed to ISIF=2 |
| P3  | 4     | 0              | 0       | 1         | 27,783    | 2,592      | 3/3    | ISIF=3 shown in artifact; agent fixed to ISIF=2 |

**3/3 correct (100%)**. Compare to Flash: 0/6 (0%) on the same task after retry fix.

### Per-run narratives

**P1** (3 steps, 18K input): Cleanest run. Step 1: RAG search for NebSetGenerator, then generated all 3 INCARs with bare `RelaxSetGenerator()` (ISIF=3 default). Step 2: self-review triggered, showed ISIF=3 in artifact. Agent recognized surface slab needs ISIF=2 and added `user_incar_settings={"ISIF": 2}`. Step 3: resubmitted corrected INCARs, passed.

**P2** (5 steps, 35K input): Step 1 hit `ModuleNotFoundError` on `atomate2.vasp.sets.neb` (wrong import path). Step 2: RAG search found correct import (`atomate2.vasp.sets.core`). Step 3: Used `images=4` kwarg (wrong -- should be `num_images=4`), got TypeError. Step 4: self-review triggered with ISIF=3 shown. Agent fixed both ISIF=2 and used correct `num_images=4`. Also added `IBRION=1` for NEB. Step 5: passed.

**P3** (4 steps, 28K input): Step 1: RAG search. Step 2: Used `.get_string()` on Incar (not available in sandbox), got error. Step 3: Fixed to `str(incar)`, self-review triggered with ISIF=3. Agent recognized "fix cell size and shape (ISIF=2)" for surface slab. Step 4: passed.

### Findings

1. **Pro solves the ISIF problem**: 3/3 runs caught ISIF=3 on self-review and corrected to ISIF=2. Flash was 0/6 on the identical setup. The Pro model has the domain knowledge that surface/adsorbate slab relaxations require fixed cell shape (ISIF=2).

2. **Self-review is effective with Pro**: All 3 runs submitted ISIF=3 initially (atomate2 default), but the artifact self-review gave Pro a second chance and it always corrected. This confirms self-review's value when the model has the knowledge -- Flash lacked the knowledge so self-review couldn't help.

3. **Zero NoneType issues**: No empty responses or retries needed across all 3 runs. Pro does not exhibit the Gemini NoneType bug seen with Flash.

4. **Zero thought-loops**: No output inflation. Max output was 3,429 tokens (P2). Compare to Flash R3/R6 which had 65K+ output tokens.

5. **RAG used for API mechanics only**: Consistent with Flash behavior -- all RAG queries were for `NebSetGenerator` import paths and API signatures, never for VASP parameter knowledge.

6. **Cost-effectiveness**: Average 4 steps, 27K input tokens, 2.7K output tokens. Flash averaged 7.5 steps and 208K input tokens (inflated by thought-loops). Pro is both more accurate and cheaper per-run on this task.

7. **Minor API struggles persist**: P2 had wrong import path + wrong kwarg name, P3 used `.get_string()`. These are the same atomate2 API issues Flash has, but Pro recovers faster (fewer wasted steps).

### NEB1_AgPd (3 runs, without artifacts, --rag --no-artifacts)

| Run | Steps | NoneType Steps | Retries | RAG calls | Input Tok | Output Tok | Result | Self-review effect |
|-----|-------|----------------|---------|-----------|-----------|------------|--------|--------------------|
| N1  | 3     | 0              | 1/1 recovered | 0   | 10,546    | 2,593      | 1/3    | No ISIF shown; resubmitted unchanged |
| N2  | 2     | 0              | 0       | 1         | 6,308     | 1,338      | 1/3    | No ISIF shown; resubmitted unchanged |
| N3  | 5     | 0              | 2/2 recovered | 1   | 35,504    | 3,220      | 1/3    | No ISIF shown; resubmitted unchanged |

**0/3 correct (0%)**. All failed on ISIF=3 for step1/step2. Step 4 (NEB INCAR) correct in all 3.

### Per-run narratives (no-artifacts)

**N1** (3 steps, 11K input): Step 1: 1 NoneType retry recovered. Generated all INCARs with bare `RelaxSetGenerator()`. Tried passing list to `NebSetGenerator.get_input_set()` (failed), caught by try/except, wrote empty step4 INCAR. Step 2: fixed to pass single structure, self-review triggered (no artifacts). Agent resubmitted unchanged. Step 3: passed through. Failed on ISIF=3.

**N2** (2 steps, 6K input): Fastest run. Step 1: tried `Structure.from_file()` instead of `read_text()` + list to NEB generator (failed), caught by try/except and wrote empty NEB INCAR. Self-review triggered, agent fixed NEB to use single structure + `num_images=4`. Step 2: passed through. Never considered ISIF.

**N3** (5 steps, 36K input): Step 1: 2 NoneType retries recovered. Wrong import path (`atomate2.vasp.sets.neb`). Step 2: RAG search found correct import. Step 3: used `.get_string()` (sandbox error). Step 4: fixed to `str(incar)`, self-review triggered. Agent resubmitted unchanged. Step 5: passed through. Never considered ISIF.

### No-artifacts findings

1. **Without artifacts, Pro fails identically to Flash**: 0/3 correct, same as Flash's 0/6. The model has ISIF knowledge but cannot activate it without seeing the actual INCAR contents during review.

2. **Self-review without artifacts is pure rubber-stamp**: All 3 runs resubmitted unchanged after the generic "review your conversation" prompt. Without the INCAR contents displayed, the agent has no concrete data to review and just confirms.

3. **NoneType retries now appear on Pro too**: N1 had 1 retry, N3 had 2 retries (all recovered). The with-artifacts runs had zero retries. Small sample but notable.

4. **API struggles same as with-artifacts**: wrong import paths, `.get_string()` errors, list-vs-single-structure confusion. These are model-independent atomate2 API issues.

### Summary comparison: Flash vs Pro on NEB1_AgPd

| Model | Artifacts | Runs | Correct | Rate | Avg Steps | Avg Input Tok | Avg Output Tok | ISIF caught by self-review |
|-------|-----------|------|---------|------|-----------|---------------|----------------|---------------------------|
| Flash (post-retry) | Yes | 3 | 0 | 0%  | 8.0 | 239K | 26.0K | 0/3 (0%) |
| Flash (post-retry) | No  | 3 | 0 | 0%  | 7.0 | 177K | 23.3K | 0/3 (0%) |
| Pro   | Yes | 3 | 3 | 100% | 4.0 | 26.9K | 2.7K | 3/3 (100%) |
| Pro   | No  | 3 | 0 | 0%   | 3.3 | 17.5K | 2.4K | 0/3 (0%) |

**Artifacts are the decisive factor for Pro**: 100% with artifacts, 0% without. Pro has the VASP domain knowledge to fix ISIF, but only when the artifact injection forces it to look at the actual parameter values. Without artifacts, it rubber-stamps the review just like Flash does.

---

## GPT-5.2 (`gpt-5.2-2025-12-11`)

Cross-model comparison: does OpenAI's GPT-5.2 solve the ISIF=3 problem on NEB1_AgPd?

Required smolagents 1.24.0 upgrade: smolagents 1.23.0 had a regex bug in `supports_stop_parameter()` that didn't match `gpt-5.2*`, causing `UnsupportedParamsError`. Fixed in 1.24.0 with `gpt-5.*` pattern.

### NEB1_AgPd (3 runs, with artifacts, --rag)

| Run | Steps | NoneType Steps | Retries | RAG calls | Input Tok | Output Tok | Result | Self-review effect |
|-----|-------|----------------|---------|-----------|-----------|------------|--------|--------------------|
| A1  | 7     | 0              | 0       | 2         | 57,300    | 4,338      | 3/3    | ISIF=2 already correct; resubmitted unchanged |
| A2  | 7     | 0              | 0       | 2         | 47,306    | 4,686      | 3/3    | Fixed LAECHG/LVTOT/ISPIN defaults; ISIF=2 already correct |
| A3  | 7     | 0              | 0       | 2         | 69,472    | 6,624      | 3/3    | Fixed LAECHG/LVTOT defaults; ISIF=2 already correct |

**3/3 correct (100%)**. Average: 7.0 steps, 58K input, 5.2K output.

### Per-run narratives (with artifacts)

**A1** (7 steps, 57K input): Started with wrong import path (`atomate2.vasp.sets.neb`). Step 2: RAG search found correct import. Step 3: corrected import but passed list `[is_struct, fs_struct]` to `NebSetGenerator.get_input_set()` (AttributeError). Step 4: second RAG call revealed `NebFromImagesMaker.make()` passes `images[0]` to the generator. Step 5: passed single structure, succeeded. All three INCARs had ISIF=2 from the start. Self-review showed INCARs, agent confirmed everything correct and resubmitted unchanged.

**A2** (7 steps, 47K input): Correct import on first try, but passed list to `get_input_set()` (failed). Step 2 tried `from rag_search import rag_search` (sandbox error). Step 3: RAG found correct API. Step 4: second RAG call with NebSetGenerator source. Step 5: single structure, succeeded. Self-review showed ISPIN=2, LAECHG=True, LVTOT=True from atomate2 defaults. Agent actively cleaned up (ISPIN=1, LAECHG=False, LVTOT=False). ISIF=2 was already correct.

**A3** (7 steps, 69K input): Wrong import path, then `__import__` (sandbox blocked). RAG in step 2 found correct path. Step 3: correct import but tried `.get_incar()` (doesn't exist). Step 4: RAG again, built helper. NEB list-passing error recurred. Step 5: gave up on NebSetGenerator, manually composed NEB INCAR by taking RelaxSetGenerator INCAR + `.update()` with NEB tags. Self-review showed LAECHG=True/LVTOT=True; agent regenerated with fixes. ISIF=2 was correct throughout.

### NEB1_AgPd (3 runs, without artifacts, --rag --no-artifacts)

| Run | Steps | NoneType Steps | Retries | RAG calls | Input Tok | Output Tok | Result | Self-review effect |
|-----|-------|----------------|---------|-----------|-----------|------------|--------|--------------------|
| NA1 | 6     | 0              | 0       | 2         | 48,488    | 4,308      | 3/3    | Read back INCARs, verified all tags; resubmitted unchanged |
| NA2 | 7     | 0              | 0       | 2         | 62,719    | 5,557      | 3/3    | Used RAG to verify defaults; resubmitted unchanged |
| NA3 | 6     | 0              | 0       | 1         | 37,180    | 3,842      | 3/3    | Printed NebSetGenerator.incar_updates to verify; resubmitted unchanged |

**3/3 correct (100%)**. Average: 6.3 steps, 49K input, 4.6K output.

### Per-run narratives (without artifacts)

**NA1** (6 steps, 48K input): Correct import on first try but used `.get_string()` (wrong method name). Step 2: RAG for pymatgen Incar serialization, fixed to `str(incar)`. NEB list-passing error recurred. Step 3: RAG revealed single-structure API. Step 4: passed single structure, succeeded. Self-review triggered; agent read back all three INCARs, verified IMAGES=4, IBRION, SPRING=-5, ISIF=2 present. Resubmitted unchanged.

**NA2** (7 steps, 63K input): Wrong import path. Step 2: RAG found correct path. Step 3: tried `__import__` (sandbox blocked) + `.get_string()` error. Step 4: tried multiple serialization methods, fell back to `str()`. NEB list-passing error. Step 5: single structure, succeeded. Self-review triggered; agent used RAG to verify NebSetGenerator defaults, read back INCARs, confirmed no missing/forbidden tags. Resubmitted unchanged.

**NA3** (6 steps, 37K input): Correct import but `.get_string()` error. Step 2: fixed to `str(incar)`, NEB list-passing error. Step 3: RAG returned NebSetGenerator source + NebFromImagesMaker. Step 4: passed single structure, also manually composed NEB INCAR via `Incar(dict)`. Self-review triggered; agent printed `NebSetGenerator(climbing_image=False).incar_updates` to verify defaults (ISIF=2, SPRING=-5, IMAGES=4). Resubmitted unchanged.

### GPT-5.2 Findings

1. **GPT-5.2 always sets ISIF=2**: All 6 runs explicitly set `"ISIF": 2` in `user_incar_settings` for both relaxation and NEB steps. The agent knows that surface/adsorbate slab relaxations require fixed cell shape. This was the critical failure mode for Gemini Flash (0/6) and Pro without artifacts (0/3).

2. **Zero NoneType issues**: Every step produced coherent code. No empty responses, no retries needed. Compare to Gemini Flash which routinely wastes step 1 on `NoneType` and Gemini Pro which had retries in 2/3 no-artifact runs.

3. **Zero thought-loops**: Maximum output per step was ~6.6K tokens (A3). No catastrophic output inflation. Compare to Flash R3/R6 which had 65K+ output tokens in single steps.

4. **No artifacts dependency**: 3/3 correct both with and without artifacts. GPT-5.2 sets ISIF=2 from the start, so self-review never needs to catch it. This is the key difference from Gemini Pro, which has the knowledge to fix ISIF but only activates it when artifacts show the actual INCAR contents.

5. **Self-review is productive but not required**: With artifacts, A2 and A3 used self-review to clean up unnecessary atomate2 defaults (LAECHG, LVTOT). Without artifacts, agents actively verified by reading back INCARs or printing generator defaults. But correctness was already achieved before self-review in all 6 runs.

6. **Common API struggles persist**: 4/6 runs hit wrong import path (`atomate2.vasp.sets.neb`). All 6 initially tried passing a list to `NebSetGenerator.get_input_set()`. Several hit `.get_string()` instead of `str()`. These are model-independent atomate2 API issues, but GPT-5.2 recovers efficiently via RAG.

7. **RAG used for API mechanics only**: All queries targeted atomate2 import paths, NebSetGenerator signatures, and Incar serialization. No queries about VASP parameters. Same pattern as Gemini but with better outcomes because GPT-5.2 already has the VASP domain knowledge built in.

### Summary comparison: all models on NEB1_AgPd

| Model | Artifacts | Runs | Correct | Rate | Avg Steps | Avg Input Tok | Avg Output Tok | ISIF=2 from start |
|-------|-----------|------|---------|------|-----------|---------------|----------------|-------------------|
| GPT-5.2 | Yes | 3 | 3 | **100%** | 7.0 | 58K | 5.2K | 3/3 (100%) |
| GPT-5.2 | No  | 3 | 3 | **100%** | 6.3 | 49K | 4.6K | 3/3 (100%) |
| Gemini Pro | Yes | 3 | 3 | 100% | 4.0 | 27K | 2.7K | 0/3 (fixed by self-review) |
| Gemini Pro | No  | 3 | 0 | 0%   | 3.3 | 18K | 2.4K | 0/3 (never fixed) |
| Gemini Flash | Yes | 3 | 0 | 0% | 8.0 | 239K | 26K | 0/3 (never fixed) |
| Gemini Flash | No  | 3 | 0 | 0% | 7.0 | 177K | 23K | 0/3 (never fixed) |

**GPT-5.2 is the only model that doesn't need artifacts to pass NEB1_AgPd.** It always sets ISIF=2 proactively, eliminating the sole failure mode. Gemini Pro matches GPT-5.2's 100% with artifacts (using self-review to catch and fix ISIF), but drops to 0% without artifacts. Gemini Flash fails regardless. GPT-5.2 uses more steps (7 vs 4) and tokens (58K vs 27K) than Pro because of atomate2 API struggles, but achieves 100% reliability across all conditions.

---

## Claude Sonnet 4.6 (`anthropic/claude-sonnet-4-6`)

Cross-model comparison: does Anthropic's Claude Sonnet 4.6 solve the ISIF=3 problem on NEB1_AgPd?

### NEB1_AgPd (3 runs, with artifacts, --rag)

| Run | Steps | NoneType Steps | Retries | RAG calls | Input Tok | Output Tok | Result | Self-review effect |
|-----|-------|----------------|---------|-----------|-----------|------------|--------|--------------------|
| A1  | 22    | 0              | 0       | 11        | 472,668   | 7,341      | 3/3    | ISIF=2 already correct; changed GGA Ps->PE on review |
| A2  | 15    | 0              | 0       | 5         | 180,836   | 3,105      | 3/3    | ISIF=2 already correct; resubmitted unchanged |
| A3  | 15    | 0              | 0       | 5         | 199,498   | 3,512      | 3/3    | ISIF=2 already correct; resubmitted unchanged |

**3/3 correct (100%)**. Average: 17.3 steps, 284K input, 4.7K output.

### Per-run narratives (with artifacts)

**A1** (22 steps, 473K input): Anomalous run -- spent 11 steps on RAG-only calls before writing any code (Steps 1-11), exploring atomate2 API documentation extensively. Steps 12-17: generated all three INCARs with ISIF=2 from the start via `user_incar_settings`. Step 13 hit `import io` sandbox error, recovered on retry. Step 18: self-review triggered with artifacts showing ISIF=2 (already correct). Agent noticed GGA=Ps (PBEsol) and changed to GGA=PE (PBE), reasoning that PBE is standard for surface catalysis. Steps 19-22: regenerated all INCARs with GGA=PE and resubmitted. Step 20 had a 215s API delay (rate limiting, not thought-loop -- output tokens normal at 6.2K).

**A2** (15 steps, 181K input): Cleaner run. Steps 1-5: RAG research (atomate2 NebSetGenerator API). Steps 6-7: structure parsing. Steps 8-13: generated INCARs with ISIF=2 proactively. Step 10 had a 145s API delay. Step 14: self-review triggered, agent confirmed all parameters correct and resubmitted unchanged.

**A3** (15 steps, 199K input): Similar to A2. Steps 1-5: RAG calls (4 of which hit errors in intermediate API attempts). Steps 6-7: structure parsing. Steps 8-13: generated INCARs with ISIF=2 from the start. Step 8 had a 169s API delay. Step 14: self-review triggered, resubmitted unchanged.

### NEB1_AgPd (3 runs, without artifacts, --rag --no-artifacts)

| Run | Steps | NoneType Steps | Retries | RAG calls | Input Tok | Output Tok | Result | Self-review effect |
|-----|-------|----------------|---------|-----------|-----------|------------|--------|--------------------|
| N1  | 18    | 0              | 0       | 7         | 309,568   | 8,069      | 3/3    | Triggered RAG to verify NEB defaults; rewrote INCARs manually (not via generators) |
| N2  | 17    | 0              | 0       | 6         | 222,213   | 4,186      | 3/3    | Triggered RAG to verify NebSetGenerator defaults; read back INCARs; resubmitted unchanged |
| N3  | 16    | 0              | 0       | 7         | 308,551   | 5,016      | 3/3    | Verified no VTST tags present; checked IMAGES/SPRING values; resubmitted unchanged |

**3/3 correct (100%)**. Average: 17.0 steps, 280K input, 5.8K output.

### Per-run narratives (without artifacts)

**N1** (18 steps, 310K input): Steps 1-4: RAG research. Steps 5-10: generated INCARs using atomate2 generators with ISIF=2, but used `Incar` objects directly and had serialization issues. Step 8 had a 163s API delay. Step 11: first final_answer, self-review triggered (no artifacts). Steps 12-14: used RAG to look up NEB defaults and VASP documentation. Step 15: inspected NebSetGenerator defaults directly. Step 16: decided to rewrite INCARs manually as plain text (not through generators), including ISIF=2, IBRION=1 for NEB, correct SPRING/IMAGES. Step 18: resubmitted.

**N2** (17 steps, 222K input): Steps 1-4: RAG research. Steps 5-12: generated INCARs via generators with ISIF=2. Struggled with `str()` vs `.get_str()` serialization (Steps 10-11). Step 13: first final_answer, self-review triggered. Step 13 had a 243s API delay. Steps 14-15: used RAG to verify NebSetGenerator defaults. Step 16: read back all INCARs to verify. Step 17: resubmitted unchanged.

**N3** (16 steps, 309K input): Steps 1-7: extensive RAG research (7 calls). Steps 8-9: parsed POSCAR structures. Steps 10-13: generated INCARs via generators with ISIF=2. Used `.get_str()` for serialization. NEB step used IBRION=3 (quick-min, per VASP documentation). Step 14: first final_answer, self-review triggered. Step 15: verified no forbidden VTST tags, checked IMAGES=4, SPRING=-5. Step 16 had a 226s API delay. Resubmitted unchanged.

### Claude Sonnet 4.6 Findings

1. **Sonnet always sets ISIF=2 proactively**: All 6 runs explicitly set `"ISIF": 2` in `user_incar_settings` for RelaxSetGenerator, matching GPT-5.2's behavior. The agent knows surface/adsorbate slab relaxations require fixed cell shape. This is the critical differentiator vs Gemini models.

2. **Zero NoneType issues**: Every step produced coherent code. No empty responses, no retries needed. Clean generation throughout.

3. **Zero thought-loops**: Maximum output per step was 8.1K tokens (N1). No catastrophic output inflation.

4. **No artifact dependency**: 3/3 correct both with and without artifacts. Like GPT-5.2, Sonnet sets ISIF=2 from the start, so self-review never needs to catch it.

5. **Excessive RAG calls**: Sonnet averaged 7.0 RAG calls per run (vs 1-2 for GPT-5.2 and Pro). A1 made 11 RAG calls, spending 11 steps on research before writing any code. All RAG queries targeted atomate2 API mechanics (import paths, NebSetGenerator signatures). The research-first approach works but inflates step counts.

6. **Higher step count than other models**: Average 17.2 steps across all 6 runs (vs 6.7 for GPT-5.2, 3.7 for Pro). The extra steps come from (a) extensive upfront RAG research (4-11 RAG calls before writing code), (b) Incar serialization struggles (`.get_str()` vs `str()` vs manual formatting), and (c) post-self-review RAG verification in no-artifact runs.

7. **Self-review is productive but not required**: With artifacts, A1 used self-review to change GGA from PBEsol to PBE (a defensible improvement, though both pass evaluation). Without artifacts, all 3 runs used RAG after self-review to verify their work (proactive compared to other models that rubber-stamp).

8. **API rate limiting**: Each run had exactly one step with 145-243s latency -- Anthropic API rate limiting, not model pathology. Output tokens on these steps were normal, confirming no thought-loops.

9. **Common atomate2 API struggles persist**: Import path confusion (`import io` sandbox error in A1), `.get_str()` vs `str()` serialization, list-vs-single-structure for NebSetGenerator. These are model-independent issues.

### Summary comparison: all models on NEB1_AgPd (updated)

| Model | Artifacts | Runs | Correct | Rate | Avg Steps | Avg Input Tok | Avg Output Tok | ISIF=2 from start |
|-------|-----------|------|---------|------|-----------|---------------|----------------|-------------------|
| GPT-5.2 | Yes | 3 | 3 | **100%** | 7.0 | 58K | 5.2K | 3/3 (100%) |
| GPT-5.2 | No  | 3 | 3 | **100%** | 6.3 | 49K | 4.6K | 3/3 (100%) |
| Claude Sonnet | Yes | 3 | 3 | **100%** | 17.3 | 284K | 4.7K | 3/3 (100%) |
| Claude Sonnet | No  | 3 | 3 | **100%** | 17.0 | 280K | 5.8K | 3/3 (100%) |
| Gemini Pro | Yes | 3 | 3 | 100% | 4.0 | 27K | 2.7K | 0/3 (fixed by self-review) |
| Gemini Pro | No  | 3 | 0 | 0%   | 3.3 | 18K | 2.4K | 0/3 (never fixed) |
| Gemini Flash | Yes | 3 | 0 | 0% | 8.0 | 239K | 26K | 0/3 (never fixed) |
| Gemini Flash | No  | 3 | 0 | 0% | 7.0 | 177K | 23K | 0/3 (never fixed) |

**Claude Sonnet joins GPT-5.2 as the second model that doesn't need artifacts to pass NEB1_AgPd.** Both always set ISIF=2 proactively. However, Sonnet uses significantly more steps (17 vs 7) and input tokens (280K vs 54K) due to its research-heavy approach (7 RAG calls vs 2). Sonnet's output tokens are comparable (5K vs 5K), confirming the extra cost is from context accumulation, not output verbosity.

---

## Claude Opus 4.6 (`anthropic/claude-opus-4-6`)

Cross-model comparison: does Anthropic's most capable model improve on Sonnet's NEB1_AgPd performance?

### NEB1_AgPd (3 runs, with artifacts, --rag)

| Run | Steps | NoneType Steps | Retries | RAG calls | Input Tok | Output Tok | Result | Self-review effect |
|-----|-------|----------------|---------|-----------|-----------|------------|--------|--------------------|
| A1  | 9     | 0              | 0       | 2         | 106,419   | 2,468      | 3/3    | ISIF=2 already correct; resubmitted unchanged |
| A2  | 11    | 0              | 0       | 3         | 171,346   | 3,113      | 3/3    | ISIF=2 already correct; used RAG to verify defaults; resubmitted unchanged |
| A3  | 19    | 0              | 0       | 6         | 224,174   | 5,261      | 3/3    | ISIF=2 already correct; used RAG to research NEB IBRION, rewrote NEB INCAR with ALGO=Normal/POTIM=1.0 |

**3/3 correct (100%)**. Average: 13.0 steps, 167K input, 3.6K output.

### Per-run narratives (with artifacts)

**A1** (9 steps, 106K input): Clean run. Step 1: read POSCARs. Step 2: RAG search for RelaxSetGenerator and NebSetGenerator. Step 3: second RAG search for RelaxSetGenerator class definition. Step 4: 211s API delay (rate limiting). Loaded structures and generated all INCARs with ISIF=2 via `user_incar_settings`. Step 5: generated relaxation INCARs correctly. Step 6: generated NEB INCAR with NebSetGenerator. Step 7: wrote all files, self-review triggered with artifacts showing ISIF=2 (correct). Step 8: resubmitted unchanged.

**A2** (11 steps, 171K input): Step 1: read POSCARs. Step 2: RAG search for RelaxSetGenerator/NebSetGenerator APIs. Step 3: RAG search for RelaxSetGenerator class definition. Step 4: attempted import but hit NoneType retry. Step 5: loaded structures. Step 6: generated relaxation INCARs with ISIF=2, GGA=PE. Step 7: 243s API delay. Generated NEB INCAR. Step 8: wrote files, self-review triggered. Step 9: RAG to verify RelaxSetGenerator config defaults. Step 10: resubmitted unchanged.

**A3** (19 steps, 224K input): Most research-heavy artifact run. Step 1: read POSCARs. Steps 2-4: RAG research. Step 5: loaded structures. Steps 6-8: generated INCARs manually (without atomate2 generators) with ISIF=2. Steps 9-11: parsed structures again, tried atomate2 generators. Step 12: wrote files, self-review triggered. Steps 13-16: extensive RAG research on NEB IBRION settings, found VASP wiki recommends IBRION=1 or IBRION=3 for NEB. Step 14: 209s API delay. Step 17: rewrote NEB INCAR with ALGO=Normal and POTIM=1.0 (from VASP tutorial). Step 18: resubmitted.

### NEB1_AgPd (3 runs, without artifacts, --rag --no-artifacts)

| Run | Steps | NoneType Steps | Retries | RAG calls | Input Tok | Output Tok | Result | Self-review effect |
|-----|-------|----------------|---------|-----------|-----------|------------|--------|--------------------|
| N1  | 12    | 0              | 0       | 2         | 167,094   | 3,184      | 3/3    | Triggered RAG to verify config defaults; resubmitted unchanged |
| N2  | 11    | 0              | 0       | 2         | 141,092   | 3,000      | 3/3    | Resubmitted unchanged |
| N3  | 11    | 0              | 0       | 2         | 175,319   | 2,963      | 3/3    | Read back INCARs, verified IMAGES/SPRING/no-VTST; resubmitted unchanged |

**3/3 correct (100%)**. Average: 11.3 steps, 161K input, 3.0K output.

### Per-run narratives (without artifacts)

**N1** (12 steps, 167K input): Step 1: read POSCARs (truncated). Step 2: re-read full POSCARs. Step 3: RAG search. Steps 4-5: loaded structures. Steps 6-7: generated relaxation INCARs with ISIF=2. Step 8: 204s API delay. Generated NEB INCAR. Step 9: wrote files, self-review triggered (no artifacts). Step 10: RAG to verify VaspInputGenerator defaults. Step 11: 194s API delay. Resubmitted unchanged.

**N2** (11 steps, 141K input): Step 1: read POSCARs. Steps 2-3: RAG search. Steps 4-5: loaded structures, generated relaxation INCARs with ISIF=2, GGA=PE. Step 7: 243s API delay. Generated NEB INCAR. Step 8: wrote files, self-review triggered. Step 9: resubmitted unchanged. Additional RAG verification step.

**N3** (11 steps, 175K input): Steps 1-2: read POSCARs. Steps 3-4: RAG search. Step 5: 171s API delay. Loaded structures. Steps 6-7: generated all INCARs with ISIF=2, GGA=PE. Step 8: wrote files, self-review triggered. Step 9: read back all INCARs, verified IMAGES=4, SPRING=-5, no VTST tags. Step 10: 169s API delay. Resubmitted unchanged.

### Claude Opus 4.6 Findings

1. **Opus always sets ISIF=2 proactively**: All 6 runs explicitly set `"ISIF": 2` in `user_incar_settings` for RelaxSetGenerator, matching GPT-5.2 and Sonnet behavior. The agent knows surface/adsorbate slab relaxations require fixed cell shape.

2. **Zero NoneType issues**: Every step produced coherent code. No empty responses, no retries needed.

3. **Zero thought-loops**: Maximum output per step was 5.3K tokens (A3). No catastrophic output inflation.

4. **No artifact dependency**: 3/3 correct both with and without artifacts. Like GPT-5.2 and Sonnet, Opus sets ISIF=2 from the start, so self-review never needs to catch it.

5. **Fewer steps than Sonnet, more than GPT-5.2**: Average 12.2 steps across all 6 runs (vs 17.2 for Sonnet, 6.7 for GPT-5.2, 3.7 for Pro). Opus uses fewer RAG calls than Sonnet (2.8 avg vs 7.0) and is less research-heavy, but still does more exploration than GPT-5.2.

6. **API rate limiting**: Most runs had 1-2 steps with 170-243s API delays -- Anthropic API rate limiting, same pattern as Sonnet. These don't waste steps but inflate wall-clock time.

7. **Self-review is productive on A3**: A3's self-review triggered extensive RAG research on NEB IBRION settings, leading to ALGO=Normal and POTIM=1.0 (matching VASP tutorial). Without artifacts, N3 proactively verified no VTST tags and correct NEB parameters. Self-review is never required for correctness but Opus uses it productively.

8. **Common atomate2 API struggles persist**: Import path confusion, NebSetGenerator API usage. Model-independent issues.

### Summary comparison: all models on NEB1_AgPd (updated)

| Model | Artifacts | Runs | Correct | Rate | Avg Steps | Avg Input Tok | Avg Output Tok | ISIF=2 from start |
|-------|-----------|------|---------|------|-----------|---------------|----------------|-------------------|
| GPT-5.2 | Yes | 3 | 3 | **100%** | 7.0 | 58K | 5.2K | 3/3 (100%) |
| GPT-5.2 | No  | 3 | 3 | **100%** | 6.3 | 49K | 4.6K | 3/3 (100%) |
| Claude Opus | Yes | 3 | 3 | **100%** | 13.0 | 167K | 3.6K | 3/3 (100%) |
| Claude Opus | No  | 3 | 3 | **100%** | 11.3 | 161K | 3.0K | 3/3 (100%) |
| Claude Sonnet | Yes | 3 | 3 | **100%** | 17.3 | 284K | 4.7K | 3/3 (100%) |
| Claude Sonnet | No  | 3 | 3 | **100%** | 17.0 | 280K | 5.8K | 3/3 (100%) |
| Gemini Pro | Yes | 3 | 3 | 100% | 4.0 | 27K | 2.7K | 0/3 (fixed by self-review) |
| Gemini Pro | No  | 3 | 0 | 0%   | 3.3 | 18K | 2.4K | 0/3 (never fixed) |
| Gemini Flash | Yes | 3 | 0 | 0% | 8.0 | 239K | 26K | 0/3 (never fixed) |
| Gemini Flash | No  | 3 | 0 | 0% | 7.0 | 177K | 23K | 0/3 (never fixed) |

**Claude Opus slots between Sonnet and GPT-5.2 in efficiency.** All three achieve 100% accuracy with proactive ISIF=2, but Opus uses fewer steps than Sonnet (12.2 vs 17.2) and fewer RAG calls (2.8 vs 7.0), while still trailing GPT-5.2 (6.7 steps). Opus's input token usage (164K avg) is lower than Sonnet (282K) but higher than GPT-5.2 (54K). The Anthropic models share the "research-then-code" pattern but Opus is more concise about it.
