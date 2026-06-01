# LUSE_VDW

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LUSE\_VDW = [logical]  
 Default: **LUSE\_VDW** = .FALSE.

Description: LUSE\_VDW=.TRUE. switches on the use of a nonlocal vdW-DF functional. These functionals depend on the electron density at two points in space and model long-range van der Waals (dispersion) correlation effects.

---

> **Mind:** In versions of VASP prior to 6.4.0, a meta-GGA functional (e.g., SCAN) could be combined only with the rVV10 nonlocal functional. Conversely, a GGA functional could be combined only with the original nonlocal functional of Dion *et al.*. This restriction is lifted since VASP.6.4.0 thanks to the introduction of the IVDW\_NL tag.

## Related tags and articles

GGA, METAGGA, IVDW\_NL, LSPIN\_VDW, Nonlocal vdW-DF functionals

Examples that use this tag

---
