# vaspin.h5

Categories: Files, Input files, HDF5 support

This file can be used to replace the typical INCAR, POSCAR, POTCAR, and KPOINTS files using a single HDF5 file.

Currently, we do not provide a tool to systematically create this file from scratch, instead, this feature is currently mostly intended to reproduce previous calculations.

A vaspout.h5 file that resulted from previous calculations can be renamed to vaspin.h5, copied to an empty directory, and used as input for a new VASP run.

## Related tags and articles

* Other important input files include INCAR, KPOINTS, POSCAR, and POTCAR
