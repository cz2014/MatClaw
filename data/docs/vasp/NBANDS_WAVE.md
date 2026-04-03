# NBANDS_WAVE

Categories: INCAR tag, Many-body perturbation theory, GW, ACFDT, Low-scaling GW and RPA

NBANDS\_WAVE = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NBANDS\_WAVE** | = NBANDSGW | for LALL\_IN\_ONE=.TRUE. and NBANDS<1 |
|  | = NBANDS | for LALL\_IN\_ONE=.TRUE. and NBANDS>0 |
|  | = NBANDSEXACT | for LALL\_IN\_ONE=.FALSE. and NBANDS<1 |
|  | = NBANDS | for LALL\_IN\_ONE=.FALSE. and NBANDS>0 |

Description: NBANDS\_WAVE specifies the number of bands written to WAVECAR in the all-in-one mode of many-body perturbation theory calculations,
i.e., ALGO=ACFDT[R], [EV]GW0[R], GWR.

> **Mind:** available as of VASP.6.4.0

---

In the all-in-one mode, VASP automatically performs the necessary DFT steps prior to the many-body perturbation theory (MBPT) calculation, i.e. a DFT calculation with NBANDS, followed by an exact diagonalization of the Kohn-Sham Hamiltonian with NBANDSEXACT bands.
Note, NBANDSEXACT is set by default to the maximum number of plane-waves given by the chosen energy cutoff for the orbitals ENCUT.
In the all-in-one mode, the actual GW/RPA calculation is also performed with NBANDSEXACT bands.
If NBANDS\_WAVE is not set, all orbitals are written to WAVECAR, which potentially becomes huge in file size.

:   > **Tip:** The NBANDS\_WAVE tag can be used to limit the number of bands written to WAVECAR if LALL\_IN\_ONE=.TRUE.

The all-in-one mode is automatically enabled for ALGO=[EV]GW[0]R, RPA[R],ACFDT[R] if NBANDS is not set.

## Related tags and articles

ALGO,
NBANDS
NBANDSEXACT
IALL\_IN\_ONE
LALL\_IN\_ONE

---
