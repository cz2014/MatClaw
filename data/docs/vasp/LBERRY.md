# LBERRY

Categories: INCAR tag, Linear response, Dielectric properties, Berry phases, Howto

LBERRY = [logical]  
 Default: **LBERRY** = .FALSE.

Description: This tag is used in the the evaluation of the Berry phase expression for the electronic polarization of an insulating system.

---

As of VASP.5.2, calculating the macroscopic polarization and Born effective charges along the lines of the following example (using LBERRY=*.TRUE.* etc) is unnecessary. The use of LCALCPOL or LCALCEPS is much more convenient.

Setting LBERRY=*.TRUE.* in the INCAR file switches on the evaluation of the Berry phase expression for the electronic polarization of an insulating system, as modified for the application of USPP's and PAW datasets .
In addition, the following keywords must be specified in order to generate the mesh of k-points:

```
IGPAR = 1|2|3
```

IGPAR tag specifies the socalled parallel or $\mathbf{G}\_{\parallel}$ direction in the integration over the reciprocal space unit cell.

```
NPPSTR = number of points on the strings in the IGPAR direction
```

NPPSTR specifies the number of k-points on the strings $\mathbf{k}\_{j} = \mathbf{k}\_{\perp} + j\mathbf{G}\_{\parallel}/\mathrm{NPPSTR}$ (with $j=0,..,\mathrm{NPPSTR}-1$).

```
DIPOL = center of cell (fractional coordinates)
```

DIPOL specifies the origin with respect to which the ionic contribution to the dipole moment in the cell is calculated. When comparing changes in this contribution due to the displacement of an ion, this center should be chosen in such a way that the ions in the distorted and the undistorted structure remain on the same side of DIPOL (in terms of a minimum image convention).

## An example: The fluorine displacement dipole (Born effective charge) in NaF

First one needs to determine the electronic polarization of the undistorted NaF.

Caluclation1:
It is usually convenient to calculate the self-consistent Kohn-Sham potential of the undistorted structure, using a symmetry reduced $6\times6\times6$ Monkhorst-Pack sampling of the Brillouin zone. Using for instance the following INCAR file:

```
PREC   = Med
ISMEAR = 0
EDIFF  = 1E-6
```

KPOINTS file:

```
6x6x6
 0
Gamma
 6 6 6
 0 0 0
```

POSCAR file:

```
NaF
 4.5102
 0.0 0.5 0.5
 0.5 0.0 0.5
 0.5 0.5 0.0
1 1
Direct
  0.0000000000000000  0.0000000000000000  0.0000000000000000
  0.5000000000000000  0.5000000000000000  0.5000000000000000
```

and LDA Na\_sv and F PAW datasets.

Calculation 2:
To calculate the electronic contribution to the polarization, along the reciprocal lattice vector $\mathbf{G}\_{1}$ (i.e. $\mathbf{P} \cdot \mathbf{G}\_{1}$), add the following lines to the INCAR file:

```
LBERRY = .TRUE.
IGPAR  = 1
NPPSTR = 8
DIPOL = 0.25 0.25 0.25
```

Setting LBERRY=*.TRUE.* automatically sets ICHARG=11, i.e., the charge density of the previous calculation is read and kept fixed, and only the orbitals and one-electron eigenenergies are recalculated for the new k-point set. This is advantageous, since the number of k-points used to evaluate the Berry phase expression can be quite large, and precalculating the charge density (ICHARG=11) saves significant CPU time.

The OUTCAR will now contain the following lines:

```
                                e<r>_ev=(     0.00000     0.00000     0.00000 ) e*Angst
                                e<r>_bp=(     0.00000     0.00000     0.00000 ) e*Angst
```

```
 Total electronic dipole moment: p[elc]=(     0.00000     0.00000     0.00000 ) e*Angst
```

```
            ionic dipole moment: p[ion]=(     2.25510     2.25510     2.25510 ) e*Angst
```

Calculations 3 and 4:
The procedure mentioned under Calculation 2 now has to be repeated with IGPAR=2 and IGPAR=3 (again using the charge density obtained from Calculation 1), to obtain the contributions to the electronic polarization along $\mathbf{G}\_2$ and $\mathbf{G}\_{3}$, respectively.

Calculations 5 to 8:
To calculate the change in the electronic polarization of NaF due to the displacement of the fluorine sublattice, one should repeat Calculations 1 to 4, using the following POSCAR file:

