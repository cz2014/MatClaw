# PARAM2

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

PARAM2 = [real]  
 Default: **PARAM2** = 1.0

Description: $\kappa$ for GGA=MK, or $\mu$ for GGA=BO.

---

The PARAM2 tag determines the value corresponding to different parameters depending on the GGA functional that is chosen:

* $\kappa$ in the optB86b ($\kappa$ is not shown in this work since implicitly set to 1.0), B86R, and DF3-opt2 exchange functionals, which have the same analytical form and correspond to GGA=MK. PARAM2 should in principle be set to 1.0 for the nonlocal optB86b-vdW functional, to 0.711357 for the nonlocal rev-vdW-DF2 functional, or to $0.58$ for the vdW-DF3-opt2 nonlocal functional.
* $\mu$ in the optB88 and DF3-opt1 exchange functionals, which have the same analytical form and correspond to GGA=BO. PARAM2 should in principle be set to 0.22 for the nonlocal optB88-vdW functional or to $10/81\approx0.1234568$ for the vdW-DF3-opt1 nonlocal functional.

The complete INCAR file for the nonlocal van der Waals functionals mentioned above can be found at Nonlocal vdW-DF functionals.

## Related tags and articles

PARAM1, GGA, Nonlocal vdW-DF functionals

Examples that use this tag

## References
