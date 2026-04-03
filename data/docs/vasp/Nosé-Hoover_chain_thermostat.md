# Nosé-Hoover chain thermostat

The standard Nosé-Hoover thermostat suffers from well-known issues, such as the ergodicity violation in the case of simple harmonic oscillator. As proposed by Martyna and Klein, these problems can be solved by using multiple Nosé-Hoover thermostats connected in a chain. Although the underlining dynamics is non-Hamiltonian, the corresponding equations of motion conserve the following energy term:

:   :   $$\mathcal{H'} = \mathcal{H}(\mathbf{r},\mathbf{p}) + \sum\limits\_{j=1}^{M} \frac{p\_{\eta\_j}^2}{2Q\_j} + (3N-N\_c)k\_{B} T \eta\_1 + k\_{B} T \sum\limits\_{j=2}^{M} \eta\_j,$$

where $\mathcal{H}(\mathbf{r},\mathbf{p})$ is the Hamiltonian of the physical system, $M$, $N$ and $N\_c$ are the numbers of thermostats, atoms in the cell, and geometric constraints, respectively, and $\eta\_{j}$, $p\_{\eta\_j}$, and $Q\_{j}$ are the position, momentum, and mass-like parameter associated with the thermostat $j$. Just like the total energy in the NVE ensemble,$\mathcal{H'}$ is valuable for diagnostics purposes. Indeed, a significant drift in $\mathcal{H'}$ indicates that the corresponding computational setting is suboptimal. Typical reasons for this behavior involve noisy forces (e.g., because of a poor SCF convergence) and/or a too large integration step (defined via POTIM).

The number of thermostats is controlled by the flag NHC\_NCHAINS. Typically, this flag is set to a value between 1 and 5, the maximal allowed value is 20. In the special case of NHC\_NCHAINS=0, the thermostat is switched off, leading to a MD in the microcanonical ensemble. Another special case of NHC\_NCHAINS=1 corresponds to the standard Nosé-Hoover thermostat.

The only parameter of this thermostat is the characteristic time scale ($\tau$), defined via flag NHC\_PERIOD. This parameter is used to setup the mass-like variables via the relations:

:   :   $$Q\_1 = 3 (N -N\_c)k\_{B} T \tau^2$$
    :   $$Q\_j = k\_{B} T \tau^2; \; \; \; j=2,\dots,M$$

Furthermore, due to rapidly varying forces in thermostat variables propagators, the standard velocity Verlet algorithm with fixed integration step might be insufficiently accurate. As proposed by Tuckerman, the RESPA methodology can be used to overcome this problem, in which the integration step used in thermostat variables propagation is split into NHC\_NRESPA equal parts, each of which may be further divided into NHC\_NS smaller parts treated by Suzuki-Yoshida scheme of fourth or sixth order.

## Related tags and articles

Molecular-dynamics calculations, Andersen thermostat, Nosé-Hoover thermostat, Langevin thermostat, CSVR thermostat, ISIF, MDALGO,NHC\_NCHAINS,NHC\_PERIOD,NHC\_NRESPA,NHC\_NS

## References
