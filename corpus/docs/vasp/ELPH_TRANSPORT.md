# ELPH_TRANSPORT

Categories: INCAR tag, Electron-phonon interactions

ELPH\_TRANSPORT = [logical]  
 Default: **ELPH\_TRANSPORT** = .FALSE.

Description: Activates transport calculation involving electron-phonon coupling

> **Mind:** Available as of VASP 6.5.0

---

When `ELPH_TRANSPORT = True`, VASP calculates the transport coefficients from the linearized Boltzmann transport equation.
In this framework, the transport coefficients are calculated from various relaxation-time approximations selectable via ELPH\_SCATTERING\_APPROX.
A convenient way to start transport calculations is to set `ELPH_MODE = transport`, which automatically provides reasonable default values for the required INCAR tags.

For more information, visit the how-to page on transport calculations.

## Related tags and articles

* Transport calculations
* ELPH\_RUN
* ELPH\_MODE
* ELPH\_SCATTERING\_APPROX
* ELPH\_TRANSPORT\_DRIVER
