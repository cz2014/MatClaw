# MIXPRE

Categories: INCAR tag, Density mixing

MIXPRE = 0 | 1 | 2 | 3  
 Default: **MIXPRE** = 1

Description: MIXPRE specifies the metric in the Broyden mixing scheme(IMIX=4).

---

* MIXPRE=0

:   No preconditioning, metric=1

* MIXPRE=1

:   "Inverse Kerker" metric with automatically determined BMIX (determined in such a way that the variation of the preconditioning weights covers a range of a factor 20)

* MIXPRE=2

:   "Inverse Kerker" metric with automatically determined BMIX (determined in such a way that the variation of the preconditioning weights covers a range of a factor 200)

* MIXPRE=3 (implemented for test purposes; **not** recommended)

:   "Inverse Kerker" metric with BMIX from INCAR, the weights for the metric are given by

    :   $$P\left(G\right)=1+\frac{B^2}{G^2}$$
:   with $B$=BMIX.

The preconditioning is done only on the total charge density (i.e. up+down component) and not on the magnetization charge density (i.e. up-down component). In our experience, the introduction of a metric always improves the convergence speed. The best choice is MIXPRE=1 (i.e. the default).

## Related tags and articles

IMIX,
INIMIX,
MAXMIX,
AMIX,
BMIX,
AMIX\_MAG,
BMIX\_MAG,
AMIN,
WC

Examples that use this tag
