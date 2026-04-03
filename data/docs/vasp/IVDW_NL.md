# IVDW_NL

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

IVDW\_NL = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **IVDW\_NL** | = 1 | for a GGA |
|  | = 2 | for a METAGGA |

Description: IVDW\_NL allows to select the kernel of the nonlocal van der Waals part of a functional (available as of VASP.6.4.0).

---

IVDW\_NL=1 corresponds to the kernel of Dion *et al.* and IVDW\_NL=2 to the kernel rVV10. Note that the kernel of Dion *et al.* contains one adjustable parameter (ZAB\_VDW), while the rVV10 kernel contains two such parameters (BPARAM and CPARAM).

## Related tags and articles

GGA, METAGGA, LUSE\_VDW, ZAB\_VDW, BPARAM, CPARAM, Nonlocal vdW-DF functionals

Examples that use this tag

---
