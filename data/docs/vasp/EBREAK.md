# EBREAK

Categories: INCAR tag, Electronic minimization

EBREAK = [real]  
 Default: **EBREAK** = EDIFF/NBANDS/4

Description: EBREAK specifies an absolute stopping criterion for the optimization of an eigenvalue.

---

The tags EBREAK, DEPER, and WEIMIN allow fine tuning of the iterative matrix diagonalization, and are best not changed. They are optimized for a large variety of systems, and changing one of the parameters usually decreases performance or can even screw up the iterative matrix diagonalization totally.
In general, these tags control when the optimization of a single band is stopped within the iterative matrix diagonalization schemes:

EBREAK determines whether a band is fully converged or not. Optimization of an eigenvalue/eigenvectors pair is stopped if the change in the eigenenergy is smaller than EBREAK.

## Related tags and articles

WEIMIN,
DEPER

Examples that use this tag

---
