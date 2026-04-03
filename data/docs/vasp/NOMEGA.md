# NOMEGA

Categories: INCAR tag, Many-body perturbation theory, GW, ACFDT, Low-scaling GW and RPA

NOMEGA = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NOMEGA** | = 100 | for GW calculations |
|  | = 12 | for ACFDT calculations |

Description: NOMEGA specifies the number of (imaginary) frequency and imaginary time grid points.

---

Typically NOMEGA should be chosen around 50-100 (for the parallel version, NOMEGA should be dividable by the number of compute nodes to obtain maximum efficiency). For quick and memory conserving calculations, it is sufficient to set NOMEGA to values around NOMEGA = 20-30, but then you must expect errors of the order of 20-50 meV for the gap and 100-200 meV for the bottom of the conduction band. We furthermore recommend to increase NOMEGA not beyond 100 for a $k$-point sampling of 4×4×4 points/atom: the joint DOS and the self-energy tend to possess spurious fine structure related to the finite $k$-point grid. This fine structure is smoothed when smaller values for NOMEGA are used or if more $k$-points are used. For 6×6×6 $k$-points/atom NOMEGA can be usually increased to 200-300 without noticing problems associated with this kind of noise.

Note that the spectral method (see LSPECTRAL) scales very favorable with respect to the number of frequency points hence NOMEGA=30 is usually only slightly faster than NOMEGA=100.

* N.B: Low-scaling GW and RPA/ACFDT calculations require considerably fewer imaginary frequency (and time) points.

## Related tags and articles

NOMEGAR,
NTAUPAR,
LSPECTRAL
NOMEGA\_DUMP

Examples that use this tag

---
