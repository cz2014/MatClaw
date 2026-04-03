# HILLS_H

Categories: INCAR tag, Advanced molecular-dynamics sampling

HILLS\_H = [Real]  
 Default: **HILLS\_H** = $10^{-3}$

Description: HILLS\_H specifies the height of the Gaussian hill (in eV) used in metadynamics (in case VASP was compiled with -Dtbdyn).

---

In metadynamics (MDALGO=11 | 21), the bias potential is given as

:   $$\tilde{V}(t,\xi) = h \sum\_{i=1}^{\lfloor t/t\_G \rfloor} \exp{\left\{ -\frac{|\xi^{(t)}-\xi^{(i \cdot t\_G)}|^2}{2
    w^2} \right\}}.$$

Thre parameters (HILLS\_H, HILLS\_W, and HILLS\_BIN) must be provided by the user.

The height of the Gaussian hills $h$ (in eV) is set by HILLS\_H.

## Related tags and articles

Metadynamics,
HILLS\_W,
HILLS\_BIN,
HILLSPOT,
MDALGO

Examples that use this tag

---
