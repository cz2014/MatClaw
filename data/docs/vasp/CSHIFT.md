# CSHIFT

Categories: INCAR tag, Linear response, Dielectric properties, Many-body perturbation theory, GW

CSHIFT = [real]

|  |  |  |
| --- | --- | --- |
| Default: **CSHIFT** | = 0.1 | for LOPTICS |
|  | = OMEGAMAX\*1.3 / max(NOMEGA,40) | for GW calculations |
|  | = 0.1 | for BSE calculations/Casida TDDFT calculations |
|  | = 0.1 | for Time Evolution TDDFT calculations |

Description: CSHIFT sets a Lorentzian broadening in eV of the dielectric tensor via the complex shift η in the Kramers-Kronig transformation of the response function.

---

The default CSHIFT=0.1 is perfectly acceptable for most calculations and causes a slight smoothing of the real part of the dielectric function. If the gap is very small (i.e. approaching two times CSHIFT), slight inaccuracies in the static dielectric constant are possible, which can be remedied by decreasing CSHIFT. If CSHIFT is further decreased, it is strongly recommended to increase the frequency grid by setting NEDOS to values around 2000.

> **Mind:** For the quartic-scaling GW algorithm, one should manually check that CSHIFT is at least as large as the grid spacing at low frequencies. If CSHIFT is smaller than the grid spacing, the QP energies might show erratic behavior (for instance large re-normalization factors Z).

## Related tags and articles

OMEGAMIN,
OMEGAMAX,
LOPTICS,
Examples that use this tag

---
