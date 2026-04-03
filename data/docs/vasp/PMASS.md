# PMASS

Categories: INCAR tag, Molecular dynamics

PMASS = [Real]  
 Default: **PMASS** = 1000

Description: PMASS assigns a fictitious mass (in amu) to the lattice degrees-of-freedom in case of Parrinello-Rahman dynamics (in case VASP was compiled with -Dtbdyn).

---

When running *NpT* simulations with a Langevin thermostat (MDALGO=3), using the method of Parrinello and Rahman, a fictitious mass (in amu) for the lattice degrees-of-freedom has to be assigned using the PMASS tag.
The friction coefficient for lattice degrees-of-freedom have to be specified (in ps-1) by means of the LANGEVIN\_GAMMA\_L tag.

The friction coefficients γ for the atomic degrees-of-freedom are specified using the LANGEVIN\_GAMMA tag.

The optimal setting for PMASS depends very much on the particular system at hand and can be considered as a compromise between two opposing factors: too large values lead to very slow variation of lattice degrees of freedom (and hence the sampling becomes inefficient) while too small value can lead to too large geometric changes in an MD step and hence may cause numerical problems. We strongly recommend to make careful tests with various settings before performing the production run.

## Related tags and articles

LANGEVIN\_GAMMA\_L,
LANGEVIN\_GAMMA,
MDALGO

## References

Examples that use this tag

---
