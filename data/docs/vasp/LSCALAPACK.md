# LSCALAPACK

Categories: INCAR tag, Performance, Parallelization

LSCALAPACK = [logical]

|  |  |  |
| --- | --- | --- |
| Default: **LSCALAPACK** | = .TRUE. | if VASP is compiled with scaLAPACK support (precompiler flag -DscaLAPACK) |
|  | = .FALSE. | otherwise |

Description: LSCALAPACK controls the use of scaLAPACK.

---

For LSCALAPACK=.TRUE., VASP uses scaLAPACK routines for the orthonormalization of the wave functions and subspace diagonalizations.

The use of scaLAPACK for the LU decomposition in the orthonormalization of the wave functions may be independently switched off (LSCALU=.FALSE.).

## Related tags and articles

NPAR,
NCORE,
LPLANE,
NSIM,
KPAR,
LSCALU,
LSCAAWARE

Examples that use this tag

---
