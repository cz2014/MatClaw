# NBLOCK

Categories: INCAR tag, Molecular dynamics, Performance

NBLOCK = [integer]  
 Default: **NBLOCK** = 1

Description: After NBLOCK ionic steps the pair-correlation function and the DOS are calculated
and the ionic configuration is written to the XDATCAR-file.

---

It is recommended to leave NBLOCK to 1, since the computational overhead to determine the DOS and pair correlation function is minimal. Only for molecular dynamics simulations with many 1000 steps or when using machine-learned force fields, it might be expedient to increase NBLOCK to say 10 or even 100, to avoid large XDATCAR-files and the evaluation of the pair correlation function at every step.

> **Tip:** If machine-learned force fields are used in prediction-only mode (`ML_MODE = run`) prefer to use the ML\_OUTBLOCK tag instead of NBLOCK to control the output frequency.

In addition

* NBLOCK controls how often the kinetic energy is scaled if `SMASS = -1`.

* After `KBLOCK * NBLOCK` ionic steps the averaged pair correlation function and DOS are written to the files PCDAT and DOSCAR. The internal accumulators are reset, and after another `KBLOCK * NBLOCK` steps the new averaged quantities are written out.

> **Warning:** The product of KBLOCK and NBLOCK should not be larger than the number of steps NSW. If `KBLOCK * NBLOCK > NSW` before starting the main ion loop then KBLOCK is automatically reset to 1. Next, if the same conditions is still true, NBLOCK is reset to NSW. Also, mind that NBLOCK will be at minimum ML\_OUTBLOCK in MLFF prediction-only MD runs.

## Related tags and articles

PCDAT, DOSCAR, XDATCAR, KBLOCK, ML\_OUTBLOCK

Examples that use this tag
