# CUTOFF_SIGMA

Categories: INCAR tag, Wannier functions

CUTOFF\_SIGMA = [real] ( [real] )

|  |  |  |
| --- | --- | --- |
| Default: **CUTOFF\_SIGMA** | = 0.1 |  |

Description: CUTOFF\_SIGMA specifies the broadening $\sigma$ in eV for the cutoff function specified by CUTOFF\_TYPE.

---

Corresponds to a broadening of the cutoff function used in the  one-shot method to obtain Wannier functions.
The meaning of $\sigma$ depends on the CUTOFF\_TYPE tag.

For spin-polarized calculations (`ISPIN = 2`), two values can be specified for CUTOFF\_SIGMA, one for each spin channel.
If only a single value is specified, it will be used for both spin channels.

## Related tags and articles

CUTOFF\_TYPE,
CUTOFF\_MU,
LSCDM,
LOCPROJ

Examples that use this tag

---
