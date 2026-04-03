# LIBXC1_Pn

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

LIBXC1\_Pn = [real]

Description: LIBXC1\_Pn, where $n=1, 2, \ldots$ allows to specify the values of the parameters of the functional implemented in Libxc that is called with LIBXC1.

---

For many of the functionals implemented in the library of exchange-correlation functionals Libxc it is possible to modify the parameters if one does not want to use the default values. If a functional from Libxc has parameters that can be modified, then they are listed in OUTCAR below "Parameters of Libxc functionals:" as P$n$ ($n=1, 2, \ldots$). LIBXC1\_Pn and LIBXC2\_Pn are for the functionals called with LIBXC1 and LIBXC2, respectively.

An example is given below for the GGA PBE functional where the default parameters $\mu=0.21951$ in exchange and $\beta=0.066725$ in correlation are changed to $\mu=10/81\approx0.12345679$ and $\beta=0.046$ to get the PBEsol functional (of course, the simpler way to use PBEsol from Libxc would be to call it directly with LIBXC1=GGA\_X\_PBE\_SOL and LIBXC2=GGA\_C\_PBE\_SOL).

```
GGA = LIBXC
LIBXC1 = GGA_X_PBE # or 101
LIBXC2 = GGA_C_PBE # or 130
LIBXC1_P2 = 0.12345679
LIBXC2_P1 = 0.046
```

> **Mind:** The ALDAX, ALDAC, AGGAX, AGGAC, AMGGAX, and AMGGAC tags are ignored if the Libxc functional is an exchange-correlation functional (those with a tag that contains XC)

For Libxc functionals that are the semilocal component of a hybrid functional, i.e. those with a tag that starts with HYB (LHFCALC=.TRUE. will be set automatically if such a functional is selected), the following explains how it works for the mixing and screening parameters:

* Mixing parameter:
  + It is usually one of the parameters LIBXC1\_Pn, and can therefore be modified.
  + For HYB\_GGA\_XC\_PBEH, HYB\_GGA\_XC\_B1WC, HYB\_GGA\_XC\_HSE03, HYB\_GGA\_XC\_HSE06, HYB\_GGA\_XC\_HSE12, and HYB\_GGA\_XC\_HSE12S, the value of AEXX (even if not specified explicitly in INCAR) will be used and automatically passed to the corresponding parameter in Libxc. On the other hand, if this corresponding parameter (LIBXC1\_Pn) is specified in INCAR, then it will be used (instead of AEXX), however note that it will be only for the semilocal component of the hybrid functional and not for the exact exchange that will still use AEXX.
  + For all hybrid functionals except those listed just above, AEXX will not be considered for the semilocal component of the hybrid functional, but only for the exact exchange component. Therefore, a particular choice for the mixing parameter has to be done by specifying both AEXX (for the exact exchange) and the appropriate LIBXC1\_Pn (for the semilocal component).
  + The ALDAX, ALDAC, AGGAX, AGGAC, AMGGAX, and AMGGAC tags are ignored if the Libxc functional is an hybrid functional (those with a tag that starts with HYB).
* Screening parameter:
  + It is usually one of the parameters LIBXC1\_Pn if it is a screened functional, and can therefore be modified.
  + For HYB\_GGA\_XC\_HSE03, HYB\_GGA\_XC\_HSE06, HYB\_GGA\_XC\_HSE12, and HYB\_GGA\_XC\_HSE12S, the value of HFSCREEN (even if not specified explicitly in INCAR) will be used and automatically passed to the corresponding parameter in Libxc. On the other hand, if this corresponding parameter (LIBXC1\_Pn) is specified in INCAR, then it will be used (instead of HFSCREEN), however note that it will be only for the semilocal component of the hybrid functional and not for the exact exchange that will still use HFSCREEN.
  + For all hybrid functionals except those listed just above, HFSCREEN will not be considered for the semilocal component of the hybrid functional, but only for the exact exchange component. Therefore, a particular choice for the screening parameter has to be done by specifying both HFSCREEN (for the exact exchange) and the appropriate LIBXC1\_Pn (for the semilocal component).

## Related tags and articles

LIBXC1,
LIBXC2,
LIBXC2\_Pn,
LTBOUNDLIBXC,
GGA,
METAGGA,
LHFCALC,
AEXX,
ALDAX,
ALDAC,
AGGAX,
AGGAC,
AMGGAX,
AMGGAC,
List of hybrid functionals

Examples that use this tag

## References

---
