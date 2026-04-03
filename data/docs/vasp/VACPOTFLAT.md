# VACPOTFLAT

Categories: INCAR tag, Electrostatics

VACPOTFLAT = [real]  
 Default: **VACPOTFLAT** = 0.1

Description: Maximum permissible 2D-averaged electric field for a region considered to be field-free in eV/Å.

---

A region of space is considered to be field-free if the 2D-averaged electric field (LVACPOTAV=True) is smaller than VACPOTFLAT.

> **Tip:** Increase VACPOTFLAT for a quick estimation of the vacuum potential and decrease for a precise value. If the cell is large and EDIFF small, the final result of LVACPOTAV should be independent of VACPOTFLAT.

## Related tags and articles

LVACPOTAV,
LVTOT,
LVHAR,
WRT\_POTENTIAL,
DIPOL,
LDIPOL,
IDIPOL
