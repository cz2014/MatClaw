# PHON_SIGMA

Categories: INCAR tag, Phonons

PHON\_SIGMA = [real]

|  |  |  |
| --- | --- | --- |
| Default: **PHON\_SIGMA** | = 0.0005 eV |  |

Description: Set the width of the Gaussian function in eV to compute the phonon density of states.

---

The density of states is computed between
$[\omega\_{\text{min}}-5\sigma,\omega\_{\text{max}}+5\sigma]$ with
$\omega\_{\text{min}}$ and
$\omega\_{\text{max}}$ the lowest and highest phonon frequency and
$\sigma$ the broadening PHON\_SIGMA.
The number of energy points in this interval is set by PHON\_NEDOS.

> **Mind:** Only available as of VASP 6.4.0.

## Related tags and articles

QPOINTS,
PHON\_NWRITE,
LPHON\_POLAR,
PHON\_DIELECTRIC,
PHON\_BORN\_CHARGES,
PHON\_G\_CUTOFF

Examples that use this tag
