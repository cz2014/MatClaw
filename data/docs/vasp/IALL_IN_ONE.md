# IALL_IN_ONE

Categories: INCAR tag, Many-body perturbation theory, GW, ACFDT, Low-scaling GW and RPA

|  |  |  |
| --- | --- | --- |
| Default: **IALL\_IN\_ONE** | = 1 | for LALL\_IN\_ONE=.TRUE. or NBANDS<0 |
|  | = -1 | for LALL\_IN\_ONE=.FALSE. |

Description: IALL\_IN\_ONE>0 enables the all-in-one mode for many-body perturbation theory calculations,
i.e., ALGO=ACFDT[R], [EV]GW0[R], GWR.

---

In the all-in-one mode, VASP automatically performs the necessary DFT steps prior to the many-body perturbation theory (MBPT) calculation, i.e. a DFT calculation with NBANDS, followed by an exact diagonalization of the Kohn-Sham Hamiltonian with NBANDSEXACT bands.
Note, NBANDSEXACT is set by default to the maximum number of plane-waves given by the chosen energy cutoff for the orbitals ENCUT.
In the all-in-one mode, the actual GW/RPA calculation is also performed with NBANDSEXACT bands.
If NBANDS\_WAVE is not set, all orbitals are written to WAVECAR, which potentially becomes huge in file size.

:   > **Tip:** The NBANDS\_WAVE tag can be used to limit the number of bands written to WAVECAR if IALL\_IN\_ONE>0.

The all-in-one mode is automatically enabled for ALGO=[EV]GW[0]R, RPA[R],ACFDT[R] if NBANDS is not set.

> **Mind:** available as of VASP.6.4.0

## Related tags and articles

ALGO,
NBANDS
NBANDSEXACT
NBANDS\_WAVE
LALL\_IN\_ONE

---
