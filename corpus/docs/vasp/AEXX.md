# AEXX

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

AEXX = [real]

|  |  |  |
| --- | --- | --- |
| Default: **AEXX** | = 0.25 | if LHFCALC=.TRUE. .AND. LRHFCALC=.FALSE. |
|  | = 1 | if LRHFCALC=.TRUE. |
|  | = 0 | if LHFCALC=.FALSE. |

Description: AEXX specifies the fraction of exact exchange in a Hartree-Fock-type/hybrid-functional calculation.

---

> **Mind:**
>
> * For versions of VASP prior to 6.4.0, ALDAX was constrained to be equal to 1.0-AEXX. This constraint is lifted since VASP.6.4.0.
> * For AEXX=1.0, VASP switches off correlation by default (ALDAC=0.0, AGGAC=0.0, and AMGGAC=0.0) and thus runs a full Hartree-Fock calculation.

## Related tags and articles

ALDAX,
ALDAC,
AGGAX,
AGGAC,
AMGGAX,
AMGGAC,
LHFCALC,
HFSCREEN,
LRHFCALC,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

## References

---
