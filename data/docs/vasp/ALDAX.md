# ALDAX

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

ALDAX = [real]

|  |  |  |
| --- | --- | --- |
| Default: **ALDAX** | = 1.0-AEXX | if LHFCALC=.TRUE. |
|  | = 1.0 | if LHFCALC=.FALSE. |

Description: ALDAX is a parameter that multiplies the LDA exchange functional or the LDA part of the GGA exchange functional.

---

ALDAX can be used as the fraction of LDA exchange in a Hartree-Fock/DFT hybrid functional.

> **Important:** ALDAX can be used only if LHFCALC=.TRUE.

> **Mind:**
>
> * For versions of VASP prior to 6.4.0, ALDAX was constrained to be equal to 1.0-AEXX. This constraint is lifted since VASP.6.4.0.
> * ALDAX is implemented for all functionals listed at GGA except AM05.
> * ALDAX is implemented for the functionals from Libxc (see LIBXC1 for details).

## Related tags and articles

AEXX,
ALDAC,
AGGAX,
AGGAC,
AMGGAX,
AMGGAC,
LHFCALC,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

---
