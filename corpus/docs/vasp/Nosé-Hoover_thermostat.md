# Nosé-Hoover thermostat

Categories: Molecular dynamics, Thermostats, Theory, Howto

In the approach by Nosé and Hoover, an extra degree of freedom is introduced in the Hamiltonian. The heat bath is considered as an integral part of the system and has a fictious coordinate $s$ which is introduced into the Lagrangian of the system. This Lagrangian for a $N$ particle system is written as

:   :   $$\mathcal{L} = \sum\limits\_{i=1}^{N} \frac{m\_{i}}{2} s^{2} \dot{\mathbf{r}}\_{i}^{2} - U(\mathbf{r}) + \frac{Q}{2} \dot{s}^{2}-g k\_{B} T \mathrm{ln} \, s$$

where $m\_{i}$ and $k\_{B}$ are the mass of ion $i$ and the Boltzmann constant, respectively. The first two terms are the kinetic and potential energy of the system. The third and fourth term represent the kinetic and potential energy of the fictitious coordinate $s$. These terms also ensure the energy conservation of the Nosé-Hoover thermostat. The parameter $g$ is usually equal to the number of degrees of freedom of the system $g=3N - N\_{\mathrm{constraint}}$, where $N\_{\mathrm{constraint}}$ is equal to the number of constraint set (fixed coordinates in the POSCAR file). The parameter $Q$ is an effective "mass" of $s$, which controls the coupling of the system to the heat bath. It is set by the INCAR tag SMASS.

The Nosé-Hoover thermostat is selected by MDALGO=2.

## Related tags and articles

Molecular-dynamics calculations, Andersen thermostat, Langevin thermostat, CSVR thermostat, Nosé-Hoover chain thermostat, ISIF, MDALGO, SMASS

## References

---
