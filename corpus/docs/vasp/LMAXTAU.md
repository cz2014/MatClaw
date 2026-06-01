# LMAXTAU

Categories: INCAR tag, Exchange-correlation functionals

LMAXTAU = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **LMAXTAU** | = 6 | if LASPH=.TRUE. |
|  | = 0 | else |

Description: LMAXTAU is the maximum *l*-quantum number included in the PAW one-center expansion of the kinetic energy density.

---

The PAW one-center expansion of the density has component up to and including *L*=2\**l*max, where *l*max is the *l*-quantum number of the partial waves on the POTCAR file, with the highest angular moment.
If the PAW one-center expansion of the density has component up to *L*, then the one-center expansion of the kinetic energy density has components up to *L*+2.

This means that as a rule of thumb, for *s*-elements: LMAXTAU=2, for *p*: LMAXTAU=4, and for *d*: LMAXTAU=6.
If you are willing to live with the computational costs, the default for LMAXTAU should be safe in all cases, except those involving *f*-elements.

## Related tags and articles

METAGGA,
CMBJ,
CMBJA,
CMBJB,
LASPH,
LMIXTAU

Examples that use this tag

---
