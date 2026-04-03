# Metadynamics

Categories: Advanced molecular-dynamics sampling, Theory

In metadynamics, the bias potential
that acts on a selected number of geometric parameters (collective variables) ξ={ξ1, ξ2, ...,ξ*m*} is constructed on-the-fly during the simulation. The Hamiltonian for the metadynamics $\tilde{H}(q,p)$ can be written as:

:   $$\tilde{H}(q,p,t) = H(q,p) + \tilde{V}(t,\xi),$$

where $H(q,p)$ is the Hamiltonian for the original (unbiased) system, and $\tilde{V}(t,\xi)$ is the time-dependent bias potential. The latter term is usually defined as a sum of Gaussian hills with height *h* and width *w*:

:   $$\tilde{V}(t,\xi) = h \sum\_{i=1}^{\lfloor t/t\_G \rfloor} \exp{\left\{ -\frac{|\xi^{(t)}-\xi^{(i \cdot t\_G)}|^2}{2
    w^2} \right\}}.$$

In practice, $\tilde{V}(t,\xi)$ is updated by adding a new Gaussian with a time increment *t*G, which is typically one or two orders of magnitude greater than the time step used in the MD simulation.

In the limit of infinite simulation time, the bias potential is related to the free energy via:

:   $$A(\xi) = - \lim\_{t \to \infty} \tilde{V}(t,\xi) + const.$$

Practical hints as how to adjust the parameters used in metadynamics (*h*, *w*, *t*G) are given in Refs. and .

The error estimation in free-energy calculations with metadynamics is discussed in Ref..

## Related tags and sections

Metadynamics calculations

## References

---
