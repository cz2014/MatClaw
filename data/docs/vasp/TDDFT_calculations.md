# Time-dependent density-functional theory calculations

Categories: Time-dependent density-functional theory, Howto

VASP offers a powerful module for performing time-dependent density-functional theory (TDDFT) or time-dependent Hartree-Fock (TDHF) calculations by solving the Casida equation . This approach can be used for obtaining the frequency-dependent dielectric function with the excitonic effects and can be based on the ground-state electronic structure in the DFT, hybrid-functional or even *GW* approximations.

## Solving Casida equation

The algorithm for solving the Casida equation can be selected by setting ALGO = TDHF. This approach is very similar to BSE but differs in the way the screening of the Coulomb potential is approximated. The TDHF approach uses the exchange-correlation kernel $f\_{\rm xc}$, whereas BSE requires the $W(\omega \to 0)$ from a preceding *GW*  calculation. Thus, in order to perform a TDHF calculation, one only needs to provide the ground-state orbitals (WAVECAR) and the derivatives of the orbitals with respect to $k$ (WAVEDER).

> **Mind:** Unlike BSE, TDHF calculations do **not** require $W(\omega \to 0)$, i.e., Wxxxx.tmp

In summary, both TDHF and BSE approaches require a preceding ground-state calculation, however, the TDHF does not need the preceding *GW* and can be performed with the DFT or hybrid-functional orbitals and energies.

## Time-dependent Hartree-Fock

The TDHF calculations can be performed in two steps:

1. ground-state calculation
2. optical absorption calculation

For example, an optical absorption calculation of bulk Si can be performed using a dielectric-dependent hybrid-functional described in Refs..

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
LFXC      = .TRUE.
LMODELHF  = .TRUE. 
AEXX      = 0.083
HFSCREEN  = 1.22
```

THDF calculations can be performed for non-spin-polarized, spin-polarized, and noncollinear cases, as well as the case with spin-orbit coupling. There is, however, one caveat. The local exchange-correlation kernel is approximated by the density-density part only. This makes predictions for spin-polarized systems less accurate than for non-spin-polarized systems.

## Time-dependent DFT calculation

The TDDFT calculation using the PBE exchange-correlation kernel can be performed by disabling the ladder diagrams LADDER = .FALSE., i.e., only the PBE exchange-correlation kernel is present in the Hamiltonian.

```
SYSTEM    = Si
ISMEAR    = 0 
SIGMA     = 0.05
NBANDS    = 16     
ALGO      = TDHF
IBSE      = 0
NBANDSO   = 4       ! determines how many occupied bands are used
NBANDSV   = 8       ! determines how many unoccupied (virtual) bands are used
LFXC      = .TRUE.
LHARTREE  = .TRUE.
LADDER    = .FALSE.
```

> **Mind:** In TDDFT calculation, where the ladder diagrams are not included (LADDER=.FALSE.) or the fraction of exact exchange in the kernel is zero (AEXX=0), the resulting dielectric function lacks the excitonic effects.

VASP tries to use sensible defaults, but it is highly recommended to check the OUTCAR file and make sure that the right bands are included. The tag OMEGAMAX specifies the maximum excitation energy of included electron-hole pairs and the pairs with the one-electron energy difference beyond this limit are not included in the Hamiltonian.

The calculated frequency-dependent dielectric function, transition energies and oscillator strength values are stored in the vasprun.xml file.

## Calculations beyond Tamm-Dancoff approximation

Calculations beyond Tamm-Dancoff approximation can be performed in the same manner as in the BSE.

## Calculations at finite wavevectors

Calculations at finite wavevectors can be performed in the same manner as in the BSE.

## References

---
