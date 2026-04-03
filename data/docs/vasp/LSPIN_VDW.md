# LSPIN_VDW

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LSPIN\_VDW = [logical]  
 Default: **LSPIN\_VDW** = .FALSE.

Description: LSPIN\_VDW=.TRUE. switches on the use of the spin-polarized formulation for the nonlocal part of a van der Waals functional (available as of VASP.6.4.0).

---

> **Mind:** LSPIN\_VDW=.TRUE. is possible only for van der Waals functionals that consist of a GGA for the semilocal part and the kernel type of Dion *et al.* (IVDW\_NL=1) for the nonlocal part.

## Related tags and articles

LUSE\_VDW, IVDW\_NL, Nonlocal vdW-DF functionals

## References
