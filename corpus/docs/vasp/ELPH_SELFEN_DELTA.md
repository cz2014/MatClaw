# ELPH_SELFEN_DELTA

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_DELTA = [real array]  
 Default: **ELPH\_SELFEN\_DELTA** = 0.01

Description: Complex imaginary shift to use when computing the self-energy due to electron-phonon coupling.

> **Mind:** Available as of VASP 6.5.0

---

If the value is set to 0.0 then the tetrahedron method is used to perform the Brillouin zone integrals and evaluate only the imaginary part of the electron self-energy. This is the recommended option for transport calculations.

For  bandgap renormalization since one is mainly interested in the real part of the self-energy due to electron-phonon coupling, a small finite value should be used and a dense **k** point mesh used.

If more than one value is specified, the number of self-energy accumulators is increased such that one exists for each value in this array.
It is possible to compute the self-energy using the tetrahedron method and a finite complex shift in the same run.

## Related tags and articles

* Bandstructure renormalization
* ELPH\_RUN
* ELPH\_SELFEN\_GAPS
* ELPH\_SELFEN\_FAN
* ELPH\_SELFEN\_STATIC
