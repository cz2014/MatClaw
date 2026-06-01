# ELPH_POT_FFT_MESH

Categories: INCAR tag, Electron-phonon interactions

ELPH\_POT\_FFT\_MESH = [real real real]

Description: Specifies the FFT mesh for mapping the electron-phonon potential to the primitive cell.

> **Mind:** Available as of VASP 6.5.0

---

Once the electron-phonon potential has been computed in the supercell, it needs to be mapped to the primitive cell.
By default, VASP chooses the primitive-cell FFT mesh to be consistent with the current ENCUT.
However, sometimes it might be necessary to specify the FFT grid dimensions manually via ELPH\_POT\_FFT\_MESH.

The chosen values must be the same as the desired NGX, NGY and NGZ of the electron-phonon calculation in the primitive cell.

> **Tip:** In order to find the FFT grid dimensions corresponding to the primitive cell, you can start a minimal VASP calculation in the primitive cell and extract the values for NGX, NGY and NGZ from the OUTCAR file.

## Related tags and articles

* ELPH\_POT\_GENERATE
* ELPH\_POT\_LATTICE
* phelel\_params.hdf5
* CONTCAR\_ELPH
* Electron-phonon potential from supercells
