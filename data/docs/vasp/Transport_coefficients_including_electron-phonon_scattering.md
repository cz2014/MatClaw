# Transport coefficients including electron-phonon scattering

Categories: Electron-phonon interactions, Howto

In the framework of the linearized Boltzmann equations, we can compute a few electronic transport observables.
The transport coefficients can be evaluated rather straightforwardly under the approximation of the constant relaxation time.
The most computationally demanding part of the calculation is the electronic linewidths due to the electron-phonon scattering.
As such, it is instructive to start by computing the transport coefficients in the constant-relaxation-time approximation (CRTA).
This gives us an idea of the **k**-point density required to obtain a precise value. See the  theory page for more details on transport coefficients.

> **Mind:** Available as of VASP 6.5.0

> **Important:** This feature requires  HDF5 support.

The most basic INCAR to compute the transport coefficients is

```
 PREC = Accurate
 EDIFF = 1e-8
 ISMEAR = -15; SIGMA = 0.01
 LREAL = .FALSE.
 LWAVE = .FALSE.
 LCHARG = .FALSE.
 
 #run electron-phonon calculation
 ELPH_MODE = TRANSPORT
 
 # for the determination of the chemical potential
 ELPH_ISMEAR = -15 # smearing method 
 
 # for the computation of transport coefficients
 TRANSPORT_NEDOS = 501
 ELPH_SELFEN_TEMPS = 0 100 200 300 400 500
```

The final output of the code is reported for each combination of computational parameters using the concept of  electron-phonon accumulators.

## Conductivity for metals

Conductivity $\sigma\_{\alpha\beta}$ relates the current to the applied electric field

:   :   $$J\_\alpha = \sigma\_{\alpha\beta} E\_\beta$$

### Constant relaxation-time approximation

The constant relaxation time is often a good approximation for metals because the density of states often changes little around the Fermi level.
What remains challenging is to determine a value for the constant relaxation time $\tau$. To avoid this, it is common to report the transport quantities in a different set of units, where $\tau=1$.
To perform a CRTA calculation, you need to add the following variables to the INCAR

```
 ELPH_SCATTERING_APPROX = CRTA
 TRANSPORT_RELAXATION_TIME = 1e-14
```

> **Mind:** This calculation can be done without the presence of the phelel\_params.hdf5 that contains the derivatives of the Kohn-Sham potential.

### Self-energy relaxation-time approximation

The **k**-mesh used in the previous calculation is a good starting point for a computation in the SERTA approximations (or MRTA) since the integral of the transport function is a requirement in both cases. This **k**-point mesh is, however, not a guarantee of a precise result: the calculation of the linewidth for each Kohn-Sham state requires an integration in a **q**-point mesh. Currently, it is not possible to choose the two separately, so we are left with the option to increase the sampling in KPOINTS\_ELPH until the transport quantities are converged.

There are a few factors determining the performance of these computations, in particular the value of TRANSPORT\_NEDOS.
This tag chooses the number of points to be used in a Gauss-Legendre integral used to integrate the spectral transport function and obtain the Onsager coefficients, which in turn are used to determine the final transport coefficients.
The number of points in turn determines an energy window for which the linewidths will contribute and need to be computed.
This selection of the states for which the linewidths are computed is crucial to attain a nearly linear scaling of the calculation with the number of k-points.
The size of the energy window also depends on the temperature: for larger temperatures, the required energy windows are larger, which means that VASP will compute the linewidths for more Kohn-Sham states. The states selected for computation are reported in the OUTCAR file

## Mobility for semiconductors

In semiconductors, it is more usual to compute the mobility instead of the conductivity.
This is because the conductivity is proportional to the number of free carriers, which means that by adding more free carriers, one obtains a larger conductivity.
By defining the mobility as the conductivity divided by the number of carriers, obtain a more intrinsic property of the material.

:   :   $$\sigma = n\_e \mu\_e + n\_h \mu\_h$$

with $n\_e$ being the density of electron carriers, $n\_h$ the density of hole carriers and $\mu\_e = \sigma\_e/n\_e$ and $\mu\_h = \sigma\_h/n\_h$ with $\sigma\_e$ being the contribution of the conduction bands to the electron conductivity and $\sigma\_h$ of the valence bands.

For the computation of a realistic mobility, it is usual to compute the conductivity for different doping levels and extrapolate to the limit of the lowest possible carrier concentration. The value of the mobility should be relatively constant in the limit of low carrier concentrations.
Additionally, one can specify electron or hole doping. A convenient setting is

```
 ELPH_SELFEN_CARRIER_DEN = -1e17 -1e16 -1e15 -1e14 1e14 1e15 1e16 1e17
```

with the negative values indicating hole doping and the positive values, electron doping.

The mobility is related to the conductivity $\sigma$, which can be defined using the transport distribution function.

:   $$\mathcal{T}(\varepsilon) = \frac{e^2}{N \Omega} \sum\_{n\mathbf{k}} \tau\_{n\mathbf{k}} \, \mathbf{v}\_{n\mathbf{k}} \otimes \mathbf{v}\_{n\mathbf{k}} \, \delta(\varepsilon\_{n\mathbf{k}} - \varepsilon),$$

