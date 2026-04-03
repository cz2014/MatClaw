# PRJCAR

Categories: Files, Output files, Crystal momentum

The PRJCAR file stores the output of the **k**-point projection scheme (for LKPROJ=.TRUE.).

---

It has the following format:

* The header section lists the basis vectors of the reciprocal space belonging to the structure defined in the POSCAR.prim file, and a list of the set of points {**k′**}, the projection scheme has found in the irreducible part of the Brillouin (IBZ) zone of the aforementioned reciprocal space cell (see the section on LKPROJ).

* The body of the PRJCAR file lists:

:   $$\Kappa\_{n\mathbf{k}\sigma\mathbf{k}'}=\sum\_{\mathbf{GG}'}
    |\langle \mathbf{k}'+\mathbf{G}'| \mathbf{k}+\mathbf{G}\rangle
    \langle \mathbf{k}+\mathbf{G} | \Psi\_{n\mathbf{k}\sigma}\rangle |^2$$

:   where *n* is the band index, **k** labels the NKPTS points in the IBZ of the structure defined by the POSCAR file, σ is the spin index, and **k′** refers to the NKPTS\_PRIME points in the IBZ of POSCAR.prim (see the section of LKPROJ).
:   For each band *n* at **k**σ the body of the PRJCAR lists the index *n* and eigenenergy εn**k**σ, followed by one or more rows with a total of NKPTS\_PRIME entries Kn**k**σ**k′**, one for each point **k′**.

## Related Tags and Sections

LKPROJ
