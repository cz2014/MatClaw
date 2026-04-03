# Category:Electronic minimization

Categories: VASP

By **electronic minimization** we denote the process of determining the electronic ground state. This is an integral part of the vast majority of VASP calculations. The **electronic minimization** in VASP is highly optimized, and different settings warrant the use of different algorithms or procedures. For instance, very elongated cells are prone to charge sloshing, which hampers convergence and can be avoided by clever settings in the density mixer. To learn the basics of electronic minimization in practice, visit the following how-to pages:

* Setting up an electronic minimization
* Troubleshooting electronic convergence

## Theoretical background

Within the context of Hohenberg-Kohn-Sham density functional theory, the ground state is that state of the system that minimizes the Kohn-Sham free energy:

:   $$F = \sum\_n f\_n \epsilon\_n -E\_{\rm H}\left[ \rho \right] +
    E\_{\rm xc} \left[ \rho \right] -\int V\_{\rm xc}({\bf r})\rho({\bf r})d{\bf r} -
    \sum\_n \sigma S \left( \frac{\epsilon\_n - \mu}{\sigma} \right)$$

where the electronic density is given by:

:   $$\rho({\bf r})= \sum\_n f\_{n} |\psi\_{n}({\bf r})|^2$$

and the Kohn-Sham orbitals and eigenenergies, $\{\psi\_n, \epsilon\_n \}$ are solutions to the Kohn-Sham equations:

:   $$H \left[ \rho \right] | \psi\_n \rangle = \epsilon\_n S | \psi\_n \rangle$$

under the constraint that the orbitals are *S*-orthonormal:

:   $$\langle \psi\_m | S | \psi\_n \rangle = \delta\_{mn}$$

The various algorithms for **electronic minimization** VASP offers, can be roughly divided into two categories:

* Iterative matrix diagonalisation + density mixing, *aka* the self-consistency cycle (SCC).
* Direct optimization of the orbitals.

Selecting a particular method of **electronic minimization** is done by means of the ALGO (or IALGO) tag.

## Self-consistency cycle

1. The SCC starts with an initial guess for the electronic density of the system. In particular, VASP uses the approximation of overlapping atomic charge densities. This density defines the initial Hamiltonian.
2. By means of iterative matrix-diagonalization techniques, one obtains the NBANDS lowest lying eigenstates of the Hamiltonian. The iterative matrix-diagonalization algorithms implemented in VASP are the blocked-Davidson algorithm and the residual-minimization method with direct inversion in the iterative subspace (RMM-DIIS). Per default VASP uses the blocked-Davidson algorithm (ALGO = Normal).
3. After the eigenstates and eigenvalues have been determined with sufficient accuracy, they are used in order to compute the total energy of the system and to construct a new electronic density.
4. In principle, this new density could be taken to define a new Hamiltonian. However, in order to obtain a stable algorithm, this new density is not used as is but is mixed with the old density. By default VASP uses a Broyden mixer. The resulting density then defines the new Hamiltonian for the next round of iterative matrix diagonalization (step 2).

Steps 2-4 are repeated until the change in the total energy from one cycle to the next drops below a specific threshold set by EDIFF.

Note that when starting from scratch (ISTART = 0), the SCC procedure of VASP always begins with several (NELMDL) cycles where the density is kept fixed at the initial approximation, i.e., overlapping atomic charge densities.
This ensures that the wavefunctions that are initialized with random numbers have converged to something sensible before they are used to construct a new charge density.

For a more detailed description of the SCC have a look at: the self-consistency cycle.

## Direct optimization

Similar to the SCC procedure described above, when starting from scratch (ISTART = 0), the direct optimization procedures in VASP always begin with several (NELMDL) self-consistency cycles where the density is kept fixed at the initial approximation (overlapping atomic charge densities).
This ensures that the wavefunctions that are initialized with random numbers have converged to a reasonable starting point for the subsequent direct optimization.

The direct optimization of the orbitals uses the gradient of the total energy with respect to the orbitals to move towards the ground state of the system: the orbitals are changed such that the total energy is lowered, using, e.g., the conjugate-gradient approximation, or damped molecular dynamics.

After every change of the orbitals, the total energy and electronic density are recomputed.
Per default, the electronic density is constructed directly from the orbitals at each step along the way, without any density mixing.
Optionally, though, density mixing may be used to stabilize these optimization procedures when charge sloshing occurs.

As for the SCC described above, the direct optimization of the orbitals stops when the change of the total energy drops below EDIFF.

For more details on the direct optimization algorithms, please read: direct optimization of the orbitals.

## Tutorials

* Lecture available on electronic optimization.
