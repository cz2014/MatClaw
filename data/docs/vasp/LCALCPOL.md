# LCALCPOL

Categories: INCAR tag, Linear response, Dielectric properties, Berry phases

LCALCPOL = .TRUE. | .FALSE.  
 Default: **LCALCPOL** = .FALSE.

Description: LCALCPOL=.TRUE. switches on the evaluation of the Berry phase expressions for the macroscopic electronic polarization in accordance with the so-called Modern Theory of Polarization.

---

For LCALCPOL=.TRUE., VASP calculates the electronic contribution to the polarization, along the three reciprocal lattice vectors **G**i, i=1,2,3, (i.e. Σi **P**·**G**i) in a single run (unlike LBERRY=.TRUE.).

### An example: The fluorine displacement dipole (Born effective charge) in NaF

* With INCAR file:

```
PREC = Med
EDIFF= 1E-6

ISMEAR = 0
DIPOL  = 0.25 0.25 0.25

LCALCPOL = .TRUE.
```

* KPOINTS file:

```
6x6x6
 0
Gamma
 6 6 6
 0 0 0
```

* POSCAR file:

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

* and LDA Na\_sv and F PAW datasets.

The OUTCAR file should now contain the following lines:

```
            Ionic dipole moment: p[ion]=(     2.25510     2.25510     2.25510 ) electrons Angst

 Total electronic dipole moment: p[elc]=(     0.00000     0.00000     0.00000 ) electrons Angst
```

Here the units "electrons Angst" denote $e\AA=-1.602 10^{-19}C\AA$.

To calculate the change in the electronic polarization of NaF due to the displacement of the fluorine sublattice we repeat the previous calculation with the following POSCAR file:

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

The OUTCAR should now contain something very similar to the following lines:

```
            Ionic dipole moment: p[ion]=(     2.25510     2.25510     1.93939 ) electrons Angst

 Total electronic dipole moment: p[elc]=(     0.00000     0.00000     0.36061 ) electrons Angst
```

From the above one easily recognizes that the change in the electronic dipole moment due to the F-sublattice displacement is:

$\Delta\mathrm{p[elc]}=0.3606\hat{z}\;e\AA$

and the corresponding change in the ionic dipole moment:

$\Delta\mathrm{p[ion]}=1.93939-2.25510=-0.31571\hat{z}\;e\AA$

Thus the total change is found to be:

$\Delta\mathrm{p[tot]}=0.36061-0.31571=0.0449\hat{z}\;e\AA$

and considering that the F-sublattice was displaced by 0.045102 Å these calculations yield a Born effective charge for fluorine of

$Z^\*=0.0449/0.045102=-0.995|e|\;$.

The socalled parallel or $\mathbf{G}\_{\parallel}$
direction in the integration over the reciprocal space unit cell is set in IGPAR.

## Related tags and articles

LCALCEPS,
EFIELD\_PEAD,
LPEAD,
IPEAD,
LBERRY,
IGPAR,
NPPSTR,
DIPOL,
Berry phases and finite electric fields

Examples that use this tag

---
