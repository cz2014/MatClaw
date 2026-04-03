# ESF_CONV

ESF\_CONV = [real]  
 Default: **ESF\_CONV** = 0.01

Description: Sets the convergence criterion for ESF\_SPLINES, i.e., the threshold for the energy difference between two interpolations (in eV).

---

If the energy between two interpolated k-point grids is less than ESF\_CONV the calculation is considered to be converged. If the threshold has not been reached within ESF\_NINTER iterations VASP will print a warning about insufficient convergence.

## Related tags and articles

ESF\_SPLINES,
ESF\_NINTER,
LOPTICS

Examples that use this tag
