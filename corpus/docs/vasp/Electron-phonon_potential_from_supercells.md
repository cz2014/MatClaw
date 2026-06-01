# Electron-phonon potential from supercells

Categories: Electron-phonon interactions, Howto

The computation of the electron-phonon potential, $\partial\_{\nu \mathbf{q}} V(\mathbf{r})$, is a prerequisite for the calculation of the electron-phonon matrix element:

:   :   $$g\_{mn \mathbf{k}, \nu \mathbf{q}}
        \equiv
        \langle
        \psi\_{m \mathbf{k} + \mathbf{q}} |
        \partial\_{\nu \mathbf{q}} V |
        \psi\_{n \mathbf{k}}
        \rangle
        .$$

$\partial\_{\nu \mathbf{q}} V$ is computed from a supercell calculation by means of Fourier interpolation while the Bloch orbitals, $\psi\_{n \mathbf{k}}(\mathbf{r})$, are computed directly in the primitive cell.
The supercell calculation and the primitive-cell calculation are performed in two separate VASP runs.
This page provides an overview of the supercell calculation and how the electron-phonon potential can be calculated.
For information regarding the electron-phonon calculation in the primitive cell, consult the documentation on phonon-induced bandstructure renormalization and on phonon-limited transport.

For the theory on the electron-phonon potential, see the end of the self-energy section of the theory page.

> **Mind:** Available as of VASP 6.5.0

> **Important:** This feature requires  HDF5 support.

> **Tip:** The entire workflow of initializing a calculation, computing the electron-phonon potential in the supercell and performing subsequent electron-phonon calculations in the primitive cell can be facilitated by velph. velph is a command-line tool included in the phelel python package. It helps guide you through the process step by step and ensures a certain level of consistency between the required VASP calculations.

## Finite displacements in the supercell

General workflow when running electron-phonon calculations using perturbation theory. Notice that both the "VASP only" workflow as well as the "VASP + phelel" workflow produce the same kind of data in phelel\_params.hdf5.

The electron-phonon potential is computed from finite atomic displacements in a sufficiently large supercell.
In this case, sufficient means that the effects of an atomic displacement become negligible at about half the supercell size.
Usually, converging the phonon frequencies is a good way of finding a supercell that is sufficiently large.
Polar materials can exhibit long-range electrostatic interactions that go beyond reasonable supercell sizes.
In this case, a correction scheme exists that explicitly treats the long-range dipole interactions and works with smaller cells.

Currently, there are two complementary ways to calculate the electron-phonon potential.
One relies solely on VASP, while the other uses VASP in combination with phelel.
Both approaches calculate the derivative of the Kohn-Sham potential in real space via the displacement of atoms.
However, they may differ in terms of flexibility and computational performance.
Below, we describe the general workflow of each approach and highlight their advantages and disadvantages.

Regardless of which approach is chosen, the output is always written to the phelel\_params.hdf5 binary file.
This file can then be read during a VASP calculation in the primitive unit cell to compute electron-phonon interactions.

### VASP internal driver

This way of calculating the electron-phonon potential is activated by setting `ELPH_POT_GENERATE = True` in the INCAR file.
It utilizes the VASP-internal finite-difference driver that is activated by setting `IBRION = 6` in the INCAR file.
The atomic displacement directions are automatically determined by VASP.
As usual, POTIM and NFREE can be used to control the displacement amount and finite-difference stencil, respectively.
This is the same procedure used to calculate phonons from finite differences and many of the same considerations regarding performance and accuracy apply in this case.
Therefore, phonon frequencies are a great way to test the convergence with respect to supercell size.

> **Mind:** Currently, VASP generates more displacements with `ELPH_POT_GENERATE = True` and `IBRION = 6` than would be required in principle. This will be improved in a future version of the code.

Once the electron-phonon potential is obtained, it is automatically mapped to the primitive cell.
The results are stored in the phelel\_params.hdf5 file.
By default, the primitive cell used for this mapping is the one determined by VASP during the supercell calculation.
It is possible to choose a different primitive unit cell by explicitly specifying its lattice vectors using the ELPH\_POT\_LATTICE INCAR tag.

> **Mind:** The cell specified via ELPH\_POT\_LATTICE must be a valid primitive cell of the underlying lattice.

In any case, the relevant primitive-cell structure is written to the CONTCAR\_ELPH file.
This file can be used as the POSCAR of the subsequent electron-phonon calculation in the primitive cell.
This way, it is guaranteed that the primitive-cell calculation is compatible with the information contained in the phelel\_params.hdf5 file.

The electron-phonon potential is stored on a real-space FFT grid in the phelel\_params.hdf5 file.
It is currently necessary to match the FFT grid dimensions of this potential to the FFT grid dimensions (NGX, NGY, NGZ) of the primitive cell that is used to perform the subsequent electron-phonon calculation.
By default, VASP determines appropriate FFT grid dimensions automatically during the supercell calculation based on the current ENCUT.
The result should be compatible with a primitive-cell calculation that uses the same ENCUT.

> **Tip:** The PREC INCAR tag influences the size of the FFT mesh. Therefore, it is recommended to choose the same PREC for both the supercell as well as the primitive-cell calculation.

It is possible to manually supply the FFT grid dimensions of the target unit cell during the supercell calculation via ELPH\_POT\_FFT\_MESH.

Information regarding the primitive cell and the FFT grid dimensions for electron-phonon calculations is also reported in the OUTCAR file and the vaspout.h5 file.
The format is explained on the ELPH\_POT\_GENERATE page.

### VASP and phelel

In this approach to calculating the electron-phonon potential, the ionic displacements are determined externally using phelel.
For people who are familiar with phonon calculations using VASP and phonopy, this workflow will look very familiar.
In general, this allows for greater flexibility.
Here, we demonstrate a common workflow that suffices for most purposes.
For a complete list of features, we refer to the documentation of phelel.

As an example,

```
phelel -d --dim 2 2 2 -c POSCAR-unitcell --pm
```

automatically determines displacement directions for a 2x2x2 supercell based on symmetry considerations.

> **Tip:** We recommend the use of the --pm option, which generates positive and negative displacements for each displacement direction.

For each displacement, phelel creates a corresponding supercell POSCAR file (POSCAR-XXX, where XXX labels the different displacements).
In addition, the file SPOSCAR is created which contains the supercell geometry in equilibrium.

For each of the generated POSCAR files, create a separate directory and run VASP there with `ELPH_PREPARE = True` set in the INCAR file.
This setting instructs VASP to write the potential as well as other important information to disk.
Finally, run phelel to combine all the data from the individual directories to obtain the electron-phonon potential, for example,

```
phelel --fft-mesh 18 18 18 --cd perfect/ disp-001/ disp-002/
```

Here, perfect, disp-001 and disp-002 are the directories corresponding to the equilibrium and displaced supercell calculations, respectively.
--fft-mesh specifies the FFT grid dimensions (NGX, NGY, NGZ) to be used in the final electron-phonon calculation in the primitive cell.
The electron-phonon potential is Fourier interpolated from the FFT grid in the supercell to the supplied grid via a non-uniform FFT.
The results are written to the phelel\_params.hdf5 file.

## Related tags and articles

* Band-structure renormalization
* Transport calculations
* phelel\_params.hdf5
* Electron-phonon interactions from Monte-Carlo sampling
