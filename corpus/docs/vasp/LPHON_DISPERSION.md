# LPHON_DISPERSION

Categories: INCAR tag, Phonons

LPHON\_DISPERSION = .TRUE. | .FALSE.

|  |  |  |
| --- | --- | --- |
| Default: **LPHON\_DISPERSION** | = .FALSE. |  |

Description: LPHON\_DISPERSION requests the calculation of the phonon dispersion along the q-point path supplied in file QPOINTS (same format as KPOINTS).

---

After the computation of the force constants using finite differences (IBRION=5,6) or density-functional perturbation theory (IBRION=7,8) on a supercell it is possible to compute the phonon dispersion for the equivalent primitive cell determined by VASP by setting LPHON\_DISPERSION=.TRUE.

> **Mind:** Only available as of VASP 6.3.2.

## Related tags and articles

QPOINTS,
PHON\_NWRITE,
LPHON\_POLAR,
PHON\_DIELECTRIC,
PHON\_BORN\_CHARGES,
PHON\_G\_CUTOFF

Examples that use this tag
