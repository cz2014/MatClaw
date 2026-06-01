# ELPH_NBANDS

Categories: INCAR tag, Electron-phonon interactions

ELPH\_NBANDS = [integer]  
 Default: **ELPH\_NBANDS** = NBANDS

Description: Number of bands to compute on the dense **k** point grid for the electron-phonon driver

> **Mind:** Available as of VASP 6.5.0

---

For transport calculations, this value should be as little as possible while including all the states potentially participating in the transport calculation.

If ELPH\_NBANDS=-2 then the number of bands is set to the maximum number of plane waves. This setting is particularly useful for calculating the  bandgap renormalization.
In this case, the final result converges slowly with the number of bands in the calculation, similar to RPA, and BSE calculations.

## Related tags and articles

* Bandstructure renormalization
* Transport calculations
* ELPH\_RUN
* ELPH\_NBANDS\_SUM
* ELPH\_SELFEN\_FAN
* ELPH\_SELFEN\_DW
