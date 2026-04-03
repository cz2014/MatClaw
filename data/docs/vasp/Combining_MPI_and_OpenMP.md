# Combining MPI and OpenMP

Categories: VASP, Installation, Parallelization

VASP can be built to use a combination of OpenMP threading and parallelization over MPI ranks. This is beneficial on some hardware.

## When to use MPI + OpenMP

When is it beneficial to run with multiple OpenMP threads per MPI rank? There are not so many cases, but we can discern at least two:

1. On nodes with many cores, e.g., 64 or more. On such nodes, the memory bandwidth and cache size per core may limit the parallel efficiency of VASP. These problems can be (partly) alleviated by the use of OpenMP.
2. When running the OpenACC port of VASP on GPUs. Execution of VASP on GPUs is most efficient when using only a single MPI rank per GPU. Therefore, only a few MPI ranks are running on the CPU in most cases. It is helpful to run with multiple OpenMP threads per MPI rank to leverage the CPU's remaining computational power for those parts of VASP that still run on the CPU side.

> **Important:** When running with a single OpenMP thread per MPI rank, there is no appreciable difference between a VASP run with an MPI+OpenMP executable and an MPI-only one. The inactive OpenMP constructs incur very little overhead. In that sense, no strong argument speaks against building VASP with OpenMP support per default.

## Compilation

To compile VASP with OpenMP support, add the following to the list of precompiler flags in your `makefile.include` file:

```
CPP_OPTIONS += -D_OPENMP
```

In addition, you need to add some compiler-specific options to the command that invokes your Fortran compiler (and sometimes to the linker as well). For instance, when using an Intel toolchain (ifort + Intel MPI), it is

```
FC = mpiifort -qopenmp
```

> **Important:** Base your makefile.include file on one of the archetypical /arch/makefile.include.\*\_omp files that are provided with your VASP.6.X.X release.

To adapt these to the particulars of your system (if necessary) please read the instructions on the installation of VASP.6.X.X.

> **Mind:** When you compile VASP with OpenMP support and you are **not** using the FFTs from the Intel-MKL library, you should compile VASP with fftlib. Otherwise, the costs of (planning) the OpenMP-threaded FFTs will become prohibitively large at higher thread counts.

## Running multiple OpenMP threads per MPI rank

In principle, running VASP on *n* MPI ranks with *m* OpenMP threads per rank is as simple as:

```
export OMP_NUM_THREADS=<m> ; mpirun -np <n> <your-vasp-executable>
```

Here, the mpirun part of the command depends on the flavor of MPI one uses and has to be replaced appropriately. Below, we will only discuss the use of OpenMPI and IntelMPI.

For proper performance, it is crucial to ensure that the MPI ranks, and the associated OpenMP threads they spawn, are placed optimally onto the *physical* cores of the node(s), and are pinned to these cores.
As an example (for a typical Intel Xeon-like architecture): Let us assume we plan to run on 2 nodes, each with 16 physical cores. These 16 cores per node are further divided into 2 *packages* (aka *sockets*) of 8 cores each. The cores on a socket share access to a block of memory and in addition, they may access the memory associated with the other package on their node via a so-called *crossbar switch*. The latter, however, comes at a (slight) performance penalty.

In the aforementioned situation, a possible placement of MPI ranks and OpenMP threads would for instance be the following: place 2 MPI ranks on each package (*i.e.*, 8 MPI ranks in total) and have each MPI rank spawn 4 OpenMP threads on the same package. These OpenMP threads will all have fast access to the memory associated with their package, and will not have to access memory through the crossbar switch.

To achieve this we have to tell both the OpenMP runtime library as well as the MPI library what to do.

> **Warning:** In the above we purposely mention *physical* cores. When your CPU supports *hyperthreading* (and if this is enabled in the BIOS) there are more *logical* cores than *physical* cores (typically a factor 2). As a rule of thumb: makes sure that the total number of MPI ranks × OMP\_NUM\_THREADS (in the above: *m*×*n*) does not exceed the total number of **physical cores** (*i.e.*, do not *oversubscribe* the nodes). In general VASP runs do not benefit from oversubscription.

### For the OpenMP runtime

Tell the OpenMP runtime it may spawn 4 threads per MPI rank:

```
export OMP_NUM_THREADS=4
```

and that it should bind the threads to the physical cores, and put them onto cores that are as close as possible to the core that is running the corresponding MPI rank (and OpenMP master thread):

```
export OMP_PLACES=cores
export OMP_PROC_BIND=close
```

