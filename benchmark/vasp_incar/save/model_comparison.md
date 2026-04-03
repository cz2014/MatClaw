# Model Comparison: VASP INCAR Benchmark

Comparison of five models across four model families on the VASP INCAR benchmark (2026-02-26). Evidence: 44+ runs across absorptionE1_Ir and NEB1_AgPd tasks.

---

## Master Results Table

### NEB1_AgPd (hard task: 2 relax + 1 NEB INCAR, 2 generators, tricky API)

| Model | Artifacts | Runs | Correct | Rate | Avg Steps | Avg Input Tok | Avg Output Tok | ISIF=2 from start |
|-------|-----------|------|---------|------|-----------|---------------|----------------|-------------------|
| **GPT-5.2** | Yes | 3 | 3 | **100%** | 7.0 | 58K | 5.2K | 3/3 (100%) |
| **GPT-5.2** | No  | 3 | 3 | **100%** | 6.3 | 49K | 4.6K | 3/3 (100%) |
| **Claude Opus** | Yes | 3 | 3 | **100%** | 13.0 | 167K | 3.6K | 3/3 (100%) |
| **Claude Opus** | No  | 3 | 3 | **100%** | 11.3 | 161K | 3.0K | 3/3 (100%) |
| **Claude Sonnet** | Yes | 3 | 3 | **100%** | 17.3 | 284K | 4.7K | 3/3 (100%) |
| **Claude Sonnet** | No  | 3 | 3 | **100%** | 17.0 | 280K | 5.8K | 3/3 (100%) |
| Gemini Pro | Yes | 3 | 3 | 100% | 4.0 | 27K | 2.7K | 0/3 (fixed by self-review) |
| Gemini Pro | No  | 3 | 0 | 0%   | 3.3 | 18K | 2.4K | 0/3 (never fixed) |
| Gemini Flash | Yes | 3 | 0 | 0% | 8.0 | 239K | 26K | 0/3 (never fixed) |
| Gemini Flash | No  | 3 | 0 | 0% | 7.0 | 177K | 23K | 0/3 (never fixed) |

### absorptionE1_Ir (simple task: 3 relaxation INCARs, 1 generator)

| Model | Artifacts | Runs | Correct | Rate |
|-------|-----------|------|---------|------|
| Gemini Flash | Yes | 4 | 4 | 100% |
| Gemini Flash | No  | 10 | 9 | 90% |

(GPT-5.2 and Pro not tested on absorption -- Flash already saturates it.)

---

## Model Profiles

### GPT-5.2 (`gpt-5.2-2025-12-11`)

**Reliability characteristics:**

| Property | Observation |
|----------|-------------|
| NoneType empty responses | **Zero** across 6 runs. Every step produces coherent code. |
| Thought-loops / repetition | **Zero**. Max output per step: ~6.6K tokens. |
| Multi-code-block responses | Not observed. Clean single-block output. |
| Code block contamination | Not observed. |
| VASP domain knowledge (ISIF) | **Strong**. Always sets ISIF=2 proactively for surface slabs. |
| Self-review effectiveness | Productive but not required for correctness. Used to clean up cosmetic defaults (LAECHG, LVTOT). |
| Artifact dependency | **None**. 100% correct with or without artifacts. |

**Strengths:**
- Best VASP domain knowledge of the three models. Knows surface/adsorbate systems need ISIF=2 and sets it explicitly in `user_incar_settings` every time, even though `RelaxSetGenerator` defaults to ISIF=3.
- Zero generation pathologies. No NoneType, no thought-loops, no code contamination. Every step is productive code.
- Effective RAG consumer. Extracts the right information from RAG results on first read (correct import path, single-structure API pattern).
- Self-correcting on API errors. Recovers from wrong import paths and wrong `get_input_set()` arguments within 1-2 steps.

