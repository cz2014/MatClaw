# LADDER

Categories: INCAR tag, Many-body perturbation theory, Bethe-Salpeter equations

LADDER = [logical]  
 Default: **LADDER** = .NOT. LRPA

Description: Controls whether the ladder diagrams are included in the BSE calculation. Note that the default for LRPA and therefore LADDER is somewhat convoluted; so better to always double-check the OUTCAR file whether VASP behaves as expected. Generally, VASP will select ladder diagrams whenever this seems reasonable. This is for instance the case for ALGO="BSE" or "TDHF" calculations.

---

LADDER is used together with LHARTREE. If LADDER=*.FALSE.*, the ladder diagrams (i.e. the exchange terms related to $W$ or the screened exchange) are not included.
If LHARTREE=*.FALSE.*, the Hartree diagrams or bubble diagrams are not included. The following table summarizes all possible combinations:

:   :   |  |  |  |
        | --- | --- | --- |
        | LHARTREE | LADDER |  |
        | .TRUE. | .TRUE. | full BSE / TDHF |
        | .FALSE. | .TRUE. | only excitonic effects (ladders) |
        | .TRUE. | .FALSE. | random phase approximation (rings = bubbles only) |
        | .FALSE. | .FALSE. | independent particle picture |

The last combination can be useful for sanity checks: the results must be identical to the results obtained using
LOPTICS=*.TRUE.* in the preceding calculations. If this is not the case, it usually implies that the one-electron
energies have been updated in the WAVECAR file, or that the WAVEDER file is not properly set up. The end of BSE explains how to recalculate
the WAVEDER file from an existing WAVECAR file.

## Related tags and articles

LHARTREE,
LOPTICS,
BSE\_calculations

Examples that use this tag

---
