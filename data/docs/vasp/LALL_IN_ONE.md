# LALL IN ONE

Categories: INCAR tag, Many-body perturbation theory, GW, ACFDT, Low-scaling GW and RPA

LALL\_IN\_ONE = .FALSE. | .TRUE.

|  |  |  |
| --- | --- | --- |
| Default: **LALL\_IN\_ONE** | = .FALSE. | for NBANDS>0 |
|  | = .TRUE. | for NBANDS<0 |

Description: LALL\_IN\_ONE=.TRUE. enables the all-in-one mode for many-body perturbation theory calculations,
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
NBANDS,
NBANDSEXACT,
NBANDS\_WAVE,
IALL\_IN\_ONE

---
