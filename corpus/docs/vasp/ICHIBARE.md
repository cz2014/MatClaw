# ICHIBARE

Categories: INCAR tag, NMR

ICHIBARE = 1 | 2 | 3  
 Default: **ICHIBARE** = 1

Description: determines the order of the finite difference stencil used to calculate the magnetic susceptibility.

---

ICHIBARE specifies the order of the finite difference stencil used to calculate the magnetic susceptibility (second order derivative in Eq. 47 of Yates *et al.*). ICHIBARE may be set to 1, 2, or 3. Often the default (ICHIBARE=1) is sufficient. A higher ICHIBARE results in a substantial increase of the computational load.

## Related tags and articles

LCHIMAG,
DQ,
LNMR\_SYM\_RED,
NLSPLINE

Examples that use this tag

## References
