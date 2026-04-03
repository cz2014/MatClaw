# HILLS_BIN

Categories: INCAR tag, Advanced molecular-dynamics sampling

HILLS\_BIN = [Integer]  
 Default: **HILLS\_BIN** = NSW

Description: HILLS\_BIN sets the number of steps after which the bias potential is updated in a metadynamics run (in case VASP was compiled with -Dtbdyn).

---

In metadynamics (MDALGO=11 | 21), the bias potential is given as

:   $$\tilde{V}(t,\xi) = h \sum\_{i=1}^{\lfloor t/t\_G \rfloor} \exp{\left\{ -\frac{|\xi^{(t)}-\xi^{(i \cdot t\_G)}|^2}{2
    w^2} \right\}}.$$

Thre parameters (HILLS\_H, HILLS\_W, and HILLS\_BIN) must be provided by the user.

The number of steps after which the bias potential is updated is set by HILLS\_BIN.

## Related tags and articles

Metadynamics,
HILLS\_H,
HILLS\_W,
HILLSPOT,
MDALGO

Examples that use this tag

---
