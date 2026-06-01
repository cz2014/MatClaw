# PHON_NEDOS

Categories: INCAR tag, Phonons

PHON\_NEDOS = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **PHON\_NEDOS** | = 2000 |  |

Description: Sets the number of frequency points to compute the phonon density of states.

---

The density of states is computed between
$[\omega\_{\text{min}}-5\sigma,\omega\_{\text{max}}+5\sigma]$ with
$\omega\_{\text{min}}$ and
$\omega\_{\text{max}}$ the lowest and highest phonon frequency and
$\sigma$ the broadening PHON\_SIGMA.

> **Mind:** Only available as of VASP 6.4.0.

## Related tags and articles

QPOINTS,
PHON\_NWRITE,
LPHON\_POLAR,
PHON\_DIELECTRIC,
PHON\_BORN\_CHARGES,
PHON\_G\_CUTOFF

Examples that use this tag
