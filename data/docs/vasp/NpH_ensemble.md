# NpH ensemble

Categories: Molecular dynamics, Ensembles, Thermostats

The NpH ensemble (isoenthalpic–isobaric ensemble) is a statistical ensemble that is used to study material properties under the conditions of a constant particle number N, a pressure p fluctuating around an equilibrium pressure $\langle p \rangle$ and a conserved enthalpy H (up to numerical inaccuracies). This page describes how to sample the NpH ensemble from a molecular-dynamics run.

**Instructions for setting up a NpH ensemble**

To run an NpH molecular-dynamics simulation `MDALGO = 3` has to be used. The LANGEVIN\_GAMMA and LANGEVIN\_GAMMA\_L have to be zero to disable any thermostatting. By setting the tag `LANGEVIN_GAMMA = 0` the friction term and
the stochastic term of the Langevin thermostat will be zero, such that the velocities are determined by the Hellmann-Feynman forces or machine-learned force fields only. Setting the tag `LANGEVIN_GAMMA_L = 0`,
removes the stochastic term and the friction term from the barostat, resulting in a box update
depending solely on the kinetic stress tensor. The inertia of lattice degrees-of-freedom is controlled with the PMASS tag.

| NpH ensemble | Langevin |
| --- | --- |
| MDALGO | 3 |
| ISIF | 3 |
| LANGEVIN\_GAMMA\_L | 0 |
| LANGEVIN\_GAMMA | 0 |
| optional tags to set | PMASS |

It is recommended to equilibrate the system of interest with an NPT molecular-dynamics run before starting the NpH run. A general guide for molecular-dynamics simulations can be found on the molecular-dynamics page.

*An example INCAR file for the NpH ensemble*

```
 #INCAR molecular-dynamics tags NpH ensemble 
 IBRION = 0                   # choose molecular-dynamics 
 MDALGO = 3                   # using Langevin thermostat
 ISIF = 3                     # compute stress tensor and allow change of box volume/shape 
 TEBEG = 300                  # set temperature 
 NSW = 10000                  # number of time steps 
 POTIM = 1.0                  # time step in femto seconds 
 LANGEVIN_GAMMA = 0.0 0.0     # setting friction and stochastic term of Langevin thermostat zero
 LANGEVIN_GAMMA_L = 0.0       # setting friction and stochastic term of Langevin barostat zero
```

> **Mind:** This INCAR file only contains the parameters for the molecular-dynamics part. The electronic minimization or the machine learning tags have to be added.

## Related tags and articles

Molecular-dynamics calculations, ISIF, MDALGO, LANGEVIN\_GAMMA, LANGEVIN\_GAMMA\_L, Ensembles
