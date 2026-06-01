# LANGEVIN_GAMMA_L

Categories: INCAR tag, Molecular dynamics, Thermostats

LANGEVIN\_GAMMA\_L = [Real]  
 Default: **LANGEVIN\_GAMMA\_L** = 0

Description: LANGEVIN\_GAMMA\_L specifies the friction coefficient (in ps-1) for lattice degrees-of-freedom in case of Parrinello-Rahman dynamics (in case VASP was compiled with -Dtbdyn).

---

When running *NpT* simulations with a Langevin thermostat (MDALGO=3), using the method of Parrinello and Rahman, the friction coefficient for lattice degrees-of-freedom have to be specified (in ps-1) by means of the LANGEVIN\_GAMMA\_L-tag.
A fictitious mass for the lattice degrees-of-freedom has to be assigned using the PMASS tag.

The friction coefficients γ for the atomic degrees-of-freedom are specified using the LANGEVIN\_GAMMA-tag.

## Related tags and articles

LANGEVIN\_GAMMA,
PMASS,
MDALGO

Examples that use this tag

## References

---
