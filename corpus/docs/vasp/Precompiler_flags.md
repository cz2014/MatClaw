# Precompiler options

Categories: VASP, Installation, Performance, GPU

Precompiler flags are used to activate/deactivate certain code features at the time of compilation, e.g., the use of MPI, the advanced molecular dynamics features, etc. Many precompiler flags are set by default in the templates
provided for the makefile.include file. The commands are as follows:

CPP
:   The command to invoke the precompiler you want to use, for instance:

    * Using Intel's Fortran precompiler:
:   ```
    CPP=fpp -f_com=no -free -w0 $*$(FUFFIX) $*$(SUFFIX) $(CPP_OPTIONS)
    ```

:   * Using cpp:
:   ```
    CPP=/usr/bin/cpp -P -C -traditional $*$(FUFFIX) >$*$(SUFFIX) $(CPP_OPTIONS)
    ```

:   > **Mind:** This variable has to include `$(CPP_OPTIONS)`. If not, `CPP_OPTIONS` will be ignored!

CPP\_OPTIONS
:   Specify the precompiler flags:

:   ```
    CPP_OPTIONS=[-Dflag1 [-Dflag2] ... ]
    ```

:   > **Mind:** `CPP_OPTIONS` is only used in makefile.include, where it is added to the `CPP` variable.

## Default

### -DHOST=[string]

:   A string (20 characters max.) that describes the platform on which VASP is compiled, e.g.,  `-DHOST=\"LinuxIFC\"` for a Linux host using an Intel Fortran compiler.

### -DMPI

:   (Mandatory) Set this to compile the parallel version of VASP.

### -Duse\_collective

:   Set this to use MPI collectives in the all-to-all communication and global summations.
:   In case one specifies this, the value of MPI\_BLOCK (below) will be meaningless.

### -DMPI\_BLOCK=[integer]

:   Specifies the block size used by the in-house MPI all-to-all communication and global summations.

### -DscaLAPACK

:   Set this to use scaLAPACK.

### -DCACHE\_SIZE=[integer]

:   Specifies the size of the cache memory. Only used by the in-house real-to-complex FFT routines (fft3dlib.F).
:   By default these are no longer used, instead we use the real-to-complex FFT routines from fftw3.

### -Davoidalloc

:   Set this to use automatic instead of allocatable arrays in many routines related to the real space projection operators. This option is by default set in all our provided makefiles, and is highly suggested to enable this option.

### -Dvasp6

:   Set this to activate all VASP.6.X.X specific features.

### -Dtbdyn

:   Adds the advanced molecular dynamics routines.

### -Dfock\_dblbuf

:   Uses double buffer technique for the computation of exchange potential. Available as of VASP.6, N/A for the CUDA-C GPU-port.

### -D\_OPENMP

:   (Optional ) Switch on a combination of MPI and OpenMP for the parallelization.

## Specific for the OpenACC port to GPUs

### -DACC\_OFFLOAD

:   Mandatory for openACC starting from version 6.5.0: Activate all OpenACC-related code paths.

### -DNVCUDA

:   Mandatory: Activate when compiling the OpenACC offloading with the Nvidia compiler suite nvhpc (new in VASP version 6.5.0).

### -DUSENCCL

:   Mandatory: Use the NVIDIA Collective Communications Library (NCCL) instead of MPI for relevant instances of collective reduction operations (MPI\_Allreduce).

### -Dqd\_emulate

:   Mandatory: To compile the OpenACC GPU-port you need either the NVIDIA HPC-SDK or a recent version (>= 19.10) of PGI's Compilers & Tools. Both of these compilers do not natively support quadruple precision and require the use of the QD library to emulate quadruple precision arithmetic.

### -DCRAY\_MPICH

:   Mandatory for Cray machines: When compiling on a Cray machine, this flag deactivates a check to determine if the MPI version used is CUDA aware, which fails for MPICH. If MPICH is not used, this flag should not be set.

## Optional

### -DVASP\_HDF5

:   (Strongly recommended) Set this to add HDF5 support. This option has been available since VASP 6.2.0.
:   **N.B.**: one needs to add HDF5 to makefile.include.

### -Duse\_shmem

:   Use shared-memory segments to reduce the memory demands of GW (ALGO = EVGW0, EVGW, QPGW0, and QPGW) and machine-learned–force-field calculations.