**Weaknesses:**
- More steps than Pro (7.0 vs 4.0 with artifacts). Hits the same atomate2 API pitfalls (wrong import path in 4/6 runs, list-vs-single-structure in 6/6 runs) and needs RAG to recover.
- Higher token usage than Pro (58K vs 27K with artifacts) due to extra recovery steps.
- Required smolagents 1.24.0 upgrade: the 1.23.0 regex in `supports_stop_parameter()` didn't match `gpt-5.2*`, causing `UnsupportedParamsError`.

**RAG usage pattern:** 1-2 calls per run, all targeting `software=["atomate2"]`. Queries are for API mechanics (import paths, method signatures), never for VASP parameters. RAG is always helpful and never causes confusion.

**Self-review pattern:** Triggered in all 6 runs. With artifacts: A2 and A3 cleaned up unnecessary atomate2 defaults (LAECHG=True->False, LVTOT=True->False). Without artifacts: agents actively verified by reading back INCARs or printing generator defaults. No confusion, no regressions. Self-review adds +1 step but ISIF was already correct before review.

---

### Claude Sonnet 4.6 (`anthropic/claude-sonnet-4-6`)

**Reliability characteristics:**

| Property | Observation |
|----------|-------------|
| NoneType empty responses | **Zero** across 6 runs. Every step produces coherent code. |
| Thought-loops / repetition | **Zero**. Max output per step: ~8.1K tokens. |
| Multi-code-block responses | Not observed. Clean single-block output. |
| Code block contamination | Not observed. |
| VASP domain knowledge (ISIF) | **Strong**. Always sets ISIF=2 proactively for surface slabs. |
| Self-review effectiveness | Productive but not required for correctness. A1 improved GGA; no-artifact runs triggered RAG verification. |
| Artifact dependency | **None**. 100% correct with or without artifacts. |

**Strengths:**
- Strong VASP domain knowledge. Knows surface/adsorbate systems need ISIF=2 and sets it explicitly every time, matching GPT-5.2's proactive behavior.
- Zero generation pathologies. No NoneType, no thought-loops, no code contamination.
- Thorough RAG consumer. Uses RAG extensively (avg 7 calls/run) to research API before writing code. This "research-first" approach is slower but ensures correctness.
- Proactive self-review behavior. Without artifacts, Sonnet uses RAG after self-review to verify its work (unique among all models tested).

**Weaknesses:**
- **Excessive steps**: 17.2 average (vs 6.7 GPT-5.2, 3.7 Pro). The research-heavy approach (4-11 RAG calls before writing code) inflates step count significantly.
- **High input token usage**: 282K average (vs 54K GPT-5.2, 27K Pro). Context accumulation from many RAG results.
- **API rate limiting**: Each run hit one 145-243s API delay, adding ~3 minutes per run. Not a model pathology but an operational concern.
- **Incar serialization struggles**: Multiple runs fought with `.get_str()` vs `str()` vs manual formatting. Same issue other models face, but Sonnet takes more attempts to resolve.

**RAG usage pattern:** 5-11 calls per run -- significantly more than other models (1-2 for GPT-5.2 and Pro). All queries target atomate2 API mechanics. Sonnet's approach is "research thoroughly, then code," whereas GPT-5.2 and Pro tend to "code first, RAG when stuck."

**Introspection pattern:** ~1 inspect call across 6 official runs (N1: inspected NebSetGenerator defaults). In early experiments, Sonnet tried `inspect.getsource()` and `inspect.signature()` when inspect was not yet authorized -- both blocked by sandbox. Once authorized, Sonnet rarely used it, preferring rag_search.

**Self-review pattern:** With artifacts: A1 changed GGA Ps->PE (PBEsol to PBE), a defensible domain improvement. A2/A3 resubmitted unchanged. Without artifacts: all 3 runs proactively used RAG to verify NEB defaults after self-review, then resubmitted (unchanged in N2/N3, rewritten manually in N1).

---

### Claude Opus 4.6 (`anthropic/claude-opus-4-6`)

