# NBSEBLOCKO

Categories: INCAR tag, Bethe-Salpeter equations, Many-body perturbation theory

NBSEBLOCKO = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NBSEBLOCKO** | = -1 |  |

Description: NBSEBLOCKO specifies the blocking factor for the occupied states when setting up the BSE Hamiltonian.

---

By default, the construction of the BSE Hamiltonian in VASP is parallelized over **k**-points, such that each MPI rank can compute a pair of **k**-points. This way the BSE Hamiltonian setup can be parallelized with

:   :   $$\text{total ranks}=\mathrm{NKPTS\times(NKPTS+1)/2}$$

or for spin-polarized case

:   :   $\text{total ranks}=\mathrm{NKPTS\times 2\times(NKPTS\times 2+1)/2}$,

where $\mathrm{NKPTS}$ is the total number of **k**-points in the full Brillouin zone. However, if a large number of MPI ranks is used in a calculation with too few **k**-point, this leads to load imbalance, where some of the MPI ranks will have no data to compute. In such cases, it is recommended to use parallelization over bands. If the parallelization over bands is used, all occupied (unoccupied) bands are divided into

:   :   $$\mathrm{NBLKO=NBANDSO/NBSEBLOCKO}$$

and

:   :   $$\mathrm{NBLKV=NBANDSV/NBSEBLOCKV}$$

blocks, respectively.

Such a band blocking allows VASP to parallelize the setup of the matrix with

:   :   $$\text{total ranks}=\mathrm{NBLKO\times NBLKV\times NKPTS\times (NBLKO\times NBLKV\times NKPTS+1)/2}$$

or for spin-polarized case

:   :   $$\text{total ranks}=\mathrm{NBLKO\times NBLKV\times NKPTS\times 2\times (NBLKO\times NBLKV\times NKPTS\times 2+1)/2}$$

If neither $\mathrm{NBSEBLOCKV}$ nor $\mathrm{NBSEBLOCKO}$ is specified, no paralliziation over bands is used and $\mathrm{NBLKO=1}$ and $\mathrm{NBLKV=1}$.

> **Mind:** Parallelization over bands with NBSEBLOCKV does not work with the old BSE driver, i.e., IBSE=0

We recommend using parallelization over bands only if the number of MPI ranks in the calculation exceeds $\text{total ranks}$.

> **Mind:** The NBSEBLOCKV and NBSEBLOCKO tags are available as of VASP.6.5.0

## Related tags and sections

BSE, NBSEBLOCKV, BSE calculations, TDDFT calculations

---
