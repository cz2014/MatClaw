# IALGO

Categories: INCAR tag, Electronic minimization

IALGO = -1 | 2-4 | 5-8 | 15-18 | 28 | 38 | 44-48 | 53-58

|  |  |  |
| --- | --- | --- |
| Default: **IALGO** | = 8 | for VASP.4.4 and older |
|  | = 38 | else (if ALGO is not set) |

Description: IALGO selects the algorithm to optimize the orbitals.

---

> **Warning:** We suggest selecting the algorithms via ALGO instead of IALGO. Algorithms other than those available via ALGO are subject to instabilities.

## Conjugate gradient algorithms

The band-by-band conjugate gradient algorithms are no longer maintained or supported.

* IALGO=5-8: Conjugate gradient algorithms

> **Deprecated:** Not supported since vasp.5.

:   Optimize each band iteratively using a conjugate gradient algorithm. Subspace-diagonalization before conjugate gradient algorithm. The conjugate gradient algorithm is used to optimize the eigenvalue of each band.

    * IALGO=5 steepest descent
    * IALGO=6 conjugated gradient
    * IALGO=7 preconditioned steepest descent
    * IALGO=8 preconditioned conjugated gradient
:   IALGO=8 is always fastest, whereas IALGO=5-7 are only implemented for test purposes.
:   Please mind, that IALGO=8 is not supported as of VASP.4.5, since M. Teter, Corning and M. Payne hold a patent on this algorithm. The algorithms have been replaced by faster and more efficient Davidson-like algorithms.

* IALGO=15-18: Conjugate gradient algorithms

> **Deprecated:** Not supported since vasp.5.

:   Subspace-diagonalization after iterative refinement of the eigenvectors using the conjugate gradient algorithm. These switches are retained for compatibility reasons only and should not be used any longer. Generally IALGO=5-8 is preferable. Sub-switches as above.

* IALGO=28: Conjugate gradient algorithm

> **Deprecated:** Not supported since vasp.5.

:   Subspace-diagonalization before conjugate gradient algorithm. No explicit orthonormalization of the gradients to the trial orbitals is done. This setting saves time, but does fail in most cases (mainly included for test purposes). Try IALGO=4X (RMM-DIIS) instead.

## The blocked-Davidson scheme

* IALGO=38: Blocked-Davidson algorithm (ALGO=N).

:   Kosugi algorithm (special blocked-Davidson iteration scheme). This algorithm is the default in VASP.4.6 and VASP.5.X. It optimizes a subset of NSIM bands simultaneously. The optimized bands are kept orthogonal to all other bands. If problems are encountered with the algorithm, try to decrease NSIM. Such problems are encountered, if linear dependencies develop in the search space. By reducing NSIM the rank of the search space is decreased.

## RMM-DIIS

* IALGO=44-48: Residual minimization method direct inversion in the iterative subspace (ALGO= F). IALGO=44-48 does not support hybrid functionals.

:   The RMM-DIIS algorithm reduces the number of orthonormalization steps ($O(N^3)$) considerably and is therefore much faster than IALGO=8 and IALGO=38, at least for large systems and for workstations with a small memory band width. For optimal performance, we recommend to use this switch together with LREAL=Auto). The algorithm works in a blocked mode in which several bands are optimized at the same time. This can improve the performance even further on systems with a low memory band width (default is presently NSIM=4).

:   The following sub-switches exist:

    * IALGO=44 steepest descent eigenvalue minimization
    * IALGO=46 residuum-minimization + preconditioning
    * IALGO=48 preconditioned residuum-minimization (ALGO=F)

:   IALGO=48 is usually most reliable (IALGO=44 and 46 are mainly for test purposes).

:   For IALGO=4X, a subspace-diagonalization is performed before the residual vector minimization, and a Gram-Schmidt orthogonalization is employed after the RMM-DIIS step. In the RMM-DIIS step, each band is optimized individually (without the orthogonality constraint); a maximum of NRMM iterative steps per band are performed for each band. The default is NRMM=4, and we recommend leaving this value unchanged.

:   Please mind, that the RMM-DIIS algorithm can fail in rare cases, whereas IALGO=38 did not fail for any system tested up to date. Therefore, if you have problems with IALGO=48 try first to switch to IALGO=38.

:   However, in some cases the performance gains due to IALGO=48 are so significant that IALGO=38 might not be a feasible option. In the following we try to explain what to do if IALGO=48 does not work reliably:

