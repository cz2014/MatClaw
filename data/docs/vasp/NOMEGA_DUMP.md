# NOMEGA_DUMP

Categories: INCAR tag, Many-body perturbation theory, GW, Low-scaling GW and RPA, Constrained-random-phase approximation, Bethe-Salpeter equations

NOMEGA\_DUMP = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NOMEGA\_DUMP** | = -1 |  |

> **Warning:** Available as of version 6.3.2.

Description: NOMEGA\_DUMP selects the imaginary frequency point of screened potential in low-scaling GW calculations that is written to file.

> **Mind:** This tag can be used to obtain WFULLxxxx.tmp for BSE calculations.

---

NOMEGA\_DUMP selects the imaginary frequency point of the screened Coulomb kernel that is written to WFULLxxxx.tmp in low-scaling GW calculations.
If set to 0, WFULLxxxx.tmp contains the screened Coulomb interaction W at $\omega=0$.
For positive values, these files contain the screened Coulomb interaction at the corresponding imaginary frequency point.
For negative values, WFULLxxxx.tmp is not written.

## Related tags and articles

ALGO,
NOMEGA

Examples that use this tag

---
