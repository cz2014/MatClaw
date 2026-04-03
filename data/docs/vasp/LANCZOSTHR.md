# LANCZOSTHR

Categories: INCAR tag, Bethe-Salpeter equations, Many-body perturbation theory

> **Deprecated:** This feature is deprecated and will be removed in a future release. Please use BSEPREC instead.

LANCZOSTHR = [real]  
 Default: **LANCZOSTHR** = $10^{-3}$

Description: LANCZOSTHR is used by the BSE Lanczos algorithm to stop the iterative procedure, once the dielectric function has reached numerical convergence.

---

The difference between the dielectric function at two consecutive iterations, $i$ and $i+1$, is computed as root-mean-square over the frequency grid

:   :   $$\mathrm{RMS}[\epsilon] = \sqrt{\sum\_{j=1}^N\frac{1}{N}\left[\epsilon\_{i}(\omega\_j)-\epsilon\_{i+1}(\omega\_j)\right]^2}$$

and once $\mathrm{RMS}[\epsilon]\lt =$LANCZOSTHR the iterative algorithm stops.

## Related tag and articles

BSE,
BSE calculations,
Bethe-Salpeter equations

---
