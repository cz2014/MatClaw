# Toolchains

Categories: VASP, Installation, Performance, GPU

Below we list the toolchains (compilers + assorted libraries) that we have used to build and test VASP in our nightly tests during the development.
Starting from VASP.6.3.0, the toolchains are listed separately for each version of VASP.

* These lists of toolchains are not comprehensive. They show what we have employed on a regular basis. Other/newer versions of the compilers and libraries than those listed below will, in all probability, work just as well (or better).

:   > **Tip:** We encourage using up-to-date versions of compilers and libraries since they are continuously improved and bugs are identified and fixed.

* Also for older versions of VASP, we recommend using up-to-date versions of compilers and libraries. In most cases, this will not be a problem. Except in some cases, VASP code was adjusted, e.g., to accommodate changes in the behavior of a compiler. This happens when compilers became more strict and do not accept certain code constructs used in older VASP versions. Here are a few known examples:
  + Compilation with GCC > 7.X.X is only possible as of VASP.6.2.0 .
  + Compilation with GCC > 15.X.X is currently (as of VASP.6.5.1) not possible due to changes due to dropped legacy code support in C and Fortran formatted strings.

## VASP.6.5.0

| Compilers | MPI | FFT | BLAS | LAPACK | ScaLAPACK | OpenMP | CUDA | HDF5 | Other | Remarks | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intel-oneapi-compilers-2024.0.2 | intel-oneapi-mpi-2021.10.0 | intel-oneapi-mkl-2023.2.0 | | | | both | - | hdf5-1.14.0 | wannier90-3.1.0 libxc-5.2.3 | Rocky Linux 8.8 | - |
| gcc-11.2.0 | openmpi-4.1.2 | fftw-3.3.10 | openblas/0.3.18 | | netlib-scalapack-2.1.0 | yes | - | hdf5-1.13.0 | wannier90-3.1.0 libxc-5.2.2 | Rocky Linux 8.8 | - |
| gcc-11.2.0 | openmpi-4.1.2 | amdfftw/3.1 | amdblis/3.1 amdlibflame/3.1 | | amdscalapack/3.1 | yes | - | hdf5-1.13.0 | wannier90-3.1.0 libxc-5.2.3 | Rocky Linux 8.8 | - |
| gcc-12.3.0 | openmpi-4.1.6 | intel-oneapi-mkl-2023.2.0 | | | netlib-scalapack-2.2.0 | yes | - | hdf5-1.14.0 | wannier90-3.1.0 libxc-5.2.3 | Rocky Linux 8.8 | - |
| nvhpc-23.7 (OpenACC) | openmpi-4.1.6 (CUDA-aware) | intel-oneapi-mkl-2023.2.0 | | | netlib-scalapack-2.2.0 | yes | cuda-11.8 | hdf5-1.14.0 | wannier90-3.1.0 | Rock Linux 8.8 NVIDIA GPUs (A30) | not working with python plugins |
| aocc-4.0.0 | openmpi-4.1.3 | amdfftw-4.0 | amdblis-4.0 | amdlibflame-4.0 | amdscalapack-4.0 | yes | - | hdf5-1.13.0 | wannier90-3.1.0 libxc-5.2.2 | On AMD CPUs (Zen3) | Reduce optimization level |
| nec-5.0.1 | nmpi-2.25.0 | nlc-3.0.0 | | | netlib-scalapack-2.2.0 | no | - | - | wannier90-3.1.0 | Rocky Linux 8.8 NEC SX-Aurora TSUBASA vector engine | VASP >= 6.3.0 |

## VASP.6.4.3

| Compilers | MPI | FFT | BLAS | LAPACK | ScaLAPACK | CUDA | HDF5 | Other | Remarks | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intel-oneapi-compilers-2024.0.2 | intel-oneapi-mpi-2021.10.0 | intel-oneapi-mkl-2023.2.0 | | | | both | - | hdf5-1.14.0 | wannier90-3.1.0 libxc-5.2.3 | Rocky Linux 8.8 | - |
| gcc-12.3.0 | openmpi-4.1.6 | intel-oneapi-mkl-2023.2.0 | | | netlib-scalapack-2.2.0 | - | hdf5-1.14.0 | wannier90-3.1.0 libxc-5.2.3 | Rocky Linux 8.8 | - |
| nvhpc-23.7 (OpenACC) | openmpi-4.1.6 (CUDA-aware) | intel-oneapi-mkl-2023.2.0 | | | netlib-scalapack-2.2.0 | cuda-11.8 | hdf5-1.14.0 | wannier90-3.1.0 | Rock Linux 8.8 NVIDIA GPUs (A30) | - |
| aocc-4.0.0 | openmpi-4.1.4 | amdfftw-4.0 | amdblis-4.0 | amdlibflame-4.0 | amdscalapack-4.0 | - | hdf5-1.13.0 | wannier90-3.1.0 libxc-5.2.2 | On AMD CPUs (Zen3) | Reduce optimization level |
| nec-5.0.2 | nmpi-2.25.0 | nlc-3.0.0 | | | netlib-scalapack-2.2.0 | - | - | wannier90-3.1.0 | Rocky Linux 8.8 NEC SX-Aurora TSUBASA vector engine | VASP >= 6.3.0 |

