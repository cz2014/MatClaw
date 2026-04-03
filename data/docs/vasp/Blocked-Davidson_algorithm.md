# Blocked-Davidson algorithm

Categories: Electronic minimization, Theory

The workflow of the blocked-Davidson iterative matrix diagonalization scheme implemented in VASP is as follows:

* Take a subset (block) of $n\_1$ orbitals out of the total set of NBANDS orbitals:

:   :   $\{ \psi\_n| n=1,..,N\_{\rm bands}\}\Rightarrow \{ \psi^1\_k| k=1,..,n\_1\}$.

* Extend the subspace spanned by $\{\psi^1\}$ by adding the preconditioned residual vectors of $\{\psi^1\}$:

:   :   $$\left \{ \psi^1\_k \, / \, g^1\_k = \left (1- \sum\_{n=1}^{N\_{\rm bands}} | \psi\_n \rangle \langle\psi\_n | {\bf S} \right) {\bf K} \left ({\bf H} - \epsilon\_{\rm app} {\bf S} \right ) \psi^1\_k \, | \, k=1,..,n\_1 \right \}.$$

* Rayleigh-Ritz optimization ("subspace rotation") within the $2n\_1$-dimensional space spanned by $\{\psi^1/g^1\}$, to determine the $n\_1$ lowest eigenvectors:

:   :   $${\rm diag}\{\psi^1/g^1\} \Rightarrow \{ \psi^2\_k| k=1,..,n\_1\}$$

* Extend the subspace with the residuals of $\{\psi^2\}$:

:   :   $$\left \{ \psi^2\_k \,/ \, g^1\_k \, / \, g^2\_k = \left (1- \sum\_{n=1}^{N\_{\rm bands}} | \psi\_n \rangle \langle\psi\_n | {\bf S} \right ) {\bf K} \left ({\bf H} - \epsilon\_{\rm app} {\bf S} \right) \psi^2\_k \, | \, k=1,..,n\_1 \right \}.$$

* Rayleigh-Ritz optimization ("subspace rotation") within the $3n\_1$-dimensional space spanned by $\{\psi^1/g^1/g^2\}$:

:   :   $${\rm diag}\{\psi^1/g^1/g^2\} \Rightarrow \{ \psi^3\_k| k=1,..,n\_1\}$$

* If need be the subspace may be extended by repetition of this cycle of adding residual vectors and Rayleigh-Ritz optimization of the resulting subspace:

:   :   $${\rm diag}\{\psi^1/g^1/g^2/../g^{d-1}\}\Rightarrow \{ \psi^d\_k| k=1,..,n\_1\}$$
:   Per default VASP will not iterate deeper than $d=4$, though it may break off even sooner when certain criteria that measure the convergence of the orbitals have been met.

* When the iteration is finished, store the optimized block of orbitals back into the set:

:   :   $\{ \psi^d\_k| k=1,..,n\_1\} \Rightarrow \{ \psi\_k| k=1,..,N\_{\rm bands}\}$.

* Move on to the next block $\{ \psi^1\_k| k=n\_1+1,..,2 n\_1\}$.
* When LDIAG=.TRUE. (default), a Rayleigh-Ritz optimization in the complete subspace $\{ \psi\_k| k=1,..,N\_{\rm bands}\}$ is performed after all orbitals have been optimized.

The blocksize $n\_1$ used in the blocked-Davidson algorithm can be set by means of the NSIM tag.
In principle $n\_1= 2\times$ NSIM, but for technical reasons it needs to be dividable by an integer *N*:

:   $$n\_1 = {\rm int}\left(\frac{2\*{\rm NSIM} + N - 1}{N}\right) N$$

where $N$ is the "number of band groups per k-point group":

:   $$N = \frac{{\rm \#\; of\; MPI\; ranks}}{{\rm IMAGES}\*{\rm KPAR}\*{\rm NCORE}}$$

(see the section on parallelization basics).

As mentioned before, the optimization of a block of orbitals is stopped when either the maximum iteration depth (NRMM), or a certain convergence threshold has been reached. The latter may be fine-tuned by means of the EBREAK, DEPER, and WEIMIN tags. Note: we do not recommend you to do so! Rather rely on the defaults instead.

The blocked-Davidson algorithm is approximately a factor of 1.5-2 slower than the RMM-DIIS, but more robust.

## References

---
