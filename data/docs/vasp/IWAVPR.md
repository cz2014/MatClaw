# IWAVPR

Categories: INCAR tag, Ionic minimization, Molecular dynamics

IWAVPR = 0 | 1 | 2 | 3 | 10 | 11 | 12 | 13

|  |  |  |
| --- | --- | --- |
| Default: **IWAVPR** | = 12 | if IBRION=0 (MD) and 11 (relaxation, on-the-fly machine learning MD) |
|  | = 0 | else (static calculation) |

Description: IWAVPR determines how orbitals and/or charge densities
are extrapolated from one ionic configuration to the next configuration.

---

For IWAVPR<10, the file TMPCAR is used to store old orbitals that
are required for the prediction. This setting is depreciated, and not supported by the MPI version.
The recommended settings are IWAVPR>10. In this case, the prediction is
performed without an external file TMPCAR (i.e. all required arrays
are stored in the main memory).

The following options are available for IWAVPR:

* IWAVPR=0 no extrapolation, usually not preferable for first-principles molecular dynamics simulations or relaxations of the ions into the groundstate.
* IWAVPR=1|11 Simple extrapolation of the charge density using atomic charge densities (eq. (9.8) in thesis G. Kresse). This switch is convenient for geometry optimizations (ionic relaxation and volume/cell shape with the conjugate gradient or Quasi-Newton methods, i.e. IBRION=1,2,3 etc.)
* IWAVPR=2|12 A second-order extrapolation for the orbitals and the charge density (eq. (9.9) in thesis G. Kresse) is performed. This results in superior performance for first-principles molecular-dynamics simulations. It might cause instabilities during on-the-fly learning, so the default is 11 in this case.

* IWAVPR=3|13 In this case a second-order extrapolation for the orbitals, and a simple extrapolation of the charge density using atomic charge densities is done. This is a mixture between IWAVPR=1 and 2, however, it is usually worse than IWAVPR=2.

:   Mind: We don't encourage this setting.

## Related tags and articles

IBRION

Examples that use this tag

---
