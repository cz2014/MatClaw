# NSIM

Categories: INCAR tag, Performance, Parallelization

NSIM = [integer]  
 Default: **NSIM** = 4

Description: NSIM sets the number of bands that are optimized simultaneously by the RMM-DIIS algorithm. This also controls for the blocked-Davidson at certain places how many orbitals are worked on simultaneously as well as in the calculation of forces. Especially, GPUs benefit from increasing NSIM.

---

The RMM-DIIS algorithm (IALGO=48) works in a blocked mode. NSIM bands are optimized at the same time. This allows to use matrix-matrix operations instead of matrix-vector operation for the evaluations of the non local projection operators in real space, and might speed up calculations on some machines. There should be no difference in the total energy and the convergence behavior between NSIM=1 and NSIM>1, only the performance should improve.

## Related tags and articles

IALGO,
NCORE,
NPAR,
LPLANE,
LSCALU,
KPAR,
LSCALAPACK,
LSCAAWARE

Examples that use this tag

---
