# LTHOMAS

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

LTHOMAS = .TRUE. | .FALSE.  
 Default: **LTHOMAS** = .FALSE.

Description: LTHOMAS selects a decomposition of the exchange functional based on Thomas-Fermi exponential screening.

---

If LTHOMAS=.TRUE. the decomposition of the exchange operator (in a range-separated hybrid functional) into a short range and a long range part will be based on Thomas-Fermi exponential screening.
The Thomas-Fermi screening length *k*TF is specified by means of the HFSCREEN tag.

For typical semiconductors, a Thomas-Fermi screening length $k\_{\rm TF}$ of about 1.8 Å-1 yields reasonable band gaps. In principle, however, the Thomas-Fermi screening length depends on the valence-electron density. VASP determines $k\_{\rm TF}$ from the number of valence electrons (read from the POTCAR file) and the volume (leading to an average density $\bar{n}$) and writes the corresponding value of $k\_{\rm TF}=\sqrt{4k\_{\rm F}/\pi}$, where $k\_{\rm F}=(3\pi^2\bar{n})^{1/3}$ to the OUTCAR file (note that this value is only printed for information; it is not used during the calculation):

```
 Thomas-Fermi vector in A             =   2.00000
```

The setting of the sX-LDA functional is shown on the page listing the hybrid functionals.

> **Mind:**
>
> * If LTHOMAS=.TRUE., then LHFCALC=.TRUE. is automatically set.
> * If LTHOMAS=.TRUE., then AEXX=1 is automatically set, but AEXX can be set to another value.

> **Important:** When AEXX=1 (the default for LTHOMAS=.TRUE.), the correlation $E\_{\mathrm{c}}^{\mathrm{SL}}$ is not included. However, it can be included by setting ALDAC=1.0 and AGGAC=1.0.

Since VASP counts the semi-core states and *d*-states as valence electrons, although these states do not contribute to the screening, the values reported by VASP are often not recommended.

## Related tags and articles

LHFCALC,
HFSCREEN,
AEXX,
LMODELHF,
LRHFCALC,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

---
