# DMFT_BASIS

Categories: Wannier functions, Many-body perturbation theory, Constrained-random-phase approximation

DMFT\_BASIS = MLWF | BLOCH | LOCPROJ

Description: Specifies which basis is used for Coulomb matrix elements in CRPA calculations.

---

This tag is effective for ALGO=CRPA[R] and ALGO=2E4W and is ignored otherwise.
The tag affects how NTARGET\_STATES is interpreted.
For instance

```
DMFT_BASIS = BLOCH
NTARGET_STATES = 1 4 5 8
```

evaluates the Coulomb matrix elements in the Bloch basis for band 1, 4, 5 and 8.

In contrast,

```
DMFT_BASIS = MLWF
NTARGET_STATES = 1 4 5 8
```

evaluates the Coulomb matrix elements in the Wannier basis for the states 1, 4, 5 and 8 defined in the INCAR file or read from the WANPROJ file.

### Related tags and articles

ALGO,
NCRPA\_BANDS,
NTARGET\_STATES,
LOCPROJ,
VIJKL,
UIJKL,
VRijkl,
URijkl

Examples that use this tag

---
