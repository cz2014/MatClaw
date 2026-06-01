# RPA/ACFDT: Correlation energy in the Random Phase Approximation

Categories: Theory, Low-scaling GW and RPA, Many-body perturbation theory

ACFDT stands for the adiabatic connection fluctuation dissipation theorem and is an alternative way to derive the energy expression for the correlation energy in the random phase approximation (RPA). In the following, the diagrammatic description is presented. For the ACFDT formulation, the reader is referred to the literature. There is also a lecture introducing RPA on our YouTube channel.

## Diagrammatic approach to the correlation energy

The correlation energy $E\_c$ is defined as the missing piece of the Hartree-Fock energy $E\_{x}$ to the total energy, that is $E\_{tot} = E\_{x} + E\_c$. The exact form of $E\_c$ is unknown and can be calculated only approximately for a realistic system. The Random Phase Approximation (RPA) is such an approximation that provides access to $E\_c$. The RPA was first studied by Bohm and Pines for the homogeneous electron gas and was later recognized by Gell-Mann and Brueckner as an approximation of $E\_c$ that can be expressed in the same language as Feynman used a few years earlier to describe the positron.

Feynman's diagrammatic approach is based on quantum field theory (QFT), which in turn is based on the Gell-Mann and Low theorem. This theorem states that the eigenstate of an interacting Hamiltonian can be expressed in terms of the eigenstates of the non-interacting one. For this reason, each diagrammatic calculation, like the RPA or GW, requires the solution of the non-interacting Hamiltonian $H\_0$ of the system, like for instance the Hartree-Fock energies and orbitals or the solutions of the Kohn-Sham Hamiltonian $\epsilon\_{n\bf k}, \phi\_{n\bf k}$.

QFT is commonly formulated in the Dirac (also known as interaction) picture, where dynamics described by the interaction part $\hat V$ of the fully interacting Hamiltonian $\hat H=\hat H\_0+\hat V$ are singled out via time-dependent operators like
$\hat V(t)=e^{i\hat H\_0t}\hat Ve^{-i\hat H\_0t}$. These operators act on states like the non-interacting groundstate of the system $|\Psi\_0\rangle$ causing fluctuations at a specific point in time. The main idea of QFT is to understand observations, which can be measured by an observer, as a collective phenomenon of all possible fluctuations.

Thereby, fluctuations are understood as the creation of virtual electrons (and holes) that interact with each other and are annihilated after some time. Formally this is achieved by introducing creation $\hat\psi^\dagger({\bf r},t)$ and annihilation operators $\hat\psi({\bf r},t)$ that satisfy following relations

$\hat\psi({\bf r},t)|\Psi\_0\rangle = 0 =\langle \Psi\_0 | \hat\psi({\bf r},t)$

