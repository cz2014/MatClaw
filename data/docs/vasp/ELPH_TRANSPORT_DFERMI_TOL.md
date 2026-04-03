# ELPH_TRANSPORT_DFERMI_TOL

Categories: INCAR tag, Electron-phonon interactions

ELPH\_TRANSPORT\_DFERMI\_TOL = [real]  
 Default: **ELPH\_TRANSPORT\_DFERMI\_TOL** = 1e-6

Description: choose the fraction of the integral weight of the derivative of the Fermi–Dirac distribution that is excluded when defining the energy window for the Onsager coefficients. Must be between 0 and 1, and is only used when ELPH\_TRANSPORT\_DRIVER=1.

> **Mind:** Available as of VASP 6.5.0

---

Using this parameter, ELPH\_TRANSPORT\_EMIN and ELPH\_TRANSPORT\_EMAX are automatically computed from the chemical potentials and the distribution $-\partial f^0/\partial \epsilon$.
Formally, the integration window $[\mu-e,\mu+e]$ is chosen such that

:   $$\int\_{\mu-e}^{\mu+e} \left(-\frac{\partial f^0}{\partial \epsilon}\right) d\epsilon
    = 1 - \alpha,$$

where $\alpha \equiv$ ELPH\_TRANSPORT\_DFERMI\_TOL.
This gives

:   $$e = k\_B T \, \ln\!\left(\tfrac{2-\alpha}{\alpha}\right).$$

A small value means that only the tails of the derivative of the Fermi-dirac distribution are excluded from the integral.
A large value means that only a small energy window around the chemical potential is used.

The integral is then discretized with a number of energy points set by TRANSPORT\_NEDOS and evaluated using the Simpson's rule.

## Related tags and articles

* Transport calculations
* ELPH\_RUN
* ELPH\_TRANSPORT
* ELPH\_TRANSPORT\_DRIVER
* ELPH\_TRANSPORT\_EMIN
* ELPH\_TRANSPORT\_EMAX
* TRANSPORT\_NEDOS
