# Shared memory

Categories: VASP, Installation, Performance, Machine-learned force fields, Memory

VASP is mainly parallelized using MPI, and as much as practically feasible the computational work and storage demands are distributed over the MPI ranks.
Unavoidably, however, some data structures are duplicated across all MPI ranks.
For some of these data structures, VASP offers the option to reduce the memory consumption by putting them into shared-memory segments. That is segments of memory shared between the MPI ranks that reside on the same compute node and hence have access to the same physical memory.

Whether to use shared memory or not has to be decided when compiling the code. It is controlled by the precompiler options: -Duse\_shmem, -Dshmem\_bcast\_buffer, -Dshmem\_rproj, and -Dsysv:

**-Duse\_shmem**

:   Use shared-memory segments to reduce the memory demands of GW (ALGO = EVGW0, EVGW, QPGW0, and QPGW) and the memory demands of machine-learned–force-field calculations.

**-Dshmem\_bcast\_buffer**

:   Use shared-memory segments to reduce the amount of MPI communication in hybrid-functional calculations.

**-Dshmem\_rproj**

:   Use shared-memory segments to reduce the storage demands of the real-space PAW projectors.

**-Dsysv** (recommended if possible, see notes below)

:   Use of ipcs shared-memory segments and system-V semaphores **instead** of using default MPI-3 shared-memory capabilities (see below).

In any case the aforementioned precompiler options have to be accompanied by an additional change to your makefile.include: The variable OBJECTS\_LIB needs to contain also the object file getshmem.o, e.g., it may look like this:

```
OBJECTS_LIB = linpack_double.o getshmem.o
```

> **Mind:** If you forget to add getshmem.o you may receive errors in the linking stage at the end of the VASP build process, e.g., `` undefined reference to `getshmem_C' ``.

The allocation and handling of shared-memory segments has been implemented in two different ways:

:   * Using the MPI-3 shared-memory capabilities (default, any of -Duse\_shmem, -Dshmem\_bcast\_buffer, -Dshmem\_rproj but **not** -Dsysv).

:   :   > **Warning:** Per default, VASP uses MPI-3 calls to allocate and manage shared-memory segments. Unfortunately, we have observed that for some MPI implementations an abnormal termination of the code (*e.g.* segfaults or user initiated abort) does not free these shared-memory segments. This is not a VASP related error. It is caused by the way these shared-memory segments are handled by the operating system and MPI. Without explicit clean-up this leads to a "memory leakage" that persists until the compute node is rebooted. Obviously this is very problematic at high-performance-computing centers. For this reason we do not recommend using shared memory indiscriminately (*i.e.*, without explicit need).

:   * Using ipcs shared-memory segments and system-V semaphores (add precompiler option -Dsysv).

:   :   > **Tip:** Using ipcs shared-memory segments and system-V semaphores (add precompiler option -Dsysv) rarely leads to memory leakage. However, when it does, it is guaranteed to persist until reboot of the node, and no manner of other clean-up will be effective.

:   :   A common problem with the use of ipcs shared-memory segments and system-V semaphores is that the maximum allowed number of semaphores and shared-memory segments, and the maximum allowed size of the latter are system-wide kernel settings. The default settings of many Linux distributions are so strict, *i.e.*, the allowed number and size of the shared-memory segments is so small, that they are completely unusable for our purposes.
    :   One can verify the current limits, by:

> ```
> #ipcs -l
> ------ Messages Limits --------
> max queues system wide = 32000
> max size of message (bytes) = 8192
> default max size of queue (bytes) = 16384
>
> ------ Shared Memory Limits --------
> max number of segments = 4096
> max seg size (kbytes) = 16777216
> max total shared memory (kbytes) = 16777216
> min seg size (bytes) = 1
>
> ------ Semaphore Limits --------
> max number of arrays = 262
> max semaphores per array = 250
> max semaphores system wide = 32000
> max ops per semop call = 32
> semaphore max value = 32767
> ```

:   :   *i.e.*, on this particular machine the maximum number of semaphores is 32000, the maximum number of shared-memory segments is 4096, and their maximum size is 16Gb.

:   :   > **Warning:** How to change the maximum number of semaphores and shared-memory segments, and the maximum size of the latter, depends on the particular Linux distribution and generally requires superuser rights. For this reason the use of this implementation of shared memory (-Dsysv) is not practical in many situations.

## Related articles

Installing VASP.6.X.X,
makefile.include,
Precompiler options,
Machine-learned force fields

---
