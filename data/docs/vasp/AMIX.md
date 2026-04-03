# AMIX

Categories: INCAR tag, Density mixing

AMIX = [real]

|  |  |  |
| --- | --- | --- |
| Default: **AMIX** | = 0.8 | if ISPIN=1 and one uses US-PPs |
|  | = 0.4 | if ISPIN=2 and one uses US-PPs |
|  | = 0.4 | if one uses PAW datasets |

Description: AMIX specifies the linear mixing parameter.

---

In VASP the eigenvalue spectrum of the charge dielectric matrix is calculated and written to the OUTCAR file at each electronic step. This allows a rather easy optimization of the mixing parameters, if required. Search in the OUTCAR file for

```
eigenvalues of (default mixing * dielectric matrix)
```

The parameters for the mixing are optimal if the mean eigenvalue Γmean=1, and if the width of the eigenvalue spectrum is minimal. For an initial linear mixing (BMIX≈0) an optimal setting for AMIX can be found easily by setting AMIXoptimal=AMIXcurrent\*Γmean. For the Kerker scheme (IMIX=1) either AMIX or BMIX can be optimized, but we recommend to change only BMIX and keep AMIX fixed (you must decrease BMIX if the mean eigenvalue is larger than one, and increase BMIX if the mean eigenvalue Γmean<1).
However, the optimal AMIX depends very much on the system, for metals this parameter usually has to be rather small, e.g. AMIX= 0.02.

## Related tags and articles

IMIX,
INIMIX,
MAXMIX,
BMIX,
AMIX\_MAG,
BMIX\_MAG,
AMIN,
MIXPRE,
WC

Examples that use this tag
