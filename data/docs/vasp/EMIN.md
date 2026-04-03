# EMIN

Categories: INCAR tag, Density of states

EMIN = [real]

|  |  |  |
| --- | --- | --- |
| Default: **EMIN** | = lowest KS eigenvalue - $\Delta$ |  |

Description: EMIN specifies the lower boundary of the energy range for the evaluation of the electronic density of states (DOS).

---

The DOS is evaluated each NBLOCK steps, DOSCAR is updated each NBLOCK\*KBLOCK steps.

> **Tip:** Set EMIN to a value larger than EMAX, if you are not sure where the region of interest lies.

## Related tags and articles

EMAX, NEDOS,
DOSCAR

Examples that use this tag
