# HILLS_W

Categories: INCAR tag, Advanced molecular-dynamics sampling

HILLS\_W = [Real]  
 Default: **HILLS\_W** = $10^{-3}$

Description: HILLS\_W specifies the width of the Gaussian hill (in units of the corresponding collective variable) used in metadynamics (in case VASP was compiled with -Dtbdyn).

---

In metadynamics (MDALGO=11 | 21), the bias potential is given as

:   $$\tilde{V}(t,\xi) = h \sum\_{i=1}^{\lfloor t/t\_G \rfloor} \exp{\left\{ -\frac{|\xi^{(t)}-\xi^{(i \cdot t\_G)}|^2}{2
    w^2} \right\}}.$$

Thre parameters (HILLS\_H, HILLS\_W, and HILLS\_BIN) must be provided by the user.

The width of the Gaussian hills $w$ (in units of the corresponding collective variable) is set by HILLS\_W.

## Related tags and articles

Metadynamics,
HILLS\_H,
HILLS\_BIN,
HILLSPOT,
MDALGO

Examples that use this tag

---
