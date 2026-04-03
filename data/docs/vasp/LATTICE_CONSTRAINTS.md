# LATTICE_CONSTRAINTS

Categories: INCAR tag, Molecular dynamics, Symmetry

LATTICE\_CONSTRAINTS = [logical][logical][logical]

Description: Sets three boolean to selectively allow changes in the lattice vectors.

---

The lattice vectors $\mathbf{a}\_{1}$, $\mathbf{a}\_{2}$, $\mathbf{a}\_{3}$
defined in the POSCAR file can be represented by following matrix:

$\mathbf{A} =
\begin{bmatrix}
a\_{11} & a\_{12} & a\_{13} \\
a\_{21} & a\_{22} & a\_{23} \\
a\_{31} & a\_{32} & a\_{33}
\end{bmatrix}.$

LATTICE\_CONSTRAINTS is used to constrain certain entries of this matrix during an MD run.

## Orthorhombic case

For orthorhombic unit cells $\mathbf{A}$ is of diagonal form:

$\mathbf{A} =
\begin{bmatrix}
a\_{11} & 0 & 0 \\
0 & a\_{22} & 0 \\
0 & 0 & a\_{33}
\end{bmatrix},$

Therefore by setting one of the entries of LATTICE\_CONSTRAINTS to FALSE the lattice parameter in this direction will not be allowed to change.
For MD simulations (IBRION=0), we recommend using LATTICE\_CONSTRAINTS for (orthorhombic) liquids in the isobaric-isothermal (NpT) ensemble in the following way:

```
LATTICE_CONSTRAINTS = .FALSE. .FALSE. .TRUE.
```

Here, the first two lattice constants are not allowed to change. The third lattice constant needs to be free to allow volume changes for the barostat. The system is then like a piston. The constraints are necessary for liquids in NpT simulations because if all lattice degrees of freedom are allowed to relax, irreversible deformations of the cell are very likely to happen. This can lead to undesirable results like a very flat supercell, which cannot be used to obtain valid MD trajectories.

For structure relaxation (IBRION=1,2), LATTICE\_CONSTRAINTS is useful to relax the lattice constants of 2D materials. In case of a slab in the $\mathbf{a}\_1$-$\mathbf{a}\_2$ plane, add vacuum padding along $\mathbf{a}\_3$ and set

```
LATTICE_CONSTRAINTS = .TRUE. .TRUE. .FALSE.
```

## Non-orthorhombic case

For non-orthorhombic boxes LATTICE\_CONSTRAINTS is more complicated to use. The tag will set certain rows and columns of the stress tensor

$\mathbf{\sigma} =
\begin{bmatrix}
xx & xy & xz \\
yx & yy & yz \\
zx & zy & zz
\end{bmatrix},$

to zero. By setting certain entries of the stress tensor to zero the corresponding entries of the lattice $\mathbf{A}$ will not be updated.
For example when setting LATTICE\_CONSTRAINTS = .FALSE. .TRUE. .TRUE. the used stress tensor will look like

$\mathbf{\sigma} =
\begin{bmatrix}
0 & 0 & 0 \\
0 & yy & yz \\
0 & zy & zz
\end{bmatrix},$

and therefore the first row and the first column of the lattice $\mathbf{A}$ will not change.
Another example would be to set LATTICE\_CONSTRAINTS = .FALSE. .TRUE. .FALSE. resulting in the following
stress tensor

$\mathbf{\sigma} =
\begin{bmatrix}
0 & 0 & 0 \\
0 & yy & 0 \\
0 & 0 & 0
\end{bmatrix}$

So only the $yy$/$a\_{22}$ entry of the lattice $\mathbf{A}$ will change.

> **Mind:** Note that for non-orthorhombic boxes the angles between the lattice vectors $\mathbf{a}\_{1}$, $\mathbf{a}\_{2}$, $\mathbf{a}\_{3}$ will not be conserved.

> **Mind:** LATTICE\_CONSTRAINTS in combination with IBRION=1,2 is available from VASP 6.4.3.

> **Mind:** LATTICE\_CONSTRAINTS in combination with ISIF=4,5 is available from VASP 6.5.1.

> **Warning:** Be aware of a bug in versions < 6.5.0 as described in following forum post[1].

## Related tags and articles

IBRION, MDALGO, Interface pinning

Examples that use this tag

---
