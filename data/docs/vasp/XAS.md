# Category:XAS

Categories: VASP, Linear response, Dielectric properties

X-ray absorption spectroscopy (XAS) is a powerful method for investigating the chemical properties of materials. The absorption of the X-ray photons involves excitations of the core electrons into conduction bands. The main challenge for an accurate description of such excitations is the interactions between a positive charge left in place of the excited core electron, i.e., **core hole**, and the excited electron, which can form a bound state called **exciton**. There are two main approaches to *ab initio* modeling of XAS. The first one is based on DFT and is commonly known as the supercell core-hole (SCH) method. The second approach is based on the many-body perturbation theory and requires solving the Bethe-Salpeter equation (BSE). In VASP both approaches rely on the frozen core (FC) approximation, where the core electrons are kept frozen in the configuration for which the PAW potential was generated. Although, a shortcoming of the PAW approach implemented in VASP, this approach nevertheless has been shown to hold very well for deep core states mostly due to the weak coupling between the core state and the valence states.

## Theoretical background

### Nomenclature

The X-ray absorption spectra are divided into two regions. The part of the spectrum starting from the absorption threshold and up to around 50 eV above the edge is called the X-ray absorption near-edge structure (XANES) or near-edge X-ray absorption fine structure (NEXAFS), which is the range VASP is designed to reproduce accurately. The part of the spectrum beyond this range is called the extended X-ray absorption fine structure (EXAFS), there the spectrum is dominated by the multiple-scattering effects and can be very challenging to converge with the number of empty states in VASP.

The edges of the absorption spectra are named by the corresponding core state, i.e., *K*-edge for the excitations from the state with $n=1$, *L*-edge for $n=2$, and *M*-edge for $n=3$. The spin-orbit interaction causes the splitting of the core states. For example, the *2p* core states due to the spin-orbit coupling are splitting into *2p*(*j=1/2*) and *2p*(*j=3/2*) states which show in XAS as the *L2*- and *L3*-edges, correspondingly.

> **Mind:** Currently the spin-orbit coupling is only supported in the valence and conduction states but not in the core states. Hence, the splitting of an absorption edge with the orbital quantum number L>0 is not captured. For example, the splitting to *L2* and *L3*-edges is not captured in the calculations and instead, a single *L*-edge is shown.

### Supercell core-hole (SCH)

The SCH approach is explained in detail on the following theory page. When the core hole is explicitly introduced in one of the atoms, i.e., a core electron is removed, it is necessary to eliminate the effective interaction of the core hole with its image across the periodic boundary. That requires using a large supercell so that this interaction is negligible.

After the self-consistent electronic minimization is converged in the presence of the core hole, the dielectric function is calculated using Fermi's golden rule

:   :   $$\varepsilon\_{\alpha \alpha}^{(2)}(\omega)= \frac{4 \pi^2 e^2 \hbar^2}{\Omega \omega^2 m\_e^2} \sum\_{\text{core}, c, \mathbf{k}} 2 w\_{\mathbf{k}} |\left\langle\psi\_{c \mathbf{k}}\right| i \nabla\_\alpha-\mathbf{k}\_\alpha\left|\psi\_{\text{core}}\right\rangle|^2\delta\left(\varepsilon\_{c \mathbf{k}}-\varepsilon\_{\text{core}}-\omega\right)$$

In the **initial state** approximation, the electronic minimization in the presence of the core hole is not carried out, thus the electron-hole interaction is completely neglected.

* Learn how to calculate the XAS via a supercell core-hole calculation

### Bethe-Salpeter equation

Within the BSE approach, the interaction between the core hole and the excited electron is explicitly included in the polarizability as explained in the theory page. The BSE is solved in the transition space as an eigenvalue problem, whose eigenvalues $\varepsilon^\lambda$ are the transitions including the excitonic effects and the eigenvectors $A^\lambda$ are the excitonic states in the transition space.
The BSE dielectric function is found via

:   :   $$\varepsilon\_{\alpha \alpha}^{(2)}(\omega)= \frac{4 \pi^2 e^2 \hbar^2}{\Omega \omega^2 m\_e^2} \sum\_\lambda\left|\sum\_{\text{core},c, \mathbf{k}} 2A\_{\text{core}, c \mathbf{k}}^\lambda \left\langle\psi\_{c \mathbf{k}}\right| i \nabla\_\alpha-\mathbf{k}\_\alpha\left|\psi\_{\text{core}}\right\rangle \right|^2 \delta\left(\varepsilon^\lambda-\omega\right)$$

The BSE calculation based on the $GW$ calculation quasiparticles is considered to be the state of the art for XAS and is overall more reliable and accurate than the SCH methods.

* Learn how to calculate the XAS via BSE.

### Comparing BSE and SCH

The scaling of the BSE+GW approach is $N^4-N^5$ with the system size, which makes it very expensive computationally for large cells. The SCH approach on the other hand scales as $N^3$ with the system size which makes it much cheaper for complex systems with large cells. Nevertheless, the BSE+GW approach can be less computationally expensive for small cells and provides a better insight into the physics of the excitons. Furthermore, some results indicate that the valence state excitations have to be included in the XAS calculations as well to reproduce the experimental results, which is only possible within the BSE formalism . SCH has been shown to provide overall an accurate approximation for the deep core excitations , but it can be less accurate for some systems, where the BSE+GW calculations are required to accurately reproduce the experimental spectra .

> **Mind:** By default the Lorentzian broadening is applied in the XAS BSE dielectric function. In SCH the default broadening function is Gaussian.

## Tutorials

Coming soon ...

## References
