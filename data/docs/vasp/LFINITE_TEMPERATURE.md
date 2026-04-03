# LFINITE_TEMPERATURE

Categories: INCAR tag, Many-body perturbation theory, GW, ACFDT, Low-scaling GW and RPA

LFINITE\_TEMPERATURE = [logical]  
 Default: **LFINITE\_TEMPERATURE** = .FALSE.

Description: LFINITE\_TEMPERATURE switches on the finite-temperature formalism of many-body perturbation theory for adiabatic-connection-fluctuation-dissipation-theorem (ACFDT)/GW calculations.

---

This feature is available as of VASP.6.1.0 for ACFDT/random-phase-approximation (RPA), i.e., ALGO=ACFDT, ACFDTR, ACFDTRK, and low-scaling GW calculations, i.e., ALGO=EVGW0R, GWR[K].

For LFINITE\_TEMPERATURE=.TRUE., a compressed Matsubara-frequency grid is used (instead of the zero-temperature formalism of many-body perturbation theory). This allows for GW and RPA calculations for metallic systems.
To this end, the electronic temperature is set with the k-point smearing parameter SIGMA in units of eV, e.g. a value of $\sigma=1 eV$ corresponds to a electronic temperature of $T\approx 11 604 K$.

> **Warning:** Can only be used in combination with Fermi smearing ISMEAR = -1.

## Related tags and articles

NOMEGA,
NOMEGAPAR,
NTAUPAR,
ISMEAR

---
