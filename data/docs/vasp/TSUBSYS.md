# TSUBSYS

Categories: INCAR tag, Molecular dynamics

TSUBSYS = [real array]

Description: TSUBSYS sets the temperatures for the atomic subsystems in calculations with multiple Anderson thermostats (in case VASP was compiled with -Dtbdyn).

---

Up to three user-defined atomic subsystems may be coupled with independent Andersen thermostats (MDALGO=13).

The simulation temperature for the atomic subsystems is set by means of the TSUBSYS tag (one has to specify one number for each subsystem).

## Related tags and articles

NSUBSYS,
PSUBSYS,
MDALGO

Examples that use this tag

## References

---
