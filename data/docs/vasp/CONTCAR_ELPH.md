# CONTCAR ELPH

Categories: Files, Output files

The CONTCAR\_ELPH file is an output file of a supercell calculation that contains the structural information of the primitive cell required for electron-phonon calculations using many-body perturbation theory.

> **Mind:** Available as of VASP 6.5.1

This file has the same format as the CONTCAR or POSCAR file.
It is typically generated alongside the phelel\_params.hdf5 file by setting `ELPH_POT_GENERATE = True`.
The CONTCAR\_ELPH file can be renamed and used as the POSCAR input for a subsequent electron-phonon calculation in the primitive cell, e.g. band-structure renormalization or transport coefficients including electron-phonon scattering.

## Related tags and articles

* CONTCAR
* POSCAR
* ELPH\_POT\_GENERATE
* ELPH\_POT\_LATTICE

---
