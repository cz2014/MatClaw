# NVE ensemble

Categories: Molecular dynamics, Ensembles, Thermostats

The NVE ensemble (micro-canonical ensemble) is a statistical ensemble that is used to study material properties under the conditions of a constant particle number N, constant volume V and a conserved internal energy E (up to numerical inaccuracies). This page describes how to sample the NVE ensemble from a molecular-dynamics run.

**Instructions for setting up a NVE ensemble**

There are multiple ways to set up a molecular-dynamics run which samples from the NVE ensemble in VASP. All options have in common that one of the available thermostats is selected but effectively disabled via their respective coupling parameters. The simplest and recommended way is to use the Andersen thermostat and setting the collision probability (ANDERSEN\_PROB) with the fictitious heat bath to zero. Another possibility is to enable the Nosé-Hoover thermostat and select the special value -3 for the mass of the virtual degree of freedom (SMASS). Both presented options will switch the thermostat off, such that the velocities are determined by the Hellmann-Feynman forces or Machine-learned force fields only.
See the following table for the corresponding MDALGO setting and related tags.

| NVE ensemble | Andersen | Nosé-Hoover |
| --- | --- | --- |
| MDALGO | 1 | 2 |
| additional tags to set | `ANDERSEN_PROB = 0.0` | `SMASS = -3` |

The additional tags in the column for every thermostat have to be set to the given values. Otherwise the NVE ensemble will not be realized.

> **Deprecated:** VASP comes with another, older implementation of the Nosé-Hoover thermostat which can be selected with `MDALGO = 0`. However, we recommend `MDALGO = 2` as stated above because the older variant comes with some drawbacks regarding post-processing: the atom coordinates in output files will always be wrapped back into the box if atoms cross the periodic boundaries. This makes it impossible to carry out certain analysis, e.g. computing the mean squared displacement (MSD).

To enforce constant volume throughout the calculation, set `ISIF < 3`. In NVE MD runs there is no control over temperature and pressure, their respective averages depend on the initial structure (lattice, atom positions provided in POSCAR) and initial velocities (either set in POSCAR or via TEBEG). Hence, it is often desirable to equilibrate the system before sampling from the NVE ensemble. This can be achieved in various ways, for example, the system can be thermalized by performing an MD simulation in the NVT ensemble or thermalized and additionally its cell equilibrated via the NpT ensemble. Preparatory steps may also include non-MD algorithms, like structure and volume optimization with `IBRION = 1 or 2` and setting `ISIF > 2`. A general guide for molecular-dynamics simulations can be found on the molecular-dynamics page.

*An example INCAR file for the Andersen thermostat*

```
 #INCAR molecular-dynamics tags NVE ensemble 
 IBRION = 0                   # choose molecular-dynamics 
 MDALGO = 1                   # using Andersen thermostat
 ISIF = 2                     # compute stress tensor but do not change box volume/shape 
 TEBEG = 300                  # set temperature 
 NSW = 10000                  # number of time steps 
 POTIM = 1.0                  # time step in femto seconds 
 ANDERSEN_PROB = 0.0          # setting Andersen collision probability to zero to get NVE enseble
```

> **Mind:** This INCAR file only contains the parameters for the molecular-dynamics part. The electronic minimization or the machine learning tags have to be added.

## Related tags and articles

Molecular-dynamics calculations, ISIF, MDALGO, Ensembles
