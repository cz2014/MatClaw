# Electronic transport coefficients

Categories: Electron-phonon interactions, Howto

The theoretical framework is based on the  linearized Boltzmann transport equation (BTE) within the relaxation time approximation (RTA).
We employ the frozen-band approximation, which assumes that the electronic potential and eigenvalues computed for the undoped system remain unchanged when electrons are added or removed.
The goal of this page is to explain how to compute the electronic lifetimes, scattering rates, and transport coefficients such as the electrical conductivity, Seebeck coefficient, and the electronic thermal conductivity.

## Electron–phonon coupling matrix elements

The starting point is the set of Kohn–Sham eigenstates obtained from density functional theory (DFT). For a given Bloch state,

:   $$H\_{\mathbf{k}} |\psi\_{n\mathbf{k}}\rangle = \epsilon\_{n\mathbf{k}} S\_{\mathbf{k}} |\psi\_{n\mathbf{k}}\rangle,$$

where $n$ is the band index, $\mathbf{k}$ is a crystal momentum, and $S\_{\mathbf{k}}$ is the overlap matrix.
The scattering with phonons is described by the electron–phonon coupling matrix elements

:   $$g\_{n\mathbf{k},n'\mathbf{k}'}^{\nu\mathbf{q}} = \langle \psi\_{n\mathbf{k}} | \partial\_{\nu\mathbf{q}} V | \psi\_{n'\mathbf{k}'} \rangle,$$

where $\partial\_{\nu\mathbf{q}} V$ is the perturbation of the crystal potential due to a phonon of branch index $\nu$ and wavevector $\mathbf{q}$. These matrix elements determine the scattering probability between states $(n,\mathbf{k})$ and $(n',\mathbf{k}')$.

## Scattering rates and lifetimes

Within Fermi’s golden rule, the inverse lifetime (scattering rate) of an electron in state $(n,\mathbf{k})$ is

:   $$\frac{1}{\tau\_{n\mathbf{k}}} = \frac{2\pi}{\hbar} \sum\_{n'\nu\mathbf{k}'} w\_{n\mathbf{k},n'\mathbf{k}'} \, |g^{\nu}\_{n\mathbf{k},n'\mathbf{k}'}|^2 \left[ (n\_{\nu\mathbf{q}} + 1 - f\_{n'\mathbf{k}'}) \, \delta(\varepsilon\_{n\mathbf{k}} - \varepsilon\_{n'\mathbf{k}'} - \hbar\omega\_{\nu\mathbf{q}}) + (n\_{\nu\mathbf{q}} + f\_{n'\mathbf{k}'}) \, \delta(\varepsilon\_{n\mathbf{k}} - \varepsilon\_{n'\mathbf{k}'} + \hbar\omega\_{\nu\mathbf{q}}) \right]$$

where:

* $f\_{n\mathbf{k}}$ is the Fermi–Dirac occupation,
* $n\_{\nu\mathbf{q}}$ is the Bose–Einstein phonon occupation,
* $\omega\_{\nu\mathbf{q}}$ is the phonon frequency.
* $w\_{n\mathbf{k},n'\mathbf{k}'}$ weight determined by the ELPH\_SCATTERING\_APPROX

The two terms correspond to phonon emission and absorption, respectively.

## Transport distribution function

The energy-resolved transport distribution function is

:   $$\mathcal{T}(\epsilon) = \frac{e^2}{N\_\mathbf{k}\Omega} \sum\_{n\mathbf{k}} \tau\_{n\mathbf{k}} \, \mathbf{v}\_{n\mathbf{k}} \otimes \mathbf{v}\_{n\mathbf{k}} \, \delta(\epsilon\_{n\mathbf{k}}-\epsilon),$$

where $\Omega$ is the unit-cell volume, $\mathbf{v}\_{n\mathbf{k}}$ are the carrier velocities, $\tau\_{n\mathbf{k}}$ are the lifetimes, and $N\_\mathbf{k}$ the number of $\mathbf{k}$-points.

## Onsager coefficients

The Onsager coefficients relate generalized forces (electric field and temperature gradient) to generalized fluxes (electronic and heat currents).
In compact matrix form:

:   $$\begin{pmatrix}
    \mathbf{J}\_e \\
    \mathbf{J}\_q
    \end{pmatrix}
    =
    \begin{pmatrix}
    L\_{11} & L\_{12} \\
    L\_{21} & L\_{22}
    \end{pmatrix}
    \begin{pmatrix}
    -\nabla \eta \\
    -\nabla T / T
    \end{pmatrix},$$

where

* $\mathbf{J}\_e$ = electrical current density,
* $\mathbf{J}\_q$ = heat current density carried by the electrons,
* $\eta$ = chemical potential (usually written as $\mu$ or $\epsilon\_F$)
* $T$ = temperature.

They are defined as

:   $$L\_{ij} = \int d\epsilon \, \mathcal{T}(\epsilon) \,
    (\epsilon-\eta)^{i+j-2}
    \left( -\frac{\partial f^0}{\partial \epsilon} \right),$$

where $\mathcal{T}(\epsilon)$ is the transport distribution function,
$\eta$ the  chemical potential, and $f^0$ the Fermi–Dirac distribution.

> **Important:** The  chemical potential is usually written as $\mu$ or $\varepsilon\_F$. To avoid confusion with the mobility, we use the notation $\eta$.

In practice, this integral can be evaluated in one of two ways determined by ELPH\_TRANSPORT\_DRIVER

Linear energy grids and Simpson rule

The integrand is computed on a linear energy grid, and the Simpson rule is used for integration. The discretized Onsager coefficient is evaluated as