$\lbrace \psi({\bf r},t),\psi^\dagger({\bf r},t)\rbrace =
\psi^\dagger({\bf r},t)\psi^\dagger({\bf r},t) +
\psi^\dagger({\bf r},t),\psi({\bf r},t)
= i\delta({\bf r}-{\bf r}')$

$\lbrace\psi^\dagger({\bf r},t),\psi^\dagger({\bf r},t) \rbrace = 0 =
\lbrace\psi({\bf r},t),\psi({\bf r},t) \rbrace.$

The first relation defines the non-interacting groundstate $|\Psi\_0\rangle$ as the Fermi vacuum (the groundstate in the absence of any fluctuations), while the second and third anti-commutator relations are a consequence of the Pauli principle. In fact, all operators that describe measurable quantities of a system of interacting electrons can be represented in terms of $\psi^\dagger({\bf r},t)$ and $\psi({\bf r},t)$ alone; additional objects are not necessary.

However, the time-ordering operator

$\hat T \hat A(t)\hat B(t') = \Theta(t-t') \hat A(t)\hat B(t') - \Theta(t'-t)\hat B(t')\hat A(t),$

where $\Theta(t)$ is the unit step function, and the time-evolution operator

$\hat S(t,t\_0)=\hat T e^{-i\int\_{t\_0}^t \hat V(t'){\rm d}t'}$

are helpful quantities, since they allow to formulate the Gell-Mann and Low theorem as follows.

### Gell-Mann and Low theorem

Using adiabatic coupling of the interaction $\hat V(t) \to \hat V\_\eta(t) = e^{-\eta|t|} \hat V$, Gell-Mann and Low proved that the vectors

$\frac{|\Omega\_\nu\rangle}{\langle \Omega\_\nu|\Psi\_\nu\rangle} =\lim\_{\eta\to0}\frac{\hat S\_\eta(0,-\infty)|\Psi\_\nu\rangle}{\langle \Omega\_\nu|\Psi\_\nu\rangle}$

are the eigenstates of the interacting Hamiltonian.

We follow the common literature and suppress the infinitesimal $\eta$ in the following bearing in mind that the limit $\eta \to 0$ is performed at the very end of the calculation.

### Diagrammatic perturbation theory

A consequence of the Gell-Mann and Low theorem, is the following form of the interacting groundstate energy

$E\_{tot}=E\_0 = \langle \Omega\_0|\hat H|\Omega\_0\rangle = \frac{\langle\Psi\_0| \hat S(\infty,-\infty)\hat H|\Psi\_0\rangle}{\langle \Psi\_0|\hat S(\infty,-\infty)|\Psi\_0\rangle},$

which can be seen as starting point of diagrammatic perturbation theory. The expression above is used to derive all possible approximations by expanding the time-evolution operator $\hat S$ into a series. The resulting matrix-elements of creation and annihilation operators are evaluated term by term using the canonical anti-commutator relations defined above (Wick's theorem). It follows that all terms in perturbation theory are expressed by only two quantities, the non-interacting Feynman propagator

$G\_0(1,2) = -i
\sum\_{n{\bf k}} \phi({\bf r}\_2)\phi^\*({\bf r}\_1) e^{-i(\epsilon\_{n \bf k}-\epsilon\_F)(t\_2-t\_1)}\left[ f\_{n\bf k}\Theta(t\_2-t\_1) - (1-f\_{n\bf k})\Theta(t\_1-t\_2)\right],
\quad 1 = ({\bf r}\_1,t\_1), 2 = ({\bf r}\_2,t\_2)$

and the Coulomb interaction

$V(1,2) = \frac{\delta( t\_1-t\_2)}{|{\bf r}\_1-{\bf r}\_2|}.$

Then, each term in the series corresponds to an integral over space-time coordinates $({\bf r},t)$.

Feynman diagrams are used to illustrate which terms are considered in the perturbation series. The illustration is usually achieved with so-called Feynman rules that map a specific diagram to an integral (and vice versa). For instance the second order diagram

is also known as the direct Møller-Plessett term and stands for following integral

$E^{(2)}\_{\rm dMP}=\int{\rm d}(1,2,3,4) G\_0(1,2)G\_0(2,1) V(1,3)V(2,4) G\_0(3,4)G\_0(4,3), \quad {\rm d}(1,\cdots,4) = {\rm d}{\bf r}\_1{\rm d}t\_1\cdots {\rm d}{\bf r}\_4{\rm d}t\_4$

All Feynman rules can be found in the book of Negele and Orland or elsewhere.

## The random-phase approximation

The RPA is obtained from neglecting all second and higher order terms in the perturbation series of the groundstate energy, except of those which can be expressed soley in terms of the independent particle polarizability

$\chi\_0(1,2) = -i G\_0(1,2) G\_0(2,1)$

corresponding to the "bubble" diagram

Because of the symmetric time property $\chi\_0(t\_2-t\_1)=\chi\_0(t\_1-t\_2)$, the independent particle polarizability is of bosonic character. Because the RPA neglects all non-bosonic terms in the perturbation series, it corresponds essentially to a "bosonization" of the many-body problem for which the n-th order term can be written analytically as

$E^{(n)}\_{\rm dMP} = \frac1{2n}\int\_{-\infty}^\infty\frac{{\rm d}\omega}{2\pi} {\rm Tr}\left[ \tilde \chi\_0(\omega) \cdot V \right]^n.$

Here, the trace of the matrix product is most effectively done in reciprocal space $\left[\tilde \chi\_0(\omega) \cdot V\right]({\bf q+G}\_1,{\bf q+G}\_2) = \sum\_{\bf G} \tilde \chi\_0({\bf q+G}\_1,{\bf G},\omega)V({\bf q+G},{\bf q+G}\_2)$ using the Fourier transformed polarizability $\tilde \chi\_0({\bf q+G}\_1,{\bf q+G}\_2,\omega)$, the diagonal Coulomb potential $V({\bf q+G}\_1,{\bf q+G}\_2)=\frac{ \delta\_{ {\bf G}\_1 {\bf G}\_2 } }{|{\bf q+G}\_1|}$ and the conserved crystal momentum ${\bf q}$ in the first Brillouin zone.

All bubble terms of order $n \ge 2$ can be written in a closed form using the series for the logarithm $\ln(1-x)+x=-\sum\_{n=2}^\infty \frac{x^n}{n}$ and define the correlation part of the RPA energy

$E\_c^{\rm RPA} = \int\frac{ {\rm d}\omega}{2\pi} {\rm Tr}\left\lbrace \ln\left[ 1-\tilde \chi\_0(\omega)\cdot V \right] + \tilde \chi\_0(\omega)\cdot V \right\rbrace.$

There are two first order contributions to the total energy that yield the exact exchange energy $E\_x=T+V\_{ext}+V\_h+V\_x$, which is usually determined separately.

## Computational Complexity

The calculation of the RPA integral requires the determination of the independent particle polarizability matrix $\tilde \chi^0\_{\bf GG'}({\bf q},\omega\_n)=\tilde \chi\_0({\bf q+G},{\bf q+G}',\omega\_n)$ on each of the $N\_{\bf q}$ sampling points of the first Brillouin zone for $N\_{\omega}$ frequency points. The number of frequency points is reduced drastically, by performing the integration over the imaginary frequency axis $\omega\to i\omega$.

The independent particle polarizability on the imaginary axis can be determined with two alternative methods.

### Quartic scaling RPA: Direct calculation

Direct calculation of $\tilde\chi^0$ using the formula of Adler and Wiser

$\tilde\chi^0\_{{\bf GG}'}({\bf q},i\omega) = \sum\limits\_{{\bf k}\in BZ}\sum\limits\_{n,n'}
\frac{
f\_{n{\bf k}}(1 - f\_{n{\bf k-q}})
}{
\epsilon\_{n{\bf k-q}}-\epsilon\_{n{\bf k}} -i \omega
}
\langle \phi\_{n {\bf k-q}} | e^{i{\bf Gr}} | \phi\_{n'{\bf k}} \rangle
\langle \phi\_{n' {\bf k}} | e^{-i{\bf G'r'}} | \phi\_{n'{\bf k-q}} \rangle$

yields an RPA algorithm that has a computational cost of $N\_\omega N\_{\bf k}^2 N\_{\bf G}^4$. Because the number of plane waves $N\_{\bf G}$ scales linearly with the system size (number of electrons in the unit cell), the direct calculation of the polarizability is unfavourable for large system sizes, e.g. for more than ~20 atoms in the unit cell.

### Cubic scaling RPA: Contraction of imaginary time Green's functions

An alternative way to determine $\tilde\chi^0$ is to frist determine imaginary time Green's functions of the form

$G\_0({\bf r,r'},i\tau) = \sum\limits\_{{\bf k}\in BZ}\sum\limits\_{n}
\phi\_{n{\bf k}}({\bf r})\phi\_{n \bf k}^\*({\bf r'}) e^{-(\epsilon\_{n\bf k}-\epsilon\_{F})\tau}\left[
\Theta(-\tau)f\_{n\bf k}-\Theta(\tau)(1-f\_{n\bf k})
\right]$

and to perform afterwards a Fourier transformation into reciprocal and imaginary frequency space of

$\chi\_0({\bf r,r'},i\tau) = -G\_0({\bf r,r'},i\tau) G\_0({\bf r',r},-i\tau).$

Although more evolved, this approach has the advantage that the computational cost for the determination of $\tilde \chi\_0$ scales with $N\_\omega N\_{\bf k} N\_{\bf G}^3$ and is essentially only cubic in system size. The space-time method allows to study relatively large systems with the RPA.

## Basis set convergence of RPA-ACFDT calculations

The expression for the ACFDT-RPA correlation energy written in terms of reciprocal lattice vectors reads:

$E\_{\rm c}^{\rm RPA}=\int\_{0}^{\infty} \frac{\mathrm{d}\omega}{2\pi} \sum\_{{\mathbf{q}}\in \mathbf{BZ} }\sum\_{{\mathbf{G}}} \left\{(\mathrm{ln}[1-\tilde\chi^0({\mathbf{q}},\mathrm{i}\omega)V({\mathbf{q}})])\_{{\mathbf{G,G}}} +V\_{{\mathbf{G,G}}}({\mathbf{q}})\tilde\chi^0({\mathbf{q}},{\mathrm{i}}\omega) \right\}$.

The sum over reciprocal lattice vectors has to be truncated at some $\mathbf{G}\_{\mathrm{max}}$, determined by $\frac{\hbar^2|{\mathbf{G}}+{\mathbf{q}}|^2}{2\mathrm{m}\_e}$ < ENCUTGW, which can be set in the INCAR file. The default value is $\frac{2}{3}\times$ ENCUT, which experience has taught us not to change. For systematic convergence tests, instead increase ENCUT and repeat steps 1 to 4, but be aware that the "maximum number of plane-waves" changes when ENCUT is increased. Note that it is virtually impossible, to converge absolute correlation energies. Rather concentrate on relative energies (e.g. energy differences between two solids, or between a solid and the constituent atoms).

Since correlation energies converge very slowly with respect to $\mathbf{G}\_{\rm max }$, VASP automatically extrapolates to the infinite basis set limit using a linear regression to the equation:

$E\_{\mathrm{c}}({\mathbf{G}})=E\_{\mathrm{c}}(\infty)+\frac{A}{{\mathbf{G}}^3}$.

Furthermore, the Coulomb kernel is smoothly truncated between ENCUTGWSOFT and ENCUTGW using a simple cosine like window function (Hann window function).
Alternatively, the basis set extrapolation can be performed by setting LSCK=.TRUE., using the squeezed Coulomb kernel method.

The default for ENCUTGWSOFT is 0.8$\times$ENCUTGW (again we do not recommend to change this default).

The integral over $\omega$ is evaluated by means of a highly accurate minimax integration. The number of $\omega$ points is determined by the flag NOMEGA, whereas the energy range of transitions is determined by the band gap and the energy difference between the lowest occupied and highest unoccupied one-electron orbital. VASP determines these values automatically (from vasp.5.4.1 on), and the user should only carefully converge with respect to the number of frequency points NOMEGA. A good choice is usually NOMEGA=12, however, for large gap systems one might obtain $\mu$eV convergence per atom already using 8 points, whereas for metals up to NOMEGA=24 frequency points are sometimes necessary, in particular, for large unit cells.

Strictly adhere to the steps outlines above. Specifically, be aware that steps two and three require the WAVECAR file generated in step one, whereas step four requires the WAVECAR and WAVEDER file generated in step three (generated by setting LOPTICS=*.TRUE.*).

## Matsubara Formalism: Metallic systems at finite Temperature

The zero-temperature formalism of many-body perturbation theory breaks down for metals (systems with zero energy band-gap) as pointed out by Kohn and Luttinger. This conundrum is lifted by considering diagrammatic perturbation theory at finite temperature $T\gt 0$, which may be understood by an analytical continuation of the real-time $t$ to the imaginary time axis $-i\tau$. Matsubara has shown that this Wick rotation in time $t\to-i\tau$ reveals an intriguing connection to the inverse temperature $\beta=1/T$ of the system.
More precisely, Matsubara has shown that all terms in perturbation theory at finite temperature can be expressed as integrals of imaginary time quantities (such as the polarizability $\chi(-i\tau)$) over the fundamental interval $-\beta\le\tau\le\beta$.

As a consequence, one decomposes imaginary time quantities into a Fourier series with period $\beta$
that determines the spacing of the Fourier modes. For instance the imaginary polarizability can be written as

$\chi(-i\tau)=\frac1\beta\sum\_{m=-\infty}^\infty \tilde \chi(i\nu\_m)e^{-i\nu\_m\tau},\quad \nu\_m=\frac{2m}\beta\pi$

and the corresponding random-phase approximation of the correlation energy at finite temperature becomes a series over (in this case, bosonic) Matsubara frequencies

$\Omega\_c^{\rm RPA}=\frac12\frac1\beta \sum\_{m=-\infty}^\infty {\rm Tr}\left\lbrace
\ln\left[ 1 -\tilde \chi(i\nu\_m) V
\right] -\tilde \chi(i\nu\_m) V
\right\rbrace,\quad \nu\_m=\frac{2m}\beta\pi$

The Matsubara formalism has the advantage that all contributions to the Green's function and the polarizability are mathematically well-defined, including contributions from states close to the chemical potential $\epsilon\_{n{\bf k}}\approx \mu$, such that Matsubara series also converge for metallic systems.

Although formally convenient, the Matsubara series converges poorly with the number of considered terms in practice. VASP, therefore, uses a compressed representation of the Fourier modes by employing the Minimax-Isometry method. This approach converges exponentially with the number of considered frequency points.

## References
