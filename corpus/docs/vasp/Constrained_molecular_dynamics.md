# Constrained molecular dynamics

Categories: Advanced molecular-dynamics sampling, Theory

Constrained molecular dynamics is performed using the SHAKE algorithm.
In this algorithm, the Lagrangian for the system $\mathcal{L}$ is extended as follows:

:   $$\mathcal{L}^\*(\mathbf{q,\dot{q}}) = \mathcal{L}(\mathbf{q,\dot{q}}) +
    \sum\_{i=1}^{r} \lambda\_i \sigma\_i(q),$$

where the summation is over *r* geometric constraints, $\mathcal{L}^\*$ is the Lagrangian for the extended system, and λ*i* is a Lagrange multiplier associated with a geometric constraint σ*i*:

:   $$\sigma\_i(q) = \xi\_i({q})-\xi\_i \;$$

with ξ*i*(*q*) being a geometric parameter and ξ*i* is the value of ξ*i*(*q*) fixed during the simulation.

In the SHAKE algorithm, the Lagrange multipliers λi are determined in the iterative procedure:

1. Perform a standard MD step (leap-frog algorithm):

   :   $$v^{t+{\Delta}t/2}\_i = v^{t-{\Delta}t/2}\_i + \frac{a^{t}\_i}{m\_i} {\Delta}t$$
   :   $$q^{t+{\Delta}t}\_i = q^{t}\_i + v^{t+{\Delta}t/2}\_i{\Delta}t$$
2. Use the new positions *q*(*t*+Δ*t*) to compute Lagrange multipliers for all constraints:

   :   $${\lambda}\_k= \frac{1}{{\Delta}t^2} \frac{\sigma\_k(q^{t+{\Delta}t})}{\sum\_{i=1}^N m\_i^{-1} \bigtriangledown\_i{\sigma}\_k(q^{t}) \bigtriangledown\_i{\sigma}\_k(q^{t+{\Delta}t})}$$
3. Update the velocities and positions by adding a contribution due to restoring forces (proportional to λk):

   :   $$v^{t+{\Delta}t/2}\_i = v^{t-{\Delta}t/2}\_i + \left( a^{t}\_i-\sum\_k \frac{{\lambda}\_k}{m\_i} \bigtriangledown\_i{\sigma}\_k(q^{t}) \right ) {\Delta}t$$
   :   $$q^{t+{\Delta}t}\_i = q^{t}\_i + v^{t+{\Delta}t/2}\_i{\Delta}t$$
4. repeat steps 2-4 until either |σ*i*(*q*)| are smaller than a predefined tolerance (determined by SHAKETOL), or the number of iterations exceeds SHAKEMAXITER.

### Constrained molecular dynamics

For a description of constrained molecular dynamics see Constrained molecular dynamics.

* For a constrained molecular dynamics run with Andersen thermostat, one has to:

1. Set the standard MD-related tags: IBRION=0, TEBEG, POTIM, and NSW
2. Select the thermostat:
   1. Set MDALGO = 1 , and choose an appropriate setting for ANDERSEN\_PROB.
   2. Set MDALGO = 2 , and choose an appropriate setting for SMASS.
3. Define geometric constraints in the ICONST-file, and set the STATUS parameter for the constrained coordinates to 0
4. When the free-energy gradient is to be computed, set LBLUEOUT=.TRUE.

## References
