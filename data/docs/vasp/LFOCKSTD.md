# LFOCKSTD

Categories: INCAR tag, Many-body perturbation theory, GW, ACFDT, Low-scaling GW and RPA

LFOCKSTD = [logical]  
 Default: **LFOCKSTD** = .FALSE.

Description: LFOCKSTD applies to RPA and GW calculations. It forces VASP to evaluate the exact exchange fully consistent with the standard treatment in HF calculations.

---

> **Mind:** Avaliable as of 6.5.2.

This feature is availabe for low-scaling  ACFDT/random-phase-approximation (RPA) and GW calculations, i.e. ALGO=ACFDTR, RPAR, EVGW0R, GWR.

VASP typically employs shape restoration (see NMAXFOCKAE and LMAXFOCKAE) to calculate the RPA correlation energy and the exact exchange energy during RPA/GW calculations. However, this results in significant noise in the exact exchange energy and its nuclear gradients. To mitigate this issue, the LFOCKSTD option was introduced, forcing VASP to use the standard HF treatment for the exact exchange while continuing to use shape restoration for the correlation energy. This reduces the noise in energies and RPA forces, and it leads to an exact exchange energy that is fully compatible with the exact exchange energy in standard HF calculations. This means that the energy " HF-free energy      FHF" in RPA calculations is identical to the "free  energy   TOTEN " when reading the WAVECAR file and performing a single-step total energy evaluation ( ALGO = Eigenval; LFHCALC = .TRUE. ; AEXX = 1.0 ; NELM = 1). In other words, when using LFOCKSTD in RPA calculations, the exact exchange energy is fully compatible with the stepwise evaluation explained here: step wise computation of the total energy.

It is strongly recommended to activate LFOCKSTD for all GW and RPA calculations starting from version 6.5.2.

Note that VASP uses one-center terms to correct the exact exchange energy for the difference in shape between all-electron and pseudo orbitals. Therefore, shape restoration is neither required nor beneficial for the exact exchange term (see NMAXFOCKAE and LMAXFOCKAE).

## Related tags and articles

LRPAFORCE

---
