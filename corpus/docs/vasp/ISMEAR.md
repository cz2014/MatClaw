# ISMEAR

Categories: INCAR tag, Electronic occupancy, Electronic minimization, Density of states

ISMEAR = -15 | -14 | -5 | -4 | -3 | -2 | -1 | 0 | [integer]>0  
 Default: **ISMEAR** = 1

Description: ISMEAR determines how the partial occupancies *f*n**k** are set for each orbital. SIGMA determines the width of the smearing in eV.

---

Please consider how-to guide to choose the optimal smearing technique.

## Tag options

* `ISMEAR > 0`: method of Methfessel-Paxton order ISMEAR with width SIGMA.

:   > **Mind:** Methfessel-Paxton can yield erroneous results for insulators because the partial occupancies can be unphysical.

* `ISMEAR = 0`: Gaussian smearing with width SIGMA.

* `ISMEAR = -1`: Fermi smearing with width SIGMA.

* `ISMEAR = -2`: Partial occupancies are read in from the WAVECAR and kept fixed throughout run. Alternatively, you can also choose occupancies in the INCAR file with the tag FERWE (and FERDO for `ISPIN = 2` calculations).

* `ISMEAR = -3`: perform a loop over SMEARINGS parameters supplied in the INCAR file.

* `ISMEAR = -4`: Tetrahedron method without smearing.

* `ISMEAR = -5`: Tetrahedron method with Blöchl corrections without smearing.

* `ISMEAR = -14`: Tetrahedron method with Fermi-Dirac smearing SIGMA.

* `ISMEAR = -15`: Tetrahedron method with Blöchl corrections with Fermi-Dirac smearing SIGMA.

:   > **Mind:** Use a Γ-centered **k**-mesh for the tetrahedron methods.

## Related tags and articles

SIGMA,
EFERMI,
FERWE,
FERDO,
SMEARINGS,
Smearing technique,
K-point integration

Examples that use this tag
