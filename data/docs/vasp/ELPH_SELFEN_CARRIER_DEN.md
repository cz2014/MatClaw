# ELPH_SELFEN_CARRIER_DEN

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_CARRIER\_DEN = [real array]  
 Default: **ELPH\_SELFEN\_CARRIER\_DEN** = 0.0

Description: List of additional carrier densities in units of $cm^{-3}$ at which to compute the phonon-mediated electron self-energy and transport coefficients.

> **Mind:** Available as of VASP 6.5.0

---

From each carrier density specified in the array, a positive (electron doping) or negative (hole doping) number of electrons is added to the value of NELECT and the chemical potential computed for the list of temperatures specified by ELPH\_SELFEN\_TEMPS.

> **Important:** The ELPH\_SELFEN\_CARRIER\_DEN adds electrons when positive, i.e., *n*-doping; when negative, ELPH\_SELFEN\_CARRIER\_DEN removes electrons from the system, i.e., *p*-doping.

For example, if `ELPH_SELFEN_CARRIER_DEN = 1e+16 1e+17 1e+18` the Chemical potential section in the OUTCAR file might show something like

```
                  Number of electrons per cell
                  ----------------------------
T=      0.00000000    18.00000048    18.00000477    18.00004770
T=    100.00000000    18.00000048    18.00000477    18.00004770
T=    200.00000000    18.00000048    18.00000477    18.00004770
T=    300.00000000    18.00000048    18.00000477    18.00004770
T=    400.00000000    18.00000048    18.00000477    18.00004770
T=    500.00000000    18.00000048    18.00000477    18.00004770
                  ----------------------------
                      Chemical potential
                  ----------------------------
T=      0.00000000     3.59844447     3.63257112     3.70609450
T=    100.00000000     3.59030071     3.62874001     3.70431410
T=    200.00000000     3.56867975     3.61741491     3.69897926
T=    300.00000000     3.56382644     3.60063388     3.69013925
T=    400.00000000     3.57552043     3.59226062     3.67812706
T=    500.00000000     3.58994519     3.59815865     3.66491104
                  ----------------------------
```

In the above tables, the number of elements in ELPH\_SELFEN\_CARRIER\_DEN determines the number of columns, while the number of elements in ELPH\_SELFEN\_TEMPS determines the number of rows.
Specifying more than one carrier density in ELPH\_SELFEN\_CARRIER\_DEN creates additional  electron-phonon accumulators.

Instead of specifying a carrier density, it is possible to explicitly specify the additional number of electrons to be added by using the ELPH\_SELFEN\_CARRIER\_PER\_CELL tag. Alternatively, one can specify the chemical potential directly and determine the carrier concentration using ELPH\_SELFEN\_MU.

The information related to the chemical potential calculation can be found under the Chemical potential calculation section in the OUTCAR.

## Related tags and articles

* Transport calculations
* Electron-phonon accumulators
* Chemical potential in electron-phonon interactions
* ELPH\_RUN
* ELPH\_SELFEN\_CARRIER\_DEN\_RANGE
* ELPH\_SELFEN\_CARRIER\_PER\_CELL
* ELPH\_SELFEN\_TEMPS
* ELPH\_SELFEN\_TEMPS\_RANGE
* ELPH\_SELFEN\_MU
* ELPH\_SELFEN\_MU\_RANGE
* NELECT
