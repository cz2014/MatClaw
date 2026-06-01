# NEDOS

Categories: INCAR tag, Density of states, Dielectric properties

NEDOS = [integer]  
 Default: **NEDOS** = $301$

Description: Number of grid points for the electronic density of states (DOS) and dielectric function.

---

The energy range between EMIN and EMAX is divided into
NEDOS intervals to obtain the grid points. The DOS for the corresponding energy is written in the DOSCAR file.

> **Tip:** Compare the DOS to the integrated DOS (also written on DOSCAR) to check if the default NEDOS is too small to resolve narrow peaks properly. At least one peak should show up at every step of the integrated DOS.

The smallest peak widths from the dispersion of the respective bands can be estimated by having a look at the Kohn-Sham eigenvalues written in OUTCAR. NEDOS has to be chosen sufficiently large to resolve this dispersion. In addition, the
energy interval defined by EMIN and EMAX can be modified.

NEDOS is also used to set the total number of frequency points when calculating the dielectric function.

## Related tags and articles

EMIN, EMAX,
DOSCAR

Examples that use this tag
