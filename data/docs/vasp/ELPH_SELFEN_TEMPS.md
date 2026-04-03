# ELPH_SELFEN_TEMPS

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_TEMPS = [real array]  
 Default: **ELPH\_SELFEN\_TEMPS** = 0 100 200 300 400 500

Description: List of temperatures for which to compute the electron self-energy due to electron-phonon coupling.

> **Mind:** Available as of VASP 6.5.0

---

This list of temperatures is used to determine the chemical potential, the occupation factors entering the electron self-energy due to electron-phonon coupling as well as the transport coefficients in the context of a transport calculation.

The chemical potential is determined for the list of temperatures ELPH\_SELFEN\_TEMPS and carrier concentrations specified by
ELPH\_SELFEN\_CARRIER\_DEN or ELPH\_SELFEN\_CARRIER\_PER\_CELL. You can also express a range of temperatures using ELPH\_SELFEN\_TEMPS\_RANGE. Alternatively, one can specify the chemical potential and determine the carrier concentration using ELPH\_SELFEN\_MU.

## Related tags and articles

* Bandstructure renormalization
* Transport calculations
* Chemical potential in electron-phonon interactions
* ELPH\_RUN
* ELPH\_SELFEN\_TEMPS\_RANGE
* ELPH\_SELFEN\_CARRIER\_DEN
* ELPH\_SELFEN\_CARRIER\_DEN\_RANGE
* ELPH\_SELFEN\_CARRIER\_PER\_CELL
* ELPH\_SELFEN\_MU
* ELPH\_SELFEN\_MU\_RANGE
* ELPH\_SELFEN\_FAN
* ELPH\_SELFEN\_DW
