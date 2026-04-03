# PSUBSYS

Categories: INCAR tag, Molecular dynamics

PSUBSYS = [real array]

Description: PSUBSYS sets the collision probabilities for the atoms in each atomic subsystem in calculations with multiple Anderson thermostats (in case VASP was compiled with -Dtbdyn).

---

Up to three user-defined atomic subsystems may be coupled with independent Andersen thermostats (MDALGO=13).

The collision probabilities for the atoms in each atomic subsystem is set by means of the PSUBSYS tag (one has to specify one number for each subsystem).

Note: 0 ≤ PSUBSYS ≤ 1

## Related Tags and Sections

NSUBSYS,
TSUBSYS,
MDALGO

Examples that use this tag

## References

---
