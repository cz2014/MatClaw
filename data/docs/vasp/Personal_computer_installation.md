# Personal computer installation

Categories: VASP, Installation

Here you will find instructions on how to install VASP on some widely-used Linux distributions. For the sake of simplicity the suggested build processes rely as much as possible on compilers and libraries provided by the operating system's package manager. The focus is on minimizing the effort to obtain working VASP binaries with only little changes required to the provided `makefile.include` templates in the `arch` directory.

> **Warning:** These short and convenient installation instructions may come at the cost of performance. They are not optimized with respect to compilers, libraries and hardware. Please consider benchmarking and optimizing your build process prior to large-scale production runs.

In order to verify each build we run the FAST category tests of the testsuite.

> **Tip:** All build instructions presented here include HDF5 support to allow post-processing of results with py4vasp.

The build instructions have been tested on clean installations (virtual machines or docker images) of the operating systems in the following table. Search for your desired combination of OS and VASP and click on the provided link to get directly to the corresponding section on this page:

| Operating system | | VASP | | | |
| --- | --- | --- | --- | --- | --- |
| Name | Version | 6.3.0 - 6.3.1 | 6.3.2 | 6.4.X | 6.5.0 |
| Debian | 11 | Link | | |
|  | 12 |  |  | Link | |
| Ubuntu | 20.04 | Link |  |  |
|  | 22.04 | Link | | |  |
|  | 24.04 |  |  |  | Link |
| Fedora | 35 | Link |  |  |  |
|  | 37 - 38 |  |  | Link |  |
|  | 41 |  |  |  | Link |
| Rocky Linux | 8.5 | Link |  |  |  |
|  | 9.0 |  | Link |  |
|  | 9.2 |  |  | Link |  |
|  | 9.3 |  |  |  | Link |
| Mac OS X | M1/2/3/4 |  |  |  | Link |

A  red box background indicates that there are known issues with the used compiler/library versions (see the individual instructions for details). The table and corresponding instructions will be updated when either a new version of VASP or a major release of the operating systems is available. However, not all combinations will be tested and hence some fields will stay blank. In these cases it may still be helpful to start from instructions for close-by tested combinations.

## Debian

### Building VASP 6.3.X to 6.4.X on Debian 11

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-10.2.1 | openmpi-4.1.0 | fftw-3.3.8 | openblas-0.3.13 | | netlib-scalapack-2.1.0 | hdf5-1.10.6 | Memory-leak |

These packages can be installed directly from the command line like this:

```
sudo apt install rsync make build-essential g++ gfortran libopenblas-dev libopenmpi-dev libscalapack-openmpi-dev libfftw3-dev libhdf5-openmpi-dev
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack-openmpi
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -L/usr/lib/x86_64-linux-gnu/hdf5/openmpi/ -lhdf5_fortran
INCS       += -I/usr/include/hdf5/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

### Building VASP 6.4.X to 6.5.0 on Debian 12

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-12.2.0 | openmpi-4.1.4 | fftw-3.3.10 | openblas-0.3.21 | | netlib-scalapack-2.2.1 | hdf5-1.10.8 |  |

These packages can be installed directly from the command line like this:

```
sudo apt install rsync make build-essential g++ gfortran libopenblas-dev libopenmpi-dev libscalapack-openmpi-dev libfftw3-dev libhdf5-openmpi-dev
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack-openmpi
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -L/usr/lib/x86_64-linux-gnu/hdf5/openmpi/ -lhdf5_fortran
INCS       += -I/usr/include/hdf5/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

## Ubuntu

### Building VASP 6.3.0 - 6.3.1 on Ubuntu 20.04

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-9.4.0 | openmpi-4.0.3 | fftw-3.3.8 | openblas-0.3.8 | | netlib-scalapack-2.1.0 | hdf5-1.10.4 | - |

These packages can be installed directly from the command line like this:

```
sudo apt install make build-essential g++ gfortran libopenblas-dev libopenmpi-dev libscalapack-openmpi-dev libfftw3-dev libhdf5-openmpi-dev
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the line adding `-fallow-argument-mismatch` to the variable `FFLAGS`:

```
# For gcc-10 and higher (comment out for older versions)
#FFLAGS     += -fallow-argument-mismatch
```

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack-openmpi
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -L/usr/lib/x86_64-linux-gnu/hdf5/openmpi/ -lhdf5_fortran
INCS       += -I/usr/include/hdf5/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

### Building VASP 6.3.X to 6.4.X on Ubuntu 22.04

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-11.2.0 | openmpi-4.1.2 | fftw-3.3.8 | openblas-0.3.20 | | netlib-scalapack-2.1.0 | hdf5-1.10.7 | - |

These packages can be installed directly from the command line like this:

```
sudo apt install rsync make build-essential g++ gfortran libopenblas-dev libopenmpi-dev libscalapack-openmpi-dev libfftw3-dev libhdf5-openmpi-dev
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack-openmpi
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -L/usr/lib/x86_64-linux-gnu/hdf5/openmpi/ -lhdf5_fortran
INCS       += -I/usr/include/hdf5/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

