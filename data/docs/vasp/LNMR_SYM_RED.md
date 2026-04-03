# LNMR_SYM_RED

Categories: INCAR tag, NMR, Symmetry

LNMR\_SYM\_RED = .TRUE. | .FALSE.  
 Default: **LNMR\_SYM\_RED** = .FALSE.

Description: discard symmetry operations that are not consistent with the way *k*-space derivatives are calculated in the linear-response calculations of chemical shifts.

---

The star on which the *k*-space derivative is calculated is oriented along the cartesian directions in *k* space. If the symmetry operations in *k* space do not map this star onto itself, erroneous results can be obtained. To check for such operations, set LNMR\_SYM\_RED=.TRUE.. VASP then disregards such operations, and the resulting first Brillouin zone (IBZ) is larger. This is only relevant if the use of symmetry is switched on, i.e. `ISYM > 0`. In case of any doubt, set LNMR\_SYM\_RED=.TRUE.

> **Warning:** It matters how the real-space-lattice vectors are set up relative to the cartesian coordinates in the POSCAR file.

It determines the orientation of the *k*-space star and, hence, can affect the efficiency via the number of *k*-points in the IBZ.

## Related tags and articles

LCHIMAG,
DQ,
ICHIBARE,
NLSPLINE

Examples that use this tag