### -Dshmem\_bcast\_buffer

:   Use shared-memory segments to reduce the amount of MPI communication in hybrid-functional calculations.

### -Dshmem\_rproj

:   Use shared-memory segments to reduce the storage demands of the real-space PAW projectors.

### -Dsysv

:   Use ipcs shared-memory segments and system-V semaphores.

### -DVASP2WANNIER90

:   Set this to include the interface between VASP and Wannier90.

> **Deprecated:** For VASP<6.2.0, see -DVASP2WANNIER90 and -DVASP2WANNIER90v2 in the deprecated section below!

### -Dlibbeef

:   Set this to include the GGA BEEF functional (corresponds to GGA=BF).
:   **N.B.**: one needs to add libbeef to makefile.include.

### -DDFTD4

:   Set this to include the DFT-D4 van der Waals functional.
:   **Note** that you need to install DFT-D4 and add it to the makefile.include.

### -DLIBMBD

:   Set this to include the library libMBD of many-body dispersion (MBD) methods for van der Waals interactions.
:   **Note** that you need to install LibMBD and add it to the makefile.include.

### -DSCPC

:   Set this to include the self-consistent potential-correction (SCPC) method.
:   **Note** that you need to install SCPC and add it to the makefile.include.

### -DPROFILING

:   Switches on detailed profiling of the code. This carries a (slight) performance penalty.

### -DUSELIBXC

:   Set this to include the library of exchange-correlation functionals Libxc.
:   **Note** that you need to install Libxc >= 5.2.0 (or the master version from gitlab for the latest implemented functionals) with the option `--disable-fhc` and add this to the makefile.include.

### -DELPA

:   Set this to include the library of ELPA eigenvalue solvers.
:   **N.B.**: one needs to add ELPA to makefile.include.

### -DLAPACK36

:   Required for LAPACK-3.6.0 and newer to replaced deprecated routine DGEGV by DGGEV.

## Deprecated

:   > **Deprecated:** `-DNGZhalf`, `-DwNGZhalf`, `-DNGXhalf`, `-DwNGXhalf` are deprecated options. Building the standard, gamma-only, or non-collinear version of the code is specified through an additional argument to the make command as discussed in Installing VASP.6.X.X.

### -D\_OPENACC

:   > **Deprecated:** This precompiler flag has been deprecated since version 6.5.0. It has been replaced by -DACC\_OFFLOAD

:   Mandatory for openACC before version 6.5.0: Activate all OpenACC-related code paths.

### -DUSENCCLP2P

:   > **Deprecated:** This precompiler flag has been deprecated since version 6.4.0.

:   Optional but strongly recommended for VASP versions < 6.4.0; (requires NCCL >= 2.7.8): Use the NVIDIA Collective Communications Library (NCCL) instead of MPI for relevant instances of all-to-all operations (MPI\_Alltoallv).

### -DnoAugXCmeta

:   This option was added to compute the meta-GGA contributions from the non-augmented pseudo density (instead of the augmented density). There is a condition concerning the behavior of the von-Weizsäcker kinetic energy density (calculated using the first derivative of the charge density) and the kinetic energy density computed from the orbitals ingrained into TPSS and revTPSS. This condition can be strongly violated when one augments the charge density. For the TPSS and revTPSS the functionals can become unstable in those cases. SCAN and its derivates (RSCAN, R2SCAN, etc) do not assume the aforementioned conditions to be met and remain stable for the augmented density as well so this option should not be used as it may negatively affect the final results.

### -DVASP2WANNIER90 and -DVASP2WANNIER90v2

:   Set this to include the interface between VASP and Wannier90.
:   Up to VASP 6.1.x you need to set -DVASP2WANNIER90 to interface with Wannier90 v.1.x, and -DVASP2WANNIER90v2 for Wannier90 v.2.x, and add the Wannier90 library to makefile.include.
:   Since VASP 6.2.0 you need to set -DVASP2WANNIER90 to interface with Wannier90 v.2.x or v.3.x.

## Related articles

Installing VASP.6.X.X,
makefile.include,
Compiler options,
Linking to libraries,
OpenACC GPU port of VASP,
Toolchains,
Validation tests,
Known issues

---
