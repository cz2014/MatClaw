# Category:Ensembles

Categories: Molecular dynamics

### Introduction

A central concept of statistical mechanics is the ensemble. An ensemble consists
of a large number of virtual copies of the system of interest. An ensemble will always depend on three thermodynamic state variables, as for example particle number N, temperature T and pressure p.
These three variables determine the type of ensemble that is studied. Depending on
these three variables there is a thermodynamic potential associated with the
ensemble, which would be the Gibbs free energy in the case of N,T and p.
Therefore, the concept of the ensemble gives access to any thermodynamic quantity.
The configurations of your system building up the ensemble can be obtained from
molecular dynamics simulations. The molecular-dynamics approach generates the configurations for
the ensemble by integrating Newton's equations of motion.

### Theory

In this section various ensembles will be introduced. To describe an ensemble mathematically
the partition function will be used. The partition function is the central mathematical
entity in statistical mechanics. As the wave function in quantum mechanics it contains
all the information about a statistical system. The partition function depends on three
thermodynamic state variables such as N,T and volume V.

**Microcanonical ensemble (N,V,E)**

To start, the three controlled external parameters have to be defined. In the case of the
microcanonical ensemble these are the particle number, the volume and the total energy E of the system.
The total energy is the sum of the kinetic energy and potential energy of the particle
system. Therefore the total energy depends on the momenta and the positions of the system.
Furthermore, the energy is an extensive variable depending on the particle number and the volume of the system.
The partition function is written as a sum over all microstates in agreement with the NVE constraints

$\Omega(N,V,E) = \sum\_{E-\delta E \lt E(N,V,\{\mathbf{r}\_{i}\},\{\mathbf{p}\_{i}\}) \lt E + \delta E } 1.$

In this equation $\delta E$ denotes a infinitesimal energy. $\{\mathbf{r}\_{i}\}$
denotes the set of particle positions and $\{\mathbf{p}\_{i}\}$ are the conjugate momenta.
The sum is over all particle positions and momenta giving an energy in agreement with the energy constraint.
Therefore, $\Omega(N,V,E)$ is the number of microstates under the given conditions.
From the microcanonical partition function it is possible to obtain the entropy by

$S(N,V,E) = k\_{B}log\Omega(N,V,E),$

where $k\_{B}$ is the Boltzmann constant. The probabilities for the different micro states (r) are given by

$P\_{r}(N,V,E) =
\begin{cases} \frac{1}{\Omega(N,V,E)}\ for\ E-\delta E \lt E \lt E + \delta E \\
0\ else
\end{cases}$.

The microcanonical ensemble is a theoretical realization of a N particle system which is placed in a box
with fixed volume and fully isolated from its surroundings. Therefore, no energy exchange with the rest of the universe is possible. In VASP this ensemble can be approximated by sampling the configurations in a molecular-dynamics run.

**Canonical ensemble ensemble (N,V,T)**

In the canonical ensemble the controlled thermodynamic state variables are the particle number, the volume and the temperature. The ensemble consists of all configurations accessible to the system at the given (N,V,T) conditions. The canonical partition function can be derived to be

$Z(N,V,T) = \sum\_{r}e^{-\beta E(N,V,\{\mathbf{r}\_{r}\},\{\mathbf{p}\_{r}\})} 1$,

where $\beta$ is the inverse temperature $\frac{1}{k\_{B}T}$.
The probability for a single microstate r is

$P\_{r}(N,V,T) = \frac{1}{Z(N,V,T)}e^{-\beta E(N,V,\{\mathbf{r}\_{i}\},\{\mathbf{p}\_{i}\})}$.

The canonical partition function is related to the Helmholtz free energy by

$F(N,V,T) = -k\_{B}logZ(N,V,T)$

and the average energy of the system under canonical conditions can be computed as

$\langle E \rangle = -k\_{B}T\frac{\partial F(N,V,T)}{\partial \beta}=
\sum\_{r}
\frac{e^{-\beta E(N,V,\{\mathbf{r}\_{r}\},\{\mathbf{p}\_{r}\})}E(N,V,\{\mathbf{r}\_{r}\},\{\mathbf{p}\_{r}\})}{Z}$.

The canonical ensemble can be visualized as N particle system in a fixed volume box which is allowed to exchange thermal energy with a huge heat bath surrounding it. Therefore, in equilibrium the instantaneous temperature (temperature derived from kinetic energy) is fluctuating around the heat bath temperature. Temperature fluctuations are proportional to $N^{-1/2}$. Hence, in the thermodynamic limit ($N \rightarrow \infty$) temperature fluctuations vanish. There are several techniques to realize the canonical ensemble in a computer simulation. The configurations in a NVT ensemble can be sampled from a molecular-dynamics run.

