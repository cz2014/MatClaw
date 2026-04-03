# ISTART

Categories: INCAR tag, Electronic minimization

ISTART = 0 | 1 | 2 | 3

|  |  |  |
| --- | --- | --- |
| Default: **ISTART** | = 1 | if a WAVECAR file exists |
|  | = 0 | else |

Description: ISTART determines whether or not to read the WAVECAR file.

---

* ISTART=0

:   Start job: "begin from scratch". Initialize the orbitals according to the flag INIWAV.

* ISTART=1

:   Continuation job: "restart with constant energy cut-off". Orbitals are read from the WAVECAR file (usage is restricted in the parallel version). The set of plane waves will be redefined and re-padded according to the new cell size/shape (POSCAR) and the new plane wave cut-off (INCAR). These values might differ from the old values, that are stored in the WAVECAR file. If the WAVECAR file is missing or if the WAVECAR file contains an inappropriate number of bands and/or k-points the flag ISTART will revert to ISTART=0 (see above).

:   The usage of ISTART=1 is recommended if the size/shape of the supercell (see section on volume relaxations) or the cut-off energy changed with respect to the last run and if one wishes to redefine the set of plane waves according to a new setting.

:   ISTART=1 is the usual setting for convergence tests with respect to the cut-off energy and for all jobs where the volume/cell-shape varies (e.g. to calculate binding energy curves looping over a set of volumes).

* ISTART=2

:   Continuation job: "restart with constant basis set". Orbitals are read from the WAVECAR file.

:   The set of plane waves will **not** be changed even if the cut-off energy or the cell size/shape given on the INCAR and POSCAR files are different from the values stored on the WAVECAR file. If the WAVECAR file is missing or if the WAVECAR file contains an inappropriate number of bands and/or k-points the ISTART will revert to ISTART=0 (see above).

:   If the cell shape has not changed then ISTART=1 and ISTART=2 lead to the same result.

:   ISTART=2 is usually used if one wishes to restart with the same basis set used in the previous run.

:   > **Mind:** Due to Pulay stresses, there is a difference between evaluating the equilibrium volume with a constant basis set and a constant energy cut-off (unless absolute convergence with respect to the basis set is achieved!).

:   If you are looking for the equilibrium volume, calculations with a constant energy cut-off are preferable to calculations with a constant basis set, therefore always restart with ISTART=1 unless you really know what you are looking for (see the section on volume relaxations).

:   There is only one exception to this general rule: all volume/cell shape relaxation algorithms implemented in VASP work with a constant basis set, so continuing such jobs requires to set ISTART=2 to get a 'consistent restart' with respect to the previous runs (see section volume relaxations)! This menas that that number of plane waves is consistent with the previous run but the energy cut-off is not (see section Pulay stress).

* ISTART=3

:   Continuation job: "full restart including orbitals and charge prediction".

:   Same as ISTART=2 but in addition a valid TMPCAR file must exist, containing the positions and orbitals at time steps $t(N-1)$ and $t(N-2)$, which are needed for the orbital and charge prediction scheme (used for MD-runs).

:   ISTART=3 is generally not recommended unless an operating system imposes a serious restriction on the CPU time per job: if you continue with ISTART=1 or 2, a relatively large number of electronic iterations might be necessary to reach convergence of the orbitals in the second and third molecular-dynamics steps. ISTART=3 therefore saves time and is important if a molecular-dynamics run is split into very small pieces (e.g., NSW<10).

:   Nevertheless, we have found that it is safer to restart the orbital prediction after 100 to 200 steps. If NSW>30, ISTART=1 or 2 is strongly recommended.

:   > **Mind:** If ISTART=3, a non-existing WAVECAR or TMPCAR file or any inconsistency of input data will immediately stop execution.

Examples that use this tag

---
