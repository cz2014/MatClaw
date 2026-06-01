# Bethe-Salpeter-equations calculations

Categories: Many-body perturbation theory, Bethe-Salpeter equations, Howto

VASP offers a powerful module for solving the Bethe-Salpeter (BSE) equation. The BSE can be used for obtaining the frequency-dependent dielectric function with the excitonic effects and can be based on the ground-state electronic structure in the DFT, hybrid-functional or *GW* approximations.

## Solving Bethe-Salpeter equation

To take into account the excitonic effects or the electron-hole interaction, one has to use approximations beyond the independent-particle (IP) and the random-phase approximations (RPA). In VASP, it is done via the algorithm selected by ALGO = BSE. These essentially solves the same equations (Casida/Bethe-Salpeter) but differ in the way the screening of the Coulomb potential is treated. The TDHF approach uses the exact-correlation kernel $f\_{\rm xc}$, whereas BSE requires the $W(\omega \to 0)$ from a preceding *GW*  calculation. Thus, in order to perform TDHF or BSE calculations, one has to provide the ground-state orbitals (WAVECAR) and the derivatives of the orbitals with respect to $k$ (WAVEDER). In addition, the BSE calculation requires files storing the screened Coulomb kernel produced in a *GW* calculation, i.e., Wxxxx.tmp.

In summary, both TDHF and BSE approaches require a preceding ground-state calculation, however, the TDHF does not need the preceding *GW* and can be performed with the DFT or hybrid-functional orbitals and energies.

## Bethe-Salpeter equation calculation

