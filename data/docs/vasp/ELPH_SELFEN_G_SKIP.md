# ELPH_SELFEN_G_SKIP

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_G\_SKIP = [logical]  
 Default: **ELPH\_SELFEN\_G\_SKIP** = .FALSE.

Description:
Skip the computation of the electron-phonon matrix elements and instead assume their numerical value is 1.

> **Mind:** Available as of VASP 6.5.0

---

This option is intended for debugging purposes, as it allows testing the self-energy and transport routines without performing the full evaluation of the coupling matrix elements.

## Related tags and articles

* ELPH\_SELFEN\_IMAG\_SKIP
* ELPH\_WF\_REDISTRIBUTE
* ELPH\_RUN
