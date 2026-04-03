# CLNT

Categories: INCAR tag, Linear response, Dielectric properties, XAS

CLNT = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **CLNT** | = 1 |  |

Description: CLNT selects the type of the excited atoms in XAS calculations with ICORELEVEL>0.

---

All atoms of the selected type are excited in the XAS calculation with ICORELEVEL=2. Hence, it is recommended that the excited atom is separated into a dedicated type with a single atom. Exciting multiple atoms in the supercell core-hole approach causes the interaction between core holes in neighboring atoms and should be avoided. Exciting multiple atoms in BSE proportionately increases the number of core states included in the BSE Hamiltonian and, hence, increases the computational cost of the calculation.

See a detailed description on how to set this tag in the SCH and BSE calculations.

## Related tags and articles

ICORELEVEL, CLN, CLL, CLZ

Examples that use this tag

---
