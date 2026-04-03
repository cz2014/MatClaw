# GW approximation of Hedin's equations

Categories: Many-body perturbation theory, Theory, Low-scaling GW and RPA

## Green's functions

The GW method can be understood in terms of the following eigenvalue equation

$(T+V\_{ext}+V\_h)\phi\_{n{\bf k}}({\bf r})+\int d{\bf r}\Sigma({\bf r},{\bf r}',\omega=E\_{n{\bf k}})\phi\_{n{\bf k}}({\bf r}') = E\_{n{\bf k}}\phi\_{n{\bf k}}({\bf r})$

Here $T$ is the kinetic energy, $V\_{ext}$ the external potential of the nuclei, $V\_h$ the Hartree potential and $E\_{n{\bf k}}$ the quasiparticle energies with orbitals $\phi\_{n{\bf k}}$. In contrast to DFT, the exchange-correlation potential is replaced by the many-body self-energy $\Sigma$ and should be obtained together with the Green's function $G$, the irreducible polarizability $\chi$, the screened Coulomb interaction $W$ and the irreducible vertex function $\Gamma$ in a self-consistent procedure. For completeness, these equations are

$G(1,2)=G\_0(1,2)+\int d(3,4) G\_0(1,3)\Sigma(3,4)G(4,2)$

$\chi(1,2)=\int d(3,4) G(1,3)G(4,1)\Gamma(3,4;2)$

$W(1,2)=V(1,2)+\int d(3,4) V(1,3)\chi(3,4)W(4,2)$

$\Sigma(1,2)=\int d(3,4) G(1,3)\Gamma(3,2;4)W(4,1)$

$\Gamma(1,2;3)=\delta(1,2)\delta(1,3)+\int d(4,5,6,7)\frac{\delta\Sigma(1,2)}{\delta G(4,5)}G(4,6)G(7,5)\Gamma(6,7;3)$

Here the common notation $1=({\bf r}\_1,t\_1)$ was adopted and $V$ denotes the bare Coulomb interaction. Note, that these equations are exact and provide an alternative to the Schrödinger equation for the many-body problem. Nevertheless, approximations are necessary for realistic systems. The most popular one is the GW approximation and is obtained by neglecting the equation for the vertex function and using the bare vertex instead:

$\Gamma(1,2;3)=\delta(1,2)\delta(1,3)$

This means that the equations for the polarizability and self-energy reduce to

$\chi(1,2)=G(1,2)G(2,1)$

$\Sigma(1,2)=G(1,2)W(2,1)$

while the equations for the Green's function and the screened potential remain the same.

However, in practice, these equations are usually solved in reciprocal space in the frequency domain

