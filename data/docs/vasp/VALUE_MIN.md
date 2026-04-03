# VALUE_MIN

Categories: INCAR tag, Molecular dynamics

VALUE\_MIN = [real array]

Description: VALUE\_MIN sets the lower limits for the monitoring of geometric parameters (in case VASP was compiled with -Dtbdyn).

---

For MDALGO=1 | 2, the geometric parameters defined in the ICONST file may be monitored without being subjected to a constraint or bias potential (STATUS=7 in the ICONST file).

If all values of monitored parameters defined in the ICONST file (STATUS=7) are smaller than VALUE\_MIN or larger than VALUE\_MAX, the simulation terminates.

Upper limits for monitored coordinates, must be supplied for each geometric parameter in the ICONST file with STATUS=7.

## Related tags and articles

VALUE\_MAX,
MDALGO

Examples that use this tag

---
