# NHC_NCHAINS

Categories: INCAR tag, Thermostats

NHC\_NCHAINS = [integer]  
 Default: **NHC\_NCHAINS** = 0

Description: Length of the Nosé-Hoover chain.

---

NHC\_NCHAINS sets the length of the chain for the Nosé-Hoover chain thermostat. Typically, this tag is set to a value between 1 and 5. The maximal allowed value is 20.

In case NHC\_NCHAINS=0, the thermostat is switched off and the underlying dynamics generate a microcanonical (NVE) ensemble. NHC\_NCHAINS=1 corresponds to the standard Nosé-Hoover thermostat.

## Related tags and articles

NHC\_PERIOD, Nosé-Hoover chain thermostat

---
