# Electrostatic corrections

Categories: Atoms and Molecules, 2D materials, Electrostatics, Howto

For charged cells or for calculations of molecules and surfaces with a large dipole moment, the energy converges very slowly with respect to the size $L$ of the supercell. Using methods discussed by Makov *et al.* and Neugebauer *et al.*, VASP can correct for the leading errors (in many details, we have taken a more general approach, though).

## Suggested combination of tags for electrostatic corrections

In cases where the system has no net charge and no net dipole moment, no specific tags need to be set and this section can be skipped.

### Bulk

If the system has a net dipole or net charge, please follow the recommendations of this wiki page.

### Surfaces

If the system has a net dipole moment, a combination of IDIPOL=1,2,3 and LDIPOL tags may be used. The former corrects the energies, while the latter corrects the potential and forces. Optionally, DIPOL may be set. The following options may be used to improve convergence for this case.

1. Use any of these tags only after pre-converging the orbitals without the LDIPOL tag

2. The center of charge should be set in the INCAR file (DIPOL= center of mass)

3. Ensure that the cell is sufficiently large to determine the dipole moment with sufficient accuracy (see DIPOL). If the cell is too small, the charge might slash through the vacuum, causing very slow convergence. Often convergence improves with the size of the supercell.

> **Warning:** Surface calculations with a net charge result in total energies that do not converge. Relative energies may still be useful.

### Wires

Not implemented.

### Molecules

If the system has a net dipole moment, use the LDIPOL tag. The former corrects the energies, while the latter corrects the potential and forces. Optionally, DIPOL may be set.

## Current limitations

For the current implementation, there are several restrictions; please read carefully:

* Charged systems:

:   Quadrupole corrections are only correct for cubic supercells (this means that the calculated 1/*L*3 corrections are wrong for charged supercells if the supercell is non-cubic). In addition, we have found empirically that for charged systems with excess electrons (NELECT>NELECTneutral) more reliable results can be obtained if the energy after correction of the linear error (1/*L*) is plotted against 1/*L*3 to extrapolate results manually for *L*→∞. This is due to the uncertainties in extracting the quadrupole moment of systems with excess electrons.

* Potential corrections are only possible for orthorhombic cells (at least the direction in which the potential is corrected must be orthogonal to the other two directions).

## Step-by-step instructions

### Using the dipole correction for slab calculations

In this section, we discuss step-by-step instructions to use the dipole corrections for slab calculations.

**Step 1:** Create a system which has enough vacuum on either side of the surface normal. An example for such a structure is shown below, for an fcc-Aluminium with a carbon adsorbed on one of its surface terminations.

```
Al3C
1.0000000000000000
   2.8637824638055176    0.0000000000000000    0.0000000000000000
   1.4318912319027588    2.4801083645679673    0.0000000000000000
   0.0000000000000000    0.0000000000000000   20.0000000000000000
Al C
3 1
Direct
   0.8333333333333333    0.5000000000000000    0.3380865704891008
   0.1666666666666666    0.8333333333333334    0.4550000000000000
   0.4999999999999999    0.1666666666666667    0.5719134295108992
   0.4999999999999999    0.1666666666666667    0.6619134295108993
```

Note that the system has plenty of vacuum on either side. This empty space is important for the potential corrections needed for the LDIPOL tag.

**Step 2:** Switch on the dipole corrections to the energy, potential and forces. Optionally set the DIPOL

```
LDIPOL    = T
IDIPOL    = 3
DIPOL     = 0.5 0.5 0.5
```

**Step 3 (Optional):** View the dipole moment for the system using the following bash command,

```
grep dipolmoment OUTCAR | tail -1
```

In this example, we get the following output:

```
 dipolmoment           0.000000      0.000000      0.128389 electrons x Angstroem
```

which refers to the dipole moment along the three axes. Consistent with the POSCAR used in this example, only the last axis has a non-zero dipole moment.

## Related Tags and Sections

NELECT,
EPSILON,
DIPOL,
IDIPOL,
LDIPOL,
LMONO,
EFIELD

## References