### Building VASP 6.5.0 on Ubuntu 24.04

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-13.3.0 | openmpi-4.1.6 | fftw-3.3.10 | openblas-0.3.26 | | netlib-scalapack-2.2.1 | hdf5-1.10.10 | - |

These packages can be installed directly from the command line like this:

```
sudo apt install rsync make build-essential g++ gfortran libopenblas-dev libopenmpi-dev libscalapack-openmpi-dev libfftw3-dev libhdf5-openmpi-dev
```

If this fails, you may run the following command and then try again

```
sudo apt-get update
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack-openmpi
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -L/usr/lib/x86_64-linux-gnu/hdf5/openmpi/ -lhdf5_fortran
INCS       += -I/usr/include/hdf5/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

## Fedora

### Building VASP 6.3.0 - 6.3.1 on Fedora 35

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-11.2.1 | openmpi-4.1.1 | fftw-3.3.8 | openblas-0.3.19 | | netlib-scalapack-2.1.0 | hdf5-1.10.7 | Memory-leak |

These packages can be installed directly from the command line like this:

```
sudo yum install gcc gcc-c++ gcc-gfortran openblas-devel openmpi-devel scalapack-openmpi-devel fftw-devel hdf5-openmpi-devel
```

Add the following lines to your `.bashrc` file located in your home directory:

```
export PATH=${PATH}:/usr/lib64/openmpi/bin/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib64/openmpi/lib
```

and either open a new shell or run this command to activate the lines above:

```
source ~/.bashrc
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -lhdf5_fortran
INCS       += -I/usr/lib64/gfortran/modules/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

### Building VASP 6.4.X on Fedora 37 to 38

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| OS version | Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 37 | gcc-12.3.1 | openmpi-4.1.4 | fftw-3.3.10 | openblas-0.3.21 | | netlib-scalapack-2.2.0 | hdf5-1.12.1 |  |
| 38 | gcc-13.2.1 | openmpi-4.1.4 | fftw-3.3.10 | openblas-0.3.21 | | netlib-scalapack-2.2.0 | hdf5-1.12.1 |  |

These packages can be installed directly from the command line like this:

```
sudo yum install rsync gcc gcc-c++ gcc-gfortran openblas-devel openmpi-devel scalapack-openmpi-devel fftw-devel hdf5-openmpi-devel
```

Add the following lines to your `.bashrc` file located in your home directory:

```
export PATH=${PATH}:/usr/lib64/openmpi/bin/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib64/openmpi/lib
```

and either open a new shell or run this command to activate the lines above:

```
source ~/.bashrc
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -lhdf5_fortran
INCS       += -I/usr/lib64/gfortran/modules/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

### Building VASP 6.5.0 on Fedora 41

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| OS version | Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 41 | gcc-14.2.1 | openmpi-5.0.5 | fftw-3.3.10 | openblas-0.3.26 | | netlib-scalapack-2.2.0 | hdf5-1.12.1 |  |

These packages can be installed directly from the command line like this:

```
sudo yum install rsync gcc gcc-c++ gcc-gfortran openblas-devel openmpi-devel scalapack-openmpi-devel fftw-devel hdf5-openmpi-devel
```

Add the following lines to your `.bashrc` file located in your home directory:

```
export PATH=${PATH}:/usr/lib64/openmpi/bin/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib64/openmpi/lib
```

and either open a new shell or run this command to activate the lines above:

```
source ~/.bashrc
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -lhdf5_fortran
INCS       += -I/usr/lib64/gfortran/modules/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

## Rocky Linux

### Building VASP 6.3.0 - 6.3.1 on Rocky Linux 8.5

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-11.2.1 | openmpi-4.1.1 | fftw-3.3.5 | openblas-0.3.12 | | netlib-scalapack-2.0.2 | hdf5-1.10.5 | Memory-leak |

Some of these packages are available from the default package sources:

```
sudo dnf install openmpi-devel fftw-devel
```