**Isothermal–isobaric ensemble (NpT)**

In the isothermal–isobaric ensemble the controlled thermodynamic state variables are the particle number, the pressure p and the temperature. The ensemble consists of all configurations accessible to the system at the given (N,p,T) conditions. The isothermal–isobaric partition function can be derived to be

$Y(N,p,T) = \sum\_{r}e^{-\beta\left( E(N,V,\{\mathbf{r}\_{r}\},\{\mathbf{p}\_{r}\})+pV\_{r}\right)}$,

where $\beta$ is the inverse temperature $\frac{1}{k\_{B}T}$ and pV
is the contribution to the energy due to volume work.
The probability for a single microstate r is

$P\_{r}(N,p,T) = \frac{1}{Y(Np,T)}e^{-\beta \left(E(N,p,\{\mathbf{r}\_{i}\},\{\mathbf{p}\_{i}\})+pV\_{r}\right)}$.

The isothermal–isobaric partition function is related to the Gibbs free energy by

$G(N,p,T) = -k\_{B}logY(Np,T)$

and the average internal energy of the system under isothermal–isobaric conditions can be computed as

$\langle E \rangle = -k\_{B}T\frac{\partial G(N,p,T)}{\partial \beta}=
\sum\_{r}
\frac{e^{-\beta \left(E(N,p,\{\mathbf{r}\_{r}\},\{\mathbf{p}\_{r}\})+pV\_{r}\right)}E(N,p,\{\mathbf{r}\_{r}\},\{\mathbf{p}\_{r}\})}{Y}$.

The isothermal–isobaric ensemble can be visualized as N particle system in a box without rigid boundaries which is allowed to exchange thermal energy with a huge heat bath surrounding it. Because the box has no rigid sides the volume and shape will change according to the pressure difference within and outside the box. In the isothermal–isobaric ensemble both the instantaneous temperature and pressure will fluctuate around the desired temperature (heat bath) and pressure (volume reservoir), respectively. As in the canonical ensemble these fluctuations vanish in the thermodynamic limit. There are several techniques to realize the isothermal–isobaric ensemble in a computer simulation. The configurations in a NpT ensemble can be sampled from a molecular-dynamics run.

**Isoenthalpic–isobaric ensemble (NpH)**

In the isoenthalpic–isobaric ensemble the controlled thermodynamic state variables are the particle number, the pressure and the enthalpy H. The ensemble consists of all configurations accessible to the system at the given (N,p,H) conditions. The isoenthalpic–isobaric partition function can be derived to be

$X(N,p,H) = \sum\_{H-\delta H\lt H(N,p,\{\mathbf{r}\_{i}\},\{\mathbf{p}\_{i}\})\lt H+\delta H} 1$.

The probability for a single microstate r is

$P\_{r}(N,p,H) =
\begin{cases} \frac{1}{X(N,p,H)}\ for\ H-\delta H \lt H \lt E + \delta H \\
0\ else
\end{cases}$.

The isoenthalpic–isobaric ensemble can be visualized as N particle system in a box without rigid boundaries which is thermally isolated from its surroundings. Because the box has no rigid sides the volume and shape will change according to the pressure difference within and outside the box. In the isoenthalpic–isobaric ensemble the instantaneous pressure will fluctuate around the desired pressure value. The configurations in a NpH ensemble can be sampled from a molecular-dynamics run.

### How To

The following table gives an overview of the possible combinations of ensembles and thermostats in VASP:

:   |  |  |  |  |  |  |  |
    | --- | --- | --- | --- | --- | --- | --- |
    |  | Thermostat | | | | | |
    | Ensemble | Andersen | Nosé-Hoover | Langevin | Nosé-Hoover chain | CSVR | Multiple Andersen |
    | Microcanonical (NVE) | MDALGO=1, ANDERSEN\_PROB=0.0 | | | | | |
    | Canonical (NVT) | MDALGO=1 | MDALGO=2 | MDALGO=3 | MDALGO=4 | MDALGO=5 | MDALGO=13 |
    | ISIF=2 | ISIF=2 | ISIF=2 | ISIF=2 | ISIF=2 | ISIF=2 |
    | Isobaric-isothermal (NpT) | not available | not available | MDALGO=3 | not available | not available | not available |
    | ISIF=3 |
    | Isoenthalpic-isobaric (NpH) | MDALGO=3, ISIF=3, LANGEVIN\_GAMMA=LANGEVIN\_GAMMA\_L=0.0 | | | | | |