:   In general two major problems can be encountered when using IALGO=48: First, the optimization of unoccupied bands might fail for molecular dynamics and relaxations. This is because our implementation of the RMM-DIIS algorithm treats unoccupied bands more "sloppy" then occupied bands during MD's. The problem can be solved rather easily by specifying WEIMIN=0 in the INCAR file. In that case all bands are treated accurately.

:   The other major problem (which occurs also for static calculations) is the initialization of the orbitals. Because the RMM-DIIS algorithm tends to find eigenvectors which are close the the initial set of trial vectors there is no guarantee to converge to the correct ground state! This situation is usually very easy to recognize; whenever one eigenvector is missing in the final solution, the convergence becomes slow at the end (mind, that it is possible that one state with a small fractional occupancy above the Fermi-level is missing). If you suspect that this is the case switch to ICHARG=12 (i.e. no update of charge and Hamiltonian) and try to calculate the orbitals with high accuracy ($10^{-6}$). If the convergence is fairly slow or stucks at some precision, the RMM-DIIS algorithm has problems with the initial set of orbitals (as a rule of thumb not more than 12 electronic iterations should be required to determine the orbital for the default precision for ICHARG=12). The first thing to do in that case is to increase the number of bands (NBANDS) in the INCAR file. This is usually the simplest and most efficient fix, but it does not work in all cases. This solution is also undesirable for MD's and long relaxations because it increases the computational demand somewhat. A simple alternative - which worked in all tested cases - is to use IALGO=38 (Davidson) for a few non selfconsistent iterations and to switch then to the RMM-DIIS algorithm. This setup is automatically selected when ALGO= Fast is specified in the INCAR file (IALGO must not specified in the INCAR file in this case).

:   The final option is somewhat complicated and requires an understanding of how the initialization algorithm of the RMM-DIIS algorithm works: after the random initialization of the orbitals, the initial orbitals for the RMM-DIIS algorithm are determined during a non selfconsistent steepest descent phase (the number of steepest descent sweeps is given by NELMDL, default is NELMDL=-12 for RMM-DIIS). During this initial phase in each sweep, one steepest descent step per orbital is performed between each sub space rotation. This "automatic" simple steepest descent approach during the delay is faced with a rather ill-conditioned minimization problem and can fail to produce reasonable trial orbitals for the RMM-DIIS algorithm. In this case the quantity in the column "rms" will not decrease during the initial phase (12 steps), and you must improve the conditioning of the problem by setting the ENINI parameter in the INCAR file. ENINI controls the cutoff during the initial (steepest descent) phase for IALGO=48. Default for ENINI is ENINI= ENCUT. If convergence problems are observed, start with a slightly smaller ENINI; reduce ENINI in steps of 20%, till the norm of the residual vector (column "rms") decreases continuously during the first 12 steps.

:   The algorithm can be combined with LDIAG=.FALSE. to conserve the initial orbital order (when orbitals are read from the WAVECAR file).

:   A final note concerns the mixing: IALGO=48 dislikes too abrupt mixing. Since the RMM-DIIS algorithm always stays in the space spanned by the initial orbitals, and too strong mixing (large AMIX, small BMIX) might require discontinuous changes of the orbitals, the initial mixing must not be too sizable for IALGO=48. Try to reduce AMIX and increase BMIX if you suspect such a situation. Increasing NBANDS also helps in this situation.

## Direct optimization

* IALGO=53-58: Treat total free energy as variational quantity and minimize the functional completely selfconsistently.

:   These algorithms have been carefully optimized and should be selected for Hartree-Fock type as well as meta-GGA functionals. The present version is rather stable and robust even for metallic systems.

:   Important sub-switches:

:   * IALGO=53 damped MD with damping term automatically determined by the given time-step (ALGO=D).
    * IALGO=54 damped MD (velocity quenched or quickmin)
    * IALGO=58 preconditioned conjugated gradient (ALGO=A)

:   Furthermore, LSUBROT determines whether the subspace rotation matrix (rotation matrix in the space spanned by the occupied and unoccupied orbitals) is optimized. The current default is LSUBROT=.FALSE. This allows for efficient groundstate calculations for insulators. When hybrid functionals are used, LSUBROT=.TRUE. can be tried for small gap semiconductors and metals. This algorithm performs standard SCF steps during the direct optimization steps in order to determine an optimal rotation matrix between occupied and unoccupied orbitals. For hybrid functionals, LSUBROT=.TRUE. is generally faster, however, in rare cases, it can lead to instabilities.

