# SHAKETOL

Categories: INCAR tag, Advanced molecular-dynamics sampling

SHAKETOL = [Real]  
 Default: **SHAKETOL** = $10^{-5}$

Description: SHAKETOL specifies the tolerance for the SHAKE algorithm (in case VASP was compiled with -Dtbdyn).

---

Constrained molecular dynamics (MDALGO=1 | 2) are performed using a SHAKE algorithm.

SHAKETOL specifies the tolerance for the SHAKE algorithm.
If the error for all geometric constraints does not decrease below this predefined tolerance within the allowed number of iterations (SHAKEMAXITER), VASP terminates with an error message.

## Related tags and articles

SHAKEMAXITER,
MDALGO

Examples that use this tag

## References

---
