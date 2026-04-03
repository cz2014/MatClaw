# ELPH_RUN

Categories: INCAR tag, Electron-phonon interactions

ELPH\_RUN = [logical]  
 Default: **ELPH\_RUN** = .false.

Description: Select whether to run and electron-phonon calculation.

> **Mind:** Available as of VASP 6.5.0

---

This flag determined whether an electron-phonon calculation should be performed.
The most fundamental quantity we compute are the electron-phonon matrix elements.

These can simply be written to file when `ELPH_DRIVER = MELS` for further post-processing.
Additionally, one can directly use these matrix elements to compute the electron self-energy due to electron-phonon coupling `ELPH_DRIVER = EL`.
The self-energy can in turn be used to compute the renormalization of the electronic bandstructure or transport coefficients involving electron-phonon scattering.

Additionally, the tag ELPH\_MODE sets defaults for other INCAR tags depending on the quantities of interest.

## Related tags and articles

* Bandstructure renormalization
* Transport calculations
* Chemical potential in electron-phonon interactions
* ELPH\_TRANSPORT
* ELPH\_MODE
* ELPH\_DRIVER
