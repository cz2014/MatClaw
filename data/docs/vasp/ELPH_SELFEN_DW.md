# ELPH_SELFEN_DW

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_DW = [logical]  
 Default: **ELPH\_SELFEN\_DW** = .FALSE.

Description: Controls whether the Debye-Waller contribution is included in the calculation of the phonon-induced electron self-energy.

> **Mind:** Available as of VASP 6.5.0

---

The phonon-induced electron self-energy has two contributions at second order in perturbation theory, the Fan-Migdal self-energy and the real-valued Debye-Waller self-energy.
ELPH\_SELFEN\_DW controls the computation of the latter, while the former can be computed via ELPH\_SELFEN\_FAN.

The result is reported individually for each self-energy accumulator in the vaspout.h5 file as

```
/results/electron_phonon/electrons/self_energy_1/selfen_dw
```

> **Mind:** The Debye-Waller self-energy is computed using the rigid-ion approximation.

## Related tags and articles

* Bandstructure renormalization
* Transport calculations
* ELPH\_RUN
* ELPH\_SELFEN\_GAPS
* ELPH\_SELFEN\_FAN

## References
