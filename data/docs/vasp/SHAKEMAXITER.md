# SHAKEMAXITER

Categories: INCAR tag, Advanced molecular-dynamics sampling

SHAKEMAXITER = [Integer]  
 Default: **SHAKEMAXITER** = 1000

Description: SHAKEMAXITER specifies the maximum number of iterations in the SHAKE algorithm (in case VASP was compiled with -Dtbdyn).

---

Constrained molecular dynamics (MDALGO=1 | 2) are performed using a SHAKE algorithm.

If the error for all geometric constraints does not decrease below a predefined tolerance (SHAKETOL) within the allowed number of iterations, VASP terminates with an error message.
The aforementioned maximum number of iterations is set by means of the SHAKEMAXITER tag.

## Related tags and articles

SHAKETOL,
MDALGO

Examples that use this tag

## References

---
