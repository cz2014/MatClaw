# PARAM1

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

PARAM1 = [real]  
 Default: **PARAM1** = 0.1234

Description: $\mu$ for GGA=MK, $\beta$ for GGA=BO.

---

The PARAM1 tag determines the value corresponding to different parameters depending on the GGA functional that is chosen:

* $\mu$ in the optB86b, B86R, and DF3-opt2 exchange functionals, which have the same analytical form and correspond to GGA=MK. PARAM1 should in principle be set to 0.1234 for the optB86b-vdW nonlocal functional or to $10/81\approx0.1234568$ for the rev-vdW-DF2 and vdW-DF3-opt2 nonlocal functionals.
* $\beta$ in the optB88 exchange functional or $\mu/\kappa$ in the DF3-opt1 exchange functional, which have the same analytical form and correspond to GGA=BO. PARAM1 should in principle be set to $0.22/1.2\approx0.1833333333$ for the optB88-vdW nonlocal functional or to $(10/81)/1.1\approx0.1122334456$ for the vdW-DF3-opt1 nonlocal functional.

The complete INCAR file for the nonlocal van der Waals functionals mentioned above can be found at Nonlocal vdW-DF functionals.

## Related tags and articles

PARAM2, GGA, Nonlocal vdW-DF functionals

Examples that use this tag

## References
