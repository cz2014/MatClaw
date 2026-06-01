# ISIF

Categories: INCAR tag, Ionic minimization, Molecular dynamics, Symmetry

ISIF = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8

|  |  |  |
| --- | --- | --- |
| Default: **ISIF** | = 0 | for `IBRION = 0` (molecular dynamics) or `LHFCALC = .TRUE.` |
|  | = 2 | else |

Description: Determines if the stress tensor is calculated and which ionic degrees of freedom are varied.

---

For ISIF$\ge$2, the stress tensor is calculated. It is defined as the negative of the derivative of the energy
$E$ with respect to the strain tensor $\eta\_{ji}$:

:   $\sigma\_{ij} = - \frac{\delta E} {\delta \eta\_{ji}}$.

This might be different from other first principles codes.
A positive in the diagonals means that the system is under compressive strain and wants to expand. A negative value implies that the system is under tensile strain and wants to reduce its volume. The stress tensor is symmetric $\sigma\_{ij}=\sigma\_{ji}$, and, thus, it has six independent entries.
The calculation of the stress tensor is relatively time-consuming, and, therefore, by default, it is switched off in some cases. The forces are always calculated.

> **Tip:** You can get information about the stress at each ionic step using `NWRITE = 0,1,2,3`.

ISIF also determines which degrees of freedom (ionic positions, cell volume, and cell shape) of the structure are allowed to change.

:   |  |  |  |  |  |  |
    | --- | --- | --- | --- | --- | --- |
    | ISIF | calculate | | degrees-of-freedom | | |
    |  | forces | stress tensor | positions | cell shape | cell volume |
    | 0 | yes | no | yes | no | no |
    | 1 | yes | trace only | yes | no | no |
    | 2 | yes | yes | yes | no | no |
    | 3 | yes | yes | yes | yes | yes |
    | 4 | yes | yes | yes | yes | no |
    | 5 | yes | yes | no | yes | no |
    | 6 | yes | yes | no | yes | yes |
    | 7 | yes | yes | no | no | yes |
    | 8 | yes | yes | yes | no | yes |

* For `ISIF = 1`, only the trace of the stress tensor is calculated. This means only the total pressure is correct and can be read off in the line:

```
external pressure =      ... kB
```

:   The individual components of the stress tensor are not reliable in this case and must be disregarded.

* Accuracy

:   > **Warning:** The PAW basis for the electronic minimization is not adjusted when the structure is varied during a calculation.

:   Therefore, carefully consider effects such as Pulay stress and choose generous settings for the electronic minimization. Generally, volume changes should be done only with an increased energy cutoff, e.g., `ENCUT = 1.3×max(ENMAX)`, and `PREC = High`.

* To further control the ionic degrees of freedom that can vary during the calculation, set `Selective dynamics` in the POSCAR file.
* `ISIF = 8` is only available as of VASP.6.4.1.

## Related tags and articles

IBRION,
structure optimization,
 Ensembles,
NWRITE,
Selective-dynamics mode of the POSCAR file,
LATTICE\_CONSTRAINTS

Examples that use this tag

---
