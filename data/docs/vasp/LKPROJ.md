# LKPROJ

Categories: INCAR tag, Crystal momentum

LKPROJ = .TRUE. | .FALSE.  
 Default: **LKPROJ** = .FALSE.

Description: switches on the **k**-point projection scheme.

---

For LKPROJ=.TRUE., VASP will project the orbitals onto the reciprocal space of an alternative unit cell.
This unit cell has to be supplied in the file POSCAR.prim, in the usual POSCAR format.

As a first step, the **k**-projection scheme determines the set {**k′**}, of **k**-points in the irreducible part of the first Brillouin zone of the structure given in POSCAR.prim, for which

:   $$\langle \mathbf{k}'+\mathbf{G}' | \mathbf{k}+\mathbf{G}\rangle \neq 0$$

where **G** and **G′** are reciprocal space vectors in the reciprocal spaces of the structures specified in POSCAR and POSCAR.prim, respectively. As usual, the set of points {**k**} is specified in the KPOINTS file.
The set {**k′**} is written to the OUTCAR file. Look at the part of the OUTCAR following NKPTS\_PRIM.

Once the set {**k′**} has been determined VASP will compute the following

:   $$\Kappa\_{n\mathbf{k}\sigma\mathbf{k}'}=\sum\_{\mathbf{GG}'}
    |\langle \mathbf{k}'+\mathbf{G}'| \mathbf{k}+\mathbf{G}\rangle
    \langle \mathbf{k}+\mathbf{G} | \psi\_{n\mathbf{k}\sigma}\rangle |^2$$

and writes this information onto the PRJCAR and vasprun.xml files.

Kn**k**σ**k′** provides a measure of how strongly the orbital $\Psi$n**k**σ contributes at the point **k′** in the reciprocal space of structure POSCAR.prim.

One may, for instance, use this scheme to project the orbitals of a supercell onto the reciprocal space of a generating primitive cell.

> **Warning:** At the moment the **k**-point projection only works with NPAR=1.

> **Mind:** Available as of VASP version 6.0.0.

## Related tags and articles

PRJCAR

Examples that use this tag
