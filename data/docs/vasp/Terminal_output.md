# Terminal output

Categories: Output files

The screen output of VASP consists of several sections and can contain important warnings and error messages.

> **Tip:** Check the **stdout** (or OUTCAR) for warning messages after a calculation finishes. Often a small oversight can lead to plausible, but incorrect results.

## The header

The header has a few sections, that may or may not get printed depending on the calculation. Additional information and warnings may be present depending on the calculation and setup. Some common blocks are described below.

### No of nodes, MPI ranks, OpenMP threads, and parallelization

The first output details rank, threading, and  parallelization information.
E.g. with `KPAR = 4` and OpenMP threading:

```
running   16 mpi-ranks, with    4 threads/rank, on    1 nodes
distrk:  each k-point on    4 cores,    4 groups
distr:  one band on    1 cores,    4 groups
```

or without OpenMP threading, but `KPAR = 1` and `NCORE = 4`

```
running   16 mpi-ranks, with    1 threads/rank, on    1 nodes
distrk:  each k-point on   16 cores,    1 groups
distr:  one band on    4 cores,    4 groups
```

### GPU detection

If the executable is  installed with  support for GPU offloading, and VASP can detect the GPUs on the execution node, it will be mentioned here:

```
Offloading initialized ...    2 GPUs detected
```

### Version number, build date, and executable type

Note that both the standard and the  noncollinear version print out "complex", while the gamma-only version prints "gamma-only":
`vasp_std` and `vasp_ncl`:

```
vasp.6.4.3 19Mar24 (build Sep 03 2024 17:30:01) complex
```

`vasp_gam`:

```
vasp.6.5.0 16Dec24 (build Feb 28 2025 14:30:48) gamma-only
```

### Structure information

```
POSCAR found type information on POSCAR CoSiTi
POSCAR found :  3 types and       4 ions
```

### ScaLAPACK

This line is present if VASP is installed with  ScaLAPACK support.

```
scaLAPACK will be used
```

### LDA part of correlation

The following line prints the implementation selected for the LDA XC energy. E.g.:

```
LDA part: xc-table for (Slater+PW92), standard interpolation
```

or

```
LDA part: xc-table for (Slater(with rela. corr.)+CA(PZ))
, standard interpolation
```

### Reading the WAVECAR header

If a WAVECAR is present, the header is read now

```
found WAVECAR, reading the header
```

If the no of **k**-points changed, a warning is printed here

```
number of k-points has changed, file:    20 present:     8
trying to continue reading WAVECAR, but it might fail
```

> **Warning:** If the no of **k** points changes, we recommend restarting from a CHGCAR file and not from the WAVECAR file.

In the case a WAVECAR is read in, but the number of **k**-points *NK1* has changed to *NK2*, the orbitals of the last **k**-point of the WAVECAR will be used for all remaining **k** points if *NK2*>*NK1*. If *NK2*<*NK1*, the first *NK2* **k**-points from the WAVECAR will be mapped to the new **k** points. In both cases the coordinates of **k** points are not considered.

### Input file check

If the  input files POSCAR, INCAR, and KPOINTS are consistent, the following line is printed

```
POSCAR, INCAR and KPOINTS ok, starting setup
```

### FFT planning

```
FFT: planning ... GRIDC
FFT: planning ... GRID_SOFT
FFT: planning ... GRID
```

### Reading WAVECAR and/or CHGCAR

Depending on the availability of the files and the setting of ISTART and ICHARG, the WAVECAR or CHGCAR are read.

```
reading WAVECAR
the WAVECAR file was read successfully
charge-density read from file: unknown
```

If the no of bands increased, this is printed

```
reading WAVECAR
random initialization beyond band           13
the WAVECAR file was read successfully
```

For `ISPIN = 2` the magnetization density can also be read from CHGCAR

```
reading WAVECAR
the WAVECAR file was read successfully
charge-density read from file: GaAs                                    
magnetization density read from file 1
```

## The body

After the line

```
entering main loop
```

the body of the **stdout** begins. It is essentially equivalent to the OSZICAR file. Please consult the OSZICAR page for an explanation of the presented data.

## Error and warning messages

Incorrect usage of INCAR tags will result in errors printed to **stdout**, and VASP will terminate immediately. E.g. `KPAR = .TRUE.` will result in:

```
 -----------------------------------------------------------------------------
|                                                                             |
|     EEEEEEE  RRRRRR   RRRRRR   OOOOOOO  RRRRRR      ###     ###     ###     |
|     E        R     R  R     R  O     O  R     R     ###     ###     ###     |
|     E        R     R  R     R  O     O  R     R     ###     ###     ###     |
|     EEEEE    RRRRRR   RRRRRR   O     O  RRRRRR       #       #       #      |
|     E        R   R    R   R    O     O  R   R                               |
|     E        R    R   R    R   O     O  R    R      ###     ###     ###     |
|     EEEEEEE  R     R  R     R  OOOOOOO  R     R     ###     ###     ###     |
|                                                                             |
|     Error reading item KPAR from file INCAR.                                |
|     Error code was IERR= 5 ... .                                            |
|                                                                             |
|       ---->  I REFUSE TO CONTINUE WITH THIS SICK JOB ... BYE!!! <----       |
|                                                                             |
 -----------------------------------------------------------------------------
```

If the problem is considered less severe, VASP will continue with the execution, but can display a warning. E.g. if the KPOINTS file is missing and KSPACING is not set in the INCAR file, VASP will execute with a default, quite coarse, mesh:

```
 -----------------------------------------------------------------------------
|                                                                             |
|           W    W    AA    RRRRR   N    N  II  N    N   GGGG   !!!           |
|           W    W   A  A   R    R  NN   N  II  NN   N  G    G  !!!           |
|           W    W  A    A  R    R  N N  N  II  N N  N  G       !!!           |
|           W WW W  AAAAAA  RRRRR   N  N N  II  N  N N  G  GGG   !            |
|           WW  WW  A    A  R   R   N   NN  II  N   NN  G    G                |
|           W    W  A    A  R    R  N    N  II  N    N   GGGG   !!!           |
|                                                                             |
|     The requested file  could not be found or opened for reading            |
|     k-point information. Automatic k-point generation is used as a          |
|     fallback, which may lead to unwanted results.                           |
|                                                                             |
 -----------------------------------------------------------------------------
```

Missing information on magnetic moments will result in, probably the wrong, automatic ferromagnetic initialization:

```
 -----------------------------------------------------------------------------
|                                                                             |
|           W    W    AA    RRRRR   N    N  II  N    N   GGGG   !!!           |
|           W    W   A  A   R    R  NN   N  II  NN   N  G    G  !!!           |
|           W    W  A    A  R    R  N N  N  II  N N  N  G       !!!           |
|           W WW W  AAAAAA  RRRRR   N  N N  II  N  N N  G  GGG   !            |
|           WW  WW  A    A  R   R   N   NN  II  N   NN  G    G                |
|           W    W  A    A  R    R  N    N  II  N    N   GGGG   !!!           |
|                                                                             |
|     You requested a magnetic or noncollinear calculation, but did not       |
|     specify the initial magnetic moment with the MAGMOM tag. Note that      |
|     a default of 1 will be used for all atoms. This ferromagnetic setup     |
|     may break the symmetry of the crystal, in particular it may rule        |
|     out finding an antiferromagnetic solution. Thence, we recommend         |
|     setting the initial magnetic moment manually or verifying carefully     |
|     that this magnetic setup is desired.                                    |
|                                                                             |
 -----------------------------------------------------------------------------
```

## Related tags and articles

OSZICAR, OUTCAR
