# ELPH_PREPARE

Categories: INCAR tag, Electron-phonon interactions

ELPH\_PREPARE = [logical]  
 Default: **ELPH\_PREPARE** = .FALSE.

Description: Writes the potential, the force-constants and other information related to electron-phonon interactions to the vaspout.h5 file.

> **Mind:** Available as of VASP 6.5.0

---

In order to calculate electron-phonon interactions, one must first perform finite-difference calculations in the supercell and generate the phelel\_params.hdf5 file.
To do this using phelel, it is necessary to provide additional supercell information to phelel.
This is accomplished by setting `ELPH_PREPARE = True` in each involved supercell calculation.
Afterwards, phelel can be used to calculate the required derivatives and produce the phelel\_params.hdf5 file.
For further information on this workflow, please consult the online documentation of phelel.

## Related tags and articles

* Electron-phonon potential from supercells
* phelel\_params.hdf5
