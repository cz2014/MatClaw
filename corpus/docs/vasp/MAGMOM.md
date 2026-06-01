# MAGMOM

Categories: INCAR tag, Magnetism, Symmetry

MAGMOM = [real array]

|  |  |  |
| --- | --- | --- |
| Default: **MAGMOM** | = NIONS \* 1.0 | for ISPIN=2 |
|  | = 3 \* NIONS \* 1.0 | for noncollinear magnetic systems (LNONCOLLINEAR=.TRUE.) |

Description: Initial magnetic moment for each atom if no magnetization density is present. Considered when symmetry is determined.

---

* For a **magnetic calculation from scratch** (ISTART=0), MAGMOM specifies (i) the initial on-site magnetic moment for each atom, and (ii) lowers the symmetry of the system (as of VASP.4.4.4). A magnetic calculation could be either a spin-polarized calculation (ISPIN=2) or noncollinear calculation (LNONCOLLINEAR=T). If the MAGMOM line breaks a symmetry of the crystal, the corresponding symmetry operation is removed and not applied during the symmetrization of, e.g., charges and forces.

* When **restarting a magnetic calculation**, MAGMOM is only used to determine the symmetry of the system and not to set the on-site magnetic moment. Therefore, if you remove the MAGMOM tag before restarting from a converged WAVECAR or CHGCAR, the magnetization is likely to be symmetrized away.

* MAGMOM also specifies the initial on-site magnetic moments when a **magnetic calculation** (ISPIN=2 or LNONCOLLINEAR=T) is **started from a non-spin-polarized calculation** (ISPIN=1 and LNONCOLLINEAR=F). This implies restarting with ICHARG=1 while the CHGCAR file contains no magnetization density. Starting magnetic calculations from a non-spin-polarized calculation can improve convergence.

The I\_CONSTRAINED\_M tag can constrain the on-site magnetic moments.

> **Tip:** To converge to the magnetic ground state, we recommend setting the magnetic moments slightly larger than the expected values, e.g., using the experimental magnetic moment multiplied by 1.2-1.5. A growing collection of experimental data is available at the Bilbao crystallographic server. If no experimental data is available, MAGMOM can be defined according to the procedure outlined in the Huebsch et al. 2021.

> **Important:** The final magnetic state strongly depends on the initial values for MAGMOM. This is true even if no symmetry is used (ISYM=-1), because of the many local minima that most exchange-correlation functionals have within spin-density-functional theory.

## Format and basis

* For a spin-polarized calculation (ISPIN=2), MAGMOM is a list of NIONS positive or negative values that specify the magnitude and relative orientation of the magnetization on each ion. The on-site magnetic moments have no direction in real space, i.e., no orientation in the lattice.

* For noncollinear calculation (LNONCOLLINEAR=T), the on-site magnetic moment is specified by three components for each ion. Without spin-orbit coupling (LSORBIT=False), the total energy depends only on the relative direction of the on-site magnetic moments. Hence, you can give the desired magnetic structure in Cartesian coordinates without considering how the lattice matrix or SAXIS is defined.

* With spin-orbit coupling (LSORBIT=True), the three components must be specified in the basis of spinor space that is defined by SAXIS. The default is $\sigma\_1=\hat x$, $\sigma\_2 =\hat y$, $\sigma\_3 = \hat z$, such that MAGMOM can be given in Cartesian coordinates. The orientation of MAGMOM with respect to the lattice only matters if spin-orbit coupling is included (LSORBIT).

## Examples

* The most simple input for a bcc cell with antiferromagnetic (AFM) spin alignment would be the following.

:   POSCAR file:

```
AFM
 2.80000
 1.00000   .00000   .00000
  .00000  1.00000   .00000
  .00000   .00000  1.00000
 1 1
Cartesian
  .00000   .00000   .00000
  .50000   .50000   .50000
```

:   with

```
 ISPIN = 2
 MAGMOM = 1.0 -1.0
```

:   specified in INCAR. In a perfectly AFM ordered cell, the total net magnetisation is zero, but the local magnetic moments can be written to the OUTCAR file by setting LORBIT tag (and if LORBIT<10 , the RWIGS tag in addition) in the INCAR file.

* If you have problems converging to a desired magnetic solution, try to calculate first the non-magnetic ground state and continue from the generated WAVECAR and CHGCAR. To restart, e.g., a calculation with two atoms that have equally large and antiferromagnetically coupled on-site magnetic moments, you need to set the following in the INCAR file:

```
ICHARG = 1 
ISPIN = 2 
MAGMOM = m -m
```

:   or for a noncollinear

```
ICHARG = 1
LNONCOLLINEAR = T
MAGMOM = 0 0 m  0 0 -m
```

* For systems containing many atoms, MAGMOM input on a single line can be hard to read, especially in the noncollinear case. It is possible to provide INCAR input on multiple lines using backslashes (**\**) as linebreaks. E.g. for a noncollinear system with AFM alignment and 16 atoms (the first 8 of them magnetic), the multi-line input could look like this:

```
MAGMOM =  3.0  2.0  1.0 \
         -3.0 -2.0 -1.0 \
          3.0  2.0  1.0 \
         -3.0 -2.0 -1.0 \
          3.0  2.0  1.0 \
         -3.0 -2.0 -1.0 \
          3.0  2.0  1.0 \
         -3.0 -2.0 -1.0 \
          24*0.0
```

## Related Tags and Sections

ISPIN,
LNONCOLLINEAR, LSORBIT, SAXIS,
LORBIT,
I\_CONSTRAINED\_M

Examples that use this tag

---
