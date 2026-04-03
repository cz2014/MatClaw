# IFC_LR

Categories: INCAR tag, Electron-phonon interactions

IFC\_LR = [integer]  
 Default: **IFC\_LR** = 1

Description: Controls the treatment of the long-range part of the interatomic force constants during electron-phonon calculations.

> **Mind:** Available as of VASP 6.5.0

---

This tag controls the treatment of the long-range electrostatic contributions to the interatomic force constants (IFC) arising in polar dielectric materials.
`IFC_LR = 1` has the same effect as `LPHON_POLAR = True` but is used in the context of electron-phonon interactions.

> **Mind:** In this case, the required Born effective charges and dielectric tensor are read from the phelel\_params.hdf5 file.

## Modes

`IFC_LR ≤ 0`
:   No long-range correction scheme is applied to the IFC matrix. This is most likely very inaccurate for semiconductors and insulators with non-vanishing Born effective charge.

`IFC_LR = 1`
:   Dipole corrections are applied to the IFC matrix.

## Related tags and articles

* Bandstructure renormalization
* Transport calculations
* ELPH\_RUN
* ELPH\_LR
