# LDAUTYPE

Categories: INCAR tag, Exchange-correlation functionals, DFT+U

LDAUTYPE = 1 | 2 | 4  
 Default: **LDAUTYPE** = 2

Description: LDAUTYPE specifies the DFT+U variant that will be used.

---

The following variants of the DFT+U are available:

* LDAUTYPE=1: The rotationally invariant DFT+U introduced by Liechtenstein *et al.*

* LDAUTYPE=2: The simplified (rotationally invariant) approach to DFT+U, introduced by Dudarev *et al.*

* LDAUTYPE=3: Linear response ansatz of Cococcioni et al. to compute U. See how to calculate U.

:   > **Mind:** For LDAUTYPE=3, the LDAUU and LDAUJ tags specify the strength of the spherical potential acting on the spin-up and spin-down manifolds, respectively.

* LDAUTYPE=4: Same as LDAUTYPE=1, but without exchange splitting.

A method to estimate the parameters for DFT+U is the constrained-random-phase approximation. Another method is the linear response ansatz with LDAUTYPE=3, mentioned above. On the other hand, in many applications, the DFT+U parameters are used as tuning parameters to fit experimental data.

> **Tip:** For band-structure calculations, increase LMAXMIX to 4 ($d$ elements) or 6 ($f$ elements).

This is because the CHGCAR file contains only information up to angular momentum quantum number set by LMAXMIX for the on-site PAW occupancy matrices. When the CHGCAR file is read and kept fixed in the course of the calculations (ICHARG=11), the results will necessarily not be identical to a self-consistent run. The deviations are often large for DFT+U calculations.

> **Warning:** The total energy will depend on the parameters $U$ (LDAUU) and $J$ (LDAUJ). It is, therefore, not meaningful to compare the total energies resulting from calculations with different $U$ and/or $J$; or $U-J$ in the case of Dudarev's approach (LDAUTYPE=2).

It is possible to use LDAUTYPE=1, 2, and 3 for a non–spin-polarized calculation with ISPIN=1.

## Related tags and articles

LDAU,
LDAUL,
LDAUU,
LDAUJ,
LDAUPRINT,
LMAXMIX

Examples that use this tag

## References

---
