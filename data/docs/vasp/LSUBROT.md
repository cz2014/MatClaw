# LSUBROT

Categories: INCAR tag, Electronic minimization

LSUBROT = .FALSE. | .TRUE.

|  |  |  |
| --- | --- | --- |
| Default: **SUBROT** | = .FALSE. |  |

Description: This flag can be set for hybrid functionals (HF-type calculations). LSUBROT determines whether an optimal rotation matrix between the occupied and unoccupied block is sought, when a direct optimization of the energy functional is performed (i.e. ALGO=All | Damped). The corresponding algorithm is unpublished. LSUBROT =.FALSE. is the standard algorithm, in which the rotation matrix between occupied and unoccupied orbitals is determined essentially using Loewdin perturbation theory, as for instance explained in Ref. . For LSUBROT =.TRUE. the rotation matrix is instead optimized by performing a few standard SCF steps, in which the orbitals are kept fixed, but rotations between the occupied and unoccupied manifold are allowed. Once satisfactory convergence has been reached, the optimized density matrix (rotation matrix between occupied and unoccupied block) is passed back to the direct optimization routine and a rotation along the suggested direction is performed alongside an update of the orbitals. This generally speeds up calculations for small gap systems as well as metals. However, in rare cases, we have observed instabilities, so be careful when selecting LSUBROT =.TRUE.

Although the flag can be set for standard functionals, it is only efficient for hybrid functionals (HF-type calculations).

## References

---
