# NHC_NS

Categories: INCAR tag, Thermostats

NHC\_NS = [integer] 1 | 3 | 7  
 Default: **NHC\_NS** = 1

Description: The number of subdivisions of each RESPA step used in the integration step used in propagation of thermostat variables in the Nosé-Hoover chain thermostat.

---

The RESPA steps used in in propagation of thermostat variables in the Nosé-Hoover chain thermostat are treated by Suzuki-Yoshida scheme, whereby each step is subdivided further into NHC\_NS parts. First, fourth, and sixth order schemes with, 1, 3, and 7 steps, respectively, are supported.

## Related tags and articles

NHC\_PERIOD, NHC\_NRESPA, Nosé-Hoover chain thermostat

---