In addition to taking care of thread placement, it is often necessary to increase the size of the private stack of the OpenMP threads (to 256 or even 512 Mbytes), since the default is in many cases too small for VASP to run, and will cause segmentation faults:

```
export OMP_STACKSIZE=512m
```

:   > **Mind:** The Intel OpenMP-runtime library (libiomp5.so) offers an alternative set of environment variables to control OpenMP-thread placement, stacksize *etc*.

### Using OpenMPI

Now start 8 MPI ranks (`-np 8`), with the following placement specification: 2 ranks/socket, assigning 4 subsequent cores to each rank (`--map-by ppr:2:socket:PE=4`), and bind them to their physical cores (`--bind-to core`):

```
mpirun -np 8 --map-by ppr:2:socket:PE=4 --bind-to core <your-vasp-executable>
```

Or all of the above wrapped into a single command:

```
mpirun -np 8 --map-by ppr:2:socket:PE=4 --bind-to core \
              -x OMP_NUM_THREADS=4 -x OMP_STACKSIZE=512m \
              -x OMP_PLACES=cores -x OMP_PROC_BIND=close \
              --report-bindings <your-vasp-executable>
```

where the `--report-bindings` is optional but a good idea to use at least once to check whether the rank and thread placement is as intended.

In our example, the above will assure that the OpenMP threads each MPI rank spawns reside on the same package/socket, and pins both the MPI ranks as well as the OpenMP threads to specific cores. This is crucial for performance.

### Using IntelMPI

Tell MPI to reserve a domain of OMP\_NUM\_THREADS cores for each rank

```
export I_MPI_PIN_DOMAIN=omp
```

and pin the MPI ranks to the cores

```
export I_MPI_PIN=yes
```

Then start VASP on 8 MPI ranks

```
mpirun -np 8 <your-vasp-executable>
```

In case one uses Intel MPI, things are fortunately a bit less involved. Distributing 8 MPI-ranks over 2 nodes with 16 physical cores each (2 sockets per node) allowing for 4 OpenMP threads per MPI-rank is as simple as:

```
mpirun -np 8 -genv I_MPI_PIN=yes -genv I_MPI_PIN_DOMAIN=omp -genv I_MPI_DEBUG=4
```

Or all of the above wrapped up into a single command:

```
 mpirun -np 8 -genv I_MPI_PIN_DOMAIN=omp -genv I_MPI_PIN=yes -genv OMP_NUM_THREADS=4 -genv OMP_STACKSIZE=512m \
              -genv OMP_PLACES=cores -genv OMP_PROC_BIND=close -genv I_MPI_DEBUG=4 <your-vasp-executable>
```

where the `-genv I_MPI_DEBUG=4` is optional but a good idea to use at least once to check whether the rank and thread placement is as intended.

In our example, the above will assure that the OpenMP threads each MPI rank spawns reside on the same package/socket, and pins both the MPI ranks as well as the OpenMP threads to specific cores. This is crucial for performance.

## MPI versus MPI/OpenMP: the main difference

By default VASP distributes work and data over the MPI ranks on a per-orbital basis (in a round-robin fashion): Bloch orbital 1 resides on rank 1, orbital 2 on rank 2. and so on.
Concurrently, however, the work and data may be further distributed in the sense that not a single, but a group of MPI ranks, is responsible for the optimization (and related FFTs) of a particular orbital.
In the pure MPI version of VASP, this is specified by means of the NCORE tag.

For instance, to distribute each individual Bloch orbital over 4 MPI ranks, one specifies:

```
NCORE = 4
```

The main difference between the pure MPI and the hybrid MPI/OpenMP version of VASP is that the latter will not distribute a single Bloch orbital over *multiple MPI ranks* but will distribute the work on a single Bloch orbital over *multiple OpenMP threads*.

As such one does not set NCORE=4 in the INCAR file but starts VASP with 4 OpenMP-threads/MPI-rank.

> **Warning:** The hybrid MPI/OpenMP version of VASP will internally set NCORE=1, regardless of what was specified in the INCAR file, when it detects it has been started on more than one OpenMP thread.

## Further reading

* *OpenMP in VASP: Threading and SIMD*, F. Wende, M. Marsman, J. Kim, F. Vasilev, Z. Zhao, and T. Steinke, Int. J. Quantum Chem. 2018;e25851

## Credits

Many thanks to Jeongnim Kim and Fedor Vasilev at Intel, and Florian Wende and Thomas Steinke of the Zuse Institute Berlin (ZIB)!

## Related tags and articles

Parallelization,
Installing VASP.6.X.X,
OpenACC GPU Port of VASP

---
