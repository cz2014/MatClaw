# LASYNC

Categories: INCAR tag, Performance, Parallelization

LASYNC = [logical]  
 Default: **LASYNC** = .FALSE.

Description: Controls the overlap in communication.

---

If LASYNC=*.TRUE.* is set in the INCAR file, VASP will try to overlap communication with calculations.
This might improve performance or degrade it depending on the MPI library and hardware you are running on.
Please do your own testing and compare the runtimes and results before using this tag in production runs.
Compiling VASP using the -DPROFILING precompiler switch provides a detailed timing of the different VASP routines which helps in determining if there is a performance gain.
Please report any issues in the VASP forum.

Examples that use this tag

---
