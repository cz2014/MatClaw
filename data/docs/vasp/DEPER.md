# DEPER

Categories: INCAR tag, Electronic minimization

DEPER = [real]  
 Default: **DEPER** = 0.3

Description: DEPER specifies a relative stopping criterion for the optimization of an eigenvalue.

---

The tags DEPER, WEIMIN, and EBREAK allow fine tuning of the iterative matrix diagonalization, and are best not changed. They are optimized for a large variety of systems, and changing one of the parameters usually decreases performance or can even screw up the iterative matrix diagonalization totally.
In general, these tags control when the optimization of a single band is stopped within the iterative matrix diagonalization schemes:

DEPER specifies a relative break-criterion: the optimization of a band is stopped after the energy change becomes smaller than DEPER multiplied with the energy change in the first iterative optimization step. The maximum number of optimization steps is always 4.

## Related tags and articles

WEIMIN,
EBREAK

Examples that use this tag