:   The preconditioned conjugate gradient (IALGO= 58, ALGO= A) algorithm is recommended for insulators. The best stability is usually obtained if the number of bands equals half the number of electrons (non-spin-polarized case). In this case, the algorithm is fairly robust and foolproof and might even outperform the mixing algorithm.

:   For small gap systems and for metals, it is however usually required (metals) or desirable (semiconductors) to use a larger value for NBANDS. In this case, we recommend using the damped MD algorithm (IALGO=53, ALGO=Damped) instead of the conjugate gradient.

:   The stability of the all bands simultaneously algorithms depends strongly on the setting of TIME. For the conjugate gradient case, TIME controls the step size in the trial step, which is required in order to perform a line minimization of the energy along the gradient (or conjugated gradient). Too small steps make the line minimization less accurate, whereas too large steps can cause instabilities. The step size is usually automatically scaled by the actual step size minimizing the total energy along the gradient (values can range from 1.0 for insulators to 0.01 for metals with a large density of states at the Fermi-level).

:   For the damped MD algorithm (IALGO=53, ALGO=Damped), a sensible TIME step is even more important. In this case TIME is not automatically adjusted, and the user is entirely responsible to choose an appropriate value. Too small time steps slow the convergence significantly, whereas too large values will always lead to divergence. It is sensible to optimize this value, in particular, if many different configurations are considered for a particular system. It is recommended to start with a small step size TIME, and to increase TIME by a factor 1.2 until the calculations diverge. The largest stable step TIME should then be used for all calculations.

The damped MD algorithm can be combined with LDIAG=.FALSE. to conserve the initial orbital order (when orbitals are read from the WAVECAR file).

:   The final algorithm IALGO=54 also uses a damped molecular dynamics algorithm but quenches the velocities to zero, if they are antiparallel to the present gradient (quick-min). It is usually not as efficient as IALGO=53, but it is also less sensitive to the TIME parameter.

> **Mind:** Conjugate gradient algorithms require a largely noise-free energy surface for fast and consistent convergence. Some functionals, for instance non-local vdW-DFT functionals or meta-GGA functionals can result in a very noisy energy surface with small discontinuities in the energy. This can cause divergence or very slow convergence of the direct minimization. The issue is usually mitigated by setting PREC = Accurate, or manually increasing the FFT grids for the densities (NGXF, NGYF, NGZF).

> **Mind:** It is very important to set an appropriate TIME for some of the algorithms. Furthermore, it might be expedient to set NELMDL to 1 or 2 for molecular dynamics simulations or relaxations in vasp.6. See the corresponding section in the documentation of NELMDL. If the ions move by a very large distance during relaxations, even NELMDL=3 can be expedient (in particular for HF type Hamiltonians).

## Miscellaneous

* IALGO=-1: Performance test.

:   VASP does not perform an actual calculation, only some important parts of the program will be executed and the timing for each part is printed out at the end.

* IALGO=2: Orbitals and one-electron energies are kept fixed.

:   One electron occupancies and electronic density of states (DOS) are, however, recalculated. This option is only useful if a pre-converged WAVECAR file is read. The option allows running selected post-processing tasks, such as local DOS, or the interface code to Wannier90.

* IALGO=3: Orbitals are kept fixed.

:   One-electron energies, band structure energies, and the electronic density of states (DOS) are, as well as, the total energy are recalculated for the present Hamiltonian (the one-electron occupancies are kept fixed, however). This option is only useful if a pre-converged WAVECAR file is read. The option also allows running selected post-processing tasks, such as local DOS, or the interface code to Wannier90.

* IALGO=4: Orbitals are updated by applying a sub-space rotation.

:   The Hamiltonian is evaluated in the space spanned by the orbitals (read from WAVECAR), and one diagonalization in this space is performed. No optimization outside the subspace spanned by the orbitals is performed. Note: if NBANDS is larger or equal to the total number of plane waves, the resulting one-electron orbitals are exact.

* IALGO=90: Exact Diagonalization. This flag selects an exact diagonalization of the one-electron Hamiltonian. This requires a fairly large amount of memory and should be selected with caution. Specifically, we recommend selecting this algorithm to prepare the WAVECAR for RPA or GW calculations, where many unoccupied orbitals are calculated (more than 30-50 % of the states spanned by the full plane-wave basis). To speed up the calculations, we recommend performing a routine ground-state calculation before calculating the unoccupied states.

## Related tags and articles

ALGO,
LSUBROT,
NELM,
TIME,
LDIAG

Examples that use this tag

## References

---
