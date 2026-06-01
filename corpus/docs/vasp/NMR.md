# Category:NMR

Categories: Linear response, Magnetism

**Nuclear magnetic resonance** (NMR) spectroscopy is a highly sensitive technique for probing the atomic-scale structure of molecules, liquids, and solids. However, directly extracting structural information from NMR spectra is often challenging. Consequently, *ab-initio* quantum mechanical simulations, such as those performed using VASP, play a crucial role in accurately linking NMR spectra to atomic-scale structural properties.

This page presents an overview of nuclear-electron interactions that can be computed and are relevant to interpret NMR spectra.

## Chemical shielding

The external magnetic field **B***ext* (purple) induces currents in the electrons in atoms. These NMR response currents (black arrows) in turn induce an opposing magnetic field **B***in* (red), reducing the magnetic field at the position of the nucleus, effectively shielding the nucleus from **B***ext*.

The effective B-field felt by a nucleus with finite nuclear spin is related to the applied B field via the chemical shielding tensor. The applied B-field induces a para- and diamagnetic NMR response current in the electrons and screens the nucleus with an induced B-field that follows from the Biot-Savart law, c.f. figure. The chemical shift is the difference in chemical shielding σ relative to a reference σref.

:   $$\delta\_{ij} = \sigma\_{ij}^{\mathrm{ref}} - \sigma\_{ij}.$$

VASP can efficiently compute electronic properties in bulk systems thanks to the projector-augmented wave (PAW) method which takes advantage of pseudopotentials and a frozen core approximation. However, the standard PAW transformation does not fully account for how the gauge field $A$ interacts with the reconstructed wavefunctions in the augmentation regions (near atomic cores). Thus, NMR calculations (`LCHIMAG = True`) are based on an extended version of the PAW method, the gauge-invariant PAW (GIPAW) method that properly ensures the gauge invariance. The NMR currents (WRT\_NMRCUR) are computed using linear response theory.

* Learn how to calculate the chemical shielding.

### Nuclear-independent chemical shielding

Nuclear-independent chemical shielding (NICS) is a computational method used to quantify aromaticity in molecules by calculating the magnetic shielding at a virtual point (not at a nucleus) in space, typically at the center of a ring or above it . See NUCIND for more information.

## Magnetic susceptibility

The macroscopic magnetic susceptibility $\chi$ is defined by

:   $$\textbf{B}\_{\textrm{in}}^{(1)}(\textbf{G}=0) = \frac{8 \pi}{3} \chi \textbf{B}\_{ext},$$

where $\textbf{B}\_{ext}$ is the external magnetic field and $\textbf{B}\_{\textrm{in}}^{(1)}$ is the induced magnetic field. This must be taken into account for the chemical shielding as a G=0 contribution.

It is calculated within linear response theory (`LCHIMAG = True`), where a key variable *Qij* is approximated in two ways. The so-called *pGv* approximation is used by default , where *p* is momentum, *v* is velocity, and *G* is a Green's function. An alternative approach, the *vGv* approximation is available to calculate the susceptibility . See LVGVCALC and LVGVAPPL to control the approximation.

* Learn how to perform a magnetic susceptibility calculation.

## Quadrupolar nuclei - electric field gradient

The quadrupolar electric field of a nitrogen nucleus coupling to electric field gradient *V* in MAPbI3 (methyl ammonium lead (III) iodide)

Nuclei with **I** > ± ½ have a non-zero electric field gradient (EFG) and an electronic quadrupolar moment. The electric quadrupolar moment couples with the EFG and so the chemical environment of the nucleus may be probed using nuclear quadrupole resonance (NQR) (sometimes called zero-field NMR spectroscopy). The EFG is the second derivative of the potential $V$:

:   $V\_{ij} = \frac{\partial^2 V}{\partial x\_i \partial x\_j}$,

which is a sum of three parts along the Cartesian *i*,*j* axes:

:   $$V\_{i,j} = \tilde{V}\_{i,j} -\tilde{V}\_{i,j}^1 + V\_{i,j}^1$$

where $\tilde{V}\_{i,j}$ is the plane-wave part of the AE potential, $\tilde{V}\_{i,j}^1$ is the one-center expansion of the pseudopotential method, and $V\_{i,j}^1$ is the one-center expansion of the AE potential.

In VASP, the EFG is calculated using the LEFG tag. The commonly reported nuclear quadrupolar coupling constant *Cq* is then printed using isotope-specific quadrupole moment defined using QUAD\_EFG .

* Learn how to perform an electric field gradient calculation.

## Hyperfine coupling

Hyperfine coupling between the nuclear spin and the electronic spin of the unpaired electron at a nitrogen-vacancy (NV) center in diamond.

The hyperfine tensor $A^I$ describes the interaction between a nuclear spin $S^I$ and the electronic spin distribution $S^e$. In most cases associated with a paramagnetic defect state measureable by electron paramagnetic resonance (EPR) :

:   $$E=\sum\_{ij} S^e\_i A^I\_{ij} S^I\_j.$$

The hyperfine tensor is split into two terms, isotropic (or Fermi contact) $A^I\_{iso}$ and anisotropic (or dipolar contributions) $A^I\_{ani}$:

:   $$A^I\_{i,j} = (A^I\_{iso})\_{i,j} + (A^I\_{ani})\_{i,j}.$$

$A^I\_{iso}$ is calculated based on the spin-density and $A^I\_{ani}$ is calculated based on the dipolar-dipolar contribution terms $W\_{i,j}(\textbf{R})$. The hyperfine tensor calculation itself is defined using `LHYPERFINE = True`. Both the Fermi contact and dipolar contribution terms are related to the nuclear gyromagnetic moment γ, which are controlled by setting NGYROMAG.

* Learn how to perform a hyperfine coupling calculation.

## Tutorials

Coming soon ...

* Lecture on PAW, GIPAW, and NMR theory.
* Lecture on NMR theory and calculations.

## References