**Reliability characteristics:**

| Property | Observation |
|----------|-------------|
| NoneType empty responses | **Zero** across 6 runs. Every step produces coherent code. |
| Thought-loops / repetition | **Zero**. Max output per step: ~5.3K tokens. |
| Multi-code-block responses | Not observed. Clean single-block output. |
| Code block contamination | Not observed. |
| VASP domain knowledge (ISIF) | **Strong**. Always sets ISIF=2 proactively for surface slabs. |
| Self-review effectiveness | Productive but not required for correctness. A3 used RAG to improve NEB IBRION/ALGO. |
| Artifact dependency | **None**. 100% correct with or without artifacts. |

**Strengths:**
- Strong VASP domain knowledge. Knows surface/adsorbate systems need ISIF=2 and sets it explicitly every time, matching GPT-5.2 and Sonnet.
- Zero generation pathologies. No NoneType, no thought-loops, no code contamination.
- More efficient than Sonnet: fewer steps (12.2 vs 17.2 avg) and fewer RAG calls (2.8 vs 7.0 avg). Less "research-heavy" while maintaining the same research-then-code pattern.
- Self-review used productively: A3 researched NEB IBRION settings via RAG during self-review, improving the NEB INCAR with ALGO=Normal and POTIM=1.0.

**Weaknesses:**
- **More steps than GPT-5.2**: 12.2 average vs 6.7 for GPT-5.2. Still has the Anthropic "research-then-code" pattern, just less extreme than Sonnet.
- **Higher input token usage than GPT-5.2**: 164K average vs 54K. Context accumulation from RAG results.
- **API rate limiting**: 1-2 steps per run with 170-243s delays, same as Sonnet. Adds ~3-5 minutes wall-clock time per run.
- **Same atomate2 API struggles**: Import path confusion, NebSetGenerator usage.

**RAG usage pattern:** 2-6 calls per run (avg 2.8) -- between GPT-5.2 (1-2) and Sonnet (5-11). All queries target atomate2 API mechanics and VASP wiki documentation. Opus is more targeted than Sonnet in its RAG usage.

**Introspection pattern:** 1 inspect call across 6 runs (A3: `inspect.signature(NebSetGenerator)`). Hit sandbox limitation on `__dataclass_fields__` access. Opus relies on rag_search for API discovery.

**Self-review pattern:** With artifacts: A1/A2 resubmitted unchanged, A3 extensively researched NEB IBRION settings and improved INCAR. Without artifacts: N1 used RAG to verify defaults, N3 read back INCARs to verify, N2 resubmitted unchanged. More proactive than GPT-5.2 but less than Sonnet in post-review verification.

---

### Gemini 3.1 Pro Preview (`gemini/gemini-3.1-pro-preview`)

**Reliability characteristics:**

| Property | Observation |
|----------|-------------|
| NoneType empty responses | Rare. 0/3 in artifact runs, 3 retries across 3 no-artifact runs (all recovered). |
| Thought-loops / repetition | **Zero** across 6 runs. |
| Multi-code-block responses | Not observed in Pro runs. |
| Code block contamination | Not observed. |
| VASP domain knowledge (ISIF) | **Has the knowledge but doesn't apply it proactively.** Needs artifact injection to trigger correction. |
| Self-review effectiveness | Decisive with artifacts (3/3 caught ISIF=3). Pure rubber-stamp without. |
| Artifact dependency | **Critical**. 100% with artifacts, 0% without. |

**Strengths:**
- Fewest steps of all models (4.0 with artifacts, 3.3 without). Most token-efficient (27K input with artifacts).
- Eliminates all Flash-specific pathologies (zero thought-loops, zero NoneType in artifact runs).
- Has VASP domain knowledge: when artifact self-review shows ISIF=3, Pro recognizes surface slabs need ISIF=2 and fixes it (3/3 times).

