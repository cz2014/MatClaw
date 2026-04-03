# Time-evolution algorithm

Categories: Many-body perturbation theory, Linear response, Bethe-Salpeter equations, Howto

The macroscopic dielectric function, $\epsilon\_{ij}(\omega)$, measures how a given dielectric medium reacts when subject to an external electric field. From $\epsilon\_{ij}(\omega)$ it is possible to extract several optical properties such as absorption, optical conductivity, and reflectance. However, it is important that the interacting electrons and holes are taken into account. This makes the evaluation of the macroscopic dielectric function more involved, since it goes beyond the single-particle level, working at the two-particle level via either the Bethe-Salpeter equation (BSE) or time-dependent density-functional theory (TDDFT).

For both frameworks, BSE and TDDFT, users can select two different strategies to compute $\epsilon\_{ij}(\omega)$. The first is based on the eigendecomposition of the electron-hole hamiltonian, $H^\mathrm{exc}$. It allows for the evaluation of $\epsilon\_{ij}(\omega)$ by initially obtaining the eigenvalues and eigenvectors of $H^\mathrm{exc}$ and then using both to evaluate $\epsilon\_{ij}(\omega)$. This strategy is based on the Bethe-Salpeter equation or the Casida equation. The second strategy transforms the mathematical expression of $\epsilon\_{ij}(\omega)$ into a time-dependent integral. By propagating the dipolar moments in time and then applying a Fourier transform, VASP can compute $\epsilon\_{ij}(\omega)$.

The advantage of the later method in relation to the former is related to their cost. The time-dependent integral has a cost of the order $O(N^2)$, while the eigendecomposition has a cost of the order $O(N^3)$, where $N$ is the rank of $H^\mathrm{exc}$. This means that for very large numbers of bands or k-points, the time-dependent formalism is cheaper than the eigendecomposition method.

Below is a brief description of the method, from its theoretical support to how calculations should be performed, with the relevant approximations needed in the two-particle Hamiltonian.

> **Warning:** In VASP < 6.5.2 the dielectric function is not calculated correctly with ALGO=TIMEEV if ISYM>0.

## The macroscopic-dielectric function as a time-dependent integral

The starting point is that one can re-write $\epsilon\_{ij}(\omega)$ as a time-dependent integral. It starts from its expression, given by

:   :   $\epsilon^M(\omega)=1+\frac{4 \pi}{\Omega\_0} \sum\_\lambda\left|\sum\_{c v \mathbf{k}} \mu\_{c v \mathbf{k}} A\_{c v \mathbf{k}}^\lambda\right|^2\left[\frac{1}{\omega+E\_\lambda+\mathrm{i} \eta}-\frac{1}{\omega-E\_\lambda+\mathrm{i} \eta}\right]$,

where $\mu\_{v c \mathbf{k}}^j=\frac{\left\langle c \mathbf{k}\left|v\_j\right| v \mathbf{k}\right\rangle}{\varepsilon\_c(\mathbf{k})-\varepsilon\_v(\mathbf{k})}$ is the dipolar moment associated to the the conduction $c$, valence band $v$, and k-point $k$. $\lambda$ is the index of the eigenstate of $H^\mathrm{exc}$, with $A^\lambda$ and $E\_\lambda$ being the associated eigenvector and eigenvalue.

This definition of $\epsilon\_{ij}(\omega)$ can be brought into operational form

:   :   $$\epsilon^M(\omega)=1+\frac{4 \pi}{\Omega\_0}\left\langle\mu\left|\left[\frac{1}{\omega+\mathrm{i} \eta+\hat{H}^{\mathrm{exc}}}-\frac{1}{\omega+\mathrm{i} \eta-\hat{H}^{\mathrm{exc}}}\right]\right| \mu\right\rangle$$

by using the spectral decomposition $\left[\hat{H}^{\mathrm{exc}}-\omega\right]^{-1}=\sum\_\lambda \frac{\left|A\_\lambda\right\rangle\left\langle A\_\lambda\right|}{E\_\lambda-\omega}$. The new expression of $\epsilon(\omega)$ is related to a time-dependent integral, using the fact that

:   :   $\frac{1}{\omega+\mathrm{i} \eta-\hat{H}^{\mathrm{exc}}}|\mu\rangle=-\mathrm{i} \int\_0^{\infty} e^{-\mathrm{i}\left(\omega-\hat{H}^{\mathrm{exc}}+\mathrm{i} \eta\right) t}|\mu\rangle=-\mathrm{i} \int\_0^{\infty} e^{-\mathrm{i}(\omega+\mathrm{i} \eta) t} e^{\mathrm{i} \hat{H}^{\mathrm{exc}}t}|\mu\rangle$,

