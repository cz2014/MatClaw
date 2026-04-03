# NBANDSO

Categories: INCAR tag, Many-body perturbation theory, Bethe-Salpeter equations

NBANDSO = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NBANDSO** | = number of occupied orbitals |  |

Description: NBANDSO determines how many occupied orbitals are included in the Casida/BSE calculations or time propagation (ALGO=TIMEEV.

---

For the time-propagation algorithm increasing NBANDSO only modestly increases the compute time.
For BSE and Casida-type calculations, the compute time grows with the third power of the number of included occupied and unoccupied bands

$(N\_{\mathrm{occ}} N\_{\mathrm{virtual}} N\_{\mathrm{k}})^{3}$

and the memory requirements increase quadratically

$(N\_{\mathrm{occ}}N\_{\mathrm{virtual}} N\_{\mathrm{k}})^{2}$

Please be aware that symmetry is not exploited in the BSE code, hence memory requirements can be excessive. To allow for calculations on large systems, the BSE code distributes the BSE matrix among all available cores and uses ScaLAPACK for the diagonalization.

VASP always uses the orbitals closest to the Fermi-level, and NBANDSO ($N\_{\mathrm{occ}}$) and NBANDSV ($N\_{\mathrm{virtual}}$) determines how many occupied and unoccupied orbitals are included. The defaults are fairly "conservative" and equal the total number of electrons/2 (this usually implies that all occupied states are included). For highly accurate results, NBANDSV often needs to be increased, whereas for large systems one is often forced to reduce both values to much smaller numbers. Sometimes qualitative results for bandlike Wannier-Mott excitons can be obtained even with a single conduction and valence band.

## Related tags and articles

NBANDSV,
BSE calculations,
Timepropagation

Examples that use this tag

---
