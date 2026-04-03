# HFSCREEN

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

HFSCREEN = [real]  
 Default: **HFSCREEN** = 0 (none)

Description: HFSCREEN (in Å-1) specifies the range-separation parameter in range-separated hybrid functionals.

---

If LHFCALC=.TRUE. and GGA=PE (PBE functional), attributing a value to HFSCREEN will switch from the PBE0 functional to, e.g., the closely related HSE03 (HFSCREEN=0.3) or HSE06 (HFSCREEN=0.2) functionals. It also needs to be set for dielectric-dependent hybrid functionals (DDH) and doubly screened hybrid (DSH) functionals, see LMODELHF.

> **Mind:** HFSCREEN can be used only when GGA=PE, PS or CA. The other GGA and METAGGA functionals have no screened version available in VASP.

## Related tags and articles

LMODELHF,
AEXX,
ALDAX,
ALDAC,
AGGAX,
AGGAC,
LTHOMAS,
LRHFCALC,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag
