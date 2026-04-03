# Category:Dielectric properties

Categories: VASP, Linear response

## Dielectric function

When light excites an electron from the valence to the conduction band, the created hole can bind with the electron to form an exciton.

When an external electric field $\mathbf E$ acts on a medium, both the electronic and ionic charges will react to the perturbing field. For dielectric materials, in a very simplistic approach, one can thinkthat the bound charges will create dipoles inside the medium leading to an induced polarization, $\mathbf P$. The combined effects of both fields are expressed in the electric displacement field $\mathbf D$, given by

:   :   $\mathbf D = \mathbf E + 4\pi\mathbf P$.

If the external field is not strong enough to significantly change the properties of the dielectric medium, one can treat the induced polarization within the so-called linear response regime. Here, the information on how the dielectric reacts on the external field is given by the **dielectric function**:

:   :   $\epsilon\_{\alpha\beta} = \delta\_{\alpha\beta} + 4\pi\frac{\partial P\_i}{\partial E\_j}$,

which (assuming that the system has time-reversal symmetry) leads to

:   :   $D\_\alpha(\omega) = \epsilon\_{\alpha\beta}(\omega)E\_\beta(\omega)$.

Depending on the nature of the external field, there are different approaches for the calculation of $\epsilon$. If $\mathbf E$ is static, then one can rely on perturbative methods based on finite differences or density functional perturbation theory (DFPT). However, if the perturbation is a time-dependent $\mathbf E$-field, (e.g., in measurements of the optical absorption, reflectance, magneto-optical Kerr effect (MOKE), etc.), the response will depend on the frequency of the external field. For these cases, one must employ methods based on time-dependent linear response, (e.g., Green-Kubo) or many-body perturbation theory.

Below we present an overview of all possible cases where VASP employs either one of such methods for the calculation of $\epsilon$.

### Static response

#### LEPSILON: density-functional-perturbation theory (DFPT)

:   By setting LEPSILON=.True., VASP uses DFPT to compute the static ion-clamped dielectric matrix with or without local field effects (LRPA). Derivatives are evaluated using Sternheimer equations, avoiding the explicit computation of derivatives of the periodic part of the wave function. This method does not require the inclusion of empty states via NBANDS.

:   At the end of the calculation, both the values of $\epsilon$ including (LRPA=.True.) or excluding (LRPA=.False.) local-field effects are printed in the OUTCAR file. Perform a consistency check by comparing the values excluding local-field effects and static limit of $\epsilon$ obtained with LOPTICS=.True., i.e., $\lim\_{\omega\to0}\epsilon(\omega)$.

#### LCALCEPS: finite differences approach

:   With LCALCEPS=.True., the dielectric tensor is computed from the derivative of the polarization, using

    :   $$\epsilon^\infty\_{ij}=\delta\_{ij}+
        \frac{4\pi}{\epsilon\_0}\frac{\partial P\_i}{\partial \mathcal{E}\_j}
        \qquad
        {i,j=x,y,z}.$$
:   However, here the derivative is evaluated explicitly by employing finite differences. The direction and intensity of the perturbing electric field have to be specified in the INCAR file using the EFIELD\_PEAD tag. As with DFPT, at the end of the calculation, VASP will write the dielectric tensor in the OUTCAR file. Control over the inclusion of local-field effects is done with the variable LRPA.

### Dynamical response: Green-Kubo and many-body perturbation theory

#### LOPTICS: Green-Kubo formula

:   LOPTICS allows for the evaluation of the frequency-dependent dielectric function once the ground state is computed. It uses the explicit expression to evaluate the imaginary part of $\epsilon$:

    :   $$\epsilon^{(2)}\_{\alpha \beta}\left(\omega\right) = \frac{4\pi^2 e^2}{\Omega}
        \mathrm{lim}\_{q \rightarrow 0} \frac{1}{q^2} \sum\_{c,v,\mathbf{k}} 2 w\_\mathbf{k} \delta( \epsilon\_{c\mathbf{k}} - \epsilon\_{v\mathbf{k}} - \omega)
        \times \langle u\_{c\mathbf{k}+\mathbf{e}\_\alpha q} | u\_{v\mathbf{k}} \rangle
        \langle u\_{v\mathbf{k}} | u\_{c\mathbf{k}+\mathbf{e}\_\beta q} \rangle,$$
