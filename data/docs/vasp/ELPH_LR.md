# ELPH_LR

Categories: INCAR tag, Electron-phonon interactions

ELPH\_LR = [integer]  
 Default: **ELPH\_LR** = 1

Description: Controls the treatment of the long-range part of the electron-phonon potential.

> **Mind:** Available as of VASP 6.5.0

---

This tag controls the treatment of the long-range electrostatic contributions to the electron-phonon coupling arising in polar dielectric materials.

> **Mind:** In this case, the required Born effective charges and dielectric tensor are read from the phelel\_params.hdf5 file.

## Modes

`ELPH_LR ≤ 0`
:   No long-range correction scheme is applied to the electron-phonon coupling. This is most likely very inaccurate for semiconductors and insulators with non-vanishing Born effective charge.

`ELPH_LR = 1`
:   Dipole corrections are applied to the electron-phonon coupling.

## Related tags and articles

* Bandstructure renormalization
* Transport calculations
* ELPH\_RUN
* IFC\_LR

## References
