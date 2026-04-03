# LCHARG

Categories: INCAR tag, Charge density

LCHARG = [logical]  
 Default: **LCHARG** = .True.

Description: Determines whether the charge density is written.

---

For LCHARG = T  (default), the files CHGCAR and CHG are written.
If LH5 = T , the charge density is instead written to vaspwave.h5.

> **Mind:** For VASP version 6.0 to 6.4.2 the default for LCHARG = .NOT.LH5

## Related tags and articles

LWAVE, LWAVEH5, LCHARGH5, LH5

Workflows that use this tag
