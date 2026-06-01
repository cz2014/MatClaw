# Conjugate gradient optimization

Categories: Electronic minimization, Theory

Instead of the previous iteration scheme, which is just
some kind of Quasi-Newton scheme, it also possible to optimize the
expectation value of the Hamiltonian using a successive number of
conjugate gradient steps.
The first step is equal to the steepest descent step in section Single band steepest descent scheme.
In all following steps the preconditioned gradient $g^N\_{n}$
is conjugated to the previous search direction.
The resulting conjugate gradient algorithm is almost as efficient as the algorithm
given in Efficient single band eigenvalue-minimization.
For further reading see .

## References

---
