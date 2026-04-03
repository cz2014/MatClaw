# EFIELD

Categories: INCAR tag, Molecules, Electrostatics

EFIELD = [real]

Description: EFIELD controls the magnitude of the applied electric force field.

---

It is possible to apply an external electrostatic field in slab, or molecular calculations. Presently only a single value can be supplied and the field is applied in the direction selected by IDIPOL=1-4. The electric force field is supplied in units of eV/Å. Dipole corrections to the potential (LDIPOL=.TRUE.) can and should be turned on to avoid interactions between the periodically repeated images.

> **Mind:** The electric field is defined opposite to the common definition. So electrons will move along the direction of the electric field.

## Related tags and articles

Monopole Dipole and Quadrupole corrections,
NELECT,
EPSILON,
IDIPOL,
DIPOL,
LMONO,
LDIPOL

Workflows that use this tag

---