```
NaF
 4.5102
 0.0 0.5 0.5
 0.5 0.0 0.5
 0.5 0.5 0.0
1 1
Direct
  0.0000000000000000  0.0000000000000000  0.0000000000000000
  0.5100000000000000  0.5100000000000000  0.4900000000000000
```

This corresponds to a displacement of the F ion by $0.01\times 4.51\AA$ along the $\hat{z}$ direction. The output of the Berry phase calculation using IGPAR=1 should now look similar to:

```
                                e<r>_ev=(     0.00000     0.00000     0.00004 ) e*Angst
                                e<r>_bp=(     0.00000     0.18028     0.18028 ) e*Angst 

 Total electronic dipole moment: p[elc]=(     0.00000     0.18028     0.18031 ) e*Angst
```

```
            ionic dipole moment: p[ion]=(     2.25510     2.25510     1.93939 ) e*Angst
```

Collecting the results:
The change in the electronic contribution to the polarization due to the F-sublattice displacement should be calculated as follows:

* Take the average of the $e\lt \mathrm{r}\gt \_\mathrm{ev}$ terms obtained in calculations 2 to 4. Lets call this $e\lt \mathrm{r}\gt \_{\mathrm{ev,undist}}$

* Add the $e\lt \mathrm{r}\gt \_{\mathrm{bp}}$ terms obtained in calculations 2 to 4. Lets call this $e\lt \mathrm{r}\gt \_{\mathrm{bp,undist}}$

* The electronic polarization of the undistorted structure is then given by:

$e\lt \mathrm{r}\gt \_{\mathrm{el,undist}}=e\lt \mathrm{r}\gt \_{\mathrm{ev,undist}}+e\lt \mathrm{r}\gt \_{\mathrm{bp,undist}}$

* Repeat the above three steps for the results obtained using the distorted structure (Calculations 6 to 8), to evaluate $e\lt \mathrm{r}\gt \_{\mathrm{ev,dist}}$, $e\lt \mathrm{r}\gt \_{\mathrm{bp,dist}}$, and $e\lt \mathrm{r}\gt \_{\mathrm{el,dist}}$

* The change in the electronic contribution to the polarization due to the F-sublattice displacement, $e\Delta\lt \mathrm{r}\gt \_\mathrm{el}$ is then given by $e\lt \mathrm{r}\gt \_{\mathrm{el,dist}}-e\lt \mathrm{r}\gt \_{\mathrm{el,undist}}$

To calculate the total change in polarization, $e\Delta\lt \mathrm{r}\gt$, one should account for the ionic contribution to this change. This contribution can be calculated from p[ion] as given above from
Calculations 2 and 5:
$\Delta\mathrm{p[ion]}=\mathrm{p[ion]}\_{\mathrm{dist}}-\mathrm{p[ion]}\_{\mathrm{undist}}$.

$e\Delta\lt \mathrm{r}\gt$ is then given by $\Delta \mathrm{p[ion]}+e\Delta\lt \mathrm{r}\gt \_\mathrm{el}$. In this example we find $e\Delta\lt \mathrm{r}\gt =0.04489$ electrons $\AA$. Considering that the moved F-sublattice was displaced by 0.045102 $\AA$, this calculation yields a Born effective charge for fluorine in NaF of $Z^{\*}=-0.995$.

N.B.(I) In the case of spinpolarized calculations (ISPIN=2),the Berry phase of the orbitals is evaluated separately for each spin direction. This means a *grep* on "$\lt \mathrm{r}\gt$" will yield two sets of $\lt \mathrm{r}\gt \_{\mathrm{ev}}$ and $\lt \mathrm{r}\gt \_{\mathrm{bp}}$ terms, which have to be added to oneanother to obtain the total electronic polarization of the system.

N.B.(II) One should take care of the fact that the calculated "Berry phase" term $\lt \mathrm{r}\gt \_{\mathrm{bp}}$ along $\mathbf{G}\_{i}$ is, in principle, obtained modulo a certain period, determined by the lattice vector $\mathbf{R}\_{i}$ ($\mathbf{R}\_{i} \cdot \mathbf{G}\_{i} = 2 \pi$), the spin multiplicity of the orbitals, the volume of the unit cell, the number of k-point in the "perpendicular" grid, and some aspects of the symmetry of the system. More information on this particular aspect of the Berry phase calculations can be found in references .

## Related tags and articles

IGPAR, DIPOL, NPPSTR, LCALCPOL, LCALCEPS, LCALCEPS, ICHARG, ISPIN

Examples that use this tag

## References

---
