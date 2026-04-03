# NTARGET_STATES

Categories: INCAR tag, Wannier functions, Many-body perturbation theory, Constrained-random-phase approximation

NTARGET\_STATES = [integer array]

Description: Controls which Wannier states are excluded in constrained random phase approximation. Check also NCRPA\_BANDS.

---

This tag is effective for ALGO=CRPA and ignored otherwise.
For instance

```
NTARGET_STATES = 1 2 4
```

selects the Wannier state 1, 2 and 4, where the ordering of the Wannier states depends on the chosen basis set.

### Related tags and articles

ALGO,
NCRPA\_BANDS,
DMFT\_BASIS

Examples that use this tag

---