## VASP.6.3.0

| Compilers | MPI | FFT | BLAS | LAPACK | ScaLAPACK | CUDA | HDF5 | Other | Remarks | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intel-oneapi-compilers-2022.0.1 | intel-oneapi-mpi-2021.5.0 | intel-oneapi-mkl-2022.0.1 | | | | - | hdf5-1.13.0 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | - |
| intel-parallel-studio-xe-2021.4.0 | | | | | netlib-scalapack-2.1.0 | - | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | - |
| gcc-11.2.0 | openmpi-4.1.2 | intel-oneapi-mkl-2022.0.1 | | | netlib-scalapack-2.1.0 | - | hdf5-1.13.0 | wannier90-3.1.0 libxc-5.2.2 | Centos 8.3 Intel Broadwell | - |
| gcc-11.2.0 | openmpi-4.1.2 | fftw-3.3.10 | openblas-0.3.18 | | netlib-scalapack-2.1.0 | - | hdf5-1.13.0 | wannier90-3.1.0 libxc-5.2.2 | Centos 8.3 Intel Broadwell | - |
| gcc-11.2.0 | openmpi-4.1.2 | amdfftw-3.1 | amdblis-3.1 | amdlibflame-3.1 | amdscalapack-3.1 | - | hdf5-1.13.0 | wannier90-3.1.0 libxc-5.2.2 | Centos 8.3 AMD Zen3 | - |
| gcc-9.3.0 | openmpi-4.0.5 | fftw-3.3.8 | openblas-0.3.10 | | netlib-scalapack-2.1.0 | - | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | Memory-leak |
| gcc-7.5.0 | openmpi-4.0.5 | intel-mkl-2020.2.254 | | | netlib-scalapack-2.1.0 | - | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | Memory-leak |
| nvhpc-22.2 (OpenACC) | openmpi-4.1.2 | intel-oneapi-mkl-2022.0.1 | | | netlib-scalapack-2.1.0 | nvhpc-22.2 (cuda-11.0) | hdf5-1.13.0 | wannier90-3.1.0 | Centos 8.3 NVIDIA GPUs (P100 & V100) | OpenACC + OpenMP |
| nvhpc-21.2 (OpenACC) | openmpi-4.0.5 (CUDA-aware) | intel-mkl-2020.2.254 | | | netlib-scalapack-2.1.0 | nvhpc-21.2 (cuda-11.0) | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 NVIDIA GPUs (P100 & V100) | Memory-leak |
| nvhpc-21.2 | openmpi-4.0.5 | intel-mkl-2020.2.254 | | | netlib-scalapack-2.1.0 | - | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | Memory-leak |
| nvhpc-21.2 | openmpi-4.0.5 | fftw-3.3.8 | openblas-0.3.10 | | netlib-scalapack-2.1.0 | - | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | Memory-leak |
| aocc-3.2.0 | openmpi-4.1.2 | amdfftw-3.1 | amdblis-3.1 | amdlibflame-3.1 | amdscalapack-3.1 | - | hdf5-1.13.0 | wannier90-3.1.0 libxc-5.2.2 | On AMD CPUs (Zen3) | - |
| nec-3.4.0 | nmpi-2.18.0 | nlc-2.3.0 | | | netlib-scalapack-2.2.0 | - | - | wannier90-3.1.0 | Centos 8.3 NEC SX-Aurora TSUBASA vector engine | VASP >= 6.3.0 |

## Older versions of VASP.6

| Compilers | MPI | FFT | BLAS | LAPACK | ScaLAPACK | CUDA | HDF5 | Other | Remarks | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intel-parallel-studio-xe-2021.1.1 | | | | | netlib-scalapack-2.1.0 | - | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | - |
| gcc-9.3.0 | openmpi-4.0.5 | fftw-3.3.8 | openblas-0.3.10 | | netlib-scalapack-2.1.0 | - | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | Memory-leak VASP >= 6.2.0 |
| gcc-7.5.0 | openmpi-4.0.5 | intel-mkl-2020.2.254 | | | netlib-scalapack-2.1.0 | - | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | Memory-leak |
| nvhpc-21.2 (OpenACC) | openmpi-4.0.5 (CUDA-aware) | intel-mkl-2020.2.254 | | | netlib-scalapack-2.1.0 | nvhpc-21.2 (cuda-11.0) | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 NVIDIA GPUs (P100 & V100) | Memory-leak |
| nvhpc-21.2 | openmpi-4.0.5 | intel-mkl-2020.2.254 | | | netlib-scalapack-2.1.0 | - | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | Memory-leak |
| nvhpc-21.2 | openmpi-4.0.5 | fftw-3.3.8 | openblas-0.3.10 | | netlib-scalapack-2.1.0 | - | hdf5-1.10.7 | wannier90-3.1.0 | Centos 8.3 Intel Broadwell | Memory-leak |

## Footnotes and references

## Related articles

Installing VASP.6.X.X,
makefile.include,
Compiler options,
Precompiler options,
Linking to libraries,
OpenACC GPU port of VASP,
Validation tests,
Known issues,
Personal computer installation
