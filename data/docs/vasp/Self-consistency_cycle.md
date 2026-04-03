# Self-consistency cycle

Categories: Electronic minimization, Theory

Fig. 1: the self-consistency cycle

The term **self-consistency cycle** (SCC) denotes a category of algorithms that determine the electronic ground state by a combination of iterative matrix diagonalization and density mixing.

Figure 1. shows a procedural flowchart of the self-consistency cycle:

1. When starting from scratch, the SCC starts with an initial guess for the electronic density of the system under consideration: VASP uses the approximation of overlapping atomic charge densities. The orbitals are initialized with random numbers. Alternatively, the SCC may (re-)start from the orbitals and/or electronic density obtained in a previous calculation.
2. The density defines the Hamiltonian.
3. By means of iterative matrix diagonalization techniques, one obtains the NBANDS lowest lying eigenstates of the Hamiltonian. The iterative matrix diagonalization algorithms implemented in VASP are the blocked-Davidson algorithm and the residual-minimization method with direct inversion in the iterative subspace (RMM-DIIS). Per default VASP uses the blocked-Davidson algorithm (ALGO = Normal). This step is often referred to as *iterative optimization/refinement of the orbitals*.
4. After the eigenstates and eigenvalues of the Hamiltonian, i.e., orbitals and one-electron energies, have been determined with sufficient accuracy, the corresponding partial occupancies of the orbitals are calculated.
5. From the one-electron energies and partial occupancies, the free energy of the system is computed.
6. From the orbitals and partial occupancies, a new electronic density is constructed.
7. In principle, the new density could be directly used to define a new Hamiltonian. In most cases, however, this does not lead to a stable algorithm (on account of, e.g., charge sloshing). Instead, the new density is not used directly but is mixed with the old density. By default VASP uses a Broyden mixer (IMIX). The resulting density then defines the new Hamiltonian for the next round of iterative matrix diagonalization.

Steps 2-7 are repeated until the change in the free energy from one cycle to the next drops below a specific threshold (EDIFF).

Note that when starting from scratch (ISTART = 0), the self-consistency cycle procedure of VASP always begins with several (NELMDL) cycles where the density is kept fixed at the initial approximation (overlapping atomic charge densities).
This ensures that the wavefunctions that are initialized with random numbers have converged to something sensible before they are used to construct a new charge density.

Especially in case of the RMM-DIIS the initial set of orbitals plays a critical role.
Therefore, either the number of non-selfconsistent cycles is chosen to be large (NELMDL = 12, for ALGO = VeryFast), or the non-selfconsistent cycles are done with the blocked-Davidson algorithm before switching over to the use of the RMM-DIIS (ALGO = Fast).

Furthermore, note that per default (LDIAG=.TRUE.) the iterative refinement of the orbitals is preceded (RMM-DIIS) or followed (blocked-Davidson) by a diagonalization of the subspace spanned by the current orbitals.
In case of the RMM-DIIS, the optimization step is additionally followed by an orthogonalization of the refined orbitals.

With respect to the aforementioned it should be emphasized that, in principle, the RMM-DIIS method should also converge without any explicit subspace diagonalization and/or re-orthonormalization. However, in our experience their inclusion speeds up the convergence of the self-consistency cycle so substantially that it shortens the time-to-solution of most calculations, even though these operations scale as $O(N^3)$.

For (a lot) more details on the self-consistency cycle and associated algorithms in VASP, we recommend the seminal papers by Kresse and Furthmüller.

## References

---