and recognizing that $e^{\mathrm{i} \hat{H}^{\mathrm{exc}}t}|\mu\rangle = |\xi(t)\rangle$ is the exponential form of a time-dependent equation operator. These considerations allow for the expression of $\epsilon\_{ij}(\omega)$ to be written as

:   :   $\epsilon\_{ij}(\omega)=\delta\_{ij}-\frac{4\pi e^2}{\Omega}\int\_0^{\infty} \mathrm{d} t
        \sum\_{c,v,\mathbf{k}}\left(\langle\mu^j\_{cv\mathbf{k}}| \xi^i\_{cv\mathbf{k}}(t)\rangle+ \mathrm{c.c.}\right) e^{-\mathrm i(\omega-\mathrm i \eta) t}$.

The fundamental aspect behind this transformation is that the new, time-dependent vector $\left.\mid \xi^j(t)\right\rangle$ follows the equation

:   :   $$\mathrm i \frac{\mathrm d}{\mathrm d t}\left|\xi^j(t)\right\rangle=\hat{H}^\mathrm{exc}(t)\left|\xi^j(t)\right\rangle,$$

with the initial vector given by $\left|\xi^j(0)\right\rangle=\left|\mu^j\right\rangle$.

To compute the dielectric function with this method, VASP evaluates and stores at each time step the projections of $\left.\mid \xi^j(t)\right\rangle$ over $\left.\mid \mu^i\right\rangle$, $c^{ij}\_{cv\mathbf k}(t) = \langle \mu^i\_{cv\mathbf k}|\xi^i\_{cv\mathbf k}(t)\rangle$. It is the fact that all these operations are of the matrix-vector type that makes this method having a cost of the order of $O(N^2)$.

## Perturbing all transitions with a delta-like potential

In order to probe all possible $v\to c$ transitions, a time-dependent term is added to the hamiltonian

:   :   $$V\_\mathrm{ext}(\mathbf r, t) = \lambda \mathbf r\cdot \mathbf D\delta(t),$$

where $\lambda$ is the perturbation strength parameter and $\mathbf D$ is the electric displacement field. The narrow (in time) potential allows all bands in the occupied and unoccupied manifolds to be included in the transition space. The constant displacement field replicates the long wavelength limit (i.e. $\mathbf q \to 0$).

## The many-body terms in the hamiltonian

Approximations to the interaction between electrons and holes are controlled in the INCAR by the tags LHARTREE, LADDER, and LFXC, which can be set to either .TRUE. or .FALSE.. Below we provide an explanation of what interaction term each tag controls.

> **Mind:** The default setup for VASP is LHARTREE and LADDER set to .FALSE., while LFXC is set to .TRUE.. This means that if no tags are set in the INCAR the time-propagation run will using the TDDFT kernel.

### Independent-particle approximation

In this approximation all interaction terms in the hamiltonian are turned off by setting LHARTREE, LADDER, and LFXC to .FALSE. in the INCAR file. This means that the computed spectrum will be equal the one obtained during a ground-state calculation with LOPTICS=.TRUE.. This calculation is useful to test if everything is in order with the input files and the workflow is properly setup.

### Hartree exchange potential

With the tag LHARTREE=.TRUE. the interaction terms in the hamiltonian will include the unscreened Coulomb exchange. These terms are also known as the bubble diagrams from many-body perturbation theory (MBPT). With both LFXC and LADDER set to .FALSE., this will be equivalent to running random-phase approximation (RPA) calculation.

Note that at the end, the dielectric function reported in the output files is the macroscopic dielectric function, where no contributions from local fields (i.e. terms with finite $\mathbf G$) are included.

The missing interaction between electrons and holes from either LFXC or LADDER has as consequence that bound excitons cannot be properly described, which is a known problem of RPA. However, it can still be used to compute the electron energy-loss function, EELS.

### Screened two-particle interaction

#### Exchange-correlation effects from time-dependent density functional theory

Setting LFXC=.TRUE. includes the local exchange-correlation kernel, $f\_\mathrm{xc}$ in the time-propagation

:   :   $$f\_{\mathrm{xc}}^{\text {loc }}\left(\mathbf{r}, \mathbf{r}^{\prime}\right)=\frac{\delta^2\left\{E\_{\mathrm{c}}^{\mathrm{DFT}}+\left(1-c\_{\mathrm{x}}\right) E\_{\mathrm{x}}^{\mathrm{DFT}}\right\}}{\delta \rho(\mathbf{r}) \delta \rho\left(\mathbf{r}^{\prime}\right)},$$

where $c\_X$ controls the fraction of the exchange energy functional that is included in the kernel (see AEXX). This lets users perform time-dependent calculations using hybrid functionals.

