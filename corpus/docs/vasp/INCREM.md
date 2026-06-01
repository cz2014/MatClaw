# INCREM

Categories: INCAR tag, Advanced molecular-dynamics sampling

INCREM = [real array]  
 Default: **INCREM** = 0

Description: INCREM controls the transformation velocity in the slow-growth approach (in case VASP was compiled with -Dtbdyn).

---

In slow-growth simulations (MDALGO=1 | 2), the value of each controlled geometric parameter with STATUS=0 is increased by INCREM in every simulation step.

It must be supplied for each controlled geometric parameter for which STATUS=0 was specified in the ICONST-file.

## Related tags and articles

MDALGO,
ICONST

Examples that use this tag

---