**Weaknesses:**
- Artifact-dependent: without artifacts showing the actual INCAR contents, Pro rubber-stamps self-review identically to Flash. The knowledge exists but is not activated without the visual prompt.
- Same atomate2 API struggles as other models (wrong import paths, `.get_string()` errors).
- Occasional NoneType retries in no-artifact runs (2/3 runs needed retries).

**RAG usage pattern:** 1-2 calls per run, atomate2 only. Same pattern as GPT-5.2. Helpful for API mechanics.

**Self-review pattern:** The key differentiator. With artifacts: sees ISIF=3 in the displayed INCAR, recognizes the surface slab context, and overwrites to ISIF=2. Without artifacts: resubmits unchanged every time.

---

### Gemini 3 Flash Preview (`gemini/gemini-3-flash-preview`)

**Reliability characteristics:**

| Property | Observation |
|----------|-------------|
| NoneType empty responses | **Critical**. 76% of steps affected in NEB runs. Dominant reliability threat. |
| Thought-loops / repetition | **High**. ~10-15% of runs. 65K+ output tokens in single steps. |
| Multi-code-block responses | Very common. 3-block pattern typical, 9-18 blocks occasionally. |
| Code block contamination | Occasional. Mixes markdown into `<code>` blocks. |
| VASP domain knowledge (ISIF) | **Weak on hard tasks.** Caught ISIF=3 on absorption (2/4 with artifacts) but never on NEB (0/6). |
| Self-review effectiveness | Rubber-stamp on NEB. Partially effective on absorption. |
| Artifact dependency | Irrelevant for NEB (fails regardless). Helpful for absorption. |

**Strengths:**
- Adequate for simple tasks: 100% with artifacts on absorptionE1_Ir.
- Cheapest per-token cost of the three models.

**Weaknesses:**
- **NoneType empty response bug**: Gemini returns `content=None` with `finish_reason='stop'`. Wastes 3-9 steps per run. Disproven hypothesis: not caused by smolagents stop sequences (tested with `stop=[]`, no improvement). Partially mitigated by `RetryingLiteLLMModel` (retries up to 3 times).
- **Catastrophic repetition loops**: 2,538 identical `<code>` blocks in a single response (843K chars, 65K output tokens). Occurs ~10-15% of runs. No mitigation.
- **Complexity cliff**: Performance drops nonlinearly from 100% (absorption) to 0% (NEB). Three failure modes compound multiplicatively: API confusion wastes steps, thought-loops escalate (7% -> 33%), context pollution drowns the ISIF signal during self-review.
- **Step 1 thought-loop**: ~60% of runs waste 3-5 minutes on step 1 producing an empty stub after 30K+ output tokens of internal reasoning.
- **ISIF blind spot on hard tasks**: even with artifacts explicitly showing `ISIF = 3`, Flash never catches it on NEB (0/6). The harder task's API complexity consumes all "attention budget."

**Aggregate impact of Flash pathologies:**

| Issue | Steps Wasted (per run) | Token Overhead | Fatal? |
|-------|----------------------|----------------|--------|
| NoneType empty response | 3-9 steps | ~10k input/step | Yes (exhausts budget) |
| Repetition loops | 1 step | 60-65k output | Rarely (1 step, but huge cost) |
| Multi-code-block | 0 (handled) | ~2x output | No |
| Code block contamination | 1 step | Minimal | No |
| Self-review blind spot | 0 (misses bugs) | 0 | No (bug was already there) |
| Step 1 thought-loop | 1 step | 30k+ output | No |

**RAG usage pattern:** Same as other models -- atomate2 API mechanics only. RAG is helpful but cannot compensate for generation pathologies.

---

## Cross-Model Analysis

### The ISIF=3 Problem

The critical test for each model: does it know that surface/adsorbate slab relaxations require ISIF=2 (fix cell shape) rather than the atomate2 `RelaxSetGenerator` default of ISIF=3 (full cell relaxation)?

