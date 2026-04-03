# NTAUPAR

Categories: INCAR tag, Many-body perturbation theory, GW, ACFDT, Performance, Parallelization, Low-scaling GW and RPA, Memory

NTAUPAR = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NTAUPAR** | = depends on MAXMEM | used in low scaling GW and RPA/ACFDT calculations. |

Description: NTAUPAR available as of VASP.6, specifies the number of MPI groups sharing same imaginary time grid points. The default value of NTAUPAR is set to the largest possible value supported on the compute nodes to speed up the GW or RPA calculation.

---

NTAUPAR has the biggest impact on memory usage as well as total runtime for low-scaling GW and RPA calculations. If not found in the INCAR, NTAUPAR is set automatically based on the value of MAXMEM (the available memory for each rank on each compute node), such that the GW and RPA job fits in the RAM on each compute node.

If MAXMEM is not set, VASP looks in "/proc/meminfo" for "MemAvailable" to set MAXMEM internally, otherwise the code uses the value provided in the INCAR.

NTAUPAR=NOMEGA is the maximum value possible, while NTAUPAR=1 is the smallest possible value.

## Related tags and articles

NOMEGAPAR,
NOMEGA

Examples that use this tag

---
