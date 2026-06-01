# NOMEGAR

Categories: INCAR tag, GW, ACFDT

NOMEGAR = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NOMEGAR** | = NOMEGA | for GW calculations |
|  | = 0 | for ACFDT calculations |

Description: NOMEGAR specifies the number of frequency grid points along the real axis.

---

Usually NOMEGAR equals NOMEGA. If NOMEGAR is smaller than NOMEGA (for instance 0), frequencies along the imaginary time axis are included (this feature is currently not fully supported).

## Related tags and articles

NOMEGA

Examples that use this tag

---
