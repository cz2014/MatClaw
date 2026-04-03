# NCORE_IN_IMAGE1

Categories: INCAR tag, Advanced molecular-dynamics sampling, Parallelization

NCORE\_IN\_IMAGE1 = [integer]  
 Default: **NCORE\_IN\_IMAGE1** = 0

Description: This tag specifies the number of cores in the first image.

---

This tag works for two images, specifically, if VCAIMAGES is set (this also sets IMAGES=2).
VCAIMAGES splits the available cores into two groups both working independently in the subdirectories
01 and 02.
The tag NCORE\_IN\_IMAGE1 defines how many of cores are used for the first image (01). The remainder of the cores is used for the second image (working in the subdirectory 02).

## Related tags and articles

VCAIMAGES, IMAGES, SCALEE

---
