# ELPH_SELFEN_BAND_START

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_BAND\_START = [real]  
 Default: **ELPH\_SELFEN\_BAND\_START** = 1

Description: Compute the electron self-energy due to electron-phonon coupling only for bands with indices starting from ELPH\_SELFEN\_BAND\_START.

> **Mind:** Available as of VASP 6.5.0

---

This tag can be used in combination with ELPH\_SELFEN\_KPTS, ELPH\_SELFEN\_IKPT or ELPH\_SELFEN\_BAND\_STOP to limit the calculation of the electron-phonon self-energy to a particular set of **k**-points and bands.

## Related tags and articles

* Bandstructure renormalization
* Transport calculations
* ELPH\_RUN
* ELPH\_SELFEN\_GAPS
* ELPH\_SELFEN\_FAN
* ELPH\_SELFEN\_KPTS
* ELPH\_SELFEN\_IKPT
* ELPH\_SELFEN\_BAND\_STOP
