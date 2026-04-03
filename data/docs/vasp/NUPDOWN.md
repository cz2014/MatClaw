# NUPDOWN

Categories: INCAR tag, Magnetism

NUPDOWN = [positive real]  
 Default: **NUPDOWN** = not set

Description: Sets the difference between the number of electrons in the up and down spin components.

---

Allows calculations for a specific spin multiplet, i.e. the difference of the number of electrons in the up and down spin component will be kept fixed to the specified value. There is a word of caution required: If NUPDOWN is set in the INCAR file the initial moment for the charge density should be the same. Otherwise convergence can slow down. When starting from atomic charge densities (ICHARG=2), VASP will try to do this automatically by setting MAGMOM to NUPDOWN/NIONS. The user can of course overwrite this default by specifying a different MAGMOM (which should still result in the correct total moment). If one initializes the charge density from the one-electron wavefunctions, the initial moment is always correct, because VASP "pushes" the required number of electrons from the down to the up component. Initializing the charge density from the CHGCAR file (ICHARG=1), however, the initial moment is usually incorrect!

If no value is set (or NUPDOWN=-1) a full relaxation will be performed. This is also the default.

## Related tags and articles

MAGMOM,ICHARG

Examples that use this tag

---
