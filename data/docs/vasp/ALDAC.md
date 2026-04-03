# ALDAC

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

ALDAC = [real]

|  |  |  |
| --- | --- | --- |
| Default: **ALDAC** | = 1.0 | if LHFCALC$=$.FALSE. or AEXX$\neq$1.0 |
|  | = 0.0 | if LHFCALC$=$.TRUE. and AEXX$=$1.0 |

Description: ALDAC is a parameter that multiplies the LDA correlation functional or the LDA part of the GGA correlation functional.

---

ALDAC can be used as the fraction of LDA correlation in a Hartree-Fock/DFT hybrid functional.

> **Mind:**
>
> * ALDAC is implemented for all functionals listed at GGA except AM05.
> * ALDAC is implemented for the functionals from Libxc (see LIBXC1 for details).

## Related tags and articles

AEXX,
ALDAX,
AGGAX,
AGGAC,
AMGGAX,
AMGGAC,
LHFCALC,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

---
