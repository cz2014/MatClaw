# AGGAX

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

AGGAX = [real]

|  |  |  |
| --- | --- | --- |
| Default: **AGGAX** | = 1.0-AEXX | if LHFCALC=.TRUE. |
|  | = 1.0 | if LHFCALC=.FALSE. |

Description: AGGAX is a parameter that multiplies the gradient correction in the GGA exchange functional.

---

AGGAX can be used as the fraction of gradient correction in the GGA exchange in a Hartree-Fock/GGA hybrid functional.

> **Important:** AGGAX can be used only if LHFCALC=.TRUE.

> **Mind:**
>
> * AGGAX is implemented for all functionals listed at GGA except AM05.
> * AGGAX is implemented for the functionals from Libxc (see LIBXC1 for details).

## Related tags and articles

AEXX,
ALDAX,
ALDAC,
AGGAC,
AMGGAX,
AMGGAC,
LHFCALC,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

---
