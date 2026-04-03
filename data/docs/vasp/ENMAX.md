# ENCUT

Categories: INCAR tag, Projector-augmented-wave method

ENCUT = [real]

|  |  |  |
| --- | --- | --- |
| Default: **ENCUT** | = largest ENMAX in the POTCAR file |  |

Description: ENCUT specifies the energy cutoff for the plane-wave basis set in eV.

---

All plane waves with a kinetic energy smaller than $E\_{\mathrm{cut}}$ are included in the basis set, i.e.,

:   :   $| \mathbf{G} + \mathbf{k} | \lt G\_{\mathrm{cut}}$ with $E\_{\mathrm{cut}} = \frac{\hbar^2}{2m} G^2\_{\mathrm{cut}}$

With this energy cutoff, the number of plane waves included in the basis set depends on the **k**-point, leading to a superior behavior. For instance, for energy-volume calculations the total number of plane waves changes fairly smoothly according to the volume, while the criterion $| \mathbf{G} | \lt G\_{\mathrm{cut}}$ (i.e. same number of plane waves for all **k**-points) would lead to a very rough energy-volume curve and, generally, to a slower energy convergence with respect to the basis set size.

The POTCAR files contain a default ENMAX (and ENMIN). Therefore, it is, in principle, not necessary to specify ENCUT in the INCAR file.
For calculations with more than one species, the maximum cutoff ENMAX (or ENMIN) value is used for the calculation (see PREC).

> **Important:**
>
> * The convergence of the quantity of interest with respect to the energy cutoff ENCUT should always be checked.
> * We strongly recommend specifying the energy cutoff ENCUT always manually in the INCAR file to ensure the same accuracy between calculations. Otherwise, the default ENCUT may differ among the different calculations (e.g., for the calculation of the cohesive energy), with the consequence that the total energies, for instance, can not be compared.

## Related tags and articles

ENMAX,
ENMIN,
ENINI,
ENAUG,
PREC,
NGX,
NGY,
NGZ,
NGXF,
NGYF,
NGZF,
POTCAR

Examples that use this tag
