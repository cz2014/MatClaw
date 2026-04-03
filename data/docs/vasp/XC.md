# XC

Categories: INCAR tag, Exchange-correlation functionals

XC = Combination of functionals

|  |  |  |
| --- | --- | --- |
| Default: **XC** | = GGA | if the GGA tag is used |
|  | = METAGGA | if the METAGGA tag is used |
|  | = The functional specified by LEXCH in the POTCAR file | if neither GGA nor METAGGA is used |

Description: Specifies a combination of exchange-correlation functionals.

---

A combination of semilocal (LDA, GGA, and METAGGA) functionals can be set with the XC tag, which provides much more flexibility in the choice of the functional compared to the GGA and METAGGA tags. The functionals that can be combined are the functionals implemented in VASP (listed at GGA and METAGGA) and the functionals implemented in Libxc (listed on the Libxc website). The combination can consist of up to 100 components; for each, a multiplication factor can be set with the XC\_C tag.

> **Mind:** This tag is available since VASP.6.4.3.

## Examples of INCAR

* 50% of PBE and 50% of PBEsol

```
XC = PE PS
XC_C = 0.5 0.5
```

* SCAN exchange combined with PBE correlation

```
XC = SCAN_X PBE_C
```

* 70% of B88 (from Libxc) and 30% of PBE for exchange and 100% of LYP (from Libxc) for correlation

```
XC = GGA_X_B88 PBE_X GGA_C_LYP
XC_C = 0.7 0.3 1.0
```

* 15% of HF, 63.75% of PBE, and 21.25% of B88 (from Libxc) for exchange and 75% of PBE and 25% of LYP (from Libxc) for correlation

```
LHFCALC = .TRUE.
XC      = PE GGA_X_B88 GGA_C_LYP
XC_C    = 0.75 0.25 0.25
AEXX    = 0.15
AGGAX   = 0.85
```

:   The PBE exchange is multiplied by $0.75\times0.85=0.6375$ and the B88 exchange by $0.25\times0.85=0.2125$.

* 15% of HF, 63.75% of PBE, and 21.25% of SCAN for exchange and 75% of PBE and 25% of SCAN for correlation

```
LHFCALC = .TRUE.
XC      = PE SCAN
XC_C    = 0.75 0.25
AEXX    = 0.15
AGGAX   = 0.85
AMGGAX  = 0.85
```

:   The PBE exchange is multiplied by $0.75\times0.85=0.6375$ and the SCAN exchange by $0.25\times0.85=0.2125$. AGGAX and AMGGAX multiply the exchange part of PBE and SCAN, respectively.

## Related tags and articles

XC\_C,
GGA,
METAGGA
LIBXC1,
LIBXC2,
ALDAX,
ALDAC,
AGGAX,
AGGAC,
AMGGAX,
AMGGAC

Examples that use this tag

## References

---
