# AMGGAC

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

AMGGAC = [real]

|  |  |  |
| --- | --- | --- |
| Default: **AMGGAC** | = 1.0 | if LHFCALC$=$.FALSE. or AEXX$\neq$1.0 |
|  | = 0.0 | if LHFCALC$=$.TRUE. and AEXX$=$1.0 |

Description: AMGGAC is a parameter that multiplies the meta-GGA correlation functional (available as of VASP.6.4.0).

---

AMGGAC can be used as the fraction of meta-GGA correlation in a Hartree-Fock/DFT hybrid functional.

> **Mind:** Note the difference with respect to AGGAC: AMGGAC multiplies the whole meta-GGA correlation functional, while AGGAC multiplies only the gradient-correction term of a GGA correlation functional.

## Related tags and articles

AEXX,
ALDAX,
ALDAC,
AGGAX,
AGGAC,
AMGGAX,
LHFCALC,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

---
