# TEBEG

Categories: INCAR tag, Molecular dynamics

TEBEG = [real]  
 Default: **TEBEG** = 0

Description: TEBEG sets the starting temperature (in K) for an ab-initio molecular dynamics run (IBRION=0) and other routines (e.g. Electron-phonon interactions from Monte-Carlo sampling).

---

If no initial velocities are supplied on the POSCAR file, the velocities are set randomly according to a Maxwell-Boltzmann distribution at the initial temperature TEBEG. Velocities are only used for molecular dynamics (IBRION=0).

**Mind**: If MDALGO>0 is used VASP defines the temperature as

:   $$T= \frac{1}{ k\_B T 3 (N\_{\rm ions}-N\_{\rm constraints})} \sum\limits\_{n}^{N\_{\rm ions}} M\_n | \vec v\_n |^2.$$

This temperature is written to the OUTCAR file.
Depending on the type of thermostat this temperature has to be rescaled to obtain the real simulation temperature.

* Nosé-Hoover thermostat:

In this thermostat the number of degrees of freedom including constraints are already accounted for in the potential energy term. In this this method the center of mass is conserved. This lowers the degrees of freedom by one which is also taken into account in the OUTCAR file.

* Andersen thermostat:

Same as for Nosé-Hoover thermostat.

* Langevin thermostat:

As for the Nosé-Hoover thermostat and Andersen thermostat in this thermostat the number of degrees of freedom including constraints are already accounted for. The center of mass is not conserved in this method, hence this method has 3 degrees of freedom more than the Nosé-Hoover thermostat and the Andersen thermostat.

## Related tags and articles

TEEND,
IBRION,
SMASS

Examples that use this tag

---
