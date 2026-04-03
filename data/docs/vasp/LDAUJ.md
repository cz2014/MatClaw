# LDAUJ

Categories: INCAR tag, Exchange-correlation functionals, DFT+U

LDAUJ = [real array]  
 Default: **LDAUJ** = NTYP\*0.0

Description: Sets the effective on-site exchange interactions (eV).

---

LDAUJ specifies the strength of the effective on-site exchange interactions in eV. It must hold one value for each atomic species.

> **Warning:** The total energy will depend on the parameters $U$ (LDAUU) and $J$ (LDAUJ). It is, therefore, not meaningful to compare the total energies resulting from calculations with different $U$ and/or $J$; or $U-J$ in the case of Dudarev's approach (LDAUTYPE=2).

> **Mind:** For LDAUTYPE=3, the LDAUU and LDAUJ tags specify the strength (in eV) of the spherical potential acting on the spin-up and spin-down manifolds, respectively.

## Related tags and articles

LDAU,
LDAUTYPE,
LDAUL,
LDAUU,
LDAUPRINT,
LMAXMIX

Examples that use this tag

---
