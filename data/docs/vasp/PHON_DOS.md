# PHON_DOS

Categories: INCAR tag, Phonons

PHON\_DOS = 0 | 1 | 2

|  |  |  |
| --- | --- | --- |
| Default: **PHON\_DOS** | = 0 |  |

Description: Select the approach to use when computing the phonon density-of-states (DOS).

---

The possible values are

| PHON\_DOS | Function |
| --- | --- |
| 0 | The phonon DOS computation is not performed. |
| 1 | A gaussian broadening function with a width specified by PHON\_SIGMA is used. |
| 2 | The tetrahedron method is used. |

To get a representative density of states the QPOINTS file should specify a regular mesh.
When line mode in the QPOINTS file and gaussian smearing (PHON\_DOS=1) is used, the phonon density of states will still be computed but the results are not reliable.

> **Mind:** Only available as of VASP 6.4.0.

## Related tags and articles

QPOINTS,
PHON\_NWRITE,
LPHON\_POLAR,
PHON\_DIELECTRIC,
PHON\_BORN\_CHARGES,
PHON\_G\_CUTOFF,
PHON\_SIGMA,
PHON\_NEDOS

Examples that use this tag
