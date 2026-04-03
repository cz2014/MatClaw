# CSVR_PERIOD

Categories: Molecular dynamics, Thermostats

CSVR\_PERIOD = [real]  
 Default: **CSVR\_PERIOD** = 0

Description: Time scale of the CSVR thermostat in terms of the number of MD steps.

---

CSVR\_PERIOD sets the time scale ($\tau$) of the CSVR thermostat. It is expressed in terms of the number of MD steps and must be interpreted in combination with the time step set by POTIM. Typically, CSVR\_PERIOD should take the values corresponding to 2-2000 fs, whereby the smaller the value, the more aggressive the thermostating. The special setting CSVR\_PERIOD=0 generates the NVE ensemble.

## Related tags and articles

POTIM, CSVR thermostat

---
