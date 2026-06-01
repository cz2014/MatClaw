# ELPH_SELFEN_MU

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_MU = [real array]  
 Default: **ELPH\_SELFEN\_MU** = 0.0

Description: List of chemical potentials at which to compute the phonon-mediated electron self-energy and transport coefficients.

> **Mind:** Available as of VASP 6.5.0

---

Each chemical potential specified in the list will be added to the Fermi energy determined for the **k** point grid KPOINTS\_ELPH.
This Fermi energy might be different from the one determined in the self-consistent calculation if the **k** point meshes or ELPH\_ISMEAR is different from ISMEAR.
The Fermi energy from the self-consistent and non-self-consistent calculations can be read from the OUTCAR file. For example

```
$ grep "Fermi energy" OUTCAR
 Fermi energy:         3.5134142202
 Fermi energy:         3.5314189274 eV (dense k-point grid)
```

In this example, `ELPH_SELFEN_MU = 0.1` means that the chemical potential will be set to (3.5314189274 + 0.1) eV.
This can be verified Chemical potential calculation section of the OUTCAR file.

```
                  Number of electrons per cell
                  ----------------------------
T=      0.00000000    18.00000452
T=    100.00000000    18.00000536
T=    200.00000000    18.00000792
T=    300.00000000    18.00001223
T=    400.00000000    18.00001792
T=    500.00000000    18.00002315

                  ----------------------------
                      Chemical potential
                  ----------------------------
T=      0.00000000     3.63141893
T=    100.00000000     3.63141893
T=    200.00000000     3.63141893
T=    300.00000000     3.63141893
T=    400.00000000     3.63141893
T=    500.00000000     3.63141893
                  ----------------------------
```

For each of these chemical potentials and temperatures, the number of electrons per cell is computed and reported.
These, in turn, can be converted to a carrier density by dividing by the volume of the unit cell.
If more than one value is present in ELPH\_SELFEN\_MU, more columns are added to the list of chemical potentials above and more instances of the electron self-energy  accumulators are created. Alternatively, you can specify a range of chemical potentials using ELPH\_SELFEN\_MU\_RANGE.
The number of rows is set by the list of temperatures in ELPH\_SELFEN\_TEMPS.

Alternatively, one can specify the carrier density in units of ${m^{-3}}$ by using the ELPH\_SELFEN\_CARRIER\_DEN tag.

## Related tags and articles

* Transport calculations
* Electron-phonon accumulators
* Chemical potential in electron-phonon interactions
* ELPH\_RUN
* ELPH\_SELFEN\_CARRIER\_DEN
* ELPH\_SELFEN\_CARRIER\_DEN\_RANGE
* ELPH\_SELFEN\_CARRIER\_PER\_CELL
* ELPH\_SELFEN\_TEMPS
* ELPH\_SELFEN\_TEMPS\_RANGE
* NELECT
* ELPH\_SELFEN\_MU\_RANGE
