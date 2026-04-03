# NCRPA_BANDS

Categories: INCAR tag, Many-body perturbation theory, Constrained-random-phase approximation

NCRPA\_BANDS = [integer array]

Description: Controls which bands are excluded in the constrained random phase approximation. Check also NTARGET\_STATES.

---

This tag is effective for ALGO=CRPA and ignored otherwise.

For instance

```
NCRPA_BANDS = 21 22 23
```

removes all screening effects between bands 21, 22 and 23 in the random phase approximation of the screened Coulomb interaction.

### Related tags and articles

ALGO,
NTARGET\_STATES

Examples that use this tag

---
