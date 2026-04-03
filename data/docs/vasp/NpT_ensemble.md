# NpT ensemble

Categories: Molecular dynamics, Ensembles, Thermostats

The NpT ensemble (isothermal-isobaric ensemble) is a statistical ensemble that is used to study material properties under the conditions of a constant particle number N, a pressure p fluctuating around an equilibrium value $\langle p \rangle$ and a temperature T fluctuating around an equilibrium value $\langle T \rangle$. This page describes how to sample the NpT ensemble from a molecular-dynamics run.

**Instructions for setting up an NpT ensemble**

The Parinello-Rahman algorithm is the method of choice when setting up an NpT molecular-dynamics run. To use the Parinello-Rahman algorithm the Langevin thermostat has
to be adjusted for an NpT simulation by setting the ISIF=3 in the INCAR file. Otherwise, the lattice is not allowed to change during the simulation, preventing VASP from keeping the pressure constant.
Additionally the user can set LANGEVIN\_GAMMA as when simulating a NVT ensemble,
the tag LANGEVIN\_GAMMA\_L which is a friction coefficient for
the lattice degrees of freedom and the PMASS tag to assign a fictitious mass to the lattice
degrees of freedom.

| NpT ensemble | Langevin |
| --- | --- |
| MDALGO | 3 |
| ISIF | 3 |
| additional tags to set | LANGEVIN\_GAMMA, LANGEVIN\_GAMMA\_L |
| optional tags to set | PMASS |

The additional tags in the column for the thermostat have to be set because the default
values are zero resulting in a different ensemble. To use the NpT ensemble VASP has to be compiled with the precompiler flag -Dtbdyn. A general guide for molecular-dynamics simulations can be found on the molecular-dynamics page.

*An example INCAR file for the NpT ensemble*

```
 #INCAR molecular-dynamics tags NpT ensemble 
 IBRION = 0                      # choose molecular-dynamics 
 MDALGO = 3                      # using Langevin thermostat
 ISIF = 3                        # compute stress tensor and change box volume/shape 
 TEBEG = 300                     # set temperature 
 NSW = 10000                     # number of time steps 
 POTIM = 1.0                     # time step in femto seconds 
 LANGEVIN_GAMMA = 10.0 10.0 10.0 # Langevin friction coefficient for three atomic species
 LANGEVIN_GAMMA_L = 10.0         # Langevin friction coefficient for lattice degrees of freedom
 PMASS = 1000                    # the fictitious mass of the lattice degrees of freedom
```

> **Mind:** This INCAR file only contains the parameters for the molecular-dynamics part. The electronic minimization or the machine learning tags have to be added.

> **Warning:** Calculations of systems with limited long-range order (e.g. liquids) may lead to irreversible deformations of the cell within this ensemble. For those systems one must use an ICONST file containing constraints for the Bravais lattice.

## Related tags and articles

Molecular-dynamics calculations, ISIF, MDALGO, LANGEVIN\_GAMMA, LANGEVIN\_GAMMA\_L, PMASS, Ensembles, ICONST

## References
