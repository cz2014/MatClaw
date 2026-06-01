# Bethe-Salpeter equation for core excitations

Categories: Many-body perturbation theory, Bethe-Salpeter equations, XAS, Howto, Linear response

VASP offers two approaches for calculating the X-ray Absorption Spectra (XAS). The supercell core-hole (SCH) method and the Bethe-Salpeter equation (BSE). As discussed in detail on the theory page, within the BSE approach the electron-hole interaction or the excitonic effects are explicitly included in the dielectric function. The screening of the electron-hole interaction is described in the random phase approximation (RPA) and the Green's functions are calculated in the GW approximation. This BSE+GW approach represents the state of the art for XAS spectra calculations in solids.

> **Mind:** Available in VASP > 6.5.1.

## Solving Bethe-Salpeter equation

The BSE calculations for core excitaions, similarly to BSE in the optical region, require a preceding $GW$ calculation. In addition to the standard VASP input files, the following files are needed to perform a BSE calculation:

* WAVECAR the quasiparticle energies and orbitals produced in the preceding $GW$ calculation
* Wxxxx.tmp the RPA dielectric matrix from the preceding $GW$ calculation
* WAVEDER\* the orbital derivatives from the $GW$ step, only required if the valence states are included

The quasiparticle energies are only calculated for the valence and conduction bands set by NBANDSGW, the energies of the core states are taken from the potentials in the POTCAR file. Hence, the absolute values for the core excitations are not accurate, but the overall shape and the relative positions of the spectral feature can be captured with high precision within BSE .

The BSE calculation workflow consists of the following steps:

1. DFT calculation with a large number of empty states
2. $GW$ calculation to obtain the quasiparticles and the RPA dielectric tensor
3. BSE calculation

Below you will find an example of the INCAR file required for an XAS calculation in BSE.

```
NBANDS     = 64      ! same as in GW calculation
ISMEAR     = 0       ! Gaussian smearing
SIGMA      = 0.05    ! rather small to avoid fractional occupations
ALGO       = BSE     ! BSE algorithm
NBANDSO    = 0       ! zero valence states 
NBANDSV    = 16      ! number of empty bands
ICORELEVEL = 2       ! enables the core states calculation
CLNT       = 1       ! species of the excited atom
CLN        = 0       ! main quantum number of the excited core state
CLL        = 0       ! orbital quantum number of the excited core state
```

> **Mind:** The core states in VASP remain frozen in the configuration for which the PAW potential was generated.

The intensities of the core state excitations can be too small for a correct representation with the four decimal places used in the standard output, thus VASP provides a tag that can be used to scale the dielectric function and the oscillator strengths by a factor CH\_AMPLIFICATION.
All atoms of the selected type CLNT are excited in the BSE calculation, therefore, it is recommended to treat the excited atom as a separate species in the POSCAR file. It is possible to excite multiple atoms in BSE, but it increases the number of core states, i.e., the size of the problem, and it should be done only if the atoms are not equivalent in the atomic configuration. The valence states are usually not included in the XAS calculations, i.e., NBANDSO=0. Nevertheless, the valence states can be included in BSE via tag NBANDSO.

## Recommendations and advice

General advice for running BSE calculations can be found in this article. Specific advice for using the BSE to calculate the XAS as given below.

### BSE solvers

The default option for solving BSE is the exact diagonalization algorithm with IBSE=2, which is the most accurate but also most time-consuming method. Approximate solvers can yield accurate spectra at a fraction of the computational time. The most efficient approach is the iterative Lanczos algorithm, which can be selected with IBSE=3. The time-evolution algorithm (IBSE=1) can be used in the XAS calculations, but it is less efficient for spectra with a wide energy range as in the case of XANES. Both approximate solvers can only be used to obtain the spectra, but cannot be used to calculated the BSE eigenvectors.

### Processing the results

The calculated dielectric function and the oscillator strength information can be found in vasprun.xml and vaspout.h5.

### Core exciton wavefunction

The excitons can be visualized in VASP as described in this article. In the case of XAS, the core state is strongly localized and only the hole position can be fixed by providing the coordinate of the excited atom via the BSEHOLE tag.

### Beyond Tamm-Dancoff approximation

The default approximation for the BSE algorithm is the Tamm-Dancoff approximation (TDA), i.e., ANTIRES=0, which usually holds for XAS. Nevertheless, the full BSE equation without TDA can be solved by setting ANTIRES=2.

### Model BSE and TDDFT

The dielectric function for the core states can be calculated with the model BSE approach or the Casida TDDFT formalism by selecting the algorithm ALGO=TDHF. However, these approximations were found inaccurate for XANES .

## Comparing to the SCH

The spectra from the SCH calculation in the initial state approximation and the BSE calculation in the independent particle approximation (IP) can be directly compared and should be identical. The initial state approximation can be selected in SCH by setting ICORELEVEL=1. The independent particle approximation (IP) can be selected in BSE by disabling both the bare and screened Coulomb interaction, i.e., LADDER=.FALSE. and LHARTREE=.FALSE..

## Related tags and articles

ALGO,
LADDER,
LHARTREE,
NBANDSV,
NBANDSO,
OMEGAMAX,
ANTIRES,
NBSEEIG,
BSEHOLE,
CLNT,
CLL,
CLN,
ICORELEVEL,
BSEFATBAND

## References