| Model | Sets ISIF=2 proactively | Catches ISIF=3 on self-review (artifacts) | Catches ISIF=3 on self-review (no artifacts) |
|-------|------------------------|------------------------------------------|----------------------------------------------|
| GPT-5.2 | **Yes** (6/6) | N/A (already correct) | N/A (already correct) |
| Claude Opus | **Yes** (6/6) | N/A (already correct) | N/A (already correct) |
| Claude Sonnet | **Yes** (6/6) | N/A (already correct) | N/A (already correct) |
| Gemini Pro | No (0/6) | **Yes** (3/3) | No (0/3) |
| Gemini Flash | No (0/12) | Partial on absorption (2/4), none on NEB (0/3) | Rare (1/10 absorption, 0/3 NEB) |

Three distinct strategies emerge:
1. **GPT-5.2, Claude Opus & Claude Sonnet: Proactive domain knowledge.** Know the right answer and apply it from the start. Self-review is redundant for correctness.
2. **Gemini Pro: Reactive domain knowledge.** Doesn't apply ISIF=2 proactively, but has the knowledge to fix it when forced to look at the actual INCAR values via artifact injection.
3. **Gemini Flash: Missing domain knowledge (on hard tasks).** May have partial knowledge (works on absorption) but loses it under cognitive load from API errors and thought-loops.

### Complexity Cliff Effect

| Task | Complexity | GPT-5.2 | Claude Opus | Claude Sonnet | Gemini Pro + artifacts | Gemini Flash + artifacts |
|------|------------|---------|-------------|---------------|----------------------|--------------------------|
| absorptionE1_Ir | Simple (1 generator) | (not tested) | (not tested) | (not tested) | (not tested) | 4/4 (100%) |
| NEB1_AgPd | Hard (2 generators, tricky API) | **6/6 (100%)** | **6/6 (100%)** | **6/6 (100%)** | **3/3 (100%)** | 0/6 (0%) |

Flash hits a cliff between simple and hard tasks. GPT-5.2, Claude Opus, Claude Sonnet, and Pro all handle NEB complexity, but through different mechanisms (proactive knowledge for GPT-5.2/Opus/Sonnet vs artifact-assisted review for Pro).

### Generation Pathologies

| Pathology | GPT-5.2 | Claude Opus | Claude Sonnet | Gemini Pro | Gemini Flash |
|-----------|---------|-------------|---------------|------------|--------------|
| NoneType empty responses | None | None | None | Rare (no-artifact only) | Critical (76% of NEB steps) |
| Thought-loops / repetition | None | None | None | None | ~10-15% of runs (65K+ tokens) |
| Multi-code-block | None | None | None | None | Very common |
| Code block contamination | None | None | None | None | Occasional |
| Step 1 empty stub | None | None | None | None | ~60% of runs |
| API rate limit delays | None | 1-2 per run (170-243s) | 1 per run (145-243s) | None | None |

GPT-5.2, Claude Opus, Claude Sonnet, and Pro are all clean generators. Both Anthropic models have API rate limit delays but no generation pathologies. Flash has multiple generation pathologies that compound on harder tasks.

### Cost Efficiency (NEB1_AgPd, with artifacts)

| Model | Avg Steps | Avg Input Tok | Avg Output Tok | Cost rank (tokens) |
|-------|-----------|---------------|----------------|-----------|
| Gemini Pro | 4.0 | 27K | 2.7K | Cheapest per-run |
| GPT-5.2 | 7.0 | 58K | 5.2K | 2x Pro |
| Claude Opus | 13.0 | 167K | 3.6K | 6x Pro (RAG-moderate) |
| Claude Sonnet | 17.3 | 284K | 4.7K | 10x Pro (RAG-heavy) |
| Gemini Flash | 8.0 | 239K | 26K | 9x Pro (inflated by thought-loops) |

