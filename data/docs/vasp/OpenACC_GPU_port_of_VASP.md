# OpenACC GPU port of VASP

Categories: VASP, Installation, Performance, GPU, Parallelization

With VASP.6.2.0 we officially released the OpenACC GPU-port of VASP:
Official in the sense that we now strongly recommend using this OpenACC version to run VASP on GPU accelerated systems.

The previous CUDA-C GPU-port of VASP is considered to be deprecated and is no longer actively developed, maintained, or supported.
As of VASP.6.3.0, the CUDA-C GPU-port of VASP has been dropped completely.

## Requirements

### Software stack

*Compiler*

* To compile the OpenACC version of VASP you need a recent version of the NVIDIA HPC-SDK (>=21.2).

:   In principle, any compiler that supports at least OpenACC standard 2.6 should do the trick, but we have only tried and tested the aforementioned ones.

:   > **Warning:** the NVIDIA HPC-SDK versions 22.1 and 22.2 have a serious bug that prohibits the execution of the OpenACC version in conjunction with OpenMP-threading. When using these compiler versions you should compile without OpenMP support. This bug is fixed as of NVIDIA HPC-SDK version 22.3.

*Libraries*

* Numerical libraries: FFTW, BLAS, LAPACK, and scaLAPACK. In case you are using the NVIDIA HPC-SDK the only numerical library you will have to install yourself is FFTW. The latter three (BLAS, LAPACK, and scaLAPACK) are shipped with the SDK. Alternatively, you can link against an installation of Intel's oneAPI MKL library that provides all four.
* The NVIDIA CUDA Toolkit (>=10.0). All necessary CUDA Toolkit components are shipped as part of the NVIDIA HPC-SDK.
* A CUDA-aware version of MPI. The OpenMPI installations that are packaged with the NVIDIA HPC-SDK are CUDA-aware. MPICH will also work on Cray machines, but the precompiler flag -DCRAY\_MPICH has to be added to the makefile.include.
* The NVIDIA Collective Communications Library (NCCL) (>=2.7.8). This library is not a strict requirement but its use is highly recommended for performance reasons. Suitable installations of NCCL are shipped as part of the NVIDIA HPC-SDK.

*Drivers*

* You need a CUDA driver that supports at least CUDA-10.0.

### Hardware

We have only tested the OpenACC GPU-port of VASP with the following NVIDIA GPUs:

* NVIDIA datacenter GPUs: P100 (Pascal), V100 (Volta), and A100 (Ampere).
* NVIDIA Quadro GPUs: GP100 (Pascal), and GV100 (Volta).

:   > **Important:** Running VASP on other NVIDIA GPUs (e.g. "gaming" hardware) is technically possible but not advisable: these GPUs are not well suited since they do not offer fast double-precision floating-point arithmetic (FP64) performance and in general have smaller memories without error correction code (ECC) capabilities.

## Building

To build the OpenACC port of VASP it is probably best to base your `makefile.include` file on one of the archetypical templates and adapt these to the particulars of your system.

## Features and limitations

* Most features of VASP have been ported to GPU using OpenACC, with the notable exception of everything involving the RPA: GW and ACFDT. This is work in progress.

* The use of parallel FFTs of the wave functions (NCORE>1) should be avoided for performance reasons. Currently, the OpenACC version will automatically switch to NCORE=1 even if otherwise specified in the INCAR file.

* **Due to the use of NCCL, the OpenACC version of VASP may only be executed using a single MPI-rank per available GPU:**

:   Using NCCL has large performance benefits in the majority of cases. However, we are aware of the fact that for calculations on small systems it would be useful to retain the ability to have multiple MPI-ranks share a GPU, and plan to make the use of NCCL optional to remove this limitation.

## Running the OpenACC version

1. Use a single MPI rank per GPU (currently, the use of NCCL precludes the use of multiple ranks per GPU).
2. Use OpenMP threads in addition to MPI ranks to leverage more of the available CPU power. The OpenACC version is currently limited to the use of 1 MPI-rank/GPU, which means that potentially quite a bit of CPU power remains unused. Since there are still parts of the code that run CPU-side it can be beneficial to allow for the use of multiple OpenMP threads per MPI rank:
   * To see how to build VASP with OpenACC- *and* OpenMP-support have a look at the makefile.include.nvhpc\_ompi\_mkl\_omp\_acc file.
   > **Important:** Here we link against Intel's MKL library for CPU-sided FFTW, BLAS, LAPACK, and scaLAPACK calls and the Intel OpenMP runtime library (libiomp5.so). This is strongly recommended when compiling for Intel CPUs, especially when using multiple threads. To ensure that MKL uses the Intel OpenMP runtime library you need to set an environment variable, either by:
   >
   > :   ```
   >     export MKL_THREADING_LAYER=INTEL
   >     ```
   > :   or by adding:
   > :   ```
   >     -x MKL_THREADING_LAYER=INTEL
   >     ```
   > :   as an option to your `mpirun` command.

   * Correct placement and pinning of OpenMPI ranks and OpenMP threads onto the CPU cores can be a bit tricky, and depends on the particular flavor of MPI one uses.
3. To achieve the best performance it is important to chose KPAR and NSIM wisely. Unfortunately, the ideal values will depend on the particulars of your system, both in the sense of workload as well as hardware, so you will have to experiment with different settings. However, as a rule of thumb one can say:
   * Set KPAR to the number of GPUs (= MPI-ranks) you are going to use. This only makes sense, though, when the number of irreducible **k**-points in your calculation is more or less evenly dividable by KPAR, otherwise the distribution of the work over the MPI-ranks will be strongly imbalanced. This means your options in choosing this parameter are somewhat limited.
   * NSIM determines the number of bands that are optimized simultaneously in many of the electronic solvers (e.g RMM-DIIS and blocked-Davidson). As a rule, one should choose this parameter larger to get good performance on GPUs than one would for CPU-sided execution.
   > **Warning:** For optimal CPU-sided execution of VASP one would normally experiment with different settings for NCORE as well. When running on GPUs anything different from NCORE=1 will adversely affect performance, and VASP will automatically switch to NCORE=1, even if otherwise specified in the INCAR file.

## Credits

A special thanks goes out to: Stefan Maintz, Markus Wetzstein, Alexey Romanenko, and Andreas Hehn from NVIDIA for all their help porting VASP to GPU using OpenACC!

## Related articles

Installing VASP.6.X.X,
makefile.include,
Compiler options,
Precompiler options,
Linking to libraries,
Toolchains,
Combining MPI and OpenMP,
Validation tests,
Known issues

---
