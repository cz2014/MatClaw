# DOSCAR

Categories: Files, Output files, Density of states

The DOSCAR file contains the DOS and integrated DOS. The units are number of states/eV and number of states, respectively and thus extensively defined. The intensive DOS is obtained by dividing by the Volume of the unit cell. For dynamic simulations and relaxations, an averaged DOS and an averaged integrated DOS is written to the file. For a description of how the averaging is done see the tags NBLOCK, KBLOCK, EMIN, EMAX and NEDOS. The first few lines of the DOSCAR file are made up by a header:

```
Number of Ions (including empty spheres), Number of Ions, 0 (no partial DOS) or 1 (incl. partial DOS), NCDIJ (currently not used)     
Volume of the unit cell [Angst**3], length of the basis vectors (a,b,c [m]), POTIM[s]
the initial Temperature TEBEG 
'CAR'
the name of the system as given by SYSTEM in INCAR
E(max), E(min), (the energy range in which the DOS is given), NEDOS,  E(fermi), 1.0000
```

which is followed by NEDOS lines with the columns

```
energy     DOS     integrated DOS
```

The density of states (DOS) $\bar n$, for Methfessel-Paxton smearing (ISMEAR>0) and Fermi-Dirac smearing (ISMEAR=-1) is determined as the difference of the integrated DOS between two pins, i.e.

:   $$\bar n(\epsilon\_i) = (N(\epsilon\_i) - N(\epsilon\_{i-1})) / \Delta \epsilon$$

where $\Delta \epsilon$ is the distance between two pins (energy difference between two grid point in the DOSCAR file), and $N(\epsilon\_i)$ is the integrated DOS

:   $$N (\epsilon\_{i}) = \int\_{-\infty}^{\epsilon\_i} n(\epsilon) d \epsilon.$$

This method conserves the total number of electrons exactly.
For the tetrahedron method (ISMEAR=-4 or -5), the total integrated DOS is computed using the formulas in Appendix A and B of Bloechl's paper and the DOS using the formulas from Appendix C .
In this case, it is not guaranteed that integrating the DOS will conserve the number of electrons. This can however be systematically improved by increasing NEDOS.

For spin-polarized calculations ISPIN=2 each line holds five data columns with the following format

```
energy     DOS(up) DOS(dwn)  integrated DOS(up) integrated DOS(dwn)
```

If RWIGS or LORBIT (important for Wigner Seitz radii) is set in the INCAR file, an lm- and site-projected DOS is calculated and written to the DOSCAR file for each ion. This data, again, contains NEDOS lines with various columns depending on the choice of LORBIT, ISPIN and LNONCOLLINEAR.

In the case of colinear calculations with ISPIN=1, the format for l-decomposed calculations for each ion is

```
energy s-DOS p-DOS d-DOS
```

while for lm-resolved calculations the format is:

```
energy  s  p_y p_z p_x d_{xy} d_{yz} d_{z2-r2} d_{xz} d_{x2-y2},...
```

For spin-polarized systems ISPIN = 2 additional columns are printed for each spin channel

```
energy s-DOS(up) s-DOS(down) p-DOS(up) p-DOS(dwn) d-DOS(up) d-DOS(dwn)
```

and correspondingly if lm-decomposed densities are selected with LORBIT.

For non-collinear calculations, information on the individual spinor components is available only for the site projected density of states:

```
energy s-DOS(total) s-DOS(mx) s-DOS(my) s-DOS(mz) p-DOS(total) p-DOS(mx) ...
```

In this case, the (site projected) total density of states (total) and the (site projected) energy resolved magnetization density in the $x$ (mx), $y$ (my) and $z$ (mz) directions are available.

In all cases, the units of the l- and site projected DOS are states/atom/energy.

The site projected DOS is not evaluated in the parallel version for the following cases:

* vasp.4.5, NPAR$\ne$1 no site projected DOS
* vasp.4.6, NPAR$\ne$1, LORBIT=0-5 no site projected DOS

In vasp.4.6 the site projected DOS can be evaluated for LORBIT=10-12, even if NPAR is not equal 1 (contrary to previous releases).

* vasp.5 needs no specification of NPAR

> **Mind:** For relaxations, the DOSCAR is usually useless. If you want to get an accurate DOS for the final configuration, first copy CONTCAR to POSCAR and continue with one static (`ISTART = 1`; `NSW = 0`) calculation.

---