and the Onsager coefficients are:

:   $$L\_{ij} = \int d\varepsilon \, \mathcal{T}(\varepsilon) \, (\varepsilon - \eta)^{i+j-2}
    \left(-\frac{\partial f^0}{\partial \varepsilon}\right).$$

where $\Omega$ is the volume of the unit cell, $\tau$ is the scattering lifetime, $v$ is the drift velocity, $f\_{n\mathbf{k}}$ is the occupation number, and $\varepsilon\_{n\mathbf{k}}$ is the band energy.

By restricting the band sums to conduction or valence bands, the conductivity can be separated into electron and hole contributions, $\sigma\_e$ and $\sigma\_h$, and the electron and hole mobilities defined:

| Quantity | Definition | Carrier density |
| --- | --- | --- |
| Electron mobility $\mu\_e$ | $\mu\_e = \tfrac{\sigma\_{n \in \text{CB}}}{n\_e}$ | $n\_e = \frac{1}{\Omega N\_\mathbf{k}}\sum\_{\mathbf{k}n \in \text{CB}} f(\varepsilon\_{\mathbf{k}n}, T, \eta)$ |
| Hole mobility $\mu\_h$ | $\mu\_h = \tfrac{\sigma\_{n \in \text{VB}}}{n\_h}$ | $n\_h = \frac{1}{\Omega N\_\mathbf{k}}\sum\_{\mathbf{k}n \in \text{VB}} \big[1 - f(\varepsilon\_{\mathbf{k}n}, T, \eta)\big]$ |

where $\sigma\_{n \in \text{CB}}$ and $\sigma\_{n \in \text{VB}}$ denote the conductivity restricted to states in the conduction and valence bands, respectively, $f\_{n\mathbf{k}}$ is the  Fermi–Dirac distribution, and $\eta$ is the  chemical potential at the given temperature.

> **Mind:** To avoid confusion with the mobility, we use the notation $\eta$. Usually, the  chemical potential is written as $\mu$ or $\varepsilon\_F$.

### Constant relaxation-time approximation

The constant relaxation time is a very crude approximation in the case of semiconductors because it is proportional to the electronic density of states which have a $\propto \sqrt{e}$ behavior around the valence band maximum or conduction band minimum.
It is however still instructive to perform these calculations, such as to get an idea of the **k**-sampling required to converge the mobility.

Because of the sharp jump in the density of states in the regions of interest for the transport computation, it is crucial to ensure that the integration mesh TRANSPORT\_NEDOS has enough points. More points are often required for semiconductors than for metals.

### Self-energy relaxation-time approximation

The same observations apply here than in the case of metals, with the particularity that it is more difficult to converge the linewidths for semiconductors. This is specially true in the case of polar materials, where the electron-phonon matrix elements have an integrable divergence when $q\rightarrow0$.

## Thermoelectric coefficients and the ZT figure of merit

The ZT figure of merit is given as a function of the transport coefficients and the absolute temperature, $T$:

:   :   $$ZT=\frac{\sigma S^2 T}{\kappa\_e+\kappa\_l}$$

The conductivity $\sigma$, Seebeck coefficient $S$ and the electronic contribution to the thermal conductivity $\kappa\_e$ are reported in the OUTCAR file.
Here is an example output where these values are reported for the different  temperatures  in a small table for each  accumulator:

```
Transport for self-energy accumulator N=     1
                 T K               mu eV           sigma S/m      mob cm^2/(V.s)       seebeck μV/K         peltier μV     kappa_e W/(m.K)
          0.00000000          9.79452083        153.09934046         95.55902268          0.00000000          0.00000000          0.00000000 Gauss-Legendre grids
        100.00000000          9.80301003        149.76360902         93.48293224        228.06843439      22806.84343939          0.00040952 Gauss-Legendre grids
        200.00000000          9.82655169        134.56767701         83.98822174        377.34590243      75469.18048584          0.00077142 Gauss-Legendre grids
        300.00000000          9.86137412        125.22459498         78.15905958        476.66107679     142998.32303627          0.00106949 Gauss-Legendre grids
        400.00000000          9.90446361        117.64008575         73.42946205        548.72555653     219490.22261143          0.00131031 Gauss-Legendre grids
        500.00000000          9.95389195        108.91505893         67.98526987        604.60014228     302300.07113882          0.00147236 Gauss-Legendre grids
```

The lattice thermal conductivity $\kappa\_l$ can be computed using the Müller-Plathe method or with an external package such as phono3py.

Because the Seebeck coefficient $S$ and electronic contribution to the thermal conductivity $\kappa\_e$ depend on the first and second momentum of the transport function, a larger number of points (TRANSPORT\_NEDOS) is often required to obtain an accurate integration of these transport quantities than for the conductivity or mobility.

## Related tags and articles

* Band-structure renormalization
* Electronic transport coefficients
* Electron-phonon potential from supercells
* Chemical potential in electron-phonon interactions
* Electron-phonon accumulators
* phelel\_params.hdf5
* Electron-phonon interactions from Monte-Carlo sampling
