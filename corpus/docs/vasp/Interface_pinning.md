# Interface pinning

Categories: Advanced molecular-dynamics sampling, Theory

**Interface pinning** is used to determine the melting point from a molecular-dynamics simulation of the interface between a liquid and a solid phase.
The typical behavior of such a simulation is to freeze or melt, while the interface is *pinned* with a bias potential.
This potential applies an energy penalty for deviations from the desired two-phase system.
It is preferred simulating above the melting point because the bias potential prevents melting better than freezing.

The Steinhardt-Nelson order parameter $Q\_6$ discriminates between the solid and the liquid phase.
With the bias potential

:   $$U\_\text{bias}(\mathbf{R}) = \frac\kappa2 \left(Q\_6(\mathbf{R}) - A\right)^2$$

penalizes differences between the order parameter for the current configuration $Q\_6({\mathbf{R}})$ and the one for the desired interface $A$.
$\kappa$ is an adjustable parameter determining the strength of the pinning.

Under the action of the bias potential, the system equilibrates to the desired two-phase configuration.
An important observable is the difference between the average order parameter $\langle Q\_6\rangle$ in equilibrium and the desired order parameter $A$.
This difference relates to the the chemical potentials of the solid $\mu\_\text{solid}$ and the liquid $\mu\_\text{liquid}$ phase

:   $$N(\mu\_\text{solid} - \mu\_\text{liquid}) =
    \kappa (Q\_{6,\text{solid}} - Q\_{6,\text{liquid}})(\langle Q\_6 \rangle - A)$$

where $N$ is the number of atoms in the simulation.

Computing the forces requires a differentiable $Q\_6(\mathbf{R})$.
In the VASP implementation a smooth fading function $w(r)$ is used to weight each pair of atoms at distance $r$ for the calculation of the $Q\_6(\mathbf{R},w)$ order parameter. This fading function is given as

:   $$w(r) = \left\{ \begin{array}{cl} 1 &\textrm{for} \,\, r\leq n \\
    \frac{(f^2 - r^2)^2 (f^2 - 3n^2 + 2r^2)}{(f^2 - n^2)^3} &\textrm{for} \,\, n\lt r\lt f \\
    0 &\textrm{for} \,\,f\leq r \end{array}\right.$$

Here $n$ and $f$ are the near- and far-fading distances, respectively.
The radial distribution function $g(r)$ of the crystal phase yields a good choice for the fading range.
To prevent spurious stress, $g(r)$ should be small where the derivative of $w(r)$ is large.
Set the near fading distance $n$ to the distance where $g(r)$ goes below 1 after the first peak.
Set the far fading distance $f$ to the distance where $g(r)$ goes above 1 again before the second peak.

## References

---
