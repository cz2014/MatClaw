# KPUSE

Categories: INCAR tag, Charge density

KPUSE = [integer array]  
 Default: **KPUSE** = not set

Description: KPUSE sets a list of **k** points that contribute to calculating the partial charge density.

---

IBAND selects a subset of *k'* points for which the partial charge density is calculated when LPARD = .TRUE..
Partial charge densities are written to the PARCHG file, or one of its variants, depending on the setting of LSEPB and LSEPK.

> **Mind:** All **k** point weights will be internally reset to 1 if KPUSE is specified. Thus results are usually only correct if the groundstate calculation and the partial charge post-processing is performed with ISYM = -1.

E.g. if `KPUSE = 1 4 7`
the charge density will be calculated for the three **k** points 1, 4, and 7.

## Related tags and articles

LPARD,
NBMOD,
EINT,
IBAND,
LSEPB,
LSEPK,
LPARDH5,
PARCHG,
vaspout.h5,
Band-decomposed charge densities

Examples that use this tag

---
