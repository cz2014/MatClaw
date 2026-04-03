# IMAGES

Categories: INCAR tag, Transition states, Parallelization

IMAGES = [integer]  
 Default: **IMAGES** = 0

Description: Defines the number of VASP calculations in separate directories, (e.g., 01, 02, 03, etc.) for nudged elastic band calculations, parallel tempering, and thermodynamic integration.

---

IMAGES sets the number of independent VASP calculations in separate directories. The primary INCAR file should be located in the root directory.
Other files such as KPOINTS, POTCAR, and POSCAR can be placed in subdirectories, e.g., 01, 02, 03, etc., or in the root directory. Files in subdirectories take precedence over those in the root directory.

See use cases described below.

## File handling

When VASP starts, it reads the file INCAR in the root directory.
Subsequently, VASP splits the MPI communicator into subgroups for each image.
If an INCAR file is present in the subdirectories 01, 02, 03, ..., VASP will process those afterward.
Otherwise, VASP continues reading from the root INCAR file.
You can also provide image-specific data in the root INCAR file if the files are very similar

```
 # general INCAR tags
 IMAGES = 4
 TEBEG = 600
 
 # INCAR tags only on IMAGE 1
 IMAGE_1 {
   TEBEG = 400
 }
 
 # INCAR tags only on IMAGE 2
 IMAGE_2 {
   TEBEG = 500
 }
```

Here, images 3 and 4 would use TEBEG=600 because the value is not specified for the image.
The files KPOINTS and POTCAR will be read from the subdirectory if available and from the root directory otherwise.
The POSCAR file and all other input files are always read from the subdirectories.
All output files (including OUTCAR and OSZICAR) are always written to the subdirectories.

To summarize, to run a calculation with IMAGES, you provide:

* an INCAR file in the root directory
* optionally an overwriting INCAR file in the subdirectories
* POSCAR files in the subdirectories
* KPOINTS and POTCAR either in the root or in the subdirectories

## Use cases

Nudged elastic bands
:   If IMAGES is set without any other tag, an elastic-band calculation is performed. This defaults to the recommended nudged-elastic-band method, but other options are available by modifying the SPRING tag. Please consider the nudged-elastic-bands how-to and the SPRING tag for more information.

Thermodynamic coupling-constant integrations
:   When VCAIMAGES is set in the INCAR file, VASP computes a thermodynamic coupling-constant integration. This, in turn, sets IMAGES=2, running two VASP calculations in the subdirectories 01 and 02. Since this is a special case where the two calculations may have different computational costs, NCORE\_IN\_IMAGE1 can be set to force an unequal split of the processes across the two images. The tag VCAIMAGES describes in more detail how to set up these calculations.

Parallel tempering/replica-exchange method and performing independent calculations
:   If the tag LTEMPER=.TRUE. is set in the INCAR file, VASP will perform parallel tempering calculations. In this case, it is necessary to provide different POSCAR files in each subdirectory and modify the TEBEG either by separate INCAR files or nested IMAGE\_*X*/TEBEG definitions in the root INCAR file. For further details, refer to the description of the LTEMPER tag. The combination LTEMPER=.TRUE. and NTEMPER=0, also allows to run entirely independent calculations in the individual subdirectories. This might be helpful to make better use of nodes with many cores.

## Related tags and articles

VCAIMAGES,
LTEMPER,
nudged-elastic-bands how-to,
SPRING

Examples that use this tag

---
