# EPSILON

Categories: INCAR tag, Molecules, Electrostatics

EPSILON = [real]  
 Default: **EPSILON** = 1

Description: EPSILON sets the dielectric constant of the medium.

---

VASP uses this flag only to scale the calculated monopole and dipole corrections. EPSILON defaults to 1, which is the proper value for isolated atoms and molecules. For solids, the screening properties can and should be determined using the linear response routines of VASP (see LEPSILON and/or LCALCEPS). Ionic contributions to the dielectric tensor should be included, if the ions are allowed to relax. Ionic contributions to the dielectric tensor can be calculated using IBRION=8.

## Related tags and articles

Monopole Dipole and Quadrupole corrections,
NELECT,
DIPOL,
IDIPOL,
LDIPOL,
LMONO,
EFIELD

Examples that use this tag

---
