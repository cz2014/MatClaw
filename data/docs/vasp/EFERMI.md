# EFERMI

Categories: INCAR tag, Electronic ground-state properties

EFERMI = MIDGAP | LEGACY | [real]  
 Default: **EFERMI** = LEGACY

Description: Defines how the Fermi energy is calculated in VASP. It is recommended to use EFERMI = MIDGAP.

---

## Fermi energy in semiconductors

For semiconducting materials, the Fermi energy is not uniquely defined in the bandgap of the material.
Any value that produces the correct number of electrons (NELECT) is allowed.
By default, VASP places the Fermi energy at a somewhat arbitrary value within the bandgap.
The precise value depends on values chosen for the smearing (ISMEAR and SIGMA) and the density of states (EMIN, EMAX, and NEDOS).
Typically, this places the Fermi energy towards the bottom of the bandgap.

You can change this behavior by setting EFERMI = MIDGAP (recommended).
VASP will then put the Fermi energy in the middle of the gap because this is the most consistent with increasing the smearing SIGMA.
This algorithm to determine the Fermi energy was introduced in VASP.6.4.
The value of the Fermi energy should not affect the outcome of the calculation.

## Fermi energy in metals

MIDGAP and LEGACY should yield the same value when your system does not have a gap.
The Fermi energy is placed precisely at the value so that underneath are enough states to accommodate NELECT electrons. The evaluation of the Fermi energy involves an integral over the 1. BZ.
Therefore, the Fermi energy in metals needs to be converged with respect to the KPOINTS mesh and smearing (ISMEAR, SIGMA).

> **Tip:** If you are interested in the properties at the Fermi energy (e.g., for transport calculations), you should compute the Fermi energy with a very dense **k**-point mesh. To save computational time, you can fix the charge density (ICHARG = 11) once the Kohn-Sham states have converged with respect to the **k**-point density and increase the number of **k**-point further to converge the value of the Fermi energy.

## Fixed Fermi energy

Occasionally, you want to compute systems with fixed Fermi energy for a given charge density.
To this end, set EFERMI to a numeric value and ICHARG = 11.
A possible use case is to set EFERMI to the converged Fermi energy in a band-structure calculation.
You may use this to introduce electron doping/depletion to a system.

> **Warning:** The Fermi energy cannot be computed based on **k** points along a path.

This is, in particular, important for band-structure calculation of metallic systems because for gaped systems the Fermi energy often still ends up at a valid value within the gap despite the inaccurate computation. Hence, to plot a band structure the band energies should be taken from the calculation with fixed charge density based on **k**-points along a path, but the Fermi energy should be taken from the calculation based on a **k** mesh (e.g., the scf calculation by which the charge density was obtained or a more precisely converged Fermi energy based on the same fixed charge density). EFERMI can fix the Fermi energy to the proper value during the band-structure calculation.

## Related tags and articles

ISMEAR,
SIGMA,
EMIN,
EMAX,
NEDOS,
Chemical potential in electron-phonon interactions
