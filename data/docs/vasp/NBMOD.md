# NBMOD

Categories: INCAR tag, Charge density

NBMOD = -3 | -2 | -1 | 0 | [positive integer]

|  |  |  |
| --- | --- | --- |
| Default: **NBMOD** | = n | if IBAND is set and contains n values |
|  | = -2 | if EINT is set and IBAND is not set |
|  | = -1 | if neither EINT nor IBAND are set |

Description: NBMOD controls how bands are selected when computing partial charge densities.

---

NBMOD is used with other tags to define the mode of band selection for partial charge densities in PARCHG, vaspout.h5, or CHGCAR files. There are several ways to set this tag.

* NBMOD = n: Use n bands

:   If a positive integer is passed, NBMOD represents the number of values in the array IBAND. If IBAND is specified, NBMOD is set automatically to the number of values passed in IBAND.

:   > **Tip:** There is no good reason to set NBMOD to a positive integer since it will be overwritten regardless if IBAND is set or not. Use the IBAND tag alone to enter this mode.

* NBMOD = 0: Use all bands

:   All bands, even unoccupied ones, are contributing to calculating the partial charge density. E.g. the resulting partial charge density in the PARCHG file will sum up to twice the value of the number of total bands NBANDS.

* NBMOD = -1: Use all occupied bands

:   This mode writes the charge density of all occupied states to the CHGCAR file, and no PARCHG file is produced. In contrast to producing a CHGCAR file from the WAVECAR input without the partial charges methodology (e.g. by setting LPARD = .FALSE., ALGO = None, and NELM = 1), the augmentation occupancies is not included in the produced CHGCAR file for NBMOD = -1. However, the fine FFT grid's valence charge density is equivalent.

* NBMOD = -2: Use an absolute energy interval to select contributing bands

:   The partial charge density is calculated for electrons in the energy interval specified by EINT.

* NBMOD = -3: Use an energy interval to select contributing bands and add the Fermi energy $\epsilon\_f$ to the passed values

:   The partial charge density is calculated for electrons in the energy interval specified by EINT. In this mode, the values in EINT are interpreted as relative to the Fermi energy $\epsilon\_f$. E.g. if EINT = -0.1 0.5 and $\epsilon\_f$ = 2.43, the chosen energy interval will range from 2.33 to 2.93 eV.

## Related tags and articles

LPARD,
IBAND,
EINT,
KPUSE,
LSEPB,
LSEPK,
LPARDH5,
PARCHG,
vaspout.h5,
Band-decomposed charge densities

Examples that use this tag

---
