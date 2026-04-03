# QMAXFOCKAE

Categories: INCAR tag, Projector-augmented-wave method

QMAXFOCKAE = [real array]

Description: Controls at which wave vectors the local augmentation
charges are fitted to obtain an accurate charge augmentation on the plane-wave grid.

---

We do not recommend setting these tags manually, except after careful inspection of the VASP code (fast\_aug.F). The default values are 6.0 Å-1
if NMAXFOCKAE=1 (corresponding to 140 eV), and 5.0 and 10 Å-1 (corresponding to 95 eV and 380 eV) for NMAXFOCKAE=2.

## Related tags and articles

NMAXFOCKAE,
LMAXFOCKAE, LFOCKAEDFT

Examples that use this tag
