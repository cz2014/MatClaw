# FMP_DIRECTION

Categories: INCAR tag, Molecular dynamics, Ensemble properties

FMP\_DIRECTION = 1 | 2 | 3  
 Default: **FMP\_DIRECTION** = 3

Description: Index of the lattice vector $\mathbf{a}\_i$ along which the temperature gradient is created in the (Müller-Plathe method).

---

FMP\_DIRECTION defines the index of the lattice vector $\mathbf{a}\_i$ along which the gradient $\partial T/\partial \mathbf{a}\_i$ is created during the reverse nonequilibrium molecular-dynamics run using the Müller-Plathe method.

> **Mind:** This tag will only be available from VASP 6.4.4

## Related tags and articles

Müller-Plathe method,
FMP\_ACTIVE,
FMP\_SNUMBER,
FMP\_SWAPNUM,
FMP\_PERIOD
