# LVGVAPPL

Categories: INCAR tag, NMR

LVGVAPPL = .TRUE. | .FALSE.  
 Default: **LVGVAPPL** = .FALSE.

Description: LVGVAPPL determines whether the *vGv* orbital magnetic susceptibility is applied in the calculation of the CSA tensor.

LVGVAPPL is available as of VASP.6.4.0.

---

When performing a chemical shift calculation the standard *pGv* susceptibility is used to calculate the $\mathbf{G=0}$ contribution to the CSA tensor by default.
This can be overruled with LVGVAPPL.
In case LVGVAPPL is true, the *vGv* susceptibility is applied for the calculation of the $\mathbf{G=0}$ contribution to the CSA tensor. For details see LVGVCALC.

## Related tags and articles

LCHIMAG, LVGVCALC

---
