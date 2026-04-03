# ELPH_USEBLAS

Categories: INCAR tag, Electron-phonon interactions

ELPH\_USEBLAS = [logical]  
 Default: **ELPH\_USEBLAS** = .TRUE.

Description: Toggles the use of BLAS routines for computing electron-phonon matrix elements.

> **Mind:** Available as of VASP 6.5.0

---

This is a performance setting that can offer a significant performance boost.
If `ELPH_USEBLAS = True`, then VASP uses BLAS routines when computing the electron-phonon matrix elements.
Otherwise, VASP-internal routines are used.

## Related tags and articles

* ELPH\_RUN
* ELPH\_DECOMPOSE
