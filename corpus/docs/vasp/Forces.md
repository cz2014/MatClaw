# Category:Forces

Categories: VASP, Ionic minimization, Machine-learned force fields, Molecular dynamics

**Forces** on particles describe the interactions that cause particles, such as atoms and molecules, to move and behave in specific ways. In materials, forces result from electromagnetic interactions, which can be computed by means of the Hellmann-Feynman theorem within density-functional theory (DFT), the random-phase approximation (RPA) or by the use of machine-learned force fields (MLFF), also refered to as machine-learned potentials. Understanding forces between atoms is crucial in many aspects of material science, for example:

* predicting the atomic structure of solids and molecules (structure optimization)
* chemical reactions, catalysis, etc. (transition states)
* thermodynamic processes (molecular dynamics)

For a classical particle, Newton's second law of motion states that the change of motion of an object is proportional to the force acting on the object and oriented in the same direction as the force vector $\mathbf{F}(t)$. Therefore, the force is defined as the change of particle momentum with time

:   :   $$\mathbf{F}(t) = m\frac{d\mathbf{v}(t)}{d t} = m\mathbf{a}(t),$$

where $\mathbf{a}(t)$ is the acceleration of the particle. Here, the velocity is defined as the change of position with time $\mathbf{v}(t) = \frac{d\mathbf{r}(t)}{dt}$, $\mathbf{r}(t)$ is the position of the particle, and the momentum $\mathbf{p}(t)$ of the particle is the velocity times the particle mass $m$: $\mathbf{p}(t) = m\mathbf{v}(t).$

> **Mind:** With this equation of motion, the knowledge of some starting conditions $\mathbf{r}(0)$ and $\mathbf{v}(0)$ and an algorithm to compute the forces $\mathbf{F}$ the trajectory $\mathbf{r}(t)$ of a particle can be predicted for all times.

Moreover, one can directly relate the force and the negative gradient of the potential energy. The gradient of the potential energy can be computed from the Lagrangian of the particle system of interest. The Lagrangian for an N particle system is

:   :   $$L= \sum\_{i=1}^{N}m\_{i}\mathbf{v}^{2}\_{i} - V(\{\mathbf{r}\_{i}\}),$$

where $V(\{\mathbf{r}\_{i}\})$ is the potential energy of the system. Using Lagrange's equation of the second kind$\frac{d}{dt}\frac{\partial L}{\partial \mathbf{v}\_{i}}=\frac{\partial L}{\partial \mathbf{r}\_{i}}$ yields the relation

:   :   $$\mathbf{F}\_{i} = -\frac{\partial V(\{\mathbf{r}\_{i}\})}{\partial \mathbf{r}\_{i}} = -\nabla V(\{\mathbf{r}\_{i}\}).$$

> **Mind:** To obtain forces and particle trajectories, the negative gradient of the potential energy has to be computed.

## DFT forces

One way to compute the potential energy's negative gradient is through DFT. In DFT there is no classical potential energy function $V(\{\mathbf{r}\_{i}\})$ but a Hamiltonian $\mathcal{H}$ depending on the ionic positions $\mathbf{R}\_{i}$ and the electronic positions $\mathbf{r}\_{i}$. The total energy is given by

