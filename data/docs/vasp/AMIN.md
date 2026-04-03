# AMIN

Categories: INCAR tag, Density mixing

AMIN = [real]  
 Default: **AMIN** = min(0.1,AMIX,AMIX\_MAG)

Description: AMIN specifies the minimal mixing parameter in Kerker's initial approximation to the charge-dielectric function used in the Broyden/Pulay mixing scheme (IMIX=4, INIMIX=1).

---

Kerker's initial approximation for the charge-dielectric function is given by

:   $$\max\left(\frac{AG^2}{G^2+B^2},A\_{\rm min}\right),$$

where $A$=AMIX, $B$=BMIX, and $A\_{\rm min}$=AMIN.

## Related tags and articles

IMIX,
INIMIX,
MAXMIX,
AMIX,
BMIX,
AMIX\_MAG,
BMIX\_MAG,
MIXPRE,
WC

Examples that use this tag

## References
