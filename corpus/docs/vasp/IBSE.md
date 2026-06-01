# IBSE

Categories: INCAR tag, Many-body perturbation theory, Bethe-Salpeter equations

IBSE = 0 | 1 | 2 | 3  
 Default: **IBSE** = 2

Description: IBSE can be used to select the algorithm for solving the Bethe-Salpeter or Casida equation.

---

The following options are available to solve the Bethe-Salpeter or Casida equation:

* IBSE = 0: Exact diagonalization with old BSE driver
* IBSE = 1: Time evolution
* IBSE = 2:  Exact diagonalization
* IBSE = 3: Lanczos algorithm

`IBSE = 2` and `IBSE = 0` yield exactly the same results but the old driver (`IBSE = 0`) is typically much slower and will be deprecated in the future.

> **Mind:** `IBSE = 2` and `IBSE = 3` are only available for VASP version 6.5.0 and above.

## Related tag and articles

IBSE,
BSEPREC,
NBANDSV,
NBANDSO,
CSHIFT,
OMEGAMAX,
BSE calculations,
Time-dependent density-functional theory calculations,
Bethe-Salpeter equations

---
