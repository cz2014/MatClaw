# Phonons from finite differences

Categories: Phonons, Howto

The phonon calculations using a finite differences approach are carried out by setting **IBRION**=5 or 6 in the INCAR file.
When these tags are set, the second-order force constants are computed using finite differences. The dynamical matrix is constructed, diagonalized and the phonon modes and frequencies of the system are reported in the OUTCAR file.
If ISIF>=3, the internal strain tensors are computed as well.

> **Mind:** Only zone-center (Γ-point) frequencies are calculated.

It is possible to obtain the phonon dispersion at different **q** points by computing the second-order force constants on a sufficiently large supercell and Fourier interpolating the dynamical matrices in the unit cell.

## Input

There are two options to compute the second-order force constants using finite differences:

* IBRION=5, all atoms are displaced in all three Cartesian directions, resulting in a significant computational effort even for moderately sized high-symmetry systems.
* IBRION=6, only symmetry inequivalent displacements are considered, and the remainder of the force-constants matrix is filled using symmetry operations.

POTIM determines the step size. If too large values are supplied in the input file, the step size defaults to 0.015 Å (starting from VASP.5.1). Expertise shows that this is a very reasonable compromise.

The NFREE tag determines how many displacements are used for each direction and ion:

* NFREE=2 uses central differences, *i.e.*, each ion is displaced by a small positive and negative displacement, ±POTIM, along each of the Cartesian directions.
* NFREE=4 uses four displacements along each of the Cartesian directions ±POTIM and ±2×POTIM.
* NFREE=1 uses a single displacement (this is strongly discouraged).

If ISIF>=3, the elastic and internal strain tensors are computed.

The selective dynamics mode of the POSCAR file is presently only supported for IBRION=5; in this case, only those components of the Hessian matrix are calculated for which the selective dynamics tags are set to .TRUE. in the POSCAR file.

> **Important:** The selective dynamics always refer to the Cartesian components of the Hessian matrix, contrary to the behavior during ionic relaxation.

For the following POSCAR file, for instance,

```
Cubic BN
   3.57
 0.0 0.5 0.5
 0.5 0.0 0.5
 0.5 0.5 0.0
   1 1
selective
Direct
 0.00 0.00 0.00  F F F
 0.25 0.25 0.25  T F F
```

atom 2 is displaced in the *x*-direction only, and only the *x*-component of the second atom of the Hessian matrix is calculated.

If LEPSILON=.TRUE. or LCALCEPS=.TRUE., additional dielectric properties are computed.

## Output

The phonon modes and frequencies are written to the OUTCAR file after the following lines:

```
 Eigenvectors and eigenvalues of the dynamical matrix
 ----------------------------------------------------
```

The following lines are repeated for each normal mode and should look like the following example output:

```
   1 f  =   14.329944 THz    90.037693 2PiTHz  477.995462 cm-1    59.263905 meV
             X         Y         Z           dx          dy          dz
      0.000000  0.000000  0.000000     0.009046   -0.082007   -0.006117
      0.000000  2.731250  2.731250     0.009046    0.106244    0.006563
      0.000000  5.462500  5.462500     0.009046    0.082007    0.006117
      0.000000  8.193750  8.193750     0.009046   -0.106244   -0.006563
      ...
   2 f  =   14.329944 THz    90.037693 2PiTHz  477.995462 cm-1    59.263905 meV
             X         Y         Z           dx          dy          dz
      0.000000  0.000000  0.000000     0.003458    0.021825   -0.093181
      0.000000  2.731250  2.731250     0.003458    0.005416    0.094689
      0.000000  5.462500  5.462500     0.003458   -0.021825    0.093181
      0.000000  8.193750  8.193750     0.003458   -0.005416   -0.094689
      ...
   ...
```

The first number is the label of the normal mode. If this number is followed by *f* it is a purely real mode, stating the mode is vibrationally stable. Otherwise, if it is followed by *f/i*, the mode is an imaginary mode ("soft mode"). These labels are followed by the eigenfrequency of the mode in different units.

The following table labeled by (*x,y,z,dx,dy,dz*) contains the Cartesian positions of the atoms and the normalized eigenvectors of the eigenmodes in Cartesian coordinates.

There should be 3$N$ normal modes, where $N$ is the number of atoms in the supercell (POSCAR). The modes are ordered in descending order with respect to the eigenfrequency. The last three modes are the translational modes (they are usually disregarded).

Finally, IBRION=6 and ISIF≥3 allows to calculate the elastic constants. The elastic tensor is determined by performing six finite distortions of the lattice and deriving the elastic constants from the strain-stress relationship. The elastic tensor is calculated both, for 'clamped' ions, as well, as allowing for relaxation of the ions. The elastic moduli for rigid ions are written after the line

```
SYMMETRIZED ELASTIC MODULI (kBar)
```

The ionic contributions are determined by inverting the ionic Hessian matrix and multiplying with the internal strain tensor, and the corresponding contributions are written after the lines:

```
ELASTIC MODULI CONTR FROM IONIC RELAXATION (kBar)
```

The final elastic moduli, including both, the contributions for distortions with rigid ions and the contributions from the ionic relaxations, are summarized at the very end:

```
TOTAL ELASTIC MODULI (kBar)
```

There are a few caveats to this approach: most notably, the plane-wave cutoff (ENCUT) needs to be sufficiently large to converge the stress tensor. This is usually only achieved if the default cutoff is increased by roughly 30%, but it is strongly recommended to increase the cutoff systematically, (e.g., in steps of 15%), until full convergence is achieved.

## Practical hints

The computation of the second-order force constants requires accurate forces.
Therefore, the tag PREC=Accurate is recommended in the INCAR.
The ADDGRID=TRUE should **not** be set without careful testing.

A practical way to check for convergence is to monitor the Γ point (**q**=0) optical mode frequencies while varying the ENCUT, PREC, and **k** point density (KPOINTS). Additionally, compare the result to phonons from density-functional-perturbation theory (DFPT).

To get the phonon frequencies quickly on the command line, simply type the following:

```
grep THz OUTCAR
```

To get an accurate phonon dispersion, perform the force-constants calculation in a large enough supercell.
When increasing the size of the supercell, we recommend decreasing the **k**-point density in the KPOINTS file to yield the same resolution.
For example, for the primitive cell of silicon, a 12x12x12 Gamma-centered **k**-point mesh is needed to obtain accurate phonon frequencies at the Gamma point. When replicating the unit cell to a 2x2x2 supercell, a 6x6x6 **k** point mesh will produce an equivalent sampling. For a 4x4x4 supercell, a 3x3x3 **k** point mesh will suffice.

It is possible to use phonopy to post-process the results of a finite differences calculation done with VASP.

> **Tip:** In contrast to computing phonons within DFPT, the finite difference approach can be used in combination with any Exchange-correlation functional.

IBRION=5, is available as of VASP.4.5, IBRION=6 starting from VASP.5.1.
In some older versions (pre VASP.5.1), NSW (number of ionic steps) must be set to 1 in the INCAR file, since NSW=0 sets the IBRION=−1 regardless of the value supplied in the INCAR file.
Although VASP.4.6 supports IBRION=5-6, VASP.4.6 does not change the set of **k** points automatically (often the displaced configurations require a different **k**-point grid). Hence, the finite difference routine might yield incorrect results in VASP.4.6.

## Related tags and sections

IBRION,
ISIF,
POTIM,
Phonons: Theory,
Phonons from density-functional-perturbation theory

## References
