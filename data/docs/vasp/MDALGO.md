# MDALGO

Categories: INCAR tag, Molecular dynamics

MDALGO = 0 | 1 | 2 | 3 | 4 | 5 | 11 | 21 | 13  
 Default: **MDALGO** = 0

Description: Specifies the thermostat and lattice dynamics for molecular-dynamics calculations (in case `IBRION = 0`).

---

The algorithm for the thermostat and lattice dynamics is a crucial choise for any molecular-dynamics (MD) calculations (`IBRION = 0`). In combination with the selected lattice degrees of freedom (ISIF), MDALGO determines the ensemble that is sampled during the MD run. The main output file is the REPORT file.

MDALGO can be applied in the context of standard molecular-dynamics calculations, constrained molecular dynamics, metadynamics calculations, the slow-growth approach, monitoring geometric parameters using the ICONST file, biased molecular dynamics, and more.

> **Mind:** `MDALGO >= 0` requires compilation with the precompiler option `-Dtbdyn`. This option is present by default in all makefile.include templates since VASP 5.4.4.

## Options

### `MDALGO = 1`: Andersen thermostat

:   The Andersen thermostat can be used to sample an NVT ensemble or NVE ensemble. It requires setting an appropriate value for ANDERSEN\_PROB. For an NVE ensemble, set `ANDERSEN_PROB = 0.0`. This is usually done after thermalization to a certain target temperature.

:   > **Tip:** Leave the value for TEBEG that was set in the thermalization. For `TEBEG < 0.1`, some part of the code assumes it is used for structure optimization and not an MD run.

### `MDALGO = 2`: Nosé-Hoover thermostat

:   The Nosé-Hoover thermostat is currently only available for the NVT ensemble. It requires setting an appropriate value for SMASS.

:   > **Tip:** The Nosé-Hoover thermostat is a special case of the Nosé-Hoover chain thermostat (`MDALGO = 4` with NHC\_NCHAINS = 1 ). The control tags for `MDALGO = 4` may be more convenient to use than the older implementation (`MDALGO = 2`).

### `MDALGO = 3`: Langevin thermostat

:   The Langevin thermostat is available for sampling the NVT ensemble, NpT ensemble and NpH ensemble. The Langevin dynamics in the NpT ensemble is calculated by the method of Parrinello and Rahman combined with a Langevin thermostat.

    * NVT ensemble: Set an appropriate value for the friction coefficients (LANGEVIN\_GAMMA) for all species in the POSCAR file to enables the Langevin thermostat. Fix the cell shape and volume with `ISIF <= 2`.
    * NpT ensemble: To enable lattice dynamics set `ISIF = 3` and specify a separate set of friction coefficient for the lattice degrees-of-freedom (LANGEVIN\_GAMMA\_L) as well as a ficticious mass for the lattice degrees-of-freedom (PMASS). At the moment, dynamics with *fixed volume+variable shape* (`ISIF = 4`) or *fixed shape+variable volume* (`ISIF = 7`) are not available. Optionally, one may define an external pressure (PSTRESS). Like for the NVT ensemble, set an appropriate value for the friction coefficients (LANGEVIN\_GAMMA) for all species in the POSCAR file to enables the Langevin thermostat.

:   Also see stochastic boundary conditions.

### `MDALGO = 4`: Nosé-Hoover chain thermostat

:   The Nosé-Hoover chain thermostat can be only used to sample an NVT ensemble and requires selecting the number of thermostats in the chain via NHC\_NCHAINS as well as choosing an appropriate setting for the thermostat parameter NHC\_PERIOD.

### `MDALGO = 5`: Canonical sampling through velocity-rescaling (CSVR thermostat)

:   > **Mind:** This option is available as of VASP 6.4.3.

:   The CSVR thermostat can be used to sample an NVT ensemble. It requires setting CSVR\_PERIOD.

### `MDALGO = 13`: Multiple Andersen thermostats

:   Up to three user-defined atomic subsystems may be coupled with independent Andersen thermostats (`MDALGO = 1`). The POSCAR file must be organized such that the positions of atoms of subsystem *i+1* are defined after those for the subsystem *i*, and the following tags must be set: NSUBSYS, TSUBSYS, and PSUBSYS.

### `MDALGO = 0` (deprecated)

:   Selects a Nosé-Hoover thermostat which allows sampling the NVT ensemble at temperature TEBEG. The Nosé-Hoover thermostat requires an appropriate setting for SMASS. To sample an NVE ensemble set `SMASS = -3`.

:   > **Deprecated:** If possible, we recommend using one of the newer Nosé-Hoover thermostat implementations VASP provides (`MDALGO = 2 or 4`). While the results (ensemble averages) should be identical ,this variant comes with some drawbacks regarding post-processing: the atom coordinates in output files will always be wrapped back into the box if atoms cross the periodic boundaries. This makes it impossible to carry out certain analysis, e.g., computing the mean squared displacement (MSD).

### `MDALGO = 11` (deprecated)

:   For VASP 5.x MDALGO = 11  selects the Andersen thermostat. This is replaced by `MDALGO = 1`.

### `MDALGO = 21` (deprecated)

:   For VASP 5.x it selects the Nosé-Hoover thermostat. This is replaced by `MDALGO = 2`.

## Related tags and articles

:   :   :   |  |  |
            | --- | --- |
            | thermostats | related INCAR tag |
            | Langevin thermostat and dynamics | LANGEVIN\_GAMMA, LANGEVIN\_GAMMA\_L, PMASS, PSTRESS |
            | Andersen thermostat | ANDERSEN\_PROB |
            | Multiple Andersen thermostats | NSUBSYS, TSUBSYS, PSUBSYS |
            | Nosé-Hoover thermostat | SMASS |
            | Nosé-Hoover chain thermostat | NHC\_NCHAINS, NHC\_PERIOD, NHC\_NRESPA, NHC\_NS |
            | CSVR thermostat | CSVR\_PERIOD |

General MD-related tags: IBRION, NSW, POTIM, ISIF, RANDOM\_SEED

MD output: REPORT

Workflows that use this tag

## References
