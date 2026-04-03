# ELPH_MODE

Categories: INCAR tag, Electron-phonon interactions

ELPH\_MODE = [string]

Description: Meta tag that selects reasonable defaults for electron-phonon calculations

> **Mind:** Available as of VASP 6.5.0

---

The required INCAR settings for electron-phonon calculations depend on the type of calculation.
For example, computing the renormalization of the electronic band structure requires a different set of options than computing transport properties.
The ELPH\_MODE tag can help you get started with electron-phonon calculations by selecting reasonable default values for other INCAR tags based on the type of calculation.

The individual tags that are set by ELPH\_MODE can still be overwritten by specifying them explicitly in the INCAR file.

## Tag options

### `ELPH_MODE = renorm` - Band-gap renormalization

* `ELPH_RUN = True`
* `ELPH_SELFEN_FAN = True`
* `ELPH_SELFEN_DW = True`
* `ELPH_SELFEN_GAPS = True`
* `ELPH_NBANDS = -2`
* `ELPH_SELFEN_DELTA = 0.01`

### `ELPH_MODE = transport` - Transport calculation

* `ELPH_RUN = True`
* `ELPH_TRANSPORT = True`
* `ELPH_SELFEN_FAN = True`
* `ELPH_SELFEN_DW = False`
* `ELPH_SCATTERING_APPROX = serta mrta_lambda`
* `ELPH_SELFEN_CARRIER_DEN = -1e21 -1e20 -1e19 -1e18 -1e17 -1e16 0 1e16 1e17 1e18 1e19 1e20 1e21`
* `ELPH_SELFEN_DELTA = 0`
* `ELPH_SELFEN_IMAG_SKIP = True`
* `ELPH_SELFEN_BROAD_TOL = 1e-4`
* `ELPH_WF_REDISTRIBUTE = True`

## Related tags and articles

* Bandstructure renormalization
* Transport calculations
* ELPH\_RUN
* ELPH\_TRANSPORT
* ELPH\_TRANSPORT\_DRIVER
* ELPH\_DRIVER