The BSE calculations require a preceding *GW* step to determine the screened Coulomb kernel $W\_{GG'}(q,\omega \to 0 )$. The details on *GW* calculations can be found in the practical guide to *GW*  calculations. Here, we note that during the *GW* calculation, VASP writes this kernel into the following files

```
W0001.tmp, W0002.tmp, ..., W{NKPTS}.tmp
```

and

```
WFULL0001.tmp, WFULL0002.tmp, ..., WFULL{NKPTS}.tmp.
```

The files Wxxxx.tmp store only the diagonal terms of the kernel and are fairly small, whereas the files WFULLxxxx.tmp store the full matrix. It is important to make sure in the *GW* step that the flag LWAVE = .TRUE. is set, so that the WAVECAR stores the one-electron *GW* energies and the one-electron orbitals, if the *GW* calculation is self-consistent. In the low-scaling *GW* algorithm use the NOMEGA\_DUMP tag to produce the WFULLxxxx.tmp files.

For the self-consistent *GW* calculations the following flags should be added

```
LOPTICS   = .TRUE. 
LPEAD     = .TRUE.
```

in order to update the WAVEDER using finite differences (LPEAD = .TRUE.). The type of *GW* calculation is selected with the ALGO tag, which is discussed in great detail in the practical guide to *GW* calculations.

Once the *GW* step is completed, the BSE calculation can be performed using the following setup

```
SYSTEM    = Si
NBANDS    = same as in GW calculation
ISMEAR    = 0
SIGMA     = 0.05
ALGO      = BSE
NBANDSO   = 4       ! determines how many occupied bands are used
NBANDSV   = 8       ! determines how many unoccupied (virtual) bands are used
OMEGAMAX  = desired_maximum_excitation_energy
```

Considering that quasiparticle energies in *GW* converge very slowly with the number of unoccupied bands and require large NBANDS, the number of bands included in the BSE calculation should be restricted explicitly by setting the occupied and unoccupied bands (NBANDSO and NBANDSV) included in the BSE Hamiltonian.

VASP tries to use sensible defaults, but it is highly recommended to check the OUTCAR file and make sure that the right bands are included. The tag OMEGAMAX specifies the maximum excitation energy of included electron-hole pairs and the pairs with the one-electron energy difference beyond this limit are not included in the BSE Hamiltonian. Hint: The convergence with respect to NBANDSV and OMEGAMAX should be thoroughly checked as the real part of the dielectric function, as well as the correlation energy, is usually very sensitive to these values, whereas the imaginary part of the dielectric function converges quickly.

At the beginning of the BSE calculation, VASP will try to read the WFULLxxxx.tmp files and if these files are not found, VASP will read the Wxxxx.tmp files. For small isotropic bulk systems, the diagonal approximation of the dielectric screening may be sufficient and yields results very similar to the calculation with the full dielectric tensor WFULLxxxx.tmp. Nevertheless, for molecules and atoms as well as surfaces, the full-screened Coulomb kernel is strictly required.

Both TDHF and BSE approaches write the calculated frequency-dependent dielectric function as well as the excitonic energies in the vasprun.xml file.

## Model BSE (mBSE)

BSE calculations can be performed using a model dielectric function. In this approach the calculation of the screened Coulomb potential is not required. Instead, the model dielectric function can be used to describe the screening of the Coulomb potential by setting the tag LMODELHF with parameters AEXX and HFSCREEN.

Model BSE calculation can be performed the following steps:

1. ground-state calculation
2. GW calculation (optional in model BSE calculation)
3. optical absorption calculation via model BSE

For example, an optical absorption calculation of bulk Si can be performed using a model dielectric function as described in Ref. .

```
SYSTEM    = Si
ISMEAR    = 0 
SIGMA     = 0.05
NBANDS    = 16      ! or any larger desired value
ALGO      = D       ! Damped algorithm often required for HF type calculations, ALGO = Normal might work as well
LHFCALC   = .TRUE. 
LMODELHF  = .TRUE. 
AEXX      = 0.083
HFSCREEN  = 1.22
LOPTICS   = .TRUE.  ! can also be done in an additional intermediate step
```

In the second step, the dielectric function is evaluated by solving the Casida equation

```
SYSTEM    = Si
ISMEAR    = 0 
SIGMA     = 0.05
NBANDS    = 16     
ALGO      = TDHF
IBSE      = 0
NBANDSO   = 4       ! number of occupied bands
NBANDSV   = 8       ! number of unoccupied bands
LHARTREE  = .TRUE.
LADDER    = .TRUE.
LFXC      = .FALSE. ! local xc kernel is disabled in mBSE 
LMODELHF  = .TRUE. 
AEXX      = 0.083
HFSCREEN  = 1.22
```

## Calculations beyond Tamm-Dancoff approximation

The TDHF and BSE calculations beyond the Tamm-Dancoff approximation (TDA) can be performed by setting the ANTIRES = 2 in the INCAR file

```
SYSTEM       = Si
NBANDS       = same as in GW calculation
ISMEAR       = 0
SIGMA        = 0.05
ALGO         = BSE  
ANTIRES      = 2      ! beyond Tamm-Dancoff
LORBITALREAL = .TRUE. 
NBANDSO      = 4 
NBANDSV      = 8
```

The flag LORBITALREAL = .TRUE. forces VASP to make the orbitals $\phi({\bf r})$ real valued at the Gamma point as well as k-points at the edges of the Brillouin zone. This can improve the performance of BSE/TDHF calculations but it should be used consistently with the ground-state calculation.

## Calculations at finite wavevectors

VASP can also calculate the dielectric function at a ${\bf q}$-vector compatible with the k-point grid (finite-momentum excitons).

```
SYSTEM       = Si
NBANDS       = same as in GW calculation
ISMEAR       = 0 
SIGMA        = 0.05
ALGO         = BSE  
ANTIRES      = 2 
KPOINT_BSE   = 3 -1 0 0  ! q-point index,  three integers
LORBITALREAL = .TRUE.
NBANDSO      = 4 
NBANDSV      = 8
```

The tag KPOINT\_BSE sets the ${\bf q}$-point and the shift at which the dielectric function is calculated. The first integer specifies the index of the ${\bf q}$-point and the other three values shift the provided ${\bf q}$-point by an arbitrary reciprocal vector $\bf G$. The reciprocal lattice vector is supplied by three integer values $n\_i$ with ${\bf G}= n\_1 {\bf G}\_1+n\_2 {\bf G}\_2+n\_3 {\bf G}\_3$. This feature is only supported as of VASP 6 (in VASP 5 the feature can be enabled, but the results are erroneous).

> **Mind:** In the limit of infinitesimal momentum $\bf q$, $\varepsilon\_{\alpha\beta}(q \to 0)$ is a $3\times 3$ tensor, where $\alpha=\{x,y,z\}$ and $\beta=\{x,y,z\}$. However, at a finite momentum $\varepsilon(\bf q \neq 0)$ is a scalar, i.e., has a single component.

## Consistency tests

In order to verify the results obtained in the BSE calculation, one can perform a number of consistency tests.

### First test: IP dielectric function

The BSE code can be used to reproduce the independent particle spectrum if the RPA and the ladder diagrams are switched off

```
LADDER   = .FALSE. 
LHARTREE = .FALSE.
```

This should yield exactly the same dielectric function as the preceding calculation with LOPTICS = .TRUE. We recommend to set the complex shift manually in the BSE as well as the preceding optics calculations, e.g. CSHIFT = 0.4. The dielectric functions produced in these calculations should be identical.

### Second test: RPA dielectric function

The RPA/*GW* dielectric function can be used to verify the correctness of the RPA dielectric function calculated via the BSE algorithm. The RPA dielectric function in the BSE code can be calculated by switching off the ladder diagrams while keeping the RPA terms, i.e., the BSE calculation should be performed with the following tags

```
ANTIRES   = 2
LHARTREE  = .TRUE.
LADDER    = .FALSE.
CSHIFT    = 0.4
```

The same dielectric function should be obtained via the *GW* code by setting these flags

```
ALGO      = CHI 
NOMEGA    = 200
CSHIFT    = 0.4
```

Make sure that a large CSHIFT is selected as the *GW* code calculates the polarizability at very few frequency points. Note that the *GW* code does not use the TDA, so ANTIRES = 2 is required for the TDHF/BSE calculation. In our experience, the agreement can be made practically perfect provided sufficient frequency points are used and all available occupied and virtual orbitals are included in the BSE step.

### Third test: RPA correlation energy

The BSE code can be used to calculate the correlation energy via the plasmon equation. This correlation energy can be compared with the RPA contributions to the correlation energies for each ${\bf q}$-point, which can be found in the OUTCAR file of the ACFDT/RPA calculation performed with ALGO = RPA:

```
q-point correlation energy      -0.232563      0.000000
q-point correlation energy      -0.571667      0.000000
q-point correlation energy      -0.176976      0.000000
```

For instance, if the BSE calculation is performed at the second ${\bf q}$-point

```
ANTIRES    = 2
LADDER     = .FALSE.
LHARTREE   = .TRUE.
KPOINT_BSE = 2 0 0 0
```

the same correlation energy should be found in the corresponding OUTCAR file:

```
plasmon correlation energy        -0.5716670828
```

For exact compatibility, ENCUT and ENCUTGW should be set to the same values in all calculations, while the head and wings of the dielectric matrix should not be included in the ACFDT/RPA calculations, i.e., remove the WAVEDER file prior to the ACFDT/RPA calculation. In the BSE/RPA calculation removing the WAVEDER file is not required. Furthermore, NBANDS in the ACFDT/RPA calculation must be identical to the number of included bands NBANDSO plus NBANDSV in the BSE/RPA, so that the same number of excitation pairs are included in both calculations. Also, the OMEGAMAX tag in the BSE calculation should not be set.

## Common issues

If the dielectric matrix contains only zeros in the vasprun.xml file, the WAVEDER file was not read or is incompatible to the WAVEDER file. This requires a recalculation of the WAVEDER file. This can be achieved even after *GW* calculations using the following intermediate step:

```
ALGO      = Nothing
LOPTICS   = .TRUE.
LPEAD     = .TRUE.
```

The flag LPEAD = .TRUE. is strictly required and enforces a "numerical" differentiation of the orbitals with respect to $k$. Calculating the derivatives of the orbitals with respect to $k$ analytically is not possible at this point, since the Hamiltonian that was used to determine the orbitals is unknown to VASP.

## Related tags and articles

ALGO,
LOPTICS,
LPEAD,
LHFCALC,
LRPA,
LADDER,
LHARTREE,
NBANDSV,
NBANDSO,
OMEGAMAX,
LFXC,
ANTIRES,
NBSEEIG,
BSEFATBAND

## References

---
