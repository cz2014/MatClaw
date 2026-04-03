# BMIX

Categories: INCAR tag, Density mixing

BMIX = [real]  
 Default: **BMIX** = 1.0

Description: BMIX sets the cutoff wave vector for Kerker mixing scheme (IMIX=1 and/or INIMIX=1).

---

The mixed density is given by

:   :   $$\rho\_{\rm mix}\left(G\right)=\rho\_{\rm in}\left(G\right)+A \frac{G^2}{G^2+B^2}\Bigl(\rho\_{\rm out}\left(G\right)-\rho\_{\rm in}\left(G\right)\Bigr)$$

with $A$=AMIX and $B$=BMIX

In VASP the eigenvalue spectrum of the charge dielectric matrix is calculated and written to the OUTCAR file at each electronic step. This allows a rather easy optimization of the mixing parameters, if required. Search in the OUTCAR file for

```
eigenvalues of (default mixing * dielectric matrix)
```

The parameters for the mixing are optimal if the mean eigenvalue Γmean=1, and if the width of the eigenvalue spectrum is minimal. For an initial linear mixing (BMIX≈0) an optimal setting for AMIX can be found easily by setting AMIXoptimal=AMIXcurrent\*Γmean. For the Kerker scheme (IMIX=1) either AMIX or BMIX can be optimized, but we recommend to change only BMIX and keep AMIX fixed (you must decrease BMIX if the mean eigenvalue is larger than one, and increase BMIX if the mean eigenvalue Γmean<1).

## Related tags and articles

IMIX,
INIMIX,
MAXMIX,
AMIX,
AMIX\_MAG,
BMIX\_MAG,
AMIN,
MIXPRE,
WC

Examples that use this tag

## References
