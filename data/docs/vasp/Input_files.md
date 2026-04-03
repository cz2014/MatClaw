# Category:Input files

Categories: VASP, Files, Calculation setup

As a minimal setup, VASP requires the following **input files**:

* the INCAR file,
* the POSCAR file, and
* the POTCAR file.

However, there are more optional **input files**, e.g., the KPOINTS file, the KPOINTS\_OPT file, the ICONST file, etc. A complete list is provided below.

VASP calculations are often continued on top of a previous VASP calculation. So, in case a calculation is restated, the output files of the previous calculation can be **input files** for the next calculation. For instance, the CHGCAR file, the WAVECAR file, the CONTCAR file copied to POSCAR, the ML\_ABN file copied to ML\_AB, etc.

When HDF5 support is enabled, the vaspin.h5 file can contain the same information and replace the INCAR, POSCAR, KPOINTS and POTCAR files.

Finally, there is a special **input file** to induce a *soft stop* of the calculation: the STOPCAR file. It is not used in a standard workflow, but it might be convenient to stop a calculation manually when it takes too long or a technical issue on the compute engine arises.
