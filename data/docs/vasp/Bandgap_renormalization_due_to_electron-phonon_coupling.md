# Bandgap renormalization due to electron-phonon coupling

Categories: Electron-phonon interactions, Howto

The band-structure renormalization within the nonadiabatic Allen Heine Cardona (AHC) theory is computed from the real part of the electron self-energy evaluated at the Kohn-Sham (KS) eigenvalue.
This calculation is activated by default when `ELPH_RUN = True` and `ELPH_DRIVER = EL`.
For the particular case where we want to determine the bandgap, we can compute the self-energy only for the states that form the gap (including all the degenerate states).
The selection of these states can be done automatically by VASP using `ELPH_SELFEN_GAPS = True`.

For the theory on bandgap renormalization from perturbation theory, see the many-body perturbation theory section of the theory page.

> **Mind:** Available as of VASP 6.5.0

> **Important:** This feature requires  HDF5 support.

> **Tip:** The phonon-induced renormalization of the fundamental gap can alternatively be calculated from a  stochastic approach.

## Basic usage

The first step of an electron-phonon calculation is the computation of the electron-phonon potential, which corresponds to the derivatives of the KS potential with ionic displacement.
This calculation produces the phelel\_params.hdf5 file, which is a required input for the subsequent calculation.
The electron-phonon matrix elements are computed using the KS states obtained from a non-self-consistent-field calculation on a dense k-point mesh.
This k-point mesh is specified in the KPOINTS\_ELPH file, which has the same format as the regular KPOINTS file.
Note that NBANDS governs the number of bands used in the self-consistent-field calculation, while ELPH\_NBANDS governs the number of bands that will be used in the electron-phonon calculation and are computed in the grid specified via KPOINTS\_ELPH.

The computation of the electronic bandgap renormalization can be done using the following INCAR file:

```
 PREC = Accurate
 ENCUT = 500
 EDIFF = 1e-8
 ISMEAR = 0; SIGMA = 0.01
 LREAL = .FALSE.
 LWAVE = .FALSE.
 LCHARG = .FALSE.
 
 #run electron-phonon calculation
 ELPH_RUN = .TRUE.
 ELPH_DRIVER = EL
 
 # use exact diagonalization and compute all the bands
 ELPH_NBANDS = -2
 KPOINTS_OPT_MODE = 2
 
 # compute gap renormalization
 ELPH_SELFEN_DELTA = 0.01
 ELPH_SELFEN_FAN = .TRUE.
 ELPH_SELFEN_DW = .TRUE.
 ELPH_SELFEN_GAPS = .TRUE.
```

> **Tip:** For your convenience, you can set `ELPH_MODE = renorm`, which automatically sets reasonable values for many of these electron-phonon tags to perform the band-gap renormalization. It is still possible to manually overwrite the chosen values.

To get an accurate value while using the smallest possible amount of computational resources, we recommend performing a basis set and k-point sampling convergence study.
This ensures that the result is precise, provides an error estimate and reveals the computationally most favorable settings.

The final output of the code is reported for each combination of computational parameters using the concept of  electron-phonon accumulators.

## Basis set convergence

First, we will deal with convergence of the bandgap renormalization with respect to the number of electronic states (NBANDS) and plane-waves (ENCUT). To avoid a more cumbersome double-convergence with ENCUT and ELPH\_NBANDS we recommend setting ELPH\_NBANDS to be equal to the maximum number of plane-waves. This can be done automatically by setting `ELPH_NBANDS = -2`.

The derivatives of the electron-phonon potential are contained in the phelel\_params.hdf5 file on a pre-selected grid (NGX, NGY, NGZ).
This means that we should avoid running the electron-phonon calculation with an ENCUT that would yield a set of NGX, NGY and NGZ that is different from the phelel\_params.hdf5 file.
We can, however, choose a smaller ENCUT and set NGX, NGY and NGZ manually in the INCAR file to be the same as the one in the phelel\_params.hdf5 file.
This allows running the calculation with different values of ENCUT and monitoring how that affects the final value of the bandgap renormalization.

Let us consider an example calculation where the electron-phonon potential was generated for Silicon with an `ENCUT = 500` which yields NGX=NGY=NGZ=28 in the primitive cell. The values of NGX, NGY and NGZ chosen by VASP can be monitored in the OUTCAR file.
A convergence study can be performed by running multiple calculations with ENCUT=200, then 300, then 400 and finally 500.
`NGX = 28`, `NGY = 28` and `NGZ = 28` are set explicitly in the INCAR file.
You can verify that the calculations with a lower cutoff run faster, highlighting the importance of convergence tests for reaching a good compromise between accuracy and computational time.

## K-point sampling convergence and extrapolation to infinity

Apart from the convergence with respect to the basis set, one should perform a convergence with respect to the k-point sampling.
This step implies running the calculation for increasingly dense k-point meshes specified in the KPOINTS\_ELPH file.
The convergence behavior with respect to k-points is mostly independent of the convergence behavior with respect to the plane-wave basis.
Therefore, it is recommended to study both types of convergence separately to save on time.

Furthermore, we recommend extrapolating the bandgap renormalization to infinite k-point density.
This is most easily accomplished by plotting the value of the renormalization as a function of the inverse k-point density.
In addition to the k-point convergence, the broadening parameter ELPH\_SELFEN\_DELTA should be monitored as well.
In principle, this parameter should be as small as possible.

> **Warning:** Choosing ELPH\_SELFEN\_DELTA too small might produce inaccurate results for numerical reasons.

The usual approach is to extrapolate the result to zero broadening.

> **Tip:** Multiple values can be specified for ELPH\_SELFEN\_DELTA. VASP then computes the self-energy for each of these broadenings and reports the results in the OUTCAR and vaspout.h5 files. For each value of the broadening, a new electron  self-energy accumulator is created with the corresponding settings and values reported in the OUTCAR file. This should help simplify the convergence study.

## Special treatment of the dipole interaction for polar materials

The convergence of the bandgap renormalization for polar materials (i.e. materials with a gap and non-zero born-effective charges) is especially challenging.
This is because the electron-phonon potential diverges as $q\rightarrow0$.
This divergence is due to long-range electrostatic interactions that are not screened by the electrons, as would be the case for metals.
In these cases, VASP can remove this long-range component from the electron-phonon potential in the supercell, Fourier interpolate it and add it back in the primitive cell.
The same treatment is done for the interatomic force constants.

To activate the long-range treatment, set the following INCAR tags:

```
 ENCUTLR = 50
 ELPH_LR = 1
 IFC_LR = 1
```

> **Mind:** The long-range treatment is activated by default when the phelel\_params.hdf5 file contains the dielectric tensor and born effective charges.

> **Tip:** The value of ENCUTLR should be the smallest possible for efficiency reasons, but large enough such that the final quantity does not depend on it. Avoid values of ENCUTLR that are too large, otherwise, the results might become unphysical.

## Related tags and articles

* Transport calculations
* Electron-phonon potential from supercells
* Electron-phonon accumulators
* phelel\_params.hdf5
* Electron-phonon interactions from Monte-Carlo sampling