Unfortunately the GCC version 8.5 provided by default is not suitable for compiling VASP. As an alternative we can use a newer version from the EPEL repositories:

```
sudo dnf install epel-release
sudo dnf install gcc-toolset-11-gcc gcc-toolset-11-gcc-c++ gcc-toolset-11-gcc-gfortran
```

Furthermore, some required libraries are available within the "PowerTools" repositories:

```
sudo dnf install dnf-plugins-core
sudo dnf config-manager --set-enabled powertools
sudo dnf install openblas-devel scalapack-openmpi-devel hdf5-openmpi-devel
```

Add the following lines to your `.bashrc` file located in your home directory:

```
export PATH=/opt/rh/gcc-toolset-11/root/bin/:/usr/lib64/openmpi/bin/:${PATH}
```

and either open a new shell or run this command to activate the lines above:

```
source ~/.bashrc
```

> **Mind:** As long as the path `/opt/rh/gcc-toolset-11/root/bin/` is in the `PATH` variable the system's default compiler binaries (`gcc`, `g++`, `gfortran`,...) are "hidden" behind the newer ones.

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -lhdf5_fortran
INCS       += -I/usr/lib64/gfortran/modules/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

### Building VASP 6.3.2 on Rocky Linux 9.0

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-11.2.1 | openmpi-4.1.1 | fftw-3.3.8 | openblas-0.3.15 | | netlib-scalapack-2.2.0 | hdf5-1.12.1 | Memory-leak |

Some of these packages are available from the default package sources:

```
sudo dnf install gcc gcc-c++ gcc-gfortran openmpi-devel fftw-devel
```

Some required libraries are available within the "CRB" ("Code Ready Builder") and EPEL repositories repositories:

```
sudo dnf config-manager --set-enabled crb
sudo dnf install openblas-devel
sudo dnf install epel-release
sudo dnf install scalapack-openmpi-devel hdf5-openmpi-devel
```

Add the following lines to your `.bashrc` file located in your home directory:

```
export PATH=${PATH}:/usr/lib64/openmpi/bin/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib64/openmpi/lib
```

and either open a new shell or run this command to activate the lines above:

```
source ~/.bashrc
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -lhdf5_fortran
INCS       += -I/usr/lib64/gfortran/modules/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

### Building VASP 6.4.X on Rocky Linux 9.2

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-11.3.1 | openmpi-4.1.1 | fftw-3.3.8 | openblas-0.3.21 | | netlib-scalapack-2.2.0 | hdf5-1.12.1 | Memory-leak |

Some of these packages are available from the default package sources:

```
sudo dnf install rsync gcc gcc-c++ gcc-gfortran openmpi-devel fftw-devel
```

Some required libraries are available within the "CRB" ("Code Ready Builder") and EPEL repositories repositories:

```
sudo dnf install 'dnf-command(config-manager)'
sudo dnf config-manager --set-enabled crb
sudo dnf install openblas-devel
sudo dnf install epel-release
sudo dnf install scalapack-openmpi-devel hdf5-openmpi-devel
```

Add the following lines to your `.bashrc` file located in your home directory:

```
export PATH=${PATH}:/usr/lib64/openmpi/bin/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib64/openmpi/lib
```

and either open a new shell or run this command to activate the lines above:

```
source ~/.bashrc
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -lhdf5_fortran
INCS       += -I/usr/lib64/gfortran/modules/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

### Building VASP 6.5.0 on Rocky Linux 9.3

---

First, we need to make sure that the prerequisites for building VASP are met. Here, we install the following compiler and libraries from the system's package manager:

| Compiler | MPI | FFT | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-11.5.0 | openmpi-4.1.1 | fftw-3.3.8 | openblas-0.3.26 | | netlib-scalapack-2.2.0 | hdf5-1.12.1 | Memory-leak |

Some of these packages are available from the default package sources:

```
sudo dnf install rsync gcc gcc-c++ gcc-gfortran openmpi-devel fftw-devel
```

Some required libraries are available within the "CRB" ("Code Ready Builder") and EPEL repositories repositories:

```
sudo dnf install 'dnf-command(config-manager)'
sudo dnf config-manager --set-enabled crb
sudo dnf install openblas-devel
sudo dnf install epel-release
sudo dnf install scalapack-openmpi-devel hdf5-openmpi-devel
```

Add the following lines to your `.bashrc` file located in your home directory:

```
export PATH=${PATH}:/usr/lib64/openmpi/bin/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib64/openmpi/lib
```

and either open a new shell or run this command to activate the lines above:

