# Blue moon ensemble

Categories: Advanced molecular-dynamics sampling, Theory

In general, constrained molecular dynamics generates biased statistical averages. The blue moon ensemble average, also known as constrained-reaction-coordinate-dynamic (CRCD) ensemble, connects constrained and unconstrained molecular dynamics, cf. blue moon ensemble calculations. It shows that the correct average for a quantity $a(\xi)$ can be obtained using the formula:

:   $$a(\xi)=\frac{\langle |\mathbf{Z}|^{-1/2} a(\xi^\*) \rangle\_{\xi^\*}}{\langle |\mathbf{Z}|^{-1/2}\rangle\_{\xi^\*}},$$

where ${\xi}$ is the reaction coordinate, $\xi^\*$ restrains the reference coordinate, e.g. to a transition state, where the associate velocity is $\dot{\xi^\*} = 0$, the $\langle ... \rangle\_{\xi^\*}$ stands for the statistical average of the quantity enclosed in angle brackets computed for a constrained ensemble, and $Z$ is a mass metric tensor defined as:

:   $$Z\_{\alpha,\beta}={\sum}\_{i=1}^{3N} m\_i^{-1} \nabla\_i \xi\_\alpha \cdot \nabla\_i \xi\_\beta, \, \alpha=1,...,r, \, \beta=1,...,r,$$

It can be shown that the free energy gradient can be computed using the equation:

:   $$\Bigl(\frac{\partial A}{\partial \xi\_k}\Bigr)\_{\xi^\*}=\frac{1}{\langle|Z|^{-1/2}\rangle\_{\xi^\*}}\langle |Z|^{-1/2} [\lambda\_k +\frac{k\_B T}{2 |Z|} \sum\_{j=1}^{r}(Z^{-1})\_{kj} \sum\_{i=1}^{3N} m\_i^{-1}\nabla\_i \xi\_j \cdot \nabla\_i |Z|]\rangle\_{\xi^\*},$$

where $A$ is the free energy, $k\_B$ is the Boltzmann constant, $T$ is the temperature, and $\lambda\_{\xi\_k}$ is the Lagrange multiplier associated with the parameter ${\xi\_k}$ used in the SHAKE algorithm.

The free-energy difference between states (1) and (2) can be computed by integrating the free-energy gradients over a connecting path, e.g. using the Simpson method:

:   $${\Delta}A\_{1 \rightarrow 2} = \int\_{{\xi(1)}}^{{\xi(2)}}\Bigl( \frac{\partial {A}} {\partial \xi} \Bigr)\_{\xi^\*} \cdot d{\xi}.$$

Note that as the free energy is a state quantity, the choice of path connecting (1) with (2) is irrelevant. As an example, when calculating the transition state, if (1) were set to the reactant and (2) to the transition state, then ${\Delta}A\_{1 \rightarrow 2}$ would be the activation free energy for the reaction.

## References
