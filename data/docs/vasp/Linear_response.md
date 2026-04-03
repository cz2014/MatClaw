# Category:Linear response

Categories: VASP

Apart from ground-state properties, VASP can compute how a system reacts to external perturbations.
Currently, we can consider three types of perturbations:

1. external electric field
2. atomic displacements
3. homogeneous strains

If we restrict ourselves to the first order of the perturbation then we are in the linear regime and thus we talk about linear response.
A central quantity in linear response is the dielectric function which relates an external electric field with the internal electric displacement.
The response to atomic displacements includes phonons and electron-phonon interactions.
The response to homogeneous strains is used to compute the elastic tensor and piezoelectric tensor when combined with a response to an external electric field.

## Polarization, berry phases, and finite electric fields

The polarization in a periodic system can be computed using the  berry phase formulation of the polarization (often referred to as the modern theory of polarization). With a method to compute the polarization, we can apply a  finite electric field to the system.
Strictly speaking, polarization, as well as the application of a finite electric field, are ground-state properties, however, because they can be used to compute the static dielectric tensor, born effective charges, and piezoelectric tensors which are response properties, we refer to this approach here.

## Static response

We consider separately static and dynamic responses for perturbations that are constant or change over time.
The different static responses can be understood as derivatives of the total energy with respect to the different external perturbations.

### Dielectric tensor

The static dielectric tensor can be computed by finite differences LCALCEPS of the polarization with respect to a finite external electric field or by using density functional perturbation theory LEPSILON.
Both LEPSILON or LCALCEPS yield the same converged results for the dielectric tensor, however, the former can only be used for local or semi-local exchange-correlation functionals and applies to both semiconductors and metals while the second can be used for METAGGA or hybrid but only for systems with a gap.

### Born effective charges

There are two approaches to compute Born effective charges implemented in VASP:
one is done by applying  finite electric fields along the three cartesian directions and computing the forces on the atoms which are activated using LCALCEPS or by computing the derivating of the wavefunction with respect to an electric field using density functional perturbation theory (DFPT) using LEPSILON.

### Piezolectric tensor

The piezoelectric tensor can be computed by finite differences with respect to a finite electric field using LCALCEPS or
by using DFPT with LEPSILON in combination with `IBRION = 5,6 or 7,8`.

### Elastic tensor

The elastic tensor is computed using strain finite differences using `IBRION = 5,6` in combination with `ISIF = 3`. It is not possible to compute it using `IBRION = 7,8` because the strain perturbation is not implemented in DFPT.

### Internal strain tensor

The internal strain tensor can be computed using finite differences using `IBRION = 5,6` or DFPT using `IBRION = 7,8`.

## Dynamic response

There are different approaches and levels of theory implemented in VASP to compute the frequency-dependent dielectric tensor. The simplest of these is done using the Green-kubo formula and is activated using LOPTICS. This however neglects local-field effects which means that it only reproduces calculations from DFPT or finite differences of a finite electric field when `LRPA = .TRUE.` when the frequency is zero (static limit). To include local field effects one should use `ALGO = CHI`. Additionally one can include electron-hole interaction when computing the dielectric function using the Bethe-Salpeter equation in the many-body perturbation theory framework using `ALGO = BSE`.

## X-ray absorption spectroscopy (XAS)

Another case of interest is the absorption of electromagnetic radiation by core electrons as measured experimentally in  X-ray absorption spectroscopy (XAS). The absorption spectra can be found from the imaginary part of the frequency-dependent dielectric function. Two methods for calculating XAS are available in VASP: the supercell core-hole (SCH) method and the Bethe-Salpeter equation (BSE). Both methods are capable of including the excitonic effects in the spectra. In SCH these effects are included at the DFT level, while the BSE approach relies on the many-body perturbation theory. A comparison of the two approaches is given in the XAS category page.

## Nuclear magnetic resonance (NMR)

Nuclear magnetic resonance is a widely used spectroscopy technique used to probe the structure and chemical composition of molecules and solids.
VASP can compute chemical shifts which is the ratio between the external and induced magnetic field compared to a reference compound, hyperfine tensors and electric field gradients.

## How to

* XAS from the supercell core-hole method
* XAS from the Bethe-Salpeter equation

## Tutorials

* Tutorial for static and frequency-dependent response calculations.
* Tutorial for phonon calculations.
* Lecture on linear response.
