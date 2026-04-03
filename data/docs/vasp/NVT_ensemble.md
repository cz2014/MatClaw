# NVT ensemble

Categories: Molecular dynamics, Ensembles, Thermostats

The NVT ensemble (canonical ensemble) is a statistical ensemble that is used to study material properties under the conditions of a
constant particle number N, constant volume V and a temperature fluctuating around an equilibrium value $\langle T \rangle$.
This page describes how to sample the NVT ensemble from a molecular-dynamics run.

**Instructions for setting up an NVT ensemble**

There are multiple choices of thermostats to control the temperature for the NVT ensemble:
The stochastic Andersen thermostat, Langevin thermostat and CSVR thermostat, as well as
the deterministic Nosé-Hoover thermostat, Nosé-Hoover chain thermostat and Multiple Andersen thermostats can be used.
See table for the corresponding MDALGO setting and related tags.

| NVT ensemble | Nosé-Hoover | Andersen | Nosé-Hoover | Langevin | Nosé-Hoover chain | CSVR | Multiple Andersen |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MDALGO | 0 | 1 | 2 | 3 | 4 | 5 | 13 |
| additional tags to set | SMASS | ANDERSEN\_PROB | SMASS | LANGEVIN\_GAMMA | NHC\_NCHAINS, NHC\_PERIOD, NHC\_NRESPA, NHC\_NS | CSVR\_PERIOD | NSUBSYS, TSUBSYS, PSUBSYS |

The additional tags in the column for every thermostat have to be set. For example, the Nosé-Hoover thermostat needs the additional SMASS tag. To enforce constant volume throughout the calculation, set `ISIF < 3`. In NVT MD runs there is no control over pressure because the volume is fixed. The average value will therefore depend on the initial lattice given in the POSCAR file. It is often desirable to equilibrate the lattice degrees of freedom, for example, by running an NpT simulation or by performing structure and volume optimization with `IBRION = 1 or 2` and setting `ISIF > 2`. A general guide for molecular-dynamics simulations can be found on the molecular-dynamics page.

*Example INCAR file for the Nosé-Hoover thermostat*

```
 #INCAR molecular-dynamics tags NVT ensemble 
 IBRION = 0                   # choose molecular dynamics 
 MDALGO = 2                   # use Nosé-Hoover thermostat 
 ISIF = 2                     # compute stress tensor but do not change box volume/shape 
 TEBEG = 300                  # set temperature 
 NSW = 10000                  # number of time steps 
 POTIM = 1.0                  # time step in femto seconds 
 SMASS = 1.0                  # setting the virtual mass for the Nosé-Hoover thermostat
```

> **Mind:** This INCAR file only contains the parameters for the molecular-dynamics part. The electronic minimization or the machine learning tags have to be added.

## Related tags and articles

Molecular-dynamics calculations, ISIF, MDALGO, LANGEVIN\_GAMMA, SMASS,ANDERSEN\_PROB, NSUBSYS, TSUBSYS, PSUBSYS

## Footnotes and references
