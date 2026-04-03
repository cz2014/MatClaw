# NHC_NRESPA

Categories: INCAR tag, Thermostats

NHC\_NRESPA = [integer]  
 Default: **NHC\_NRESPA** = 1

Description: The number of subdivisions of the integration step used in propagation of thermostat variables in the Nosé-Hoover chain thermostat.

---

NHC\_NRESPA sets the number of subdivisions of the integration step used in propagation of thermostat variables in the [[Nosé-Hoover chain thermostat. This might be needed in accurate calculations where, due to rapidly varying terms appearing in thermostat variables propagators could cause significant drifts of total energy (including energy contributions due to thermostat), which is a conserved quantity.

## Related tags and articles

NHC\_PERIOD, NHC\_NS, Nosé-Hoover chain thermostat

---
