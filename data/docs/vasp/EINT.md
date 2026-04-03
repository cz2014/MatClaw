# EINT

Categories: INCAR tag, Charge density

EINT = [real1] [real2] | [real1]  
 Default: **EINT** = not set

Description: EINT sets the energy interval for bands contributing to the calculation of the partial charge density in eV.

---

* EINT= [real1] [real2]:

:   If two values are given, the energy interval between those values is used.

* EINT= [real1]:

:   If only one value is given, the Fermi energy $\epsilon\_f$ is used as the other limit [real2] of the interval.

---

> **Important:** The energies passed in EINT are used as set if NBMOD = -2, but will be added to the Fermi energy ($\epsilon\_f$ + real1 and $\epsilon\_f$ + real2) if NBMOD = -3.

If [real1] is larger than [real2], the two values will be flipped internally, so a meaningful energy interval is used.

If EINT is set, but NBMOD is not, it will be internally set to NBMOD = -2, and the input values of EINT will be treated as absolute energies.

EINT can be conveniently used in combination with NBMOD = -3 to mimic the bias-voltage for simulating a scanning-tunneling-microscope image.

## Related tags and articles

LPARD,
NBMOD,
IBAND,
KPUSE,
LSEPB,
LSEPK,
LPARDH5,
PARCHG,
vaspout.h5,
Band-decomposed charge densities

Examples that use this tag

---
