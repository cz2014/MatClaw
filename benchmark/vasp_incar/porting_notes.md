# Porting Notes: VaspAgent_with_Benchmark -> vasp_incar

Tips for creating evaluation constraints and task descriptions when porting tasks
from the sibling project `VaspAgent_with_Benchmark` (arxiv 2512.19458).

## config_constraints (properties.json)

1. **Do not require tags that have acceptable VASP defaults.**
   VASP silently applies sensible defaults for many tags. If the default falls
   within the acceptable range, omitting the tag is valid behavior -- not an error.
   The evaluator's `_VASP_DEFAULTS` dict in `evaluate.py` handles this automatically:
   when a tag is missing from the INCAR, `config_check` looks up the VASP default
   and passes the constraint if the default satisfies it. You can still add
   constraints for these tags -- the check only applies when the tag is absent.

   Current defaults in `_VASP_DEFAULTS`:
   ISPIN=1, ISIF=2, ISMEAR=1, SIGMA=0.2, POTIM=0.5, SPRING=-5.0

2. **ISPIN: relax `exact 1` to `in_set [1, 2]`, keep `exact 2` strict.**
   If the reference uses ISPIN=1 (non-magnetic system), both 1 and 2 produce
   correct physics -- ISPIN=2 just costs ~2x more because VASP computes both
   spin channels even though they converge to the same density. Accept both.
   If the reference uses ISPIN=2 (magnetic system: Fe, Co, Ni, open-shell
   molecules like O2), then ISPIN=2 is required -- using ISPIN=1 would give
   wrong physics. Keep `exact: 2`.

3. **Use `in_set` over `exact` when multiple algorithms are acceptable.**
   The upstream data files often record the single choice the reference author made
   (e.g., IBRION=2). But conjugate gradient (2) and RMM-DIIS (1) are both valid
   for relaxation. Broaden to `in_set` unless there is a physics reason for one
   specific value. See point 9 for NEB-specific IBRION guidance.

4. **ENCUT: use `gt` (minimum threshold), not `range` with an upper bound.**
   ENCUT only needs to exceed a minimum (typically ~350 eV for standard calculations).
   Higher values are always physically correct -- they just cost more compute. atomate2's
   `RelaxSetGenerator` inherits `ENCUT=680` from its `MPScanRelaxSet` base config, which
   is valid but would fail a range check with a low upper bound. Use `"match": "gt",
   "min": 349` instead of `"match": "range", "min": 350, "max": 550`.

5. **VASP boolean normalization.**
   VASP accepts `.TRUE.`, `.true.`, `T`, and `True` interchangeably. The evaluator
   coerces these via `_VASP_BOOLS` in `evaluate.py`. Store expected booleans as
   `.TRUE.`/`.FALSE.` strings in properties.json to keep them readable, but be aware
   the comparison is done after coercion.

## question.txt

6. **Do not embed absolute paths or host-specific placeholders.**
   The runner copies POSCAR files into the agent's workspace. Reference them by
   filename only (e.g., `POSCAR-CO`), not by `{data_dir}/POSCAR-CO`. The agent
   reads them via `read_text("POSCAR-CO")`.

7. **Instruct the agent to write files, not return strings.**
   The return format section must show `write_text("step1/INCAR", content)` and
   `final_answer({"step1_incar": path})`. The evaluator reads INCAR content from
   file paths, not from raw strings. The `reject_non_file` check enforces this at
   runtime.

8. **Keep domain expertise out of Tier 1/2 prompts.**
   VASP-specific knowledge belongs in question.txt (Tier 3) and optionally RAG,
   not in `config/prompts.yaml` or `config/llm_config.yaml`. The same generic
   materials-science template works across all benchmarks.

9. **NEB IBRION: accept 1, 2, and 3 (`in_set [1, 2, 3]`).**
   The VASP wiki [Nudged elastic bands](https://www.vasp.at/wiki/index.php/Nudged_elastic_bands)
   page explicitly recommends both IBRION=1 (RMM-DIIS) and IBRION=3 (quick-min)
   for NEB, and warns that IBRION=2 (CG) can cause convergence issues. However,
   IBRION=2 is still used in official VASP examples
   ([ammonia flipping](https://www.vasp.at/wiki/index.php/TS_search_using_the_NEB_Method))
   and produces correct physics. The official tutorials use IBRION=1
   ([Pt adatom](https://www.vasp.at/wiki/index.php/Collective_jumps_of_a_Pt_adatom_on_fcc-Pt_(001):_Nudged_Elastic_Band_Calculation),
   [Part 1](https://www.vasp.at/tutorials/latest/transition_states/part1/)).
   All three are valid NEB optimizers -- do not use `exact` for any single value.

10. **Strip VTST-only tags from constraints.**
   VaspAgent tasks assume VTST-patched VASP. Tags like `LCLIMB`, `ICHAIN`, `IOPT`,
   `IBRION=3/POTIM=0` (VTST optimizer combo) are not standard VASP. Do not include
   them in `config_constraints`. Standard VASP NEB only needs `IMAGES` and `SPRING`.
   Note: atomate2's `NebSetGenerator(climbing_image=True)` also injects VTST tags --
   use `climbing_image=False` for standard VASP.
