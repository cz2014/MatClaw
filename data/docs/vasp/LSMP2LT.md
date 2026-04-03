# LSMP2LT

Categories: INCAR tag, Many-body perturbation theory, MP2

LSMP2LT = .FALSE. | .TRUE.

|  |  |  |
| --- | --- | --- |
| Default: **LSMP2LT** | = .FALSE. |  |

Description: LSMP2LT selects a stochastic Laplace transformed MP2 algorithm.

---

If LSMP2LT=.TRUE. and ALGO=ACFTDRK is set, a quartic scaling stochastic Laplace transformed MP2 algorithm is selected.

This tag should be used in combination with KPAR to tweak parallelization as described in this tutorial.

## Related tags and articles

NOMEGA,
ESTOP,
NSTORB,
KPAR,
ALGO

Examples that use this tag

---
