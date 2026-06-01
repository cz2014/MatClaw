# ELPH_ISMEAR

Categories: INCAR tag, Electron-phonon interactions

ELPH\_ISMEAR = -15 | -14 | -5 | -4 | -1 | 0 | [integer]>0  
 Default: **ELPH\_ISMEAR** = 0

Description: Chooses the smearing method to determine the fermi level and chemical potential before an electron-phonon calculation.

> **Mind:** Available as of VASP 6.5.0

---

ELPH\_ISMEAR is very similar to ISMEAR.
The difference is that ELPH\_ISMEAR is used to determine the chemical potential in the context of electron-phonon calculation.
The Kohn-Sham states for which to calculate the chemical potential correspond to the **k**-point grid specified via the KPOINTS\_ELPH file.

The chemical potential is determined for the list of temperatures ELPH\_SELFEN\_TEMPS and carrier concentrations specified by
ELPH\_SELFEN\_CARRIER\_DEN or ELPH\_SELFEN\_CARRIER\_PER\_CELL. Alternatively, one can specify the chemical potential and determine the carrier concentration using ELPH\_SELFEN\_MU.

## Tag options

`ELPH_ISMEAR > 1`
:   Method of Methfessel-Paxton of order ELPH\_ISMEAR (for details see ISMEAR)

`ELPH_ISMEAR = 0`
:   Gaussian smearing (for details see ISMEAR)

`ELPH_ISMEAR = -1`
:   Fermi-Dirac smearing (for details see ISMEAR)

`ELPH_ISMEAR = -4`
:   Tetrahedron method (zero temperature) (for details see ISMEAR)

`ELPH_ISMEAR = -5`
:   Tetrahedron method (zero temperature) with Blöchl corrections (for details see ISMEAR)

`ELPH_ISMEAR = -14`
:   Tetrahedron method (finite temperature)

`ELPH_ISMEAR = -15`
:   Tetrahedron method (finite temperature) with Blöchl corrections

`ELPH_ISMEAR = -24`
:   Tetrahedron method (finite temperature) - same as -14 but using a faster and memory saving algorithm

## Related tags and articles

* ISMEAR
* ELPH\_SELFEN\_MU
* KPOINTS\_ELPH