$W\_{{\bf G}{\bf G}'}({\bf q},\omega)=\left[\delta\_{{\bf G}{\bf G}'}-\chi\_{{\bf G}{\bf G}'}({\bf q},\omega)V\_{{\bf G}{\bf G}'}({\bf q})\right]^{-1}V\_{{\bf G}{\bf G}'}({\bf q})$

$G\_{{\bf G}{\bf G}'}({\bf q},\omega)=\left[\delta\_{{\bf G}{\bf G}'}-\Sigma\_{{\bf G}{\bf G}'}({\bf q},\omega)G^{(0)}\_{{\bf G}{\bf G}'}({\bf q})\right]^{-1}G^{(0)}\_{{\bf G}{\bf G}'}({\bf q})$

In principle Hedin's equations have to be solved self-consistently, where in the first iteration $G^{(0)}$ is the non-interacting Green's function

$G^{(0)}({\bf r},{\bf r}',\omega)=\sum\_{n{\bf k}}\frac{\phi\_{n{\bf k}}^{\*(0)}
({\bf r})\phi^{(0)}\_{n{\bf k}}
({\bf r}')}{\omega-E^{(0)}\_{n{\bf k}}}$

with $\phi^{(0)}\_{n{\bf k}}$ being a set of one-electron orbitals and $E\_{n{\bf k}}^{(0)}$ the corresponding energies. Afterwards the polarizability $\chi^{(0)}$ is determined, followed by the screened potential $W^{(0)}$ and the self-energy $\Sigma^{(0)}$. This means that GW calculations require a first guess for the one-electron eigensystem, which is usually taken from a preceding DFT step.

In principle, one has to repeat all steps by the updating the Green's function with the Dyson equation given above in each iteration cycle until self-consistency is reached. In practice, this is hardly ever done due to computational complexity on the one hand (in fact fully self-consistent GW calculations are available as of VASP 6 only).

On the other hand, one observes that by keeping the screened potential $W$ in the first iteration to the DFT level one benefits from error cancelling, which is the reason why often the screening is kept on the DFT level and one aims at self-consistency in Green's function only.

Following possible approaches are applied in practice and selectable within VASP with the ALGO tag.

## Single Shot: G0W0

Performing only one GW iteration step is commonly referred to the G0W0 method. Here the self-energy $\Sigma^{(0)}$ is determined and the corresponding eigenvalue equation is solved. Formally, this is a five step precedure

* Determine the independent particle polarizability $\chi^{(0)}\_{\bf GG'}({\bf q},\omega)$
* Determine the screened Coulomb potential $W^{(0)}\_{\bf GG'}({\bf q},\omega)$
* Determine the self-energy $\Sigma^{(0)}({\bf r,r'},\omega)$
* Solve the eigenvalue equation $(T+V\_{ext}+V\_h)\phi\_{n{\bf k}}({\bf r})+\int d{\bf r}\Sigma^{(0)}\left({\bf r},{\bf r}',\omega=E^{(1)}\_{n{\bf k}}\right)\phi\_{n{\bf k}}({\bf r}') = E^{(1)}\_{n{\bf k}}\phi\_{n{\bf k}}({\bf r})$ for the quasi-particle energies $E\_{n\bf k}^{(1)}$.

To save further computation time, the self-energy is linearized with a series expansion around the Kohn-Sham eigenvalues $\epsilon\_{n\bf k}$

$\Sigma^{(0)}({\bf r,r'},\omega)\approx\Sigma^{(0)}({\bf r,r'},\epsilon\_{n{\bf k}})+ \left.\frac{\partial\Sigma^{(0)}}{\partial \omega}({\bf r,r'},\omega)\right|\_{\omega=\epsilon\_{n{\bf k}}}(\omega-\epsilon\_{n{\bf k}})$

and the renormalization factor $Z^{(0)}\_{n{\bf k}}=\left[ 1-{\rm Re}\left( \left.\frac{\partial\Sigma^{(0)}}{\partial \omega}({\bf r,r'},\omega)\right|\_{\omega=\epsilon\_{n{\bf k}}}\right)\right]^{-1}$ is introduced. This allows to obtain the G0W0 quasi-particle energies from following equation

$E^{(1)}\_{n\bf k}=\epsilon\_{n\bf k}+ Z\_{n\bf k}^{(0)} {\rm Re}\left[
\langle \phi\_{n\bf k}|
-\frac{\Delta}2+V\_{ext}+V\_h+\Sigma^{(0)}(\omega=\epsilon\_{n\bf k}) -\epsilon\_{n\bf k}
|\phi\_{n\bf k}\rangle
\right]$

The G0W0 method avoids the direct computation of the Green's function and neglects self-consistency in $G$ completely. In fact, only the Kohn-Sham energies are updated from $\epsilon\_{n\bf k}\to E^{(1)}\_{n\bf k}$, while the orbitals remain unchanged. This is the reason why the G0W0 method is internally selected as of VASP6 with ALGO =EVGW0 ("eigenvalue GW") in combination with NELM=1 to indicate one single iteration, even though the method is commonly known as the G0W0 approach. To keep backwards-compatibility, however, ALGO=G0W0 is still supported in VASP6.

Note that avoiding self-consistency might seem a drastic step at first sight. However, the G0W0 method often yields satisfactory results with band-gaps close to experimental measurements and is often employed for realistic band gap calculations.

## Partially self-consistent: GW0 or EVGW0

The G0W0 quasi-particle energies can be used to update the poles of the Green's function in the spectral representation
$G^{(i)}({\bf r},{\bf r}',\omega)=\sum\_{n{\bf k}}\frac{\phi\_{n{\bf k}}^{\*(0)}
({\bf r})\phi^{(0)}\_{n{\bf k}}
({\bf r}')}{\omega-E^{(i)}\_{n{\bf k}}}$
which in turn can be used to update the self-energy via $\Sigma^{(0)} = G^{(i)}W^{(0)}$. This allows to form a partial self-consistency loop, where the screening is kept on the DFT level. The method is commonly known as GW0, even though only eigenvalues are updated:

* Determine the independent particle polarizability $\chi^{(0)}\_{\bf GG'}({\bf q},\omega)$
* Determine the screened Coulomb potential $W^{(0)}\_{\bf GG'}({\bf q},\omega)$ and keep it fixed in the following
* Determine the self-energy $\Sigma^{(j)}({\bf r,r'},\omega)= G^{(j)}W^{(0)}$.
* Update quasi-particle energies $E^{(j+1)}\_{n\bf k}=\epsilon\_{n\bf k}+ Z\_{n\bf k}^{(j)} {\rm Re}\left[
  \langle \phi\_{n\bf k}|
  -\frac{\Delta}2+V\_{ext}+V\_h+\Sigma^{(j)}(\omega=E^{(j)}\_{n\bf k}) -\epsilon\_{n\bf k}
  |\phi\_{n\bf k}\rangle
  \right]$. In the first iteration use $E\_{n\bf k}^{(0)}=\epsilon\_{n\bf k}$

The last two steps are repeated until self-consistency is reached. The GW0 method is computationally slightly more expensive than the single-shot approach, but yields often excellent agreement with experimentally measured band gaps while being computationally affordable at the same time.

Note that the GW0 and its single-shot approach do not allow for updates in the Kohn-Sham orbitals $\phi\_{n\bf k}$, merely the eigenvalues are updated. Furthermore, the name GW0 indicates an update in the Green's function as a solution of the Dyson equation, while the used spectral representation of the Green's function above is strictly speaking correct only in the single-shot approach. Since VASP6 allows to update the Green's function from the solution of the corresponding Dyson equation, the commonly known GW0 method is also selectable with ALGO=EVGW0 ("eigenvalue GW") and the number of iteration is set with NELM.

## Self-consistent Quasi-particle approximation: scQPGW0

In addition to eigenvalues one can use the self-consistent Quasi-particle GW0 approach (scQPGW0) to update the orbitals $\phi\_{n\bf k}\to \psi^{(j)}\_{n\bf k}$ as well. This approach was presented first by Faleev et. al, and used a hermitized self-energy $\Sigma^{\rm herm}=\frac{\Sigma+\Sigma^\dagger}2$ in the eigenvalue equation to determine both, quasi-particle energies $E\_{n\bf k}$ and corresponding orbitals $\psi\_{n\bf k}$.

In contrast to the Faleev approach one may consider a generalized eigenvalue problem instead that is obtained consistently from the linearization of the self-energy
$\Sigma(E^{(j+1)})\approx \Sigma(E^{(j)}) + \xi(E^{(j)})(E^{(j+1)}-E^{(j)})$ (where $\xi(E^{(j)})=\partial\Sigma(E^{(j)})/ \partial E^{(j)}$) and reads

$\underbrace{\left[
T + V\_{ext}+V\_h + \Sigma\left(E\_{n\bf k}^{(j)}\right) - \xi\left(E^{(j)}\_{n\bf k}\right) E^{(j)}\_{n\bf k}\right]}\_{{\bf H}(E^{(j)}\_{n\bf k})}
\left|\psi\_{n\bf k}^{(j+1)} \right\rangle = E^{(j+1)}\_{n\bf k}\underbrace{\left[1-\xi(E^{(j)}\_{n\bf k}) \right]}\_{{\bf S}(E^{(j)}\_{n\bf k})} \left|\psi\_{n\bf k}^{(j+1)} \right\rangle$

The resulting Hamiltonian ${\bf H}$ and overlap matrix ${\bf H}$ are non-hermitian in general, implying that the resulting orbitals $\left|\psi\_{n\bf k}^{(j+1)} \right\rangle$ are not normalized to 1. Therefore, VASP determines the hermitian parts $H= \frac{ {\bf H} + {\bf H}^\dagger }{2}, S = \frac{ {\bf S} + {\bf S}^\dagger }{2}$ and diagonalizes following matrix instead

$S^{-1/2} H S^{-1/2} = U \Lambda U^\dagger$

The resulting diagonal matrix $\Lambda$ contains the new quasi-particles, while the unitary matrix $U$ determine the new orbitals $\psi\_{n\bf k}^{(j+1)} = \sum\_{m}U\_{nm} \psi\_{m\bf k}^{(j+1)}$.
The method can be selected in VASP with ALGO=QPGW0. See here for more information.

## Low-scaling GW: The Space-time Formalism

Available as of VASP.6 are low-scaling algorithms for ACFDT/RPA. This page describes the formalism of the corresponding low-scaling GW approach.
A theoretical description of the ACFDT/RPA total energies is found here. A brief summary regarding GW theory is given below, while a practical guide can be found here.

## Theory

The GW implementations in VASP described in the papers of Shishkin *et al.* avoid storage of the Green's function $G$ as well as Fourier transformations between time and frequency domain entirely. That is, all calculations are performed solely on the real frequency axis using Kramers-Kronig transformations for convolutions in the equation of $\chi$ and $\Sigma$ in reciprocal space and results in a relatively high computational cost that scales with $N^4$ (number of electrons).

The scaling with system size can, however, be reduced to $N^3$ by performing a so-called Wick-rotation to imaginary time $t\to i\tau$.

Following the  low scaling ACFDT/RPA algorithms the space-time implementation determines first, the non-interacting Green's function on the imaginary time axis in real space

$G({\bf r},{\bf r}',i\tau)=-\sum\_{n{\bf k}}\phi\_{n{\bf k}}^{(0)}({\bf r}) \phi\_{n{\bf k}}^{\*(0)}({\bf r}') e^{-(\epsilon\_{n{\bf k}}-\mu)\tau}\left[\Theta(\tau)(1-f\_{n{\bf k}})-\Theta(-\tau)f\_{n{\bf k}}\right]$

Here $\Theta$ is the step function and $f\_{n{\bf k}}$ the occupation number of the state $\phi\_{n{\bf k}}^{(0)}$. Because the Green's function is non-oscillatory on the imaginary time axis it can be represented on a coarse grid $\tau\_{m}$, where the number of time points can be selected in VASP via the NOMEGA tag. Usually 12 to 16 points are sufficient for insulators and small band gap systems.

Subsequently, the irreducible polarizability is calculated from a contraction of two imaginary time Green's functions

$\chi({\bf r},{\bf r}',i\tau\_m) = -G({\bf r},{\bf r}',i\tau\_m)G({\bf r}',{\bf r},-i\tau\_m)$

Afterwards, the same compressed Fourier transformation as for the  low scaling ACFDT/RPA algorithms is employed to obtain the irreducible polarizability in reciprocal space on the imaginary frequency axis $\chi({\bf r},{\bf r}',i\tau\_m) \to \chi\_{{\bf G}{\bf G}'}({\bf q},i \omega\_n)$.

The next step is the computation of the screened potential

$W\_{{\bf G}{\bf G}'}({\bf q},i\omega\_m)=\left[\delta\_{{\bf G}{\bf G}'}-\chi\_{{\bf G}{\bf G}'}({\bf q},i\omega\_m)V\_{{\bf G}{\bf G}'}({\bf q})\right]^{-1}V\_{{\bf G}{\bf G}'}({\bf q})$

followed by the inverse Fourier transform $W\_{{\bf G}{\bf G}'}({\bf q},i \omega\_n) \to \chi({\bf r},{\bf r}',i\tau\_m)$ and the calculation of the self-energy

$\Sigma({\bf r},{\bf r}',i\tau\_m) = -G({\bf r},{\bf r}',i\tau\_m)W({\bf r}',{\bf r},i\tau\_m)$

From here, several routes are possible including all approximations mentioned above, that is the single-shot, EVG0 and QPEVG0 approximation. All approximations have one point in common.

In contrast to the real-frequency implementation, the low-scaling GW algorithms require an analytical continuation of the self-energy from the imaginary frequency axis to the real axis. In general, this is an ill-defined problem and usually prone to errors, since the self-energy is known on a finite set of points. VASP determines internally a Padé approximation of the self-energy $\Sigma(z)$ from the calculated set of NOMEGA points $\Sigma(i\omega\_n)$ and solves the non-linear eigenvalue problem

$\left[ T+V\_{ext}+V\_h+\Sigma(z) \right]\left|\phi\_{n\bf k}\right\rangle = z\left| \phi\_{n\bf k} \right\rangle$

on the real frequency axis $z=\omega$.

Because preceding Fourier transformations have been carried out with exponentially suppressed errors, the analytical continuation $\Sigma(z)$ of the self-energy can be determined with high accuracy. The analytical continuation typically yields energies that differ less than 20 meV from quasi-particle energies obtained from the real-frequency calculation.

In addition, the space-time formulation allows to solve the full Dyson equation for $G({\bf r,r'},i\tau)$ with decent computational cost. This approach is known as the self-consistent GW approach (scGW) and is available as of VASP6.

## Limitations of GW

From a physical point of view, the scGW method yields mostly unsatisfactory results compared to experiment. Notably, the band gaps are significantly overestimated compared to experiment, and plasmonic satellites are entirely missing in the spectral
function.

The fact that "sloppier" GW flavours, such as EVGW0 or even the single-shot approach yield more accurate results is due to fortuitous error cancelling and can be understood in terms of the band-gap $\Delta$ of a system. The DFT gap is typically smaller than the GW band gap and yields, therefore, a larger dielectric function $\epsilon(\omega)=1-\chi(\omega)V$ (the polarizability is inverse proportional to the band gap of the system). Although the band gap is corrected by GW, at the same time the screening of the Coulomb interaction is weakened. Forcing self-consistency only increases the effect and deteriorates the agreement with experimental band gaps.
The rather disappointing results of the self-consistent GW approximation shows the general limitations of Hedin's equations in the absence of vertex corrections. It can be shown that inclusion of vertex corrections yields band gaps that are again in agreement with experiment.

## References

---
