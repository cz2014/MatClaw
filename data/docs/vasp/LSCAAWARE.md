# LSCAAWARE

Categories: INCAR tag, Performance, Parallelization

LSCAAWARE = [logical]

|  |  |  |
| --- | --- | --- |
| Default: **LSCAAWARE** | = .TRUE. | if VASP is compiled with scaLAPACK support (precompiler flag -DscaLAPACK) |
|  | = .FALSE. | otherwise |

Description: LSCAAWARE controls the distribution of the Hamilton matrix.

---

For LSCAAWARE=.TRUE., VASP distributes the Hamilton matrix among the MPI ranks.
For LSCAAWARE=.FALSE., each MPI ranks allocates the complete Hamiltonain. In both cases LSCALAPACK decides if ScaLAPACK routines are used for diagonalization.

## Related tags and articles

NPAR,
NCORE,
LPLANE,
NSIM,
KPAR,
LSCALU,
LSCALAPACK

Examples that use this tag

---
