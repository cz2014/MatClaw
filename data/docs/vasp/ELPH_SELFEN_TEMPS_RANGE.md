# ELPH_SELFEN_TEMPS_RANGE

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_TEMPS\_RANGE = [real array]

Description: The range of temperatures (in K) at which to compute the phonon-mediated electron self-energy and transport coefficients.

> **Mind:** Available as of VASP 6.5.0

---

This list of temperatures is used to determine the chemical potential, the occupation factors entering the electron self-energy due to electron-phonon coupling as well as the transport coefficients in the context of a transport calculation.

A range of temperatures can be defined using `ELPH_SELFEN_TEMPS_RANGE = l u n`, where:

* *l* is the lower limit of the temperature range.
* *u* is the upper limit of the temperature range.
* *n* is the number of steps between the two limits.

For example, `ELPH_SELFEN_TEMPS_RANGE = 0 700 41` would create a list of **41** points from 0 K to 700 K. This is printed in the OUTCAR file:

```
elph_selfen_temps=
      0.000
     17.500
     35.000
  ...
    665.000
    682.500
    700.000
```

At each temperature an electron-phonon calculation is performed, rather than defining it manually using ELPH\_SELFEN\_TEMPS.

## Related tags and articles

* Transport calculations
* Electron-phonon accumulators
* Chemical potential in electron-phonon interactions
* ELPH\_RUN
* ELPH\_SELFEN\_MU
* ELPH\_SELFEN\_MU\_RANGE
* ELPH\_SELFEN\_CARRIER\_DEN
* ELPH\_SELFEN\_CARRIER\_DEN\_RANGE
* ELPH\_SELFEN\_CARRIER\_PER\_CELL
* ELPH\_SELFEN\_TEMPS
* NELECT
