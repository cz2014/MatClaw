# PHON_G_CUTOFF

Categories: INCAR tag, Phonons

PHON\_G\_CUTOFF = [real]

|  |  |  |
| --- | --- | --- |
| Default: **PHON\_G\_CUTOFF** | = 8.0 |  |

Description: PHON\_G\_CUTOFF sets the cutoff radius in reciprocal space used to determine the number of $\mathbf{G}$ vectors involved in the Ewald sum in polar phonon calculations.

---

The Ewald sum that accounts for the long-range electrostatic interactions in phonon calculations runs over all G-vectors inside a cutoff sphere.
The radius of this sphere is given by PHON\_G\_CUTOFF as a multiple of the longest reciprocal lattice vector of the primitive cell (as detected by VASP).
Specifying the cutoff this way (as opposed to an absolute length or energy) ensures a default value that is relatively system-independent.

The default value of PHON\_G\_CUTOFF is a safe choice in most cases.
Lowering PHON\_G\_CUTOFF can result in faster phonon calculations.
However, ensure that the phonon spectrum is properly converged.
If you run into convergence problems, try raising the value until the phonon dispersion converges.

For more information on polar phonon calculations, see LPHON\_POLAR.

> **Mind:** Only available as of VASP 6.3.2.

## Related tags and articles

QPOINTS,
LPHON\_DISPERSION,
PHON\_NWRITE,
LPHON\_POLAR,
PHON\_DIELECTRIC,
PHON\_BORN\_CHARGES

Examples that use this tag
