# CSVR thermostat

Categories: Molecular dynamics, Thermostats, Theory

One popular strategy to control the temperature in NVT MD is based on rescaling atomic velocities ($\mathbf{v}\_{i}$) at a certain predefined frequency by a factor $\alpha = \sqrt{\bar{K}/K}$ in such a way that the total kinetic energy of the system

:   :   $$K= \frac{1}{2} \sum\limits\_{i=1}^{N} m\_i |\mathbf{v}\_{i}|^2,$$

is equal to the average kinetic energy corresponding to a given temperature:

:   :   $$\bar{K} = \frac{1}{2}N\_f k\_B T$$

where $N\_f$ is the number of degrees of freedom (e.g., $N\_f = 3N -3$ in the case of 3D periodic systems) and $N$ is the number of atoms per the simulation cell. Such a method, however, suffers from several problems. First, the ensemble generated is not strictly canonical. Second, rescaling velocities creates discontinuities in trajectories. As a consequence, the method has no conserved quantity that could be used to guide the choice of simulation parameters, such as the size of the integration step. Also, the rescaling introduces artificial fast fluctuations to velocities, making the evaluation of time correlations problematic. Finally, the trajectories generated via a naïve rescaling method often suffer from ergodicity issues, such as the flying ice-cube problem, in which kinetic energy of a part of the vibrational degrees of freedom is transferred into translations and/or rotations, violating the equipartition principle.

The canonical sampling through velocity rescaling (CSVR) proposed by Bussi et al. removes most of the difficulties of the naïve rescaling approach. Here, the term $\bar{K}$ is replaced by $K\_{t}$ obtained for each time step by propagating in time via auxiliary dynamics

:   :   $$dK = (\bar{K} - K) \frac{dt}{\tau} + 2\sqrt{\frac{K\bar{K}}{N\_f}} \frac{dW}{\sqrt{\tau}}$$

where $dW$ is a Wiener noise and $\tau$ determines the characteristic time scale of the CSVR thermostat. The latter is the only parameter of this thermostat and can be defined via flag CSVR\_PERIOD. Importantly, the auxiliary dynamics generates canonical distribution for kinetic energy:

:   :   $$P(K\_t) dK\_t \propto K\_t^{(N\_f/2 - 1)} e^{-K\_t/k\_B T} dK\_t$$

The conserved quantity of the CSVR thermostat is the effective energy $\tilde{H}$ defined as:

:   :   $$\tilde{H}(t) = H(t) - \int\_0^{t'} (\bar{K}-K)\frac{dt'}{\tau} - 2\int\_0^{t} \sqrt{\frac{K{t'}\bar{K}}{N\_f}} \frac{dW(t')}{\sqrt{\tau}}$$

As shown by Bussi et al., the CSVR thermostat does not significantly affect the evaluation of dynamical properties, such as the velocity autocorrelation functions or diffusion coefficients.

## Related tags and articles

Molecular-dynamics calculations, Andersen thermostat, Nosé-Hoover thermostat, Langevin thermostat, Nosé-Hoover chain thermostat, ISIF, MDALGO, CSVR\_PERIOD

---

## References
