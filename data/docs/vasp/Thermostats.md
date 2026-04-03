# Category:Thermostats

Categories: VASP, Molecular dynamics

**Thermostats** are used in molecular-dynamics calculations within the NVT ensemble and NpT ensemble in order to apply a certain temperature to the ionic degrees of freedom.

Choose between stochastic **thermostats**:

* Andersen thermostat
* Langevin thermostat
* CSVR thermostat

and deterministic **thermostats**:

* Nosé-Hoover thermostat
* Nosé-Hoover chain thermostat

> **Mind:** All **thermostats** are available in the NVT ensemble but currently only the Langevin thermostat is available for the NpT ensemble.

The following table gives an overview of the possible combination of ensembles and **thermostats** in VASP:

:   |  |  |  |  |  |  |  |
    | --- | --- | --- | --- | --- | --- | --- |
    |  | Thermostat | | | | | |
    | Ensemble | Andersen | Nosé-Hoover | Langevin | Nosé-Hoover chain | CSVR | Multiple Andersen |
    | Microcanonical (NVE) | MDALGO=1, ANDERSEN\_PROB=0.0 | | | | | |
    | Canonical (NVT) | MDALGO=1 | MDALGO=2 | MDALGO=3 | MDALGO=4 | MDALGO=5 | MDALGO=13 |
    | ISIF=2 | ISIF=2 | ISIF=2 | ISIF=2 | ISIF=2 | ISIF=2 |
    | Isobaric-isothermal (NpT) | not available | not available | MDALGO=3 | not available | not available | not available |
    | ISIF=3 |
    | Isoenthalpic-isobaric (NpH) | MDALGO=3, ISIF=3, LANGEVIN\_GAMMA=LANGEVIN\_GAMMA\_L=0.0 | | | | | |