```
source ~/.bashrc
```

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu_omp` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu_omp makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -lscalapack
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -lfftw3 -lfftw3_omp
INCS       += -I/usr/include
```

* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -lhdf5_fortran
INCS       += -I/usr/lib64/gfortran/modules/openmpi/
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j
```

Once the build process is complete the binaries are located in the VASP `bin` subfolder. They were compiled with OpenMP-threading support. Before running VASP please always check if the `OMP_NUM_THREADS` environment variable is set according to your needs. For example, if you require only pure MPI parallelization without OpenMP threading add

```
export OMP_NUM_THREADS=1
```

in your `~/.bashrc` file.

## Mac OS X

### Building VASP 6.5.1 on Mac OS X (Apple Silicon M1/2/3/4)

---

VASP can be compiled on recent Apple Silicon hardware running Mac OS. First, we need to make sure that the prerequisites for building VASP are met. Here, we use the package manager [https:/brew.sh/ homebrew] to install all required dependencies:

| Compiler | MPI | FFTW | BLAS | LAPACK | ScaLAPACK | HDF5 | Known issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gcc-14.2.0 | openmpi-5.0.7 | fftw-3.3.10 | openblas-0.3.29 | | netlib-scalapack-2.2.2 | hdf5-1.14.5 | some test fail with precision loss |

These packages can be installed directly from the command line after [https:/brew.sh/ homebrew] is installed:

```
brew install gfortran gcc fftw hdf5 openmpi openblas scalapack qd
```

make sure that all brew packages are linked to the default install location, i.e. you can run `brew link -n openblas` to check whether brew already linked all library and include files.

Next, unpack the VASP source code to a location of your choice. Then change into the VASP base directory and use the `arch/makefile.include.gnu` template as basis for the `makefile.include`:

```
cp arch/makefile.include.gnu makefile.include
```

Search for the paragraph in `makefile.include` starting with `## Customize as of this point!` and apply the following changes below:

* Define a new variable `BREW_ROOT = /opt/homebrew/`
* Comment out the `OPENBLAS_ROOT` variable (not needed) and set `BLASPACK`:

```
# BLAS and LAPACK (mandatory)
#OPENBLAS_ROOT ?= /path/to/your/openblas/installation
BLASPACK    = -L$(BREW_ROOT)/lib -lopenblas
```

* Comment out the `SCALAPACK_ROOT` variable (not needed) and set `SCALAPACK`:

```
# scaLAPACK (mandatory)
#SCALAPACK_ROOT ?= /path/to/your/scalapack/installation
SCALAPACK   = -L$(BREW_ROOT)/lib -lscalapack
```

* Comment out the `FFTW_ROOT` variable (not needed). Set `LLIBS` and `INCS` in the FFTW section:

```
# FFTW (mandatory)
#FFTW_ROOT  ?= /path/to/your/fftw/installation
LLIBS      += -L$(BREW_ROOT)/lib -lfftw3
INCS       += -I$(BREW_ROOT)/include
```

* Quad precision support with openmpi in brew seems to be broken (test failures in GW tests). To fix this we have to link explicitly against the qd library by adding the following lines in the makefile:

  ```
  CPP_OPTIONS += -Dqd_emulate
  LLIBS       += -L$(BREW_ROOT)/lib -lqdmod
  INCS        += -I$(BREW_ROOT)/include/qd
  ```
* Enable HDF5 support by adding `-DVASP_HDF5` to the `CPP_OPTIONS` variable. Leave `HDF5_ROOT` variable commented out (not needed). Set `LLIBS` and `INCS` in the HDF5 section:

```
# HDF5-support (optional but strongly recommended)
CPP_OPTIONS+= -DVASP_HDF5
#HDF5_ROOT  ?= /path/to/your/hdf5/installation
LLIBS      += -L$(BREW_ROOT)/lib -lhdf5_fortran
INCS       += -I$(BREW_ROOT)/include
```

Save your `makefile.include` and compile VASP:

```
make DEPS=1 -j N
```

where N is the number of threads you want to use for building. Once the build process is complete the binaries are located in the VASP `bin` subfolder. OpenMP support can be enabled but there are no performance gains for standard SCF calculations. The Apple provided "Accelerate" LAPACK implementation does compile `-framework Accelerate` but crashes upon execution.

The hardware seems to benefit from small NCORE and high KPAR settings. To increase performance avoid using the efficiency cores, i.e. run VASP only with number of MPI ranks equivalent to the number of performance cores.

## Footnotes and references
