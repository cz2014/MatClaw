# NBANDSGW

Categories: INCAR tag, Many-body perturbation theory, GW

NBANDSGW = [integer]  
 Default: **NBANDSGW** = twice the number of occupied states

Description: The flag determines how many QP energies are calculated and updated in GW type calculations.

---

This value usually needs to be increased somewhat for partially or fully self-consistent calculations. Very accurate results
are only obtained when NBANDSGW approaches NBANDS, although this dramatically increases the computational requirements.

## Related tags and articles

NBANDS

Examples that use this tag

---
