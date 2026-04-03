# ELPH_SELFEN_STATIC

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_STATIC = [logical]  
 Default: **ELPH\_SELFEN\_STATIC** = .FALSE.

Description: Activates the adiabatic approximation for the phonon-induced electron self-energy.

> **Mind:** Available as of VASP 6.5.0

---

The adiabatic approximation assumes that the electron dynamics are much faster than the phonon dynamics.
In other words, there is no energy exchange between the electronic and the phononic subsystems.
Mathematically, this is equivalent to setting the phonon frequencies in the denominator of the Fan-Migdal self-energy to zero.

> **Warning:** The adiabatic approximation is ill-suited for polar materials where it may introduce large errors .

## Related tags and articles

* ELPH\_RUN
* ELPH\_SELFEN\_FAN
* ELPH\_SELFEN\_DELTA

## References
