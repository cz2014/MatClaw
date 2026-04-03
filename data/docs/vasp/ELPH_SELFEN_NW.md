# ELPH_SELFEN_NW

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_NW = [integer]  
 Default: **ELPH\_SELFEN\_NW** = 1

Description: Number of energies to use when computing the phonon-induced electron self-energy.

> **Mind:** Available as of VASP 6.5.0

---

The electron self-energy, $\Sigma\_{n \mathbf{k}}(\omega)$, depends on the frequency $\omega$ (or energy $\hbar \omega$).
ELPH\_SELFEN\_NW controls the number and location of frequencies when computing the self-energy in the following way:

`ELPH_SELFEN_NW > 0`
:   The self-energy is computed at ELPH\_SELFEN\_NW equally spaced energies between $\varepsilon\_{n \mathbf{k}} - \frac{1}{2} E^{\text{W}}$ and $\varepsilon\_{n \mathbf{k}} + \frac{1}{2} E^{\text{W}}$. The interval is centered around each Kohn-Sham eigenvalue, $\varepsilon\_{n \mathbf{k}}$, and its width, $E^{\text{W}}$, is controlled via ELPH\_SELFEN\_WRANGE. If ELPH\_SELFEN\_NW is an even number, it is automatically increased by one so that the center-most energy in each interval always coincides with the corresponding Kohn-Sham eigenvalue.

`ELPH_SELFEN_NW < 0`
:   The self-energy is computed at |ELPH\_SELFEN\_NW| equally spaced energies between $\varepsilon^{\text{min}}\_{\mathbf{k}} - \frac{1}{2} E^{\text{W}}$ and $\varepsilon^{\text{max}}\_{\mathbf{k}} + \frac{1}{2} E^{\text{W}}$, where $\varepsilon^{\text{min}}\_{\mathbf{k}}$ and $\varepsilon^{\text{max}}\_{\mathbf{k}}$ are the minimum and maximum Kohn-Sham eigenvalues of the calculation, respectively. Once again, $E^{\text{W}}$ is controlled via ELPH\_SELFEN\_WRANGE and allows to extend the interval in both directions.

## Related tags and articles

* ELPH\_RUN
* ELPH\_SELFEN\_FAN
* ELPH\_SELFEN\_DW
* ELPH\_SELFEN\_WRANGE
