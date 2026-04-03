# ELPH_SELFEN_ENERGY_WINDOW

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_ENERGY\_WINDOW = [real, real]  
 Default: **ELPH\_SELFEN\_ENERGY\_WINDOW** = 0.0 0.0

Description:
Specifies the energy window (in eV) around the band edges within which the electron-phonon self-energy is computed.

> **Mind:** Available as of VASP 6.5.0

---

The self-energy is evaluated for electronic states with energies in the intervals around the valence band minimum (VBM) and the conduction band minimum (CDM), with an energy window defined with `ELPH_SELFEN_ENERGY_WINDOW = a b`:

* from VBM – *a* up to VBM, and
* from CBM up to CBM + *b*

## Related tags and articles

* ELPH\_RUN
* ELPH\_TRANSPORT
* ELPH\_SCATTERING\_APPROX
* ELPH\_SELFEN\_IMAG\_SKIP
