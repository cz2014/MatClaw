# Command-line arguments

Categories: Calculation setup

You provide command line arguments to the VASP executables.
These options give you access to some build information about the executables without the need to provide all necessary input files to run VASP.
You can also use the dry run mode to quickly check the sanity of your input files.

## --cpp-options / -c

Print the CPP\_OPTIONS set in the makefile.include during the build of the executable to the standard output.
The code exits after printing the CPP\_OPTIONS.

## --dry-run / -n

Execute most of VASP setup routines but stop before doing any of the computational expensive tasks.
Use this mode to quickly test whether your input files are correct e.g. before submitting the job to the queue of an HPC.
Among other things, this mode will:

* Assess your setup and inform you if the version of VASP is incompatible. This could be if you try to run the Γ-point version with multiple **k** points or the standard version with spin-orbit coupling.

* Check whether your INCAR file can be parsed and understood. This can catch issues where you assigned a tag to an inappropriate type e.g. ENCUT=F. The beginning of the OUTCAR file reports also the interpretation of the INCAR file and the parameters of the run which you can inspect for consistency.

* Notify you about potential issues in your POSCAR file. This includes incorrect formatting, missing atoms or types, and too small distances between atoms.

* Parse the KPOINTS file to the IBZKPT file. If the parsing fails you can correct the KPOINTS setup. The IBZKPT reports the number of irreducible **k** points. You can use this information to choose an adequate KPAR setting.

* Read the POTCAR file to detect mismatches with the POSCAR file.

> **Tip:** The output of a dry-run will typically not produce output that postprocessing tools can understand. You may consider ALGO=None as an alternative.

## --link-line / -l

Print the LLIBS set in the makefile.include during the build of the executable to the standard output. The code exits after printing the LLIBS.

## --version / -v

Print the version string of this VASP executable.
In addition, report when the VASP executable was build and whether this is a gamma-only or a complex version of VASP.

---
