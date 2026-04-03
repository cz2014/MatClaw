# Preconditioning

Categories: Electronic minimization, Theory

The idea is to find a matrix that multiplied with the residual vector gives the
exact error in the wavefunction. Formally this matrix (the Greens function) can be written
down and is given by

:   :   $$\frac{1}{{\bf H} - \epsilon\_n},$$

where $\epsilon\_n$ is the exact eigenvalue for the band in interest.
Actually the evaluation of this matrix is not possible, recognizing that the
kinetic energy dominates the Hamiltonian for large $\mathbf{G}$-vectors
(i.e. $H\_{\mathbf{G},\mathbf{G'}} \to \delta\_{\mathbf{G},\mathbf{G'}} \frac{\hbar^2}{2m} \mathbf{G}^2$), it
is a good idea to approximate the matrix by a diagonal
function which converges to $\frac{2m}{\hbar^2 \mathbf{G}^2}$ for large $\mathbf{G}$ vectors, and possess
a constant value for small $\mathbf{G}$ vectors.
We actually use the preconditioning function proposed by Teter et. al

:   :   $$\langle \mathbf{G} | {\bf K} | \mathbf{G'}\rangle = \delta\_{\mathbf{G} \mathbf{G'}} \frac{ 27 + 18 x+12 x^2 + 8x^3}
        {27 + 18x + 12x^2+8x^3 +16x^4} \quad \mbox{and} \quad
        x = \frac{\hbar^2}{2m} \frac{G^2} {1.5 E^{\rm kin}( \mathbf{R}) },$$

with $E^{\rm kin}(\mathbf{R})$ being the kinetic energy of the residual vector.
The preconditioned residual vector is then simply

:   :   $$| p\_n \rangle = {\bf K} | R\_n \rangle.$$

## References

---
