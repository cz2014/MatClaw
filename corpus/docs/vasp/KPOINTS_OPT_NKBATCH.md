# KPOINTS_OPT_NKBATCH

Categories: VASP, INCAR tag, Memory

KPOINTS\_OPT\_NKBATCH = [integer]

Default: KPOINTS\_OPT\_NKBATCH = Number of k-points in the irreducible Brillouin zone of the self-consistent calculation.

Description: KPOINTS\_OPT\_NKBATCH determines the size of the batch of k-points for the KPOINTS\_OPT driver.

---

When the KPOINTS\_OPT is present an additional non-self-consistent calculation is performed after self-consistency is reached.
This one-shot calculation is done in batches of N k-points to reduce memory usage.
Increasing the size of the batch leads to faster calculation times but higher memory usage in the non-self-consistent calculation.

## Related tags and articles

LKPOINTS\_OPT, KPOINTS\_OPT, PROCAR\_OPT

Examples that use this tag

---
