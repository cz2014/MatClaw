# CLN

Categories: INCAR tag, Linear response, Dielectric properties, XAS

CLN = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **CLN** | = 1 |  |

Description: CLN selects the main quantum number $n$ of the excited core electron when using ICORELEVEL>0.

---

> **Mind:** Currently the spin-orbit coupling is only supported in the valence and conduction states but not in the core states. Hence, the splitting of an absorption edge with the orbital quantum number L>0 is not captured. For example, the splitting to *L2* and *L3*-edges is not captured in the calculations and instead, a single *L*-edge is shown.

## Related tags and articles

ICORELEVEL,
CLNT,
CLN,
CLL
LADDER,
LHARTREE,
NBANDSV,
NBANDSO,
OMEGAMAX,
ANTIRES

Examples that use this tag

---
