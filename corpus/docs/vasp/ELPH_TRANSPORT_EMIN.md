# ELPH_TRANSPORT_EMIN

Categories: INCAR tag, Electron-phonon interactions

ELPH\_TRANSPORT\_EMIN = [real]

Description: Lower bound of the energy window in which states are considered for transport calculations.

> **Mind:** Available as of VASP 6.5.0

---

In transport calculations, only a small amount of electronic states around the chemical potential have a sizeable contribution.
Therefore, in order to improve performance, only states inside an energy window centered around the chemical potential are considered during the calculation.
By default, the location and width of the energy window are determined automatically by VASP.
By setting ELPH\_TRANSPORT\_EMIN and ELPH\_TRANSPORT\_EMAX, one can control the energy window manually.

## Related tags and articles

* Transport calculations
* ELPH\_RUN
* ELPH\_TRANSPORT
* ELPH\_TRANSPORT\_EMAX
