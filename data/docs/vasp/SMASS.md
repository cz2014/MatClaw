# SMASS

Categories: INCAR tag, Molecular dynamics, Thermostats

SMASS = -3 | -2 | -1 | [real] ≥ 0  
 Default: **SMASS** = -3

Description: SMASS controls the velocities during an ab-initio molecular-dynamics run.

---

* SMASS=-3

:   For SMASS=-3 a microcanonical ensemble (NVE ensemble) is simulated (constant energy molecular dynamics). The calculated Hellmann-Feynman forces serve as an acceleration acting onto the ions. The total free energy (i.e. free electronic energy + Madelung energy of ions + kinetic energy of ions) is conserved.

:   > **Tip:** Another possible way to sample from the NVE ensemble is to use `MDALGO = 1` and `ANDERSEN_PROB = 0.0`.

* SMASS=-2

:   For SMASS=-2 the initial velocities are kept constant. This allows to calculate the energy for a set of different linear dependent positions (for instance frozen phonons, or dimers with varying bond lengths).
:   **Mind**: if SMASS=-2 the actual steps taken are POTIM×(velocities-read-from-the-POSCAR-file). To avoid ambiguities, set POTIM=1.

* SMASS=-1

:   In this case the velocities are scaled each NBLOCK step (starting at the first step i.e. MOD(NSTEP,NBLOCK)=1) to the temperature: T=TEBEG+(TEEND-TEBEG)×NSTEP/NSW,
:   where NSTEP is the current step (starting from 1). This allows a continuous increase or decrease of the kinetic energy. In the intermediate period, a micro-canonical ensemble is simulated.

* SMASS≥0

:   For SMASS≥0, a canonical ensemble is simulated using the algorithm of Nosé. The Nosé mass controls the frequency of the temperature oscillations during the simulation. For SMASS=0, a Nosé-mass corresponding to period of 40 time steps will be chosen. The Nosé-mass should be set such that the induced temperature fluctuation show approximately the same frequencies as the typical 'phonon'-frequencies for the specific system. For liquids something like 'phonon'-frequencies might be obtained from the spectrum of the velocity auto-correlation function. If the ionic frequencies differ by an order of magnitude from the frequencies of the induced temperature fluctuations, Nosé thermostat and ionic movement might decouple leading to a non-canonical ensemble. The frequency of the approximate temperature fluctuations induced by the Nosé-thermostat is written to the OUTCAR file.

## Related tags and articles

structure optimization,
IBRION,
POTIM,
NBLOCK,
TEBEG,
TEEND

Examples that use this tag

## References

---