:   while the real part is evaluated using the Kramers-Kroing relation. At this level, there are no effects coming from local fields.

:   This method requires two steps: First, obtain the electronic ground state. Secondly, increase the value of NBANDS in the INCAR file to include unoccupied states. Always check for convergence w.r.t. the number of unoccupied states.

:   Furthermore, the INCAR should also include values for CSHIFT (the broadening applied to the Lorentzian function which replaces the $\delta$-function), and NEDOS (the frequency grid for $\omega$).

#### ALGO = TDHF: Casida equation

:   This option performs a time-dependent Hartree-Fock or time-dependent density-functional-theory (TDDFT) calculation. It follows the Casida equation and uses a Fourier transform of the time-evolving dipoles to compute $\epsilon$.

:   The number of NBANDS controls how many bands are present in the time evolution. This can be fewer empty states compared to LOPTICS.

:   The choice of time-dependent kernel is controlled by AEXX, HFSCREEN, and LFXC tags. For calculations using hybrid functionals, AEXX controls the fraction of exact exchange used in the exchange-correlation potential, while HFSCREEN specifies the range-separation parameter. For a pure TDDFT calculation, LFXC uses the local exchange-correlation kernel in the time-evolution equations.

#### ALGO = TIMEEV: delta-pulse electric field

:   Uses a delta-pulse electric field to probe all transitions and calculate the dielectric function by following the evolution in time of the dipole momenta. This algorithm is able to fully reproduce the absorption spectra from standard Bethe-Salpeter calculations by setting the correct time-dependent kernel with LHARTREE=.True. and LFXC=.True.

:   The time step is controlled automatically by the CSHIFT and PREC. This means that the smaller the value of CSHIFT and the more accurate the level of precision chosen by the user, the higher the number of time steps that VASP will perform, and the higher the cost of the calculation.

:   The number of valence and conduction bands involved in the time propagation is set by the NBANDSO and NBANDSV tags, respectively. Choose a small number of bands near the band gap to reproduce optical measurements.

:   Finally, the maximum energy used in both the Fourier transform and in calculating the frequency-dependent dielectric function is set by OMEGAMAX, and the sampling of the frequency grid is controlled by NEDOS.

#### ALGO = CHI: polarizability within RPA approximation

:   Here, the frequency dielectric function is computed within the Random-Phase approximation. VASP will compute the polarizability $\chi$ by setting ALGO=Chi in the INCAR file and then use

