# AMGGAX

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

AMGGAX = [real]

|  |  |  |
| --- | --- | --- |
| Default: **AMGGAX** | = 1.0-AEXX | if LHFCALC=.TRUE. |
|  | = 1.0 | if LHFCALC=.FALSE. |

Description: AMGGAX is a parameter that multiplies the meta-GGA exchange functional (available as of VASP.6.4.0).

---

AMGGAX can be used as the fraction of meta-GGA exchange in a Hartree-Fock/DFT hybrid functional (possible since VASP.6.4.0).

> **Important:** AMGGAX can be used only if LHFCALC=.TRUE.

> **Mind:**
>
> * Note the difference with respect to AGGAX: AMGGAX multiplies the whole meta-GGA exchange functional, while AGGAX multiplies only the gradient-correction term of a GGA exchange functional.
> * AMGGAX is implemented for the functionals from Libxc (see LIBXC1 for details).

## Related tags and articles

AEXX,
ALDAX,
ALDAC,
AGGAX,
AGGAC,
AMGGAC,
LHFCALC,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

---
