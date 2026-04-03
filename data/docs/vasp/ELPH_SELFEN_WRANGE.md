# ELPH_SELFEN_WRANGE

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_WRANGE = [real]  
 Default: **ELPH\_SELFEN\_WRANGE** = 0

Description: Together with ELPH\_SELFEN\_NW specifies the energy window in which to evaluate the phonon-induced electron self-energy.

> **Mind:** Available as of VASP 6.5.0

---

The electron self-energy, $\Sigma\_{n \mathbf{k}}(\omega)$, depends on the frequency $\omega$ (or energy $\hbar \omega$).
The tag ELPH\_SELFEN\_WRANGE determines the width of the energy window in which to evaluate the self-energy.
However, the location and width of the energy window is also influenced by the sign of ELPH\_SELFEN\_NW.
For more information, we refer to the documentation of ELPH\_SELFEN\_NW.

## Related tags and articles

* ELPH\_RUN
* ELPH\_SELFEN\_FAN
* ELPH\_SELFEN\_DW
* ELPH\_SELFEN\_NW