:   :   $$\epsilon^{-1}\_{\mathbf G\mathbf G'}(\mathbf q,\omega) = \delta\_{\mathbf G\mathbf G'} + v(\mathbf q+\mathbf G)\chi\_{\mathbf G\mathbf G'}(\mathbf q,\omega)$$

:   to compute the dielectric function. Here, $v$ is the bare Coulomb potential describing electron-electron interaction. This requires increasing NBANDS to include unoccupied states as generally the case for GW calculations.

:   Two methods for computing the polarizability are available: For LSPECTRAL=.True., VASP will avoid direct computation of $\chi$ and use a fast matrix-vector product. However, this can introduce spurious peaks at low frequencies for some values of CSHIFT and NOMEGA. The second method computes $\chi$ directly and is activated by setting LSPECTRAL=.False.. However, it is much slower than the former method.

#### ALGO = BSE: macroscopic dielectric function including excitons

:   Setting ALGO=BSE computes the macroscopic dielectric function $\epsilon\_M$ by solving the Bethe-Salpeter equations. The electron-hole pairs are treated as a new quasi-particle called exciton, and the dielectric function is built using the eigenvectors ($X\_{\lambda}^{cv\mathbf k}$) and eigenvalues ($\omega\_\lambda$):

:   :   $$\epsilon\_M(\mathbf{q},\omega)=
        1+v(\mathbf q)\sum\_{\lambda\lambda'}
        \sum\_{c,v,\mathbf k}\sum\_{c',v',\mathbf k'}\langle c\mathbf{k}|e^{i\mathbf{qr}}|v\mathbf{k}\rangle X\_\lambda^{cv\mathbf{k}}
        \langle c'\mathbf{k'}|e^{-i\mathbf{qr}}|v'\mathbf{k'}\rangle X\_{\lambda'}^{c'v'\mathbf{k}',\*}\times S^{-1}\_{\lambda,\lambda'}
        \left(\frac{1}{\omega\_\lambda - \omega - i\delta} + \frac{1}{\omega\_\lambda+\omega + i\delta}\right)~.$$

:   Here, $S\_{\lambda\lambda'}$ is the overlap between exciton states of indices $\lambda$ and $\lambda'$ (in general, the BSE Hamiltonian is not hermitian, so eigenstates associated to different eigenvalues are not necessarily orthogonal).

:   The number of occupied and unoccupied states that are included in the BSE Hamiltonian is controlled by the NBANDSO and NBANDSV, respectively. Normally only a few bands above and below the band gap are required to converge the optical spectrum, and the memory requirements increase quickly with the number of bands. Thus, be careful in setting up these two tags.

:   Regarding the comparison with optical experiments, (e.g., absorption, MOKE, reflectance), $q$ is the photon momentum. Often, the $\mathbf q \to 0$ limit is considered. Furthermore, the coupling between the resonant and anti-resonant terms can be switched off, in what is called the Tamm-Dancoff approximation. This approximation can be activated with the variable ANTIRES set to 0. Setting this variable to 1 or 2 will include the coupling, but increase the computational cost.

## Level of approximation

### Microscopic and macroscopic quantities

It is important to distinguish between macroscopic quantities, measured over several repetitions of the unit cell, and microscopic quantities, which include fields that change rapidly in all regions of the unit cell.

When measuring a property experimentally, it is the macroscopic version that will be represented in the experimental data. On the other hand, computationally, the microscopic quantities are more accessible. In other words, in order to compare experimental and computational results, the microscopic quantities, e.g., the dielectric function, must be averaged over several repetitions of the unit cell. It is possible to show that the macroscopic dielectric function, $\epsilon\_M(\mathbf q,\omega)$ is related to the microscopic one via

:   :   $$\epsilon\_M(\mathbf q,\omega) = \frac{1}{\epsilon\_{\mathbf G = 0, \mathbf G'=0}^{-1}(\mathbf q,\omega)}$$

where $\epsilon\_{\mathbf G = 0, \mathbf G'=0}^{-1}(\mathbf q,\omega)$ is the inverse dielectric function at $\mathbf G = \mathbf G'=0$.

Note that this does not mean that $\epsilon\_M(\mathbf q,\omega) = \epsilon\_{\mathbf G = 0, \mathbf G'=0}(\mathbf q,\omega)$! The full matrix $\epsilon\_{\mathbf G, \mathbf G'}(\mathbf q,\omega)$ has to be inverted and it is the component at $\mathbf G = \mathbf G'=0$ that is used to calculate $\epsilon\_M(\mathbf q,\omega)$.

### Finite momentum dielectric function

In the optical limit, the momentum of the incoming photon, $\mathbf q$, is almost zero, since the wavelength of the electric field is several times larger than the dimensions of the unit cell. Since the Coulomb potential diverges at very small momenta, the optical limit of the dielectric function must be obtained by taking with the limit of $\mathbf q\to 0$ instead of setting $\mathbf q\to 0$.
For instance, in the case of the independent particle approximation of full BSE, one yields

:   :   $$\lim\_{\mathbf q\to0}\frac{\langle c\mathbf k + \mathbf q|e^{\mathrm i\mathbf q\cdot\mathbf r}|v\mathbf k\rangle}{q} \approx \lim\_{\mathbf q\to0}\frac{\langle c\mathbf k+\mathbf q|1 + \mathrm i\mathbf q\cdot\mathbf r|v\mathbf k\rangle}{q} = \hat{\mathbf{q}}\cdot \langle c\mathbf k+\mathbf q|\mathbf r|v\mathbf k\rangle.$$

VASP can also analyze the effects of finite momentum excitons. This is important, e.g., in the case of the optical absorption of bulk hexagonal BN. To calculate the absorption spectrum at finite momentum, set KPOINT\_BSE to the index of the desired **q** point.

### Local fields in the Hamiltonian

Local fields, i.e., terms with finite $\mathbf G$, can be turned on or off in the Coulomb potential when evaluating the polarizability. VASP will distinguish the results in the OUTCAR file with:

```
MACROSCOPIC STATIC DIELECTRIC TENSOR (including local field effects)
```

```
BORN EFFECTIVE CHARGES (including local field effects)
```

```
PIEZOELECTRIC TENSOR (including local field effects)
```

and

```
MACROSCOPIC STATIC DIELECTRIC TENSOR (excluding local field effects)
```

```
BORN EFFECTIVE CHARGES (excluding local field effects)
```

```
PIEZOELECTRIC TENSOR (excluding local field effects)
```

for both cases.

Another approximation can also be taken, where the contributions from the exchange-correlation kernel are neglected when evaluating the polarizability. This is equivalent to the so-called random-phase approximation (RPA) and can be activated by setting LRPA=.True. in the INCAR.

### Ion-clamped vs relaxed-ion/dressed dielectric function

The dielectric function computed either in the static or dynamical response regimes does not consider the effects coming from changes of the ionic positions due to the incoming electric field. This can be corrected by computing the relaxed-ion (or dressed) dielectric function $\bar\epsilon$

:   :   $$\bar\epsilon\_{\alpha\beta} = \epsilon\_{\alpha\beta} + \Omega\_0^{-1}Z\_{m\alpha}(\Phi^{-1})\_{mn}Z\_{n\beta},$$

where $\Omega\_0$ is the volume of the unit cell, $Z\_{n\alpha}$ is the Born effective charge, and $\Phi\_{mn}$ is the force constants matrix.

### Density-density versus current-current response functions

The inclusion of an electromagnetic field in the Hamiltonian is subject to a gauge choice. For instance, a classical electric field can be described by either a scalar potential $\phi$ or a longitudinal vector potential $\mathbf A$ in the incomplete Weyl gauge ($\phi$ = 0). The former means that the perturbing potential couples to the electronic density, while the second, implies a vector potential couples to a current. The fundamental consequence is that one can define two different response functions: a density-density response function for the first, $\chi\_{\rho\rho}$; and a current-current response function, $\chi\_{jj}$. This circumstance is a common source of error when comparing experimental and computational optical properties of periodic systems, as discussed by Sangalli et al..

Infact, perturbations associated with longitudinal fields will be described by the density-density polarisability function $\chi\_{\rho\rho}$, (e.g., laser fields taken in the classical limit), while transverse fields will be described by the current-current polarizability $\chi\_{jj}$, which is in fact a 3x3 tensor, (e.g., required to obtain the MOKE). Fundamentally, the time-dependent density is associated only with the longitudinal part of the current via the continuity equation. This also links both response functions via

:   :   $$q^2 \chi\_{jj}(\mathbf q,\omega) = \omega^2\chi\_{\rho\rho}(\mathbf q, \omega).$$

It guarantees that the dielectric functions obtained from either approach match at finite momentum and frequency: $\epsilon[\chi\_{\rho\rho}]= \epsilon[\chi\_{jj}]$.

The current-current dielectric function is exact at both $\mathbf q \to 0$ and at $\mathbf q = 0$. Especially for metals, it will reproduce the proper behavior of the Drude tail at $\omega=0$. However, $\chi\_{jj}$ is more prone to numerical instabilities.

## Other dielectric properties

### Electron energy loss spectroscopy (EELS)

In EELS experiments a narrow beam of electrons with a well defined energy is shot at the sample. These electrons then lose energy to the sample by exciting plasmons, electron-hole pairs, or other higher-order quasiparticles. The loss function can then be expressed as

:   :   $$\mathrm{EELS} = -\mathrm{Im}\left[\epsilon^{-1}(\omega)\right].$$

### Optical conductivity

From Maxwell's equations and the microscopic form of Ohm's law it is possible to arrive at the following relation between the tensorial dielectric function and the optical conductivity $\sigma(\omega)$

:   :   $$\sigma\_{\alpha\beta}(\omega) = \mathrm i\frac{\omega}{4\pi}\left[\delta\_{\alpha\beta} - \epsilon\_{\alpha\beta}(\omega)\right].$$

### Optical absorption

For an electromagnetic wave traveling through a medium, one can express the electric field as $\mathbf E(\mathbf r, t) = \mathbf E\_0e^{-\mathrm i(\omega t - \mathbf q \cdot \mathbf r)}$, and the effects of the medium in the wave propagation are contained inside the dispersion relation $\omega = \omega(\mathbf q)$. Using Maxwell's equations, one can arrive at

:   :   $$q^2 = \frac{\omega^2}{c^2}\epsilon(\omega).$$

If the magnetic permeability of the material is assumed to be equal to that of vacuum, the equation above implies that the refractive index can be written as $n = \sqrt{\epsilon(\omega)} = \tilde{n} + \mathrm i k$. Since $n$ is complex, the exponential factor in $\mathbf E(\mathbf r, t)$ will have a dampening factor, $e^{-\frac{\omega}{c}k\hat q\cdot \mathbf r}$, which accounts for the absorption of electromagnetic energy by the medium. With this relation one can define the absorption coefficient, $\alpha(\omega)$ as

:   :   $$\alpha(\omega) = \frac{2\omega}{c}k(\omega).$$

### X-ray absorption

Core-state excitations can be modeled using two main approaches:

* the supercell core-hole method
* the Bethe–Salpeter equation.

In both cases, the interaction between the excited electron and the core hole can be included. In the supercell core-hole approach, the core-hole is introduced explicitly by removing an electron and then relaxing the charge density in the presence of the core hole. The dielectric function is then found within the independent-particle approximation via

:   :   $$\varepsilon\_{\alpha \alpha}^{(2)}(\omega)= \frac{4 \pi^2 e^2 \hbar^2}{\Omega \omega^2 m\_e^2} \sum\_{\text{core}, c, \mathbf{k}} 2 w\_{\mathbf{k}} |\left\langle\psi\_{c \mathbf{k}}\right| i \nabla\_\alpha-\mathbf{k}\_\alpha\left|\psi\_{\text{core}}\right\rangle|^2\delta\left(\varepsilon\_{c \mathbf{k}}-\varepsilon\_{\text{core}}-\omega\right).$$

In the BSE approach, core-state excitations are included explicitly in the response-function calculation.
As a result, the electron-core-hole interaction enters the dielectric function through the eigenvectors of the two-particle Hamiltonian $A^\lambda$:

:   :   $$\varepsilon\_{\alpha \alpha}^{(2)}(\omega)= \frac{4 \pi^2 e^2 \hbar^2}{\Omega \omega^2 m\_e^2} \sum\_\lambda\left|\sum\_{\text{core},c, \mathbf{k}} 2A\_{\text{core}, c \mathbf{k}}^\lambda \left\langle\psi\_{c \mathbf{k}}\right| i \nabla\_\alpha-\mathbf{k}\_\alpha\left|\psi\_{\text{core}}\right\rangle \right|^2 \delta\left(\varepsilon^\lambda-\omega\right).$$

### Reflectance

From the previous subsection, one can also define the reflectivity coefficient at normal incidence as

:   :   $$R = \frac{(1-\tilde n)^2 + k^2}{(1+\tilde n)^2 + k^2}.$$

This equation can be generalized for any angle of incidence $\theta$, resulting in the general form of Fresnel equations.

### Magneto-optical Kerr effect (MOKE)

The incoming electromagnetic wave interacts with the finite magnetic moment of the material. Usually, the interaction is with the magnetization of the medium, but there are also antiferromagnetic systems that can observe a finite MOKE.
Generally, the reflected wave will gain an extra complex phase with respect to the incident $\mathbf E$-field. For a surface or two-dimensional material, (e.g., hexagonal BN, MoS$\_2$), this phase can be computed using the off-diagonal components of the current-current dielectric tensor:

:   :   $$\theta\_\mathrm K(\omega) = -\mathrm{Re}\left[\frac{\epsilon\_{xy}(\omega)}{(\epsilon\_{xx}(\omega)-1)\sqrt{\epsilon\_{xx}(\omega)}}\right].$$

## Electric response combined with perturbations of the ionic degrees of freedom

### Low-frequency corrections from atomic displacements

The corrections from ionic motion to the low frequency regime can be added to $\epsilon\_{\alpha\beta}^\infty$ following

:   :   $$\epsilon\_{\alpha\beta}(\omega) = \epsilon\_{\alpha\beta}^\infty + \frac{4\pi e^2}{\Omega\_0}\sum\_\nu\frac{S\_{\alpha\beta,\nu}}{\omega\_\nu^2 - (\omega+\mathrm i\eta)^2},$$

where $\omega\_\nu$ is the phonon frequency of mode $\nu$, and $S\_{\alpha\beta,\nu}$ is the mode-oscillator strength, defined by

:   :   $$S\_{\alpha\beta,\nu} = \left(\sum\_{I,\delta}Z^\*\_{I\alpha\delta}\varepsilon^\*\_{I\delta,\nu}(\mathbf{q = 0})\right)\left(\sum\_{J,\delta'}Z^\*\_{J\beta\delta'}\varepsilon\_{J\delta',\nu}(\mathbf{q = 0})\right).$$

Here $Z^\*\_{J\beta\delta'}$ are the Born effective charges and $\varepsilon\_{J\delta',\nu}(\mathbf{q = 0})$ are the eigendisplacements associated with the vibration mode $\nu$ for atom $J$ along direction $\delta'$. More information on the theory and methods behind the computation of phonon frequencies and eigendisplacements can be found in the phonons dedicated page.

Inclusion of the low-frequency corrections can be activated in the INCAR file with either IBRION = 5,6 (DFPT) or 7,8 (finite differences), and by setting to .True. the variables LEPSILON or LCALCEPS.

#### Polar materials

For polar materials it is important to recall that there is a discontinuity near $\Gamma$, i.e. $\omega^2\_\nu(\mathbf{q\to 0}) \neq \omega^2\_\nu(\mathbf{q= 0})$, and in fact, for a given unitary directional vector $\mathbf q$, it can be shown that the Lyddane-Sachs-Teller relationship holds

:   :   $$\prod\_\nu\frac{\omega^2\_\nu(\mathbf{q \to 0})-\omega^2}{\omega^2\_\nu(\mathbf{q= 0}) - \omega^2} = \frac{\sum\_{\alpha\beta}q\_\alpha\epsilon\_{\alpha\beta}(\omega)q\_\beta}{\sum\_{\alpha\beta}q\_\alpha\epsilon\_{\alpha\beta}^\infty q\_\beta},$$

meaning that the splitting in frequencies between the LO and TO modes at zero momentum carries over the evaluation of the dielectric function.

In order to obtain smooth phonon dispersions and to properly account for the LO-TO splitting in the evaluation of the optical limit of the dielectric function, users should read the dedicated page on LO-TO splitting, where it is explained how to set the variables LPHON\_POLAR, PHON\_DIELECTRIC, and PHON\_BORN\_CHARGES in the INCAR file.

### Corrections from strain

The dielectric tensor can also be included in the evaluation of the elastic tensor, $C\_{jk}$, (see theory of static linear response for more information on derived quantities from the static linear response). While this quantity is normally evaluated at fixed $\mathbf E$-field, in cases where a thin film is placed between layers of insulating materials, it is more convenient to evaluate the elastic tensor for fixed displacement field $\mathbf D$, since the boundary conditions fix the components of this vector in the direction normal to the surface.

If $C^E\_{jk}$ is the elastic tensor defined at fixed $\mathbf E$-field and $C^D\_{jk}$ the elastic tensor defined at fixed $\mathbf D$-field, then they are related by

:   :   $$C^D\_{jk} = C^E\_{jk} + e\_{\alpha j}(\epsilon)^{-1}\_{\alpha\beta}e\_{\beta k},$$

where $e\_{\alpha j}$ is the ion-relaxed piezoelectric tensor.

## Tutorials

* Tutorials for linear response.
* Tutorials for GW.
* Tutorials for BSE.
* Lecture on dielectric properties from first principles.
* Lecture on the optical bandgap.

## References
