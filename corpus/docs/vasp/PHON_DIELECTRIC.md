# PHON_DIELECTRIC

Categories: INCAR tag, Phonons

PHON\_DIELECTRIC = [3x3 real]

|  |  |  |
| --- | --- | --- |
| Default: **PHON\_DIELECTRIC** | = None |  |

Description: PHON\_DIELECTRIC sets the static dielectric tensor to be used for the dipole-dipole corrections in the computation of the phonon dispersion. This is only used when LPHON\_POLAR=.TRUE.

---

If the material is non-metallic and polar (i.e. two or more atoms in the unit cell carry nonzero Born effective charge tensors), a special treatment of the long-range dipole-dipole interaction is required to obtain a smooth phonon dispersion.
This is activated by setting LPHON\_POLAR=.TRUE. and supplying the static dielectric tensor (PHON\_DIELECTRIC) and the Born-effective charges (PHON\_BORN\_CHARGES) which can be obtained in a separate VASP calculation using the LEPSILON or LCALCEPS tag.
The dipole-dipole part of the interatomic force-constants is evaluated using an Ewald summation with the number of $\mathbf{G}$ vectors determined by the cutoff length (PHON\_G\_CUTOFF).

> **Mind:** Only available as of VASP 6.3.2.

## Related tags and articles

QPOINTS,
LPHON\_DISPERSION,
PHON\_NWRITE,
LPHON\_POLAR,
PHON\_BORN\_CHARGES,
PHON\_G\_CUTOFF

Examples that use this tag
