# LPHON_POLAR

Categories: INCAR tag, Phonons

LPHON\_POLAR = .TRUE. | .FALSE.  
 Default: **LPHON\_POLAR** = .FALSE.

Description: LPHON\_POLAR includes dipole-dipole corrections in the computation of the phonon dispersion. For this mode, PHON\_DIELECTRIC and PHON\_BORN\_CHARGES must also be set.

---

If the material is non-metallic and polar (i.e. two or more atoms in the unit cell carry nonzero Born effective charge tensors), a special treatment of the long-range dipole-dipole interaction is required to obtain a smooth phonon dispersion.
This is activated by setting LPHON\_POLAR=.TRUE. and supplying the static dielectric tensor (PHON\_DIELECTRIC) and the Born-effective charges (PHON\_BORN\_CHARGES) which can be obtained in a separate VASP calculation using the LEPSILON or LCALCEPS tag.
The dipole-dipole part of the interatomic force-constants is evaluated using an Ewald summation with the number of $\mathbf{G}$ vectors determined by the cutoff length (PHON\_G\_CUTOFF).

In the case of metals, the dielectric function is infinite, for nonpolar semiconductors the Born effective charges are zero which in both cases means that the long-range interatomic force-constants are zero and this dipole-dipole correction does not need to be applied.

> **Mind:** Only available as of VASP 6.3.2.

## Related tags and articles

QPOINTS,
LPHON\_DISPERSION,
PHON\_NWRITE,
PHON\_DIELECTRIC,
PHON\_BORN\_CHARGES,
PHON\_G\_CUTOFF

Examples that use this tag
