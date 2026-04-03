# Category:Phonons

Categories: VASP, Linear response

Phonons are the collective excitation of nuclei in an extended periodic system.

Here we will present a short summary with the complete derivation presented on the theory page.
Let us start by making the Taylor expansion of the total energy $E$ in terms of the ionic displacement
$u\_{I\alpha} = R\_{I\alpha} - R^0\_{I\alpha}$
around the equilibrium positions of the nuclei $R^0\_{I\alpha}$

:   $$E(\{\mathbf{R}\})=
    E(\{\mathbf{R}^0\})+
    \sum\_{I\alpha} -F\_{I\alpha} (\{\mathbf{R}^0\}) u\_{I\alpha}+
    \sum\_{I\alpha J\beta} \Phi\_{I\alpha J\beta} (\{\mathbf{R}^0\}) u\_{I\alpha} u\_{J\beta} +
    \mathcal{O}(\mathbf{R}^3)$$

with $F\_{I\alpha}$ being the atomic forces and
$\Phi\_{I\alpha J\beta}$ the interatomic force constants (IFC).

If the structure is in equilibrium (i.e. the forces are zero) then we can find the normal modes of vibration of the system
by solving the eigenvalue problem

:   $$\sum\_{J\beta} \frac{1}{\sqrt{M\_I M\_J}} \Phi\_{I\alpha J\beta} e^{i\mathbf{q} \cdot (\mathbf{R}\_J-\mathbf{R}\_I)} (\mathbf{q})
    \varepsilon\_{J\beta,\nu}(\mathbf{q}) =
    \omega\_\nu(\mathbf{q})^2 \varepsilon\_{I\alpha,\nu}(\mathbf{q})$$

where the normal modes $\varepsilon\_{I\alpha,\nu}(\mathbf{q})$
and corresponding frequencies $\omega\_\nu(\mathbf{q})^2$ are the phonons in the adiabatic harmonic approximation.

The computation of the IFCs using the supercell approach can be done using finite-differences or  density functional perturbation theory.

It is possible to obtain the phonon dispersion at different **q** points by computing the IFCs on a sufficiently large supercell and Fourier interpolating the dynamical matrices in the unit cell.

## Electron-phonon interaction

The movement of the nuclei leads to changes in the electronic degrees of freedom with this
coupling between the electronic and phononic systems commonly referred to as  electron-phonon interactions.
These interactions can be captured by  perturbative methods or  Monte-Carlo sampling to populate a supercell with phonons and monitor how the electronic band-structure changes.

## How to

* Phonons from finite differences
* Phonons from density-functional-perturbation theory
* Computing the phonon dispersion and DOS
* Electron-phonon interactions from Monte-Carlo sampling

## Tutorials

* Tutorial for lattice parameter, phonon dispersion and DOS, and long-range dipole-dipole interaction calculations.
* Lecture on phonons.
