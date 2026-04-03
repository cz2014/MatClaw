# ANDERSEN_PROB

Categories: INCAR tag, Molecular dynamics, Thermostats

ANDERSEN\_PROB = 0≤[real]≤1  
 Default: **ANDERSEN\_PROB** = 0

Description: ANDERSEN\_PROB sets the collision probability for the Anderson thermostat (in case VASP was compiled with -Dtbdyn).

---

In the approach proposed by Andersen the system is thermally coupled to a fictitious heat bath with the desired temperature. The coupling is represented by stochastic impulsive forces that act occasionally on randomly selected particles. The collision probability is defined as an average number of collisions per atom and time-step. This quantity can be controlled by the flag ANDERSEN\_PROB. The total number of collisions with the heat-bath is written in the file REPORT for each MD step.

> **Tip:** Setting ANDERSEN\_PROB=0, *i.e.*, no collisions with the heat-bath) generates the microcanonical (*NVE*) ensemble.

## Related tags and articles

MDALGO

Examples that use this tag

## References

---
