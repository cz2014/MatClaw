# FMP_SNUMBER

Categories: INCAR tag, Molecular dynamics, Ensemble properties

FMP\_SNUMBER = integer  
 Default: **FMP\_SNUMBER** = 10

Description: Number of slabs perpendicular to the temperature gradient in the Müller-Plathe method.

---

FMP\_SNUMBER defines the number of slabs perpendicular to the lattice vector $\mathbf{a}\_i$ along which the gradient $\partial T/\partial \mathbf{a}\_i$ is created during the reverse nonequilibrium molecular dynamics run using the Müller-Plathe method.

> **Mind:** This tag will only be available from VASP 6.4.4

## Related tags and articles

Müller-Plathe method,
FMP\_ACTIVE,
FMP\_DIRECTION,
FMP\_SWAPNUM,
FMP\_PERIOD
