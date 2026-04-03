# AGGAC

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

AGGAC = [real]

|  |  |  |
| --- | --- | --- |
| Default: **AGGAC** | = 1.0 | if LHFCALC$=$.FALSE. or AEXX$\neq$1.0 |
|  | = 0.0 | if LHFCALC$=$.TRUE. and AEXX$=$1.0 |

Description: AGGAC is a parameter that multiplies the gradient correction in the GGA correlation functional.

---

AGGAC can be used as the fraction of gradient correction in the GGA correlation in a Hartree-Fock/DFT hybrid functional.

> **Mind:**
>
> * AGGAC is implemented for all functionals listed at GGA except AM05.
> * AGGAC is implemented for the functionals from Libxc (see LIBXC1 for details).

## Related tags and articles

AEXX,
ALDAX,
ALDAC,
AGGAX,
AMGGAX,
AMGGAC,
LHFCALC,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

---
