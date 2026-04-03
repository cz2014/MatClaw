# ELPH_SELFEN_CARRIER_PER_CELL

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_CARRIER\_PER\_CELL = [real array]  
 Default: **ELPH\_SELFEN\_CARRIER\_PER\_CELL** = 0.0

Description: List of additional number of carriers for which to compute the phonon-mediated electron self-energy and transport coefficients.

> **Mind:** Available as of VASP 6.5.0

---

Each number of carriers specified in the array is added to the value of NELECT and the chemical potential computed for the list of temperatures specified by ELPH\_SELFEN\_TEMPS.
A positive number adds electrons (electron doping), while a negative one removes (hole doping).

For example, `ELPH_SELFEN_CARRIER_PER_CELL = 0.001 0.01 0.1` means that the number of electrons per cell `NELECT = 18` will be increased by the specified values which will produce the following table in the Chemical potential calculation section in the OUTCAR file

```
                  Number of electrons per cell
                  ----------------------------
T=      0.00000000    18.00100000    18.01000000    18.10000000
T=    100.00000000    18.00100000    18.01000000    18.10000000
T=    200.00000000    18.00100000    18.01000000    18.10000000
T=    300.00000000    18.00100000    18.01000000    18.10000000
T=    400.00000000    18.00100000    18.01000000    18.10000000
T=    500.00000000    18.00100000    18.01000000    18.10000000
                  ----------------------------
                      Chemical potential
                  ----------------------------
T=      0.00000000     3.94721622     4.38382135     4.91829386
T=    100.00000000     3.94656996     4.38304274     4.91799255
T=    200.00000000     3.94463398     4.38100398     4.91688588
T=    300.00000000     3.94140548     4.37778815     4.91488514
T=    400.00000000     3.93688727     4.37341919     4.91204101
T=    500.00000000     3.93108216     4.36792102     4.90841405
                  ----------------------------
```

The number of elements in ELPH\_SELFEN\_CARRIER\_PER\_CELL determines the number of columns in the tables above, while ELPH\_SELFEN\_TEMPS determines the number of rows.
Specifying more than one carrier density in ELPH\_SELFEN\_CARRIER\_PER\_CELL creates additional  electron-phonon accumulators.

Instead of specifying the number of carriers, it is possible to specify an additional carrier density in units of ${m^{-3}}$ via the ELPH\_SELFEN\_CARRIER\_DEN tag. Alternatively, one can specify the chemical potential and determine the carrier concentration using ELPH\_SELFEN\_MU.

## Related tags and articles

* Transport calculations
* Electron-phonon accumulators
* Chemical potential in electron-phonon interactions
* ELPH\_RUN
* ELPH\_SELFEN\_CARRIER\_DEN
* ELPH\_SELFEN\_CARRIER\_DEN\_RANGE
* ELPH\_SELFEN\_MU
* ELPH\_SELFEN\_MU\_RANGE
* ELPH\_SELFEN\_TEMPS
* ELPH\_SELFEN\_TEMPS\_RANGE
* NELECT
