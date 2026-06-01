# RMM-DIIS

Categories: Electronic minimization, Theory

The implementation of the Residual Minimization Method with Direct Inversion in the Iterative Subspace (RMM-DIIS) in VASP is based on the original work of Pulay:

* The procedure starts with the evaluation of the preconditioned residual vector for some selected orbital $\psi^0\_m$:

:   :   $$K \vert R^0\_m \rangle = K \vert R(\psi^0\_m) \rangle$$
:   where $K$ is the preconditioning function, and the residual is computed as:

    :   $$\vert R(\psi) \rangle = (H-\epsilon\_{\rm app}) \vert \psi \rangle$$
:   with

    :   $$\epsilon\_{\rm app} = \frac{\langle \psi \vert H \vert \psi \rangle}{\langle \psi \vert S \vert \psi \rangle}$$

* Then a Jacobi-like trial step is taken in the direction of the vector:

:   :   $$\vert \psi^1\_m \rangle = \vert \psi^0\_m \rangle + \lambda K \vert R^0\_m \rangle$$
:   and a new residual vector is determined:

    :   $$\vert R^1\_m \rangle = \vert R(\psi^1\_m) \rangle$$

* Next a linear combination of the initial orbital $\psi^0\_m$ and the trial orbital $\psi^1\_m$

:   :   $$\vert \bar{\psi}^M \rangle = \sum^M\_{i=0} \alpha\_i \vert \psi^i\_m \rangle, \,\, M=1$$
:   is sought, such that the norm of the residual vector is minimized. Assuming linearity in the residual vector:

    :   $$\vert \bar{R}^M \rangle = \vert R(\bar{\psi}^M) \rangle = \sum^M\_{i=0} \alpha\_i \vert R^i\_m \rangle$$
:   this requires the minimization of:

    :   $$\frac{\sum\_{ij} \alpha\_i^\* \alpha\_j \langle R^i\_m \vert R^j\_m \rangle}{\sum\_{ij}\alpha\_i^\* \alpha\_j \langle \psi^i\_m \vert S \vert \psi^j\_m \rangle}$$
:   with respect to ${\{\alpha\_i | i=0,..,M\}}$.
:   This step is usually called *direct inversion of the iterative subspace* (DIIS).

* The next trial step ($M=2$) starts from $\bar{\psi}^1$, along the direction $K \bar{R}^1$. In each iteration $M$ is increased by 1, and a new trial orbital:

:   :   $$\vert \psi^M\_m \rangle = \vert \bar{\psi}^{M-1} \rangle + \lambda K \vert \bar{R}^{M-1} \rangle$$
:   and its corresponding residual vector $R(\psi^M\_m)$ are added to the iterative subspace, that is subsequently inverted to yield $\bar{\psi}^M$.
:   The algorithm keeps iterating until the norm of the residual $\bar{R}^M$ has dropped below a certain threshold, or the maximum number of iterations per orbital has been reached (NRMM).

* Replace $\psi^0\_m$ by $\bar{\psi}^M$ and move on to start work on the next orbital, *e.g.* $\psi^0\_{m+1}$.

The size of the trial step $\lambda$ is a critical value for the stability of the algorithm. We have found that a reasonable choice for the trial step can be obtained from the minimization of the Rayleigh quotient along the search direction in *the first step*, this optimal $\lambda$ is then used for a particular orbital until the algorithm moves on to the next orbital.

As mentioned before, the optimization of an orbital is stopped when either the maximum number of iterations per orbital (NRMM), or a certain convergence threshold has been reached. The latter may be fine-tuned by means of the EBREAK, DEPER, and WEIMIN tags. Note: we do not recommend you to do so! Rather rely on the defaults instead.

The RMM-DIIS algorithm works on a "per-orbital" basis and as such it trivially parallelizes over orbitals, which is the default  parallelization strategy of VASP. However, to cast some of the operations involved into the form of *matrix-matrix multiplications* and leverage the performance of BLAS3 library calls, the RMM-DIIS implementation in VASP works on NSIM orbitals simultaneously.

Note that, in the self-consistency cycle of VASP, subspace rotation and RMM-DIIS refinement of the orbitals alternate.
Furthermore, VASP re-orthonormalizes the orbitals after the RMM-DIIS refinement step.
It should be emphasized that, in principle, the RMM-DIIS method should also converge without any explicit subspace diagonalization and/or re-orthonormalization.
However, in our experience their inclusion speeds up convergence so substantially that it shortens the time-to-solution of most calculations, even though these operations scale as $O(N^3)$.

A drawback of the RMM-DIIS method is that it always converges toward the eigenstates which are closest to the initial trial orbitals. This leads, in principle, to serious problems because there is no guarantee of convergence to the correct ground state at all: if the initial set of orbitals does not ‘‘span’’ the ground state it might happen that in the final solution some eigenstates are ‘‘missing’’. To avoid this, the initialization of the orbitals must be done with great care.
Therefore, either the number of non-selfconsistent cycles at the start of self-consistency cycle is chosen to be large (NELMDL = 12, for ALGO = VeryFast), or the non-selfconsistent cycles are done with the blocked-Davidson algorithm before switching over to the use of the RMM-DIIS (ALGO = Fast).

The RMM-DIIS is approximately a factor of 1.5-2 faster than the blocked-Davidson algorithm, but less robust.

## References

---
