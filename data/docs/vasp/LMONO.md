# LMONO

Categories: INCAR tag, Molecules, Electrostatics

LMONO = .TRUE. | .FALSE.  
 Default: **LMONO** = .FALSE.

Description: LMONO switches on monopole-monopole corrections for the total energy.

---

The flag switches on monopole corrections for charged systems. The correction is calculated only a posteriori for the total energy. No correction to the potential is calculated.

> **Tip:** If corrections for the potential are desired as well, please use LDIPOL instead (when using LDIPOL, VASP automatically determines whether the system is charged and activates the monopole corrections automatically).

The primary use of this flag is for defect calculations in charged supercells, as well
as charged 0D systems (molecules and atoms). VASP also automatically calculates
corrections to the total energy related to repeated dipoles (IDIPOL=4).
The user then needs to decide whether
those are sensible or not. Specifically, for super cells using periodic boundary conditions,
it is often not possible to determine the dipole at the defect site accurately,
whereas for 0D systems (i.e. atoms and molecules) the dipole can be determined
accurately.

## Related tags and articles

Monopole Dipole and Quadrupole corrections,
NELECT,
EPSILON,
IDIPOL,
DIPOL,
LDIPOL,
EFIELD

Examples that use this tag

---
