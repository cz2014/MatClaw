# ELPH_POT_LATTICE

Categories: INCAR tag, Electron-phonon interactions

ELPH\_POT\_LATTICE = [3x3 real]

Description: Allows specifying an alternative primitive cell for the mapping of the electron-phonon potential.

> **Mind:** Available as of VASP 6.5.0

---

Once the electron-phonon potential has been computed in the supercell, it needs to be mapped to the primitive cell.
This is done via `ELPH_POT_GENERATE = True`.
By default, VASP performs the mapping for the primitive cell that is found by the symmetry routines and that is reported in the OUTCAR file.
In cases where the primitive cell needs to be specified manually, ELPH\_POT\_LATTICE can be used.

`ELPH_POT_LATTICE = a1x a1y a1z a2x a2y a2z a3x a3y a3z` specifies the three primitive lattice vectors $\mathbf{a}\_1$, $\mathbf{a}\_2$ and $\mathbf{a}\_3$ in Cartesian coordinates.
These lattice vectors are then used to construct the primitive-cell information in the phelel\_params.hdf5 file.

> **Mind:** The supplied lattice vectors must span a valid primitive cell of the supercell or the code will exit with an error.

> **Tip:** The primitive cell used for mapping is also written to the CONTCAR\_ELPH file, which can conveniently be used as the POSCAR input for the subsequent electron-phonon calculation. This ensures that the primitive-cell calculation is consistent with the information in the phelel\_params.hdf5 file.

## Related tags and articles

* ELPH\_POT\_GENERATE
* ELPH\_POT\_FFT\_MESH
* phelel\_params.hdf5
* CONTCAR\_ELPH
* Electron-phonon potential from supercells
