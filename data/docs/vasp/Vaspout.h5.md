# vaspout.h5

Categories: Files, Output files, HDF5 support

The vaspout.h5 file is a hierarchical HDF5 file containing the inputs and outputs of a VASP calculation.

To analyze the data in this file we recommend using py4vasp.

This file is only produced if your VASP version was compiled with HDF5 support.

## Contents of the file

At the highest level, the vaspout.h5 has the following HDF5 groups:

1. input - contains hierarchical versions of these files after parsing.
2. original - contains a textual copy of the KPOINTS, INCAR, POSCAR and POTCAR files that were provided to start the calculation.
3. intermediate - contains information from MD and ionic relaxation calculations, including the positions of the ions, forces, stresses, and total energies for each ionic step.
4. results - contains the final quantities of the calculation like the density of states, electronic eigenvalues, linear-response functions, etc...
5. version - keeps track of which version of VASP was used to produce this file. This is needed for compatibility reasons with older files.

## Related tags and sections

vaspin.h5, vaspwave.h5, OUTCAR
