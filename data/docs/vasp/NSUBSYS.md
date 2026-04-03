# NSUBSYS

Categories: INCAR tag, Molecular dynamics

NSUBSYS = [integer array]

Description: NSUBSYS defines the atomic subsystems in calculations with multiple Anderson thermostats (in case VASP was compiled with -Dtbdyn).

---

Up to three user-defined atomic subsystems may be coupled with independent Andersen thermostats (MDALGO=13).

These subsystems are defined by specifying the last atom for each subsystem (two or three values must be supplied). For instance, if total of 20 atoms is defined in the POSCAR-file, and the initial 10 atoms belong to the subsystem 1, the next 7 atoms to the subsystem 2, and the last 3 atoms to the subsystem 3, NSUBSYS should be defined as follows:

```
NSUBSYS= 10 17 20
```

Note that the last number in the previous example is actually redundant (clearly the last three atoms belong to the last subsystem) and does not have to be user-supplied.

## Related tags and articles

TSUBSYS,
PSUBSYS,
MDALGO

Examples that use this tag

## References

---
