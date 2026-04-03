# Category:Exchange-correlation functionals

Categories: VASP

In the Kohn-Sham (KS) formulation of density-functional theory (DFT), the total energy is given by

:   $$E\_{\rm tot}^{\rm DFT} = -\frac{1}{2}\sum\_{i}\int\psi\_{i}^{\*}({\bf r})\nabla^{2}\psi\_{i}({\bf r})d^{3}r - \sum\_{A}\int\frac{Z\_{A}}{\left\vert{\bf r}-{\bf R}\_{A}\right\vert}n({\bf r})d^{3}r + \frac{1}{2}\int\int\frac{n({\bf r})n({\bf r'})}{\left\vert{\bf r}-{\bf r'}\right\vert}d^{3}rd^{3}r' + E\_{\rm xc} + \frac{1}{2}\sum\_{A\ne B}\frac{Z\_{A}Z\_{B}}{\left\vert{\bf R}\_{A}-{\bf R}\_{B}\right\vert}$$

where the terms on the right-hand side represent the non-interacting kinetic energy of the electrons, the electrons-nuclei attraction energy, the classical Coulomb electron-electron repulsive energy, the exchange-correlation energy, and the nuclei-nuclei repulsion energy, respectively. The KS orbitals $\psi\_{i}$ and the electron density $n=\sum\_{i}\left\vert\psi\_{i}\right\vert^{2}$ that are used to evaluate $E\_{\rm tot}^{\rm DFT}$ are obtained by solving self-consistently the (generalized) KS equations

:   $$\left(-\frac{1}{2}\nabla^{2} -\sum\_{A}\frac{Z\_{A}}{\left\vert{\bf r}-{\bf R}\_{A}\right\vert} + \int\frac{n({\bf r'})}{\left\vert{\bf r}-{\bf r'}\right\vert}d^{3}r' + \hat{v}\_{\rm xc}({\bf r})\right)\psi\_{i}({\bf r}) = \epsilon\_{i}\psi\_{i}({\bf r}).$$

The only terms in $E\_{\rm tot}^{\rm DFT}$ and in the (g)KS equations that are not known exactly are the **exchange-correlation energy functional** $E\_{\rm xc}$ and **potential** $\hat{v}\_{\rm xc}$. Therefore, the accuracy of the calculated properties depends strongly on the approximations used for $E\_{\rm xc}$ and $\hat{v}\_{\rm xc}$.

Note that depending on the type of approximation for $E\_{\rm xc}$ the potential $\hat{v}\_{\rm xc}$ is calculated either as the derivative with respect to the density, $v\_{\rm xc}=\delta E\_{\rm xc}/\delta n$ (KS scheme), or as the derivative with respect to the orbitals, $\hat{v}\_{\mathrm{xc}}\psi\_{i}=\delta E\_{\mathrm{xc}}/\delta\psi\_{i}^{\*}$ (generalized KS scheme).

Several hundreds of approximations for the **exchange and correlation** have been proposed. They can be classified into families like the local density approximation (LDA), semilocal approximations (generalized gradient approximation (GGA) and METAGGA), or hybrid. There is also the possibility to include a van der Waals correction or an on-site Coulomb repulsion using DFT+U on top of another functional. The different types of approximations available in VASP are listed below. Also mentioned are the many-body methods for an accurate calculation of the correlation energy, which, however, are not DFT methods.

### Which exchange-correlation method to choose?

Among the hundreds of methods available, the choice for the exchange and correlation method should be done by considering the following points:

* **Appropriate for the studied system and property**:
  + Some functionals were constructed without emphasis on a particular property or class of systems, while others were developed specifically for van der Waals interactions, strongly correlated systems, or band gap calculation, for instance.
  + Therefore, a method should be appropriately chosen according to the information found in the literature.
* **Computational power**:
  + The hybrid functionals and the many-body methods are computationally much more expensive (by orders of magnitude!) than the (semi)local approximations. Thus, it is especially important for such methods to have a rough idea of the required computational time and memory. This can be done by first considering systems of smaller size and reduced parameters (basis-set size and k-point mesh), and then increasing them gradually to see how the calculation time evolves.
  + If the calculations are unaffordable given the available computer power, then using a cheaper method should be considered. For instance, for strongly correlated systems, the DFT+U may be as reliable as the much more costly hybrid functionals.

## Types of approximations

### Local density approximation (LDA)

The LDA functionals are purely local in the sense that they depend solely on the **electron density $n$**:

:   $$E\_{\mathrm{xc}}^{\mathrm{LDA}}=\int\epsilon\_{\mathrm{xc}}^{\mathrm{LDA}}(n)d^{3}r$$

with a corresponding potential given by

:   $$v\_{\mathrm{xc}}^{\mathrm{LDA}} = \frac{\partial\epsilon\_{\mathrm{xc}}^{\mathrm{LDA}}}{\partial n}.$$

The most common LDA functionals, e.g. Slater+Perdew-Zunger, provide the (nearly) exact exchange-correlation energy for the homogeneous electron gas. However, they are in general quite inaccurate for real systems and rarely used nowadays.

* GGA,XC

### Generalized gradient approximation (GGA)

Compared to LDA there is an additional dependency on the **gradient of the electron density $\nabla n$**:

:   $$E\_{\mathrm{xc}}^{\mathrm{GGA}}=\int\epsilon\_{\mathrm{xc}}^{\mathrm{GGA}}(n,\nabla n)d^{3}r$$

leading to an additional term in the potential:

:   $$v\_{\mathrm{xc}}^{\mathrm{GGA}} = \frac{\partial\epsilon\_{\mathrm{xc}}^{\mathrm{GGA}}}{\partial n} -
    \nabla\cdot\frac{\partial\epsilon\_{\mathrm{xc}}^{\mathrm{GGA}}}{\partial\nabla n}.$$

The GGA functional that has been the most commonly used in solid-state physics is PBE, and is still widely used in particular for the geometry optimization.

* GGA,XC

### Meta generalized gradient approximation (meta-GGA)

Compared to the GGAs, the meta-GGA functionals depend additionally on the **kinetic-energy density $\tau$** and/or the **Laplacian of the electron density $\nabla^{2}n$**:

:   $$E\_{\mathrm{xc}}^{\mathrm{MGGA}}=\int\epsilon\_{\mathrm{xc}}^{\mathrm{MGGA}}(n,\nabla n,\nabla^{2}n,\tau)d^{3}r$$

leading to

:   $$\hat{v}\_{\mathrm{xc}}^{\mathrm{MGGA}}\psi\_{i} =
    \frac{\delta E\_{\mathrm{xc}}^{\mathrm{MGGA}}}{\delta\psi\_{i}^{\*}} =
    \left(\frac{\partial\epsilon\_{\mathrm{xc}}^{\mathrm{MGGA}}}{\partial n} -
    \nabla\cdot\frac{\partial\epsilon\_{\mathrm{xc}}^{\mathrm{MGGA}}}{\partial\nabla n} +
    \nabla^2\frac{\partial\epsilon\_{\mathrm{xc}}^{\mathrm{MGGA}}}{\partial\nabla^2 n}
    \right)\psi\_{i} -
    \frac{1}{2}\nabla\cdot\left(\frac{\partial\epsilon\_{\mathrm{xc}}^{\mathrm{MGGA}}}{\partial \tau}
    \nabla\psi\_{i}\right).$$

The last term is of non-multiplicative type and arises due to the dependency of the functional on $\tau$. Thus, the $\tau$-dependency leads to a method that belongs to the generalized KS scheme.

Although meta-GGAs are slightly more expensive than GGAs, they are still fast to evaluate and appropriate for very large systems. Furthermore, meta-GGAs, like SCAN, can be more accurate than GGAs and more broadly applicable.

* METAGGA,XC
* band-structure calculation using meta-GGA functionals

### Hartree-Fock (HF) and hybrid functionals

In hybrid functionals the exchange part consists of a linear combination of the **HF exchange** and a semilocal (e.g., GGA) functional:

:   $$E\_{\mathrm{xc}}^{\mathrm{hybrid}}=\alpha E\_{\mathrm{x}}^{\mathrm{HF}} + (1-\alpha)E\_{\mathrm{x}}^{\mathrm{SL}} + E\_{\mathrm{c}}^{\mathrm{SL}}$$

where $\alpha$ determines the relative amount of HF and semilocal exchange. The hybrid functionals can be divided into families according to the interelectronic range at which the HF exchange is applied: at full range (unscreened hybrids) or either at short or long range (called screened or range-separated hybrids). From the practical point of view, the short-range hybrid functionals like HSE06 are preferable for periodic solids, since leading to faster convergence with respect to the number of k-points (or size of the unit cell).

The HF method, where $E\_{\mathrm{xc}}=E\_{\mathrm{x}}^{\mathrm{HF}}$, is not accurate since correlation is entirely missing, however it is the basis of the many-body methods.

On the technical side, $E\_{\mathrm{x}}^{\mathrm{HF}}$ is expensive to evaluate and, since it is orbital-dependent, it leads to a nonlocal potential implemented in the generalized KS scheme.

* Hybrid functionals

### Exact exchange optimized-effective potential (EXX-OEP), localized Hartree-Fock (LHF), and Krieger-Li-Iafrate (KLI)

In these methods the minimization of the exact-exchange HF energy expression is done with respect to the electron density $n$, instead of with respect to the orbitals $\psi\_i$. That means that a local (in the sense of multiplicative) KS potential is calculated. EXX-OEP provides the exact potential, however, performing such calculations is non-trivial in particular since the unoccupied orbitals are required. LHF is an approximation to EXX-OEP that alleviates the use of unoccupied orbitals, while KLI is a further approximation.

These methods are available in VASP, but not documented.

### Density functional theory plus U (DFT+U)

The semilocal approximations, LDA and GGA in particular, often fail to describe systems with localized (strongly correlated) $d$ or $f$ electrons (this manifests itself primarily in the form of unrealistic one-electron energies or too small magnetic moments). In some cases this can be remedied by introducing on the $d$ or $f$ atom a strong intra-atomic interaction in a simplified (screened) Hartree-Fock like manner ($E\_{\text{HF}}[\hat{n}]$), as an on-site replacement of the semilocal functional:

:   $$E\_{\text{xc}}^{\text{DFT}+U}[n,\hat{n}] = E\_{\text{xc}}^{\text{SL}}[n] + E^{\text{HF}}[\hat{n}] - E\_{\text{dc}}[\hat{n}]$$

where $E\_{\text{dc}}[\hat{n}]$ is the double-counting term, that removes some of the on-site exchange-correlation effects present in $E\_{\text{xc}}^{\text{SL}}[n]$, and $\hat{n}$ is the on-site occupancy matrix of the $d$ or $f$ electrons. This approach, known as the DFT+U method (traditionally called LSDA+U,) can often be used as a cheap alternative to the much more costly hybrid functionals. Several variants of the DFT+U method exist, differing mostly in the expression for $E\_{\text{dc}}[\hat{n}]$.

* DFT+U

### van der Waals (vdW) functionals

The semilocal and hybrid functionals do not include the London dispersion forces. Therefore, they can not be applied reliably on systems where the London dispersion forces play an important role. To account more properly for the London dispersion forces in DFT, a correlation dispersion term can be added to the semilocal or hybrid functional. This leads to the so-called **van der Waals functionals**:

:   $$E\_{\text{xc}}^{\text{vdW}} = E\_{\text{xc}}^{\text{SL/hybrid}} + E\_{\text{c,disp}}.$$

Most of the existing approximations for calculating $E\_{\text{c,disp}}$ belong to one of these types: atom-pairwise, many-body dispersion, or nonlocal vdW-DF functionals.

* Van der Waals functionals

### Many-body methods

Methods based on many-body perturbation theory provide a first-principle approach to the correlation effects. They allow to calculate accurately the total energy or the electronic structure of materials. Such methods lie formally outside the DFT framework, although strong connections to DFT can be made. Some of the most known many-body methods are the random-phase approximation (RPA) and GW. The disadvantage of these methods is to be computationally much more expensive than DFT.

Also quite popular is DFT+DMFT, which is a non-perturbative method to calculate the correlation effects. It can be regarded as a many-body extension of DFT+U and is also mainly used for systems with strongly correlated $d$ or $f$ electrons.

* Many-body perturbation theory
* DFT+DMFT

## References
