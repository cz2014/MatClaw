# AMIX_MAG

Categories: INCAR tag, Density mixing, Magnetism

AMIX\_MAG = [real]  
 Default: **AMIX\_MAG** = 1.6

Description: Linear mixing parameter for the magnetization density.

---

The default mixing parameters for spinpolarized calculations are:

:   IMIX=4, AMIX=0.4, AMIN=min(0.1,AMIX,AMIX\_MAG), BMIX=1.0, AMIX\_MAG=1.6, and BMIX\_MAG=1.0.

These settings are consistent with an (initial) spin enhancement factor of 4, which is usually a reasonable approximation.

There are only a few other parameter combinations that can be tried if convergence turns out to be very slow. In particular, for slabs, magnetic systems, and insulating systems (e.g. molecules and clusters), an initial "linear mixing" can result in faster convergence than the Kerker model function. One can therefore try to use the following setting

```
AMIX     = 0.2
BMIX     = 0.0001 ! almost zero, but 0 will crash some versions
AMIX_MAG = 0.8
BMIX_MAG = 0.0001 ! almost zero, but 0 will crash some versions
```

> **Mind:** For spin-polarized calculations the defaults for the mixing parameters AMIX and BMIX are different than for the non-spin-polarized case.

## Related tags and articles

IMIX,
INIMIX,
MAXMIX,
AMIX,
BMIX,
BMIX\_MAG,
AMIN,
MIXPRE,
WC

Examples that use this tag