:   :   $$E\_{tot} = -\frac{1}{2}\int \sum\_{i}\psi\_{i}^{\*}({\bf r})\nabla^{2}\psi\_{i}({\bf r}) d{\bf r} - \int \sum\_{A}\frac{Z\_{A}}{\left\vert{\bf r}-{\bf R}\_{A}\right\vert}n({\bf r})d{\bf r} + \int \int \frac{1}{2}\frac{n({\bf r})n({\bf r'})}{\left\vert{\bf r}-{\bf r'}\right\vert} d{\bf r'}d{\bf r}+ E\_{\rm xc} + \frac{1}{2}\sum\_{A\ne B}\frac{Z\_{A}Z\_{B}}{\left\vert{\bf R}\_{A}-{\bf R}\_{B}\right\vert},$$

where $n(\mathbf{r})$ denotes the electronic ground-state density and $\psi\_{i}$ are the Kohn-Sham orbitals. $E\_{\rm xc}$ is the exchange-correlation energy. To obtain the force acting on ion A, the Hellmann-Feynman theorem has to be used.

:   :   $$\mathbf{F}\_{A}=-\nabla\_{A} E\_{tot}=\nabla\_{A}\sum\_{A}\int\frac{Z\_{A}}{\left\vert{\bf r}-{\bf R}\_{A}\right\vert}n({\bf r})d^{3}r -\nabla\_{A}\frac{1}{2}\sum\_{A\ne B}\frac{Z\_{A}Z\_{B}}{\left\vert{\bf R}\_{A}-{\bf R}\_{B}\right\vert},$$

where $\nabla\_{A}$ denotes the gradient with respect to ionic position $\mathbf{R}\_{A}$. The DFT forces will depend on the chosen exchange-correlation functional via the electronic ground-state density $n({\bf r})$. Therefore, the choice of the proper exchange-correlation functional for the system of interest is crucial for obtaining proper forces and, hence, the correct material properties.

## RPA forces

The RPA can be used to yield estimates for the exchange-correlation energy as well as forces (LRPAFORCE) within many-body perturbation theory.
Note that the RPA is a correction to the underlying functional. Therefore, the choice
of the proper exchange-correlation functional is still crucial in the RPA approach for obtaining forces.

> **Tip:** It is recommended to use the Perdew-Burke-Ernzerhof (PBE) XC potential, i.e., XC = PE .

The RPA forces are computed by the following equation

:   :   $$\mathbf{F}\_{A}=-Tr[\rho^{(1)}\nabla\_{A}V^{KS}-\gamma^{(1)}\nabla\_{A}S]$$

The operators $\rho^{1}$ and $\gamma^{1}$ are associated with the functional derivatives $\delta E/\delta V^{KS}$ and $\delta E/\delta S$ respectively. S defines the overlap operator between the Kohn-Sham orbitals of the used DFT approximation. The first term of the force equation can be associated with the exchange energy and the second term of the equation can be associated with the correlation part.

> **Mind:** It is recommended to use the GW POTCAR-files.

* ACFDT/RPA calculations

## Machine-learned forces

A speedy but less accurate approach for obtaining forces is through a machine-learned force field (MLFF). In this approach, a machine-learning model is first trained on either the DFT or RPA forces, whereby also energies and stresses are considered. In the case of the RPA, the stress tensor is not computed. The machine-learning approach will be an approximation to the underlying method against which it was fitted.

The MLFF approach is based on decomposing the total DFT energy into local atomic contributions $E\_{B}(\{\mathbf{R}\_{C}\})$ depending on all atomic positions in the system. Therefore, the force acting on ion A is computed by

:   $$\mathbf{F}\_{A} = -\nabla\_{A}\sum\_{B=1}^{N}E\_{B}(\{\mathbf{R}\_{C}\})=-\sum\_{B}^{N}w\_{B}\frac{dK\_{B}(\{\mathbf{R}\_{C}\})}{d\mathbf{R}\_{A}},$$

where $K(\mathbf{R}\_{C})$ is the kernel matrix which can be found on the machine learning theory page. The kernel matrix as the local energies depends on the positions of all atoms $\{\mathbf{R}\_{C}\}$ in the actual atomic configuration.

* Machine learning Basics
* Machine learning best practice

It is possible to **apply external machine-learned models** during a VASP run using the Python-plugins feature. The PLUGINS/MACHINE\_LEARNING tag in combination with a Python script offers a hook to directly supply a machine-learned potential or any other model expressed in terms of an ASE Calculator.

## Applying external forces

There are multiple ways to run simulations with effective forces acting on the ions. This includes selective dynamics defined in the POSCAR file, the LATTICE\_CONSTRAINTS tag and the ICONST file. To apply static driving forces in a closer sense, the EFOR tag offers direct control. Additionally it is possible to apply dynamically changing forces and stress using the Python-plugins feature. In particular, the PLUGINS/FORCE\_AND\_STRESS tag in combination with an appropriate Python script yields direct control at each ionic step.

> **Tip:** Depending on the method, an overall **drift** may be removed from the forces. See #DFT forces For instance, for structure optimization and for the Nosé-Hoover thermostat drifts are removed, but not for the stochastic Langevin thermostat.

## Related concepts

### Stress and pressure

The stress tensor (see ISIF) provides valuable information about how forces are distributed throughout a material, both in magnitude and direction. It includes normal stresses, which act perpendicular to a given plane, and shear stresses, which act parallel to the plane. Together, these components allow predicting how materials will behave under various conditions, such as tension, compression, or shear. The stress tensor can be computed from a viral theorem, including pair forces, or with a finite difference approach deforming the simulation box.

Pressure, often denoted as P, is a scalar component of the stress tensor. It represents the normal force per unit area acting on a surface within the material. In the stress tensor, pressure is related to the diagonal components $\sigma\_{xx}$, $\sigma\_{yy}$, and $\sigma\_{zz}$:

:   $$P = \frac{1}{3}(\sigma\_{xx} + \sigma\_{yy} + \sigma\_{zz}).$$

In other words, the pressure is the average of the normal components of the stress tensor in the three spatial directions. In electronic structure calculations, finite basis sets are used to express the electron density. Due to this finiteness of the basis set, errors on the stress tensor and the pressure are introduced. The error in the pressure is referred to as Pulay stress and can be corrected with the tag PSTRESS or by increasing ENCUT.

Related how-to pages:

* Volume relaxation
* NpT ensemble

### Force-constant matrix and phonons

The forces are defined as the negative gradient of the potential energy. The **force-constant matrix** is defined by

:   $$\Phi\_{I\alpha J\beta} (\{\mathbf{R}^0\}) =
    \left. \frac{\partial E(\{\mathbf{R}\})}{\partial R\_{I\alpha} \partial R\_{J\beta}} \right|\_{\mathbf{R} =\mathbf{R^0}}
    =
    - \left. \frac{\partial F\_{I\alpha}(\{\mathbf{R}\})}{\partial R\_{J\beta}} \right|\_{\mathbf{R} =\mathbf{R^0}}$$

and is, therefore, the gradient of the force. The force-constant matrix is a fundamental concept in solid-state physics and materials science, especially in the context of understanding the vibrational properties of crystals, i.e., phonons. It is a generalization of the spring constant $k$ inside ($\mathbf{F}=k\mathbf{x}$) for the case of 3D crystals. This matrix is used to describe the relationships between atomic displacements and the resulting forces that occur in a crystal. By Fourier transforming the force-constant matrix, the dynamical matrix is obtained.

By computing the eigenvalues of the dynamical matrix on various reciprocal lattice points, the phonon-dispersion relation can be obtained.
Understanding phonons is essential as they influence materials' properties directly, such as lattice thermal conductivity and mechanical properties, as well as indirectly via electron-phonon coupling that provides access to transport properties such as electrical conductivity, mobility, and electronic thermal conductivity.

* Phonons from finite differences
* Phonons from density-functional-perturbation theory
* Computing the phonon dispersion and DOS

## References
