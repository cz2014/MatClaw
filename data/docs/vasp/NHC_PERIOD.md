# NHC_PERIOD

Categories: Molecular dynamics, Thermostats

NHC\_PERIOD = [real]  
 Default: **NHC\_PERIOD** = 40

Description: Time scale of the Nosé-Hoover chain in terms of the number of MD steps.

---

NHC\_PERIOD sets the time scale ($\tau$) of the Nosé-Hoover chain thermostat. It is expressed in terms of the number of MD steps and must be interpreted in combination with the time step set by POTIM. The setting NHC\_PERIOD=0 corresponds will generate the NVE ensemble.

> **Tip:** The value of NHC\_PERIOD should correspond to a characteristic time scale in the system. If this is unknown, NHC\_PERIOD should be set to a value between 20 and 200.

## Related tags and articles

POTIM, NHC\_NCHAINS, Nosé-Hoover chain thermostat

---