These kernels often lack the long-range component (which goes as $-1/q^2$, where $q$ is the momentum difference between the electron and the hole). When using them in periodic or extended systems it is very likely that they will fail to properly reproduce the binding energies of electron-hole pairs.

#### Ladder diagrams from many-body perturbation theory

By setting LADDER=.TRUE. the interaction hamiltonian will include the screened exchange interaction potential, $W(\mathbf r,\mathbf r';\omega)$. This treats the electron-hole interaction by including the ladder diagrams from MBPT. This term also has the correct long-range behaviour, meaning that it can properly describe bound electron-hole pairs in solids and large molecules.

At the present, the screened interaction has to be computed from a model dielectric function, given by

:   ${\varepsilon}\_{\mathbf{G},\mathbf{G}}^{-1}(\mathbf{q})=1-(1-{{\varepsilon}\_{\infty}^{-1}})\text{exp}\left(-\frac{|\mathbf{q+G}|^2}{4{\lambda}^2}\right)$.

Both LHFCALC and LMODELHF must be set to .TRUE.. Also, VASP must be provided both with HFSCREEN ($\lambda$) and AEXX (${\varepsilon}\_{\infty}^{-1}$) to control the range separation parameters in the model dielectric function.

## Step-by-step instructions on bulk Si

### Step 1: ground state with extra empty states

The starting point is a ground-state calculation which includes extra empty states, whose number is controlled in the INCAR file with the tag NBANDS. In the following example INCAR file

```
SYSTEM = Si
NBANDS = 12
ISMEAR = 0 ; SIGMA = 0.05
ALGO = N
LOPTICS = .TRUE.
KPAR = 4
```

8 empty bands are chosen (silicon has 4 occupied bands in the pseudo-potential file, thus making a total of 12 bands for NBANDS). However, with ALGO=N, VASP will employ an iterative diagonalization algorithm, meaning that the last conduction states will not be converged with the same accuracy level as the occupied states. It is possible to avoid this by setting ALGO=Exact, or by increasing the number of bands to make sure that the states which will be used in the time-propagation step are converged with the same level of accuracy.

Finally, with LOPTICS=.TRUE., VASP will compute the dipole momentum for each possible $v\to c$ transition (recall the definition of the dipole momentum vector). These are written in the file WAVEDER, which will be used in the next step.

> **Mind:** This calculation was performed on bulk Si (primitive cell), with a gamma-centred, 4x4x4 k-point grid, using the PBE standard pseudopotential.

### Step 2: time-evolution run

Once the ground state with extra empty states is computed, the resulting WAVECAR and WAVEDER files are ready to use in a time-propagation calculation. The following will be used as an example INCAR file:

```
SYSTEM = Si
ALGO = TIMEEV
!Information about the bands
NBANDS = 12
NBANDSO = 4
NBANDSV = 8
!Smearing parameters
ISMEAR = 0 ; SIGMA = 0.05
!Direction of propagation
IEPSILON = 1 
!Parallelization options
KPAR = 4
!Time-propagation parameters
NELM = 2000
CSHIFT = 0.1
OMEGAMAX = 20
!Particle interactions
LHARTREE = .TRUE.
LADDER = .TRUE.
LFXC = .FALSE.
LHFCALC = .TRUE.
LMODELHF = .TRUE.
AEXX = 0.088
HFSCREEN = 1.26
```

Here ALGO is set to TIMEEV, meaning that VASP will now perform a time-propagation calculation.

#### Setting up the bands

With NBANDS=12 informs VASP that there are 12 states in total in the WAVECAR and WAVEDER. This must be consistent with Step 1! The number of occupied and unoccupied states that are used in the propagation is controlled by the NBANDSO and NBANDSV tags, respectively. To choose which bands to use it is advisable to understand the type of property that is going to be studied. For instance, in the case of optical absorption, materials are probed within a few hundreds of milli-electronvolt of the band gap. In this case it means that only states that lie close to the band extrema are important for the time-propagation.

In this example VASP will use NBANDSO=4 occupied and NBANDSV=8 unoccupied states during the time propagation. There is no need to use the total number of bands set up by NBANDS, but still NBANDSO+NBANDSV cannot be larger than NBANDS.

#### Setting up the time-step

VASP is now integrating a time-dependent differential equation so the time-step used to propagate the dipole moments can be specified in the INCAR. By default, VASP will use 20000 steps, however a different number can be set with the tag NELM. Nevertheless, NELM must be larger than 100, otherwise VASP will revert to the default value.

The time-step, $\Delta t$, and maximum propagation time, $T\_\mathrm{max}$, are not dependent on the size of the interacting hamiltonian matrix. However they are dependent on the system in case and the input tag CSHIFT and OMEGAMAX. This comes from the Fourier transform used to integrate the time-dependent dipole moments, which leads to $T\_\mathrm{max} \approx 1/\mathrm{CSHIFT}$ and $\Delta t \approx 1/\mathrm{OMEGAMAX}$.

The tag CSHIFT also controls the width used in the plotting of the dielectric function, since

:   :   $$\frac{1}{\omega - E\_\lambda + \mathrm i \eta} = \frac{1}{\omega - E\_\lambda} - \mathrm i\pi \delta(\omega - E\_\lambda)$$

and the $\delta$-function is approximated as $\delta(\omega - E\_\lambda) = \lim\_{\eta\to 0^+}\frac{1}{\pi}\frac{\eta}{(\omega - E\_\lambda)^2+\eta^2}$, with CSHIFT=$\eta$.

Setting CSHIFT = 0.1 ~ 0.01 is often a good choice, as lower values will lead to unnecessarily long propagation times and spectra with very narrow peaks. OMEGAMAX is automatically from the maximum energy difference between occupied and unoccupied states, but can be lowered to decrease the number of pairs used in the basis set and the size of the interacting hamiltonian.

#### Choosing the direction of perturbation

The dipole momentum vector $\mu^i$ is direction dependent. The direction of propagation is chosen in the INCAR with the tag IEPSILON, which can take values of 1, 2, or 3 (corresponding to x, y, and z direction, respectively), and 4 (corresponding to all directions).

While choosing a single direction of propagation decreases the computing time, it is important to pay attention to the symmetries of the material in study. For example, in the case of bulk silicon, since the material has cubic symmetry propagating along one direction (x, or y, or z) is enough. However, for a material like monolayer hexagonal boron nitride, the crystal symmetries destroy the equivalency between the x and y directions. For this system propagation should happen along both x and y, and then the dielectric function should be the average of both calculations.

### Analysing the results

Once the calculation is finished, the dielectric function can be plotted by executing the following script

```
 #!/bin/sh
 awk 'BEGIN{i=0} /<dielectricfunction comment="time-propagation">/,\
                /<\/dielectricfunction>/ \
                 {if ($1=="<r>") {a[i]=$2 ; b[i]=($3+$4+$5)/3 ; c[i]=$4 ; d[i]=$5 ; i=i+1}} \
     END{for (j=0;j<i/2;j++) print a[j],b[j],b[j+i/2]}' vasprun.xml > optics.dat
```

which can be copied to a file (e.g. extract\_optics.sh) in the same directory where the calculation was performed and then ran with

```
$ sh extract_optics.sh
```

This creates a file called optics.dat with three data columns. The first column is the energy of excitation, in eV. The second and third columns correspond to the imaginary and real parts of $\frac{1}{3}[\epsilon\_{xx}(\omega)+\epsilon\_{yy}(\omega)+\epsilon\_{zz}(\omega)]$. For the example shown here, the obtained $\mathrm{Im}[\epsilon]$ should be similar to the following image.

Alternatively, if VASP was compiled with hdf5 support, the results can also be plotted with py4vasp

```
 import py4vasp
 #replace path_to_calculation below with the path to the directory where the corresponding vaspout.h5 is located
 calc=py4vasp.Calculation.from_path("path_to_calculation")

 calc.dielectric_function.plot("TIMEEV")
```

which will create the following figure with both the real and imaginary part of $\epsilon(\omega)$.

> **Mind:** It should be stated that this is just an example, not a converged calculation! Several numerical parameters should be checked for convergence (e.g. number of k-points, number of empty states, etc).

## Comparison to other methods

VASP offers two other methods with which you can compute the macroscopic dielectric function. These are based on eigendecomposition of the two particle hamiltonian, $H^\mathrm{exc}$. While more expensive than time-evolution, both these methods are able to compute eigenvalues and eigenstates of $H^\mathrm{exc}$, thus providing direct access to the excitation energies of a system.

### Bethe-Salpeter equation

Here the full Bethe-Salpeter equation is employed by setting ALGO=BSE. The interaction hamiltonian is built using the dielectric function from RPA, and has the right behaviour in the long range regime. This means that it can accurately describe bound excitons in solids and large molecules. However, it is more costly than time-evolution, scaling with $N\_\mathrm{rank}^3$.

### Casida equation

Similar to the Bethe-Salpeter equation, the Casida equation employs an eigensolver method to compute the dielectric function. This is chosen in the INCAR with ALGO=TDHF. The key difference is that the Casida method does not require a preceding GW run to compute the RPA screening and can be performed with either DFT or hybrid-functional orbitals and energies.

## Related tags and articles

NBANDSO, NBANDSV, IEPSILON, NELM, LHARTREE, LADDER, LFXC, LHFCALC, LMODELHF, AEXX, HFSCREEN

Time-dependent density-functional theory calculations

Bethe-Salpeter-equations calculations

## References
