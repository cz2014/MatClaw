# IBAND

Categories: INCAR tag, Charge density

IBAND = [integer array]  
 Default: **IBAND** = not set

Description: IBAND sets a list of bands that contribute to calculating the partial charge density.

---

IBAND selects a subset of bands for which the partial charge density is calculated when LPARD = .TRUE..
Partial charge densities are written to the PARCHG file, or one of its variants, depending on the setting of LSEPB and LSEPK.

> **Mind:** Setting IBAND will automatically set NBMOD = N, where N is the number of bands passed to IBAND, regardless of the NBMOD setting in the INCAR file.

E.g. if
`IBAND = 20 21 22 23 45`
the charge density will be calculated for the four bands 20 to 23 and band 45, and NBMOD will be set to 5.

## Related tags and articles

LPARD,
NBMOD,
EINT,
KPUSE,
LSEPB,
LSEPK,
LPARDH5,
PARCHG,
vaspout.h5,
Band-decomposed charge densities

Examples that use this tag

---
