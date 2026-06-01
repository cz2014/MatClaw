# ELPH_POT_GENERATE

Categories: INCAR tag, Electron-phonon interactions

ELPH\_POT\_GENERATE = [logical]  
 Default: **ELPH\_POT\_GENERATE** = False

Description: Calculates the electron-phonon potential from finite atomic displacements.

> **Mind:** Available as of VASP 6.5.0

---

Performing electron-phonon calculations using  many-body perturbation theory requires as input a phelel\_params.hdf5 file.
Setting `ELPH_POT_GENERATE = True` provides a way to generate the phelel\_params.hdf5 file directly in VASP by  computing the electron-phonon potential.
This is accomplished by using finite atomic displacements in a supercell.
Therefore, in addition to setting `ELPH_POT_GENERATE = True`, it is necessary to set `IBRION = 6` to activate the finite-difference routines.

> **Mind:** We currently do not support all symmetry operations when considering the atomic displacements for `ELPH_POT_GENERATE = True`. Therefore, more atomic displacements are generated compared to typical finite-difference calculations using `IBRION = 6`.

When `ELPH_POT_GENERATE = True`, VASP will additionally produce the CONTCAR\_ELPH file.
This file contains the primitive-cell crystal structure in the POSCAR format and can directly be used as input for the subsequent electron-phonon calculation.
The primitive cell is automatically determined by VASP during the supercell calculation, but can optionally be specified via the ELPH\_POT\_LATTICE tag.

Finally, the electron-phonon potential in the phelel\_params.hdf5 file is computed on a real-space FFT grid that has to match exactly the FFT grid dimensions (NGX, NGY, NGZ) of the primitive cell used in the subsequent electron-phonon calculation.
The dimensions of the FFT grid used to compute the electron-phonon potential can be chosen via the ELPH\_POT\_FFT\_MESH tag.
If one does not specify an FFT grid explicitly, VASP will determine the FFT grid dimensions automatically based on the current ENCUT.
This should produce an FFT mesh for the electron-phonon potential that is compatible with the FFT mesh used in a primitive-cell calculation at the same ENCUT.

> **Tip:** The PREC INCAR tag influences the size of the FFT mesh. Therefore, it is recommended to choose the same PREC for both the supercell as well as the primitive-cell calculation.

Basic information about the primitive-cell geometry and FFT grid is written to the OUTCAR file in the following format:

```
 Generation of phelel_params.hdf5
 ================================

Primitive cell 
   a1 =     1.78093078    1.78093078    0.00000000
   a2 =     0.00000000    1.78093078    1.78093078
   a3 =     1.78093078    0.00000000    1.78093078

Primitive FFT mesh =     18    18    18
```

It is also written to the machine-readable vaspout.h5 file at the following HDF5 paths:

```
results/elph_potential/primitive_positions
results/elph_potential/primitive_fft_mesh
```

This information is already contained within the generated phelel\_params.hdf5 file.
However, it is mirrored in the standard output to make it easier for users to check their calculations and to automate workflows.

## Related tags and articles

* ELPH\_POT\_LATTICE
* ELPH\_POT\_FFT\_MESH
* IBRION
* Electron-phonon potential from supercells
* phelel\_params.hdf5
* CONTCAR\_ELPH