Pro is most token-efficient. GPT-5.2 uses 2x Pro's tokens due to extra API recovery steps but achieves the same 100% accuracy. Claude Opus sits between GPT-5.2 and Sonnet -- fewer RAG calls than Sonnet (2.8 vs 7.0 avg) but still more than GPT-5.2 (1.7). Claude Sonnet's high input tokens come from its research-heavy approach (avg 7 RAG calls), not pathology. Flash is expensive due to thought-loops inflating both input and output.

### Introspection Strategy: rag_search vs inspect

Both Anthropic models have access to `rag_search` (BM25 over atomate2/VASP wiki) and Python's `inspect` module. Their usage patterns:

| Model | rag_search (6 runs) | inspect (6 runs) | Preferred strategy |
|-------|--------------------|--------------------|-------------------|
| Claude Opus | 22 (avg 3.7/run) | 1 (A3: inspect.signature) | rag_search |
| Claude Sonnet | 41 (avg 6.8/run) | ~1 (N1 only) | rag_search |
| GPT-5.2 | 10 (avg 1.7/run) | 0 | rag_search |

**Observation 1: Both Anthropic models strongly prefer rag_search.** Opus: 22 rag vs 1 inspect. Sonnet: 41 rag vs ~1 inspect. In early Sonnet experiments where `inspect` was not in `additional_authorized_imports`, Sonnet tried `inspect.getsource()` and `inspect.signature()` but both were blocked.

**Observation 2: inspect has sandbox limitations.** `inspect.signature()` works but returns limited info. `inspect.getsource()` fails (smolagents sandbox uses AST interpretation, not source files). `__dataclass_fields__` access is blocked ("Forbidden access"). These make rag_search the more reliable API discovery tool.

**Observation 3: RAG research cost is a trade-off.** Opus A3 spent 6 extra steps (~120K tokens) researching NEB IBRION settings via RAG during self-review, improving the INCAR (ALGO=Normal, POTIM=1.0). Sonnet A1 spent 11 steps on RAG research before writing code. The token cost of thorough research must be weighed against the cost of incorrect DFT calculations.

### Recommendations

1. **For reliability**: GPT-5.2, Claude Opus, and Claude Sonnet are the safest choices. All three achieve 100% correct regardless of artifact injection, zero generation pathologies. GPT-5.2 is most token-efficient (54K avg input), followed by Opus (164K) and Sonnet (282K).
2. **For cost**: Gemini Pro + artifacts is the cheapest correct configuration. But it requires artifact injection infrastructure and fails completely without it.
3. **For Anthropic users**: Opus is strictly better than Sonnet on this task -- same 100% accuracy with ~30% fewer steps and ~42% fewer input tokens. The "research-first" pattern is less extreme in Opus.
4. **For simple tasks**: Gemini Flash is adequate and cheapest-per-token. But it cannot handle NEB-level complexity.
5. **Avoid**: Gemini Flash on multi-generator tasks. Gemini Pro without artifacts.

### Open Questions

- Where is Pro's complexity cliff? NEB1_AgPd is within range. Harder workflows (phonon + relaxation + NEB chains) may reveal it.
- Can RAG-based VASP parameter validation close Flash's knowledge gap? Currently no model queries RAG for VASP parameters -- all queries are for atomate2 API mechanics.
- Does the Gemini NoneType bug correlate with context length or specific prompt patterns? Root cause remains unknown.
- Why do Anthropic models use more RAG calls than GPT-5.2? All three (GPT-5.2, Opus, Sonnet) have the same VASP domain knowledge, but Anthropic models' "research-first" strategy delays code generation. Opus (2.8 avg) is more efficient than Sonnet (7.0 avg) but still exceeds GPT-5.2 (1.7 avg). Could a prompt nudge to "code first, search when stuck" reduce step counts?
- Does Anthropic prompt caching work effectively with smolagents? The steps.jsonl doesn't record per-step cache_read tokens, so we can't verify from run data. The 170-243s API delays suggest rate limiting may negate caching latency benefits.