:   $$L\_{ij} \;\approx\; \sum\_{k=1}^{N} w\_k \;
    \mathcal{T}(\epsilon\_k)\;
    (\epsilon\_k - \eta)^{\,i+j-2}\;
    \left( -\frac{\partial f^0}{\partial \epsilon} \right).$$

with $\epsilon\_k = \epsilon\_\text{min}+(k-1)\Delta \epsilon,\;\; k=1,\dots,N$ and
$\Delta \epsilon = \tfrac{\epsilon\_\text{max}-\epsilon\_\text{min}}{N-1}$
and $\epsilon\_\text{min}$=ELPH\_TRANSPORT\_EMIN and
$\epsilon\_\text{max}$=ELPH\_TRANSPORT\_EMAX or alternatively both $\epsilon\_\text{min}$ and $\epsilon\_\text{max}$ are set by ELPH\_TRANSPORT\_DFERMI\_TOL and $w\_k$ the weights due to the Simpson integration rule.

Gauss–Legendre quadrature

A change of variables is introduced to avoid explicitly sampling the sharp derivative of the Fermi–Dirac function.
Define

:   $$x = 1-2f(\epsilon-\eta,T)$$

so that $\epsilon = \eta + k\_B T \ln\frac{1+x}{1-x}$.
With this substitution, the derivative of the Fermi–Dirac distribution is absorbed into the Jacobian, and the Onsager coefficients take the form

:   $$L\_{ij} \;\approx\; \tfrac{1}{2} \sum\_{k=1}^N
    w\_k \,
    \left( \frac{k\_B T}{-e} \ln \frac{1+x\_k}{1-x\_k} \right)^{i+j-2}
    \mathcal{T}\!\left(\eta + k\_B T \ln\frac{1+x\_k}{1-x\_k}\right),$$

with $w\_k$ and $x\_k$ the weights and abscissae of the Gauss-Legendre quadrature rule.

The Gauss–Legendre approach has the advantage that the integration grid adapts naturally to the width of the Fermi window, making it numerically efficient without having define manually the energy window through ELPH\_TRANSPORT\_DFERMI\_TOL or ELPH\_TRANSPORT\_EMIN and ELPH\_TRANSPORT\_EMAX. Instead, only the number of points $N$ in the sum above needs to be defined through TRANSPORT\_NEDOS.

## Transport coefficients

| Quantity | Formula | Physical meaning |
| --- | --- | --- |
| Electrical conductivity $\sigma$ | $\sigma = L\_{11}$ | Charge current response to an electric field |
| Seebeck coefficient $S$ | $S = \tfrac{1}{T} L\_{11}^{-1} L\_{12}$ | Voltage generated per temperature gradient |
| Peltier coefficient $\Pi$ | $\Pi = T S = L\_{11}^{-1} L\_{12}$ | Heat carried per unit charge current |
| Electronic thermal conductivity $\kappa\_e$ | $\kappa\_e = \tfrac{1}{T} ( L\_{22} - L\_{21} L\_{11}^{-1} L\_{12} )$ | Heat current carried by electrons in response to a thermal gradient |

The lattice thermal conductivity $\kappa\_l$, i.e., the heat current carried by the lattice in response to a thermal gradient, can be computed using the Müller-Plathe method or with an external package such as phono3py.

## Electron and hole mobilities in semiconductors

In semiconductors, the electrical conductivity can be separated into contributions from conduction-band electrons and valence-band holes.
This is only meaningful in materials with a finite band gap, where carriers can be clearly identified as either electrons in the conduction band (CB) or holes in the valence band (VB).

| Quantity | Definition | Carrier density |
| --- | --- | --- |
| Electron mobility $\mu\_e$ | $\mu\_e = \tfrac{\sigma\_{n \in \text{CB}}}{n\_e}$ | $n\_e = \frac{1}{\Omega N\_\mathbf{k}}\sum\_{\mathbf{k}n \in \text{CB}} f(\varepsilon\_{\mathbf{k}n}, T, \eta)$ |
| Hole mobility $\mu\_h$ | $\mu\_h = \tfrac{\sigma\_{n \in \text{VB}}}{n\_h}$ | $n\_h = \frac{1}{\Omega N\_\mathbf{k}}\sum\_{\mathbf{k}n \in \text{VB}} \big[1 - f(\varepsilon\_{\mathbf{k}n}, T, \eta)\big]$ |

Here:

* $\sigma\_{n \in \text{CB}}$ and $\sigma\_{n \in \text{VB}}$ denote the conductivity restricted to states in the conduction and valence bands, respectively.
* $f\_{n\mathbf{k}}$ is the Fermi–Dirac distribution.
* $\Omega$ is the volume of the unit cell.
* $N\_\mathbf{k}$ is the total number of k-points.
* $\eta$ is the  chemical potential at the given temperature.

> **Important:** The  chemical potential is usually written as $\mu$ or $\varepsilon\_F$. To avoid confusion with the mobility, we use the notation $\eta$.

## Approximations and methods

* Tetrahedron method: used for Brillouin-zone integration, avoiding the need for ad-hoc smearing parameters.
* Plane-wave Bloch states: ensure systematic convergence and avoid interpolation errors.
* Selection algorithms: restrict scattering processes to those allowed by energy conservation (delta functions), minimizing the number of matrix elements to compute.

## Related tags and articles

* Band-structure renormalization
* Electron-phonon potential from supercells
* Transport coefficients including electron-phonon scattering
* Chemical potential in electron-phonon interactions
* Electron-phonon accumulators
* phelel\_params.hdf5
* Electron-phonon interactions from Monte-Carlo sampling
* ELPH\_SCATTERING\_APPROX
* ELPH\_TRANSPORT\_DRIVER
