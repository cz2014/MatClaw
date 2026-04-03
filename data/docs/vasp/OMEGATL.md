# OMEGATL

Categories: INCAR tag, Many-body perturbation theory, GW, ACFDT

OMEGATL = [real]  
 Default: **OMEGATL** = 10 $\times$ outermost node in dielectric function $\epsilon(\omega)$

Description: OMEGATL specifies the maximum frequency for the coarse part of the frequency grid.

---

For the frequency grid along the real and imaginary axis sophisticated schemes are used, which are based on simple model functions for the macroscopic dielectric function. The grid spacing is dense up to roughly 1.3\*OMEGAMAX and becomes coarser for larger frequencies.
The default has been carefully tested, and it is recommended to leave it unmodified whenever possible.

## Related tags and articles

OMEGAMAX,
OMEGAMIN,
CSHIFT,
NOMEGA

Examples that use this tag

---
