# FMP_PERIOD

Categories: INCAR tag, Molecular dynamics, Ensemble properties

FMP\_PERIOD = integer  
 Default: **FMP\_PERIOD** = 10

Description: Number of time steps between two swapping events in the Müller-Plathe method.

---

This tag defines how many MD steps are done between two consecutive velocity-swapping events. The period is counted in MD steps and not in simulation time.

> **Mind:** This tag will only be available from VASP 6.4.4

## Related tags and articles

Müller-Plathe method,
FMP\_ACTIVE,
FMP\_DIRECTION,
FMP\_SNUMBER,
FMP\_SWAPNUM
