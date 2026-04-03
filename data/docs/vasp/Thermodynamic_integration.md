# Thermodynamic integration

Categories: Advanced molecular-dynamics sampling, Theory

A detailed description of thermodynamic integration is given in reference .

The free energy of a fully interacting system can be written as the sum of the free energy a non-interacting reference system and the difference in the free energy of the fully interacting system and the non-interacting system

:   :   $F\_{1} = F\_{0} + \Delta F\_{0\rightarrow 1}$.

Using thermodynamic integration the free energy difference between the two systems is written as

$\Delta F\_{0\rightarrow 1} = \int\limits\_{0}^{1} d\lambda \langle U\_{1}(\lambda) - U\_{0}(\lambda) \rangle\_{\lambda}$.

Here $U\_{1}(\lambda)$ and $U\_{0}(\lambda)$ describe the potential energies of a fully-interacting and a non-interacting reference system, respectively. The coupling strength of the systems is controlled via the coupling parameter $\lambda$. It is neccessary that the connection of the two systems via the coupling constant is reversible. The notation $\langle \ldots \rangle\_{\lambda}$ denotes an ensemble average of a system driven by the following classical Hamiltonian

:   :   $H\_{\lambda}= \lambda H\_{1} + (1-\lambda) H\_{0}$.

## Thermodynamic integration with harmonic reference

The Helmholtz free energy ($A$) of a fully interacting system (1) can be expressed in terms of that of system harmonic in Cartesian coordinates (0,$\mathbf{x}$) as follows

:   $$A\_{1} = A\_{0,\mathbf{x}} + \Delta A\_{0,\mathbf{x}\rightarrow 1}$$

where $\Delta A\_{0,\mathbf{x}\rightarrow 1}$ is anharmonic free energy. The latter term can be determined by means of thermodynamic integration (TI)

:   $$\Delta A\_{0,\mathbf{x}\rightarrow 1} = \int\_0^1 d\lambda \langle V\_1 -V\_{0,\mathbf{x}} \rangle\_\lambda$$

with $V\_i$ being the potential energy of system $i$, $\lambda$ is a coupling constant and $\langle\cdots\rangle\_\lambda$ is the NVT ensemble average of the system driven by the Hamiltonian

:   $$\mathcal{H}\_\lambda = \lambda \mathcal{H}\_1 + (1-\lambda)\mathcal{H}\_{0,\mathbf{x}}$$

Free energy of harmonic reference system within the quasi-classical theory writes

:   $$A\_{0,\mathbf{x}} = A\_\mathrm{el}(\mathbf{x}\_0) - k\_\mathrm{B} T \sum\_{i = 1}^{N\_\mathrm{vib}} \ln \frac{k\_\mathrm{B} T}{\hbar \omega\_i}$$

with the electronic free energy $A\_\mathrm{el}(\mathbf{x}\_0)$ for the
configuration corresponding to the potential energy minimum with the
atomic position vector $\mathbf{x}\_0$,
the number of vibrational degrees of freedom $N\_\mathrm{vib}$, and the angular frequency $\omega\_i$ of vibrational mode $i$ obtained using the Hesse matrix $\underline{\mathbf{H}}^\mathbf{x}$.
Finally, the harmonic potential energy is expressed as

:   $$V\_{0,\mathbf{x}}(\mathbf{x}) = V\_{0,\mathbf{x}}(\mathbf{x}\_0) + \frac{1}{2} (\mathbf{x} - \mathbf{x}\_0)^T \underline{\mathbf{H}}^\mathbf{x} (\mathbf{x} - \mathbf{x}\_0)$$

Thus, a conventional TI calculation consists of the following steps:

1. determine $\mathbf{x}\_0$ and $V\_{0,\mathbf{x}}(\mathbf{x}\_0)$ in structural relaxation
2. compute $\omega\_i$ in vibrational analysis
3. use the data obtained in the point 2 to determine $\underline{\mathbf{H}}^\mathbf{x}$ that defines the harmonic forcefield
4. perform NVT MD simulations for several values of $\lambda \in \langle0,1\rangle$ and determine $\langle V\_1 -V\_{0,\mathbf{x}} \rangle$
5. integrate $\langle V\_1 -V\_{0,\mathbf{x}} \rangle$ over the $\lambda$ grid and compute $\Delta A\_{0,\mathbf{x}\rightarrow 1}$

Unfortunately, there are several problems linked with such a straightforward approach. First, the systems with rotational and/or translational degrees of freedom cannot be treated in a straightforward manner because $V\_{0,\mathbf{x}}(\mathbf{x})$ is not invariant under rotations and translations. Conventional TI is thus unsuitable for simulations of gas phase molecules or adsorbate-substrate systems. and this problem also imposes restrictions on the choice of thermostat used in NVT simulation (Langevin thermostat, for instance, does not conserve position of the center of mass and is therefore unsuitable for the use in conventional TI). Furthermore, if the Hesse matrix of the harmonic system has one or more eigenvalues that nearly vanish, the simulations with $\lambda \rightarrow$ 0 is likely to generate unphysical configurations causing serious convergence issues. These problems have been addressed in series of works by Amsler et al.

First, the method was formulated in terms of rotationally and translationally invariant internal coordinates $\mathbf{q}=\mathbf{q}(\mathbf{x})$, whereby the free energy of interacting system is repartitioned as follows:

:   $$A\_1 = A\_{0,\mathbf{x}} + \Delta A\_{0,\mathbf{x} \rightarrow 0,\mathbf{q}} + \Delta A\_{0,\mathbf{q} \rightarrow 1}$$

where $\Delta A\_{0,\mathbf{x} \rightarrow 0,\mathbf{q}}$ is the free energy change due to transformation from the system harmonic in $\mathbf{x}$ into the system harmonic in $\mathbf{q}$ and $\Delta A\_{0,\mathbf{q} \rightarrow 1}$ is that for the transformation of the latter into a fully interacting system. The force field for the system harmonic in $\mathbf{q}$ is defined as:

:   $$V\_{0,\mathbf{q}}(\mathbf{q}) = V\_{0,\mathbf{q}}(\mathbf{q}\_0) + \frac{1}{2} (\mathbf{q} - \mathbf{q}\_0)^T \mathbf{\underline{H}^q} (\mathbf{q} - \mathbf{q}\_0)$$

where $\mathbf{q}\_0=\mathbf{q}(\mathbf{x}\_0)$ and the Hesse matrix $\mathbf{\underline{H}}^\mathbf{q}$ defined for a potential energy minimum is related to $\mathbf{\underline{H}}^\mathbf{x}$ via
$\mathbf{\underline{H}}^\mathbf{x} = \mathbf{\underline{B}}^T \mathbf{\underline{H}}^\mathbf{q} \mathbf{\underline{B}}$
with
$\mathbf{\underline{B}}\_{i,j} = \frac{\partial q\_i}{\partial x\_j}$
being the Wilson matrix. Note that the calculation of the term $\Delta A\_{0,\mathbf{x} \rightarrow 0,\mathbf{q}}$ is inexpensive as it corresponds to a force field to force field transformation. Furthermore, this term vanishes in the case of phase volume conserving coordinates, such as interatomic distances.

## References

---
