# NCSHMEM

Categories: Performance, Many-body perturbation theory, GW, Memory

NCSHMEM = [integer]  
 Default: **NCSHMEM** = 1

Description: NCSHMEM determines the number of compute cores sharing the memory in MPI in the non-cubic scaling GW routines.

---

By default no shared memory MPI is in the non-cubic scaling GW routines (ALGO=EVGW, EVGW0, QPGW and QPGW0).
For using shared memory MPI in the non-cubic scaling GW set NCSHMEM=-1.

> **Warning:** For the openmp version NCHSMEM is not active and shared memory is not used for MPI. In that case the memory is shared between threads.

## Related tags and articles

Shared memory, ALGO, Practical guide to GW calculations
