# LMP2LT

Categories: INCAR tag, Many-body perturbation theory, MP2

LMP2LT = .FALSE. | .TRUE.

|  |  |  |
| --- | --- | --- |
| Default: **LMP2LT** | = .FALSE. |  |

Description: LMP2LT selects a Laplace transformed MP2 algorithm.

---

If LMP2LT=.TRUE. and ALGO=ACFTDRK is set, a quartic scaling Laplace transformed MP2 algorithm is selected.

This tag should be used in combination with KPAR to tweak parallelization as described in this tutorial.

## Related tags and articles

NOMEGA,
ALGO,
LSMP2LT,
KPAR

Examples that use this tag

---
