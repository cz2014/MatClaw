# LVGVCALC

Categories: INCAR tag, NMR

LVGVCALC = .TRUE. | .FALSE.  
 Default: **LVGVCALC** = .TRUE.

Description: LVGVCALC switches on calculation of the *vGv* expression for the orbital magnetic susceptibility.

LVGVCALC is available as of VASP.6.4.0.

---

When performing a chemical shift calculation the standard *pGv* susceptibility is calculated and used in the calculation of the CSA tensor . When LVGVCALC is true, the magnetic susceptibility is also calculated with the *vGv* approximation. LVGVAPPL determines whether the *vGv* or *pGv* result is applied in the calculation of the $\mathbf{G=0}$ contribution to the CSA tensor.

The *vGv* expression for the orbital susceptibility was introduced by d'Avezac *et al.* .
In VASP its ultra-soft generalization is used .

## Related tags and articles

LCHIMAG, LVGVAPPL

## References
