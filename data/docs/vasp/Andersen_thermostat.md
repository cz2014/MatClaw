# Andersen thermostat

Categories: Molecular dynamics, Thermostats, Theory, Howto

In the approach proposed by Andersen the system is thermally coupled to a fictitious heat bath with the desired temperature. The coupling is represented by stochastic collisions that act occasionally on randomly selected particles. In particular the momentum of the *lucky* particle at every collision step is instantaneously chosen at random from the Boltzmann distribution at the selected temperature. The collision probability is defined as an average number of collisions per atom and time-step and the collision frequency occurs with the following distribution

:   :   $$P(t)=\nu e^{-\nu t}.$$

The exponent of this the distribution ($\nu t$) is controlled by the flag ANDERSEN\_PROB. Since $t$ is the time step in the calculation ANDERSEN\_PROB has to be scaled if the time step changes. The total number of collisions with the heat-bath is written out to the file REPORT for each MD step.

A very good implementation of the Andersen thermostat can be found in chapter 6.1.1 of reference .

The Andersen thermostat is selected by setting MDALGO=1.

## Related tags and articles

Molecular-dynamics calculations, Nosé-Hoover thermostat, Langevin thermostat, CSVR thermostat, Nosé-Hoover chain thermostat, ISIF, MDALGO, ANDERSEN\_PROB

## References

---
