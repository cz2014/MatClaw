# Direct optimization of the orbitals

Categories: Electronic minimization, Theory

With "direct optimization of the orbitals" we denote a category of electronic minimization algorithms that use the gradient of the free energy with respect to the orbitals to move towards the ground state of the system: the orbitals are changed such that the total energy is lowered, using, *e.g.* the conjugate gradient approximation, or damped molecular dynamics.

In direct optimization methods, the orthogonality constraints are directly incorporated into the functional that is optimized, through Lagrange multipliers.
So in fact, instead of minimizing the  Kohn-Sham free energy functional *F*, one minimizes the following Langrangian:

:   $$\bar{F} = F - \sum\_{mn} \gamma\_{mn} \left( \langle \psi\_m |S| \psi\_n \rangle - \delta\_{mn} \right) -
    \mu \left( \sum\_n f\_n - N\_{\rm el} \right)$$

The gradient of this Langrangian with respect to an orbital $\psi\_n$, is given by:

:   $$| g\_n \rangle = f\_n \Big(1-\sum^N\_{m=1} \hat{S} \vert \psi\_m \rangle \langle \psi\_m \vert\Big) \hat{H} \vert \psi\_n \rangle +
    \sum^N\_{m=1} \frac{1}{2} {\bf H}\_{nm} (f\_n - f\_m) \hat{S} \vert \psi\_m \rangle$$

where $\{ f\_i | i=1,..,N \}$ are the partial occupancies, and

:   $${\bf H}\_{nm}=\langle \psi\_m \vert \hat{H} \vert \psi\_n \rangle$$

is the Hamiltonian expressed within the subspace spanned by the current orbitals $\{ \psi\_i | i=1,..,N \}$.

The structure of the gradient may be understood as follows: the first part on the right-hand side describes the change of the free energy with respect to changes in the orbitals that are outside (orthogonal) the subspace spanned by the current set of orbitals,
whereas the second part describes the changes of the free energy due to a unitary transformation between the orbitals within this subspace.

To derive a search direction, *i.e.*, actual change in the orbitals from the gradient these aforementioned parts are treated separately.
The search direction related to the out-of-subspace part of the gradient is:

:   $$\vert p\_n \rangle = f\_n K \Big(1-\sum^N\_{m=1} \hat{S} \vert \psi\_m \rangle \langle \psi\_m \vert\Big) \hat{H} \vert \psi\_n \rangle$$

where $K$ is a preconditioning function.

The search direction associated with the subspace rotational part of the gradient may be constructed using Loewdin perturbation theory:

:   $$U\_{nm} = \delta\_{nm} - \Delta \frac{H\_{nm}}{H\_{mm}-H\_{nn}}$$

where $\Delta$ denotes the stepsize.
Note that taking a step along this search direction amounts to a rotation of the orbitals (*rotation* on account of $U$ being unitary):

:   $$\vert \psi\_n \rangle = \sum^N\_{m=1} U\_{nm} \vert \psi\_m \rangle$$

Per default, however, VASP constructs a search direction for the subspace rotational part of the gradient in the manner proposed by Freysoldt *et al.*

Changes in the partial occupancies are computed in accordance with the aforementioned work as well.

When the three contributions to the "search direction" (*out-of-subspace*, *subspace rotational*, and *change in the partial occupancies*) have been determined, they are used to update the orbitals and partial occupancies, either by steepest descent, by means of the conjugate-gradient approximation, or using a damped molecular dynamics scheme.

After every change of the orbitals and partial occupancies, the total energy and electronic density are recomputed.
Per default, the electronic density is constructed directly from the orbitals and partial occupancies at each step along the way, without any density mixing.
Optionally, though, density mixing may be used to stabilise these optimisation procedures when charge sloshing occurs.

The direct optimization of the orbitals stops when the change of the total energy drops below EDIFF.

Note that, when starting from scratch (ISTART = 0), the direct optimization procedures in VASP always begin with several (NELMDL) self-consistency cycles where the density is kept fixed at the initial approximation (overlapping atomic charge densities), using the blocked-Davidson algorithm to optimize the orbitals.
This ensures that the orbitals, that are initialised with random numbers, have converged to reasonable starting point for the subsequent direct optimization.

## References

---
