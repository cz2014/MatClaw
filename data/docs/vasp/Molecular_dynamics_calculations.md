# Molecular-dynamics calculations

Categories: Molecular dynamics, Howto

To run a basic molecular dynamics calculation perform the following steps:

* Choose a POSCAR containing a large enough super cell.
* If a continuation run is performed copy CONTCAR to POSCAR or possibly deliver initial velocities in the POSCAR file. They are written after the Wycoff positions in an own paragraph. If no initial velocities are provided random velocities are assumed at the beginning of the calculation. This is fully ok but the user should be aware that due to the initial random velocities the trajectories obtained from different calculations are difficult to compare.
* Set main INCAR tags:
  + IBRION=0: Molecular dynamics calculations are enabled by setting the IBRION tag to 0.
  + POTIM: This tag sets the time step in fs for the molecular dynamics run.
  + NSW: This tag sets the number of steps performed in the molecular dynamics run.
  + TEBEG: If a thermostat is used define the desired temperature at which the molecular dynamics calculations should run.
  + ISIF (optional).
  + MDALGO: This tag decides with which thermostat the molecular dynamics calculation is executed. For regular molecular dynamics calculations the thermostat is selected by a one digit number (e.g. 1 for Andersen, 2 for Nosé-Hoover etc.). For biased molecular dynamics, metadynamics etc. the thermostat is selected the same way from VASP 6 or higher. In VASP 5.x it is selected by a two digit number where the first digit corresponds to the thermostat analogously to regular molecular dynamics and the second digit corresponds to the molecular dynamics type (e.g. 11 metadynamics with Andersen thermostat, 21 metadynamics with Nosé-Hoover thermostat etc.). The NVE ensemble is a special case. It is available by selecting the Andersen thermostat and setting no collisions with the heat bath (ANDERSEN\_PROB=0).
  + ISIF: In molecular dynamics calculations this tag is used to choose the NVT ensemble or NpT ensemble (the NVE ensemble is a special case!). For ISIF=2 the volume is kept constant and the NVT ensemble is used. Using this tag the stress tensor is calculated and hence the pressure can be monitored. For ISIF=3 the stress tensor (pressure) is kept constant and the NpT ensemble is used. Using this tag the volume is calculated and can be monitored.
* Decide which ensemble to use:
  + NVT ensemble: Set ISIF=2.
  + NpT ensemble: Set ISIF=3.
  + NVE ensemble: Set MDALGO=1 and ANDERSEN\_PROB=0.0.
* Decide which thermostat to use (the combination of thermostats and ensembles is given in table):
  + Andersen thermostat: Set MDALGO=1. Also set ANDERSEN\_PROB>0.0 to control the stochastic update frequency of the thermostat.
  + Nosé-Hoover thermostat: Set MDALGO=2. Also set SMASS>0.0 to control the coupling to the heat bath.
  + Langevin thermostat: Set MDALGO=3. Also set LANGEVIN\_GAMMA>0.0 to control the friction parameter. If the NpT ensemble is used (by setting ISIF=3) additionally the friction coefficient of the lattice LANGEVIN\_GAMMA\_L has to be provided too.
  + Nosé-Hoover chain thermostat: Set MDALGO=4. Also set the NHC\_NCHAINS>0 to adjust the length of the Nosé-Hoover chain. With NHC\_PERIOD the period (coupling strength to the heat bath) of the Nosé-Hoover chains thermostat is set.
  + CSVR thermostat: Set MDALGO=5 and additionally adjust CSVR\_PERIOD>0.

The following combinations of thermostats and barostats is possible:

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

## Compilation

Many of the simulation methods described in this section are included in VASP as of version 5.2.12, and require VASP to be compiled with the preprocessor flag `-Dtbdyn`. This is usually the case because all makefile.include templates shipped with VASP since version 5.4.4 contain this flag by default.

---
