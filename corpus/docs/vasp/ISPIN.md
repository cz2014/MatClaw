# ISPIN

Categories: INCAR tag, Magnetism

ISPIN = 1 | 2  
 Default: **ISPIN** = 1

Description: ISPIN specifies spin polarization.

---

* ISPIN=1: non-spin-polarized calculations are performed.
* ISPIN=2: spin-polarized calculations (collinear) are performed.

By combining ISPIN with MAGMOM collinear magnetism can be studied.

> **Important:** For noncollinear calculations ISPIN is ignored. In VASP 6.5.0, the calculation will exit with an error message if ISPIN=2 and MAGMOM is used in combination with the LNONCOLLINEAR=.TRUE.

## Related tags and articles

MAGMOM

Examples that use this tag
