# PHON_NWRITE

Categories: INCAR tag, Phonons

PHON\_NWRITE = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **PHON\_NWRITE** | = 1 |  |

Description: PHON\_NWRITE
determines how much output is written to the OUTCAR file when computing the phonon dispersion LPHON\_DISPERSION=.TRUE.

---

Positive numbers mean human-readable output, and negative numbers mean one-line format. The available options are:

| PHON\_NWRITE | Description |
| --- | --- |
| 2 | For each q point, write the same as 1 and then the phonon modes with the displacement of each atom in the three cartesian directions per line. |
| 1 | For each q point, q-point coordinates are written in one line and the phonon frequencies are written one branch per line in different units. |
| 0 | No phonon output is written to OUTCAR. |
| -1 | For each q point, only a single line is written containing q-point coordinates and frequencies. |
| -2 | For each q point, q-point coordinates and frequencies are written in separate blocks and frequencies are reported in different units. |
| -3 | Like -2, but in addition, the phonon eigenvectors are written for each q point. |

> **Mind:** Only available as of VASP 6.3.2.

## Related tags and articles

QPOINTS,
LPHON\_DISPERSION,
LPHON\_POLAR,
PHON\_DIELECTRIC,
PHON\_BORN\_CHARGES,
PHON\_G\_CUTOFF

Examples that use this tag
