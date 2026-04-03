# LSCALU

Categories: INCAR tag, Performance, Parallelization

LSCALU = [logical]  
 Default: **LSCALU** = .FALSE.

Description: LSCALU switches on the parallel LU decomposition (using scaLAPACK) in the orthonormalization of the wave functions.

---

For LSCALU=.TRUE. the LU decomposition in the orthormalization of the wave functions is done in parallel, using scaLAPACK routines.
Provided, of course, LSCALAPACK=.TRUE. and VASP was compiled with scaLAPACK support (precompiler flag: -DscaLAPACK).

In many cases, the scaLAPACK LU decomposition based is *slower* than the serial LU decomposition (compare the timing ORTHCH in the respective OUTCAR files). Hence the default is LSCALU=.FALSE.
(subspace rotations, however, are still done using scaLAPACK).

## Related tags and articles

NPAR,
NCORE,
LPLANE,
NSIM,
KPAR,
LSCALAPACK,
LSCAAWARE

Examples that use this tag

---
