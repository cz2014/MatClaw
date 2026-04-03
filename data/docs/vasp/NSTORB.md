# NSTORB

Categories: INCAR tag, Many-body perturbation theory, MP2

NSTORB = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NSTORB** | = -1 |  |

Description: NSTORB specifies the number of stochastic orbitals per cycle in the stochastic MP2 algorithm.

---

NSTORB defines the number of stochastic orbitals per cycle, i.e., the number of stochastic orbitals that define one stochastic sample. If the sample is not large enough, the calculations are repeated until the accuracy, defined by ESTOP, is reached.

As a rule of thumb, we recommend setting

$\texttt{NSTORB} = \sqrt{\texttt{NBANDS}} \;.$

See here for a small tutorial on stochastic Laplace transformed MP2 calculations.

## Related tags and articles

NOMEGA,
ESTOP,
LSMP2LT,
LMP2LT,
NBANDS,
KPAR,
ALGO

---
