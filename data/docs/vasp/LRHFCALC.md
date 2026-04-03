# LRHFCALC

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

LRHFCALC = .TRUE. | .FALSE.  
 Default: **LRHFCALC** = .FALSE.

Description: Switch on the decomposition of the exchange for the hybrid functionals using full Hartree-Fock exchange at long range, like RSHXLDA or RSHXPBE.

---

If LRHFCALC=.TRUE. the exchange functional is decomposed into short-range LDA, PBE or PBEsol (GGA=CA, PE, PS, respectively) and long-range Hartree-Fock, like for instance in RSHXLDA or RSHXPBE. The screening parameter is specified by means of the HFSCREEN tag.

The setting of the RSHXLDA and RSHXPBE functionals is shown on the page listing the hybrid functionals.

> **Mind:**
>
> * If LRHFCALC=.TRUE., then LHFCALC=.TRUE. is automatically set.
> * If LRHFCALC=.TRUE., then AEXX=1 is automatically set, but AEXX can be set to another value.

> **Important:** When AEXX=1 (the default for LRHFCALC=.TRUE.), the correlation $E\_{\mathrm{c}}^{\mathrm{SL}}$ is not included. However, it can be included by setting ALDAC=1.0 and AGGAC=1.0.

## Related tags and articles

LHFCALC,
HFSCREEN,
AEXX,
LMODELHF,
LTHOMAS,
list of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

---
