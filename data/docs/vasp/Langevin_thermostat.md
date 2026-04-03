# Langevin thermostat

Categories: Molecular dynamics, Thermostats, Theory, Howto

The Langevin thermostat maintains the temperature through a modification of Newton's equations of motion

:   $$\dot{r\_i} = p\_i/m\_i \qquad
    \dot{p\_i} = F\_i - {\gamma}\_i\,p\_i + f\_i,$$

where *Fi* is the force acting on atom *i* due to the interaction potential, γi is a friction coefficient, and *fi* is a random force simulating the random kicks by the damping of particles between each other due to friction. The random numbers are chosen from a Gaussian distribution with the following variance

:   $$\sigma\_i^2 = 2\,m\_i\,{\gamma}\_i\,k\_B\,T/{\Delta}t$$

with Δ*t* being the time-step used in the MD to integrate the equations of motion. Obviously, Langevin dynamics is identical to the classical Hamiltonian in the limit of vanishing γ.

* NVT ensemble:

The friction coefficient is set by the LANGEVIN\_GAMMA parameter.

* NpT ensemble:

As for the NVT ensemble the LANGEVIN\_GAMMA parameter has to be set. If the NpT ensemble is used (by setting ISIF=3) additionally the friction coefficient of the lattice LANGEVIN\_GAMMA\_L has to be provided too.

The Langevin thermostat is selected by MDALGO=3.

## Related tags and articles

Molecular-dynamics calculations, Andersen thermostat, Nosé-Hoover thermostat, CSVR thermostat, Nosé-Hoover chain thermostat, ISIF, MDALGO, LANGEVIN\_GAMMA, LANGEVIN\_GAMMA\_L

## References

---
