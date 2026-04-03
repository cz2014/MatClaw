# ELPH_SELFEN_FAN

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_FAN = [logical]  
 Default: **ELPH\_SELFEN\_FAN** = .FALSE.

Description: Controls whether the Fan-Migdal contribution is included in the calculation of the phonon-induced electron self-energy.

> **Mind:** Available as of VASP 6.5.0

---

The phonon-induced electron self-energy has two contributions at second order in perturbation theory, the Fan-Migdal self-energy and the real-valued Debye-Waller self-energy.
ELPH\_SELFEN\_FAN controls the computation of the former, while the latter can be computed via ELPH\_SELFEN\_DW.

The result is reported individually for each self-energy accumulator in the vaspout.h5 file as

```
/results/electron_phonon/electrons/self_energy_1/selfen_fan
```

## Related tags and articles

* Bandstructure renormalization
* Transport calculations
* ELPH\_RUN
* ELPH\_SELFEN\_DW
* ELPH\_SELFEN\_STATIC
