# NWRITE

Categories: INCAR tag, Symmetry, Forces, Ionic minimization, Electronic minimization, Performance

NWRITE = 0 | 1 | 2 | 3 | 4  
 Default: **NWRITE** = 2

Description: This tag determines how much will be written to the file OUTCAR ('verbosity tag').

---

The options for NWRITE are given in detail as

:   :   |  |  |  |  |  |
        | --- | --- | --- | --- | --- |
        | Feature | NWRITE = 0 | NWRITE = 1 | NWRITE = 2 | NWRITE = 3 |
        | Contributions to electronic energy at each electronic iteration | f | f | e | e |
        | Convergence information | f | f | e | e |
        | Eigenvalues | f+l | i | i | e |
        | DOS + charge density | f+l | i | i | e |
        | Total energy and electronic contributions | i | i | i | i |
        | Stress | i | i | i | i |
        | Basis vectors | f+l | i | i | i |
        | Forces | f+l | i | i | i |
        | Lattice and space group information for ISYM>0 | f | f | f | f |
        | Symmetry operations for ISYM>0 |  |  |  | f |
        | Timing information |  |  | X | X |

where the following abbreviations have been used

:   :   |  |  |
        | --- | --- |
        | Code | Meaning |
        | f+l | first and last ionic step |
        | f | first ionic step |
        | i | each ionic step |
        | e | each electronic step |
        | X | when applicable |

> **Tip:** For long molecular-dynamics runs, use `NWRITE = 0` or `NWRITE = 1`. For short runs use `NWRITE = 2`. `NWRITE = 3` might give information if something goes wrong.

> **Important:** `NWRITE = 4` is for debugging only.

## Related tags and articles

OUTCAR, IALGO, IBRION, MDALGO, ISIF, ISYM, EDIFF, EDIFFG, Troubleshooting electronic convergence

Examples that use this tag
