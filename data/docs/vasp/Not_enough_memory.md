# Not enough memory

Categories: Performance, Howto, Memory

Nowadays, for standard DFT and hybrid functional calculations, memory is usually not an issues.
Furthermore, by increasing the number of cores, the memory requirements per core can be reduced significantly.

If memory shortage is encountered, the following steps can be taken in order to reduce the memory requirements per core.

* For large and many-atom systems, it is advised to increase NCORE to larger values (say to 4, 8 potentially to or even beyond the number of cores per node). This allows to decrease the memory requirements per core for the storage of the non-local projectors. Furthermore, real space projection, LREAL= A, also decreases the required memory per core.
* KPAR allows to distribute the k-points over cores. Unfortunately, only the calculations are distributed, but the storage of the orbitals is not distributed over cores. This means that using KPAR=1 results in the smallest memory footprint per core (but slower calculations, since VASP needs to rely on other less efficient parallelization strategies).
* Switch of symmetrisation (ISYM=0). Charge symmetrisation is done locally on each node requiring three fairly large arrays. VASP.4.4.2 (and newer versions) posses a switch to run a more memory conserving symmetrization. From VASP.5 onwards, the memory conserving version, ISYM=2, is the default. Results might differ slightly from ISYM=1 (usually by about 1E-5 eV).
* Make sure to use scaLAPACK if your system becomes large. If scaLAPACK is not available, VASP needs to store an NBANDS x NBANDS matrix on each core, in order to diagonalize the Hamiltonian in the subspace of the calculated orbitals. If scaLAPACK is compiled in and used, the matrix is distributed over all cores jointly handling one k-point. Note that decreasing KPAR reduces the memory demand for this matrix (if scaLAPACK is used).

A final hint is in place. At some key places, the VASP code reports the required memory per core in the OUTCAR file. Please search the lines

```
total amount of memory used by VASP MPI-rank0   457796. kBytes
=======================================================================
  base      :      30000. kBytes
  nonlr-proj:      12085. kBytes
  fftplans  :      29652. kBytes
  grid      :      54584. kBytes
  one-center:        211. kBytes
  wavefun   :     331264. kBytes
```

and inspect how much memory VASP uses per core. "base" is the estimated memory use for the executable and libraries, "nonlr-proj" the required memory for the non-local projection operators, "grid" that for 3D arrays representing the charge density, potentials, etc., and "wavefun" the requirements for the one-electron wavefunctions (orbitals). Storage of the orbitals is usually most memory demanding.

---
