# ELPH_SELFEN_MU_RANGE

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_MU\_RANGE = [real array]

Description: List of the range of chemical potentials (in eV) at which to compute the phonon-mediated electron self-energy and transport coefficients.

> **Mind:** Available as of VASP 6.5.0

---

A set of different chemical potentials can be set using ELPH\_SELFEN\_MU\_RANGE as a shift with respect to the Fermi level $E\_F$ as an alternative to ELPH\_SELFEN\_MU.
A range of chemical potentials can be defined using `ELPH_SELFEN_MU_RANGE = l u n`, where:

* *l* is the lower limit of the chemical potential range.
* *u* is the upper limit of the chemical potential range.
* *n* is the number of steps between the two limits.

For example, `ELPH_SELFEN_MU_RANGE = -1.0 1.0 101` would create a list of **101** points around the Fermi level between $E\_F - 1.0$ and $E\_F + 1.0$.

## Related tags and articles

* Transport calculations
* Electron-phonon accumulators
* Chemical potential in electron-phonon interactions
* ELPH\_RUN
* ELPH\_SELFEN\_MU
* ELPH\_SELFEN\_CARRIER\_DEN
* ELPH\_SELFEN\_CARRIER\_DEN\_RANGE
* ELPH\_SELFEN\_CARRIER\_PER\_CELL
* ELPH\_SELFEN\_TEMPS
* ELPH\_SELFEN\_TEMPS\_RANGE
* NELECT
