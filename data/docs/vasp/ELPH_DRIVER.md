# ELPH_DRIVER

Categories: INCAR tag, Electron-phonon interactions

ELPH\_DRIVER = el | mels  
 Default: **ELPH\_DRIVER** = el

Description: Chooses which driver to use for electron-phonon calculations.

> **Mind:** Available as of VASP 6.5.0

---

This is a high-level tag that chooses what to compute during an electron-phonon calculation.
Currently, the following drivers are supported:

`ELPH_DRIVER = el`
:   Computes the phonon-induced electron self-energy. This can be used to compute the renormalization of the electronic band structure and electronic transport properties.

`ELPH_DRIVER = mels`
:   Computes the electron-phonon matrix elements and writes them to the vaspelph.h5 file. For performance reasons, it is usually not recommended to write the matrix elements and process them externally. However, this mode is still useful for analyzing or plotting the matrix elements directly.

## Related tags and articles

* ELPH\_RUN
* ELPH\_DECOMPOSE
* ELPH\_SELFEN\_FAN
* ELPH\_SELFEN\_DW
