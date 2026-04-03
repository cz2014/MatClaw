# KPAR

Categories: INCAR tag, Performance, Parallelization, MP2

KPAR = [integer]  
 Default: **KPAR** = 1

Description: KPAR determines the number of **k**-points that are to be treated in parallel (available as of VASP.5.3.2). Also, KPAR is used as parallelization tag for Laplace transformed MP2 calculations.

---

VASP currently offers parallelization and data distribution over bands and/or over plane wave coefficients (see NCORE and NPAR), and as of VASP.5.3.2, parallelization over **k**-points.
To obtain high efficiency on massively parallel systems or modern multi-core machines, it is strongly recommended to use all at the same time. Most algorithms work with any data distribution (except for the single band conjugated gradient, which is considered to be obsolete).

The set of **k**-points is distributed over KPAR groups of compute cores, in a round-robin fashion.
This means that a group of *N*=(# of cores/KPAR) compute cores together work on an individual **k**-point (choose KPAR such that it is an integer divisor of the total number of cores).
Within this group of *N* cores that share the work on an individual **k**-point, the usual parallelism over bands and/or plane wave coefficients applies (as set by means of the NCORE and NPAR tags).

This is especially powerful for reducing MPI communication. In electronic minimizations, MPI communication mainly occurs between ranks working on the same **k**-point. Hence, dividing ranks into groups that each handle separate **k**-points greatly reduces MPI communication. This is particularly important for the blocked-Davidson algorithm ALGO=Normal, and less so for ALGO=Fast or ALGO=VeryFast.

For example, if your calculation has 16 **k**-points and you are using 16 MPI ranks in total, setting KPAR=16 minimizes MPI communication to an absolute minimum. Hence, try to assign each physical node its own group of **k**-points; ideally also each NUMA domain.

**Note**: the data is not distributed additionally over **k**-points.

**Note**: KPAR becomes obsolete if LMP2LT or LSMP2LT are set and specifies the number of plane-waves treated in parallel, see here for more information.

## Related tags and articles

NCORE,
NPAR,
LPLANE,
LSCALU,
NSIM,
LSCALAPACK,
LSCAAWARE,
LSMP2LT,
LMP2LT

Examples that use this tag

---
