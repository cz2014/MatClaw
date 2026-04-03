# ELPH_TRANSPORT_DRIVER

Categories: INCAR tag, Electron-phonon interactions

ELPH\_TRANSPORT\_DRIVER = [integer]  
 Default: **ELPH\_TRANSPORT\_DRIVER** = 2

Description: choose method to compute the Onsager coefficients, which are then used to compute the transport coefficients.

> **Mind:** Available as of VASP 6.5.0

---

The Onsager coefficients can be computed using either of the options below, each with its own advantages and disadvantages.
They are defined as

:   $$L\_{ij} = \int d\epsilon \, \mathcal{T}(\epsilon) \,
    (\epsilon-\mu)^{i+j-2}
    \left( -\frac{\partial f^0}{\partial \epsilon} \right),$$

where $\mathcal{T}(\epsilon)$ is the  transport distribution function,
$\mu$ the  chemical potential, and $f^0$ the Fermi–Dirac distribution.

`ELPH_TRANSPORT_DRIVER = 1`
:   The discretized Onsager coefficient is evaluated as

    :   $$L\_{ij} \;\approx\; \sum\_{k=1}^{N} w\_k \;
        \mathcal{T}(\epsilon\_k)\;
        (\epsilon\_k - \mu)^{\,i+j-2}\;
        \left( -\frac{\partial f^0}{\partial \epsilon} \right).$$
:   with $\epsilon\_k = \epsilon\_\text{min}+(k-1)\Delta \epsilon,\;\; k=1,\dots,N$ and $\Delta \epsilon = \tfrac{\epsilon\_\text{max}-\epsilon\_\text{min}}{N-1}$ and $\epsilon\_\text{min}$=ELPH\_TRANSPORT\_EMIN and $\epsilon\_\text{max}$=ELPH\_TRANSPORT\_EMAX or alternatively both $\epsilon\_\text{min}$ and $\epsilon\_\text{max}$ are set by ELPH\_TRANSPORT\_DFERMI\_TOL, $w\_k$ the weights due to the Simpson integration rule and N=TRANSPORT\_NEDOS.

`ELPH_TRANSPORT_DRIVER = 2`
:   Use Gauss-Legendre integration to evaluate the Onsager coefficients. The convergence of the integral can be checked by performing a convergence study with respect to N=TRANSPORT\_NEDOS alone. In this case the Onsager coefficients are evaluated using the following discretization

    :   $$L\_{ij} \;\approx\; \tfrac{1}{2} \sum\_{k=1}^N
        w\_k \,
        \left( \frac{k\_B T}{-e} \ln \frac{1+x\_k}{1-x\_k} \right)^{i+j-2}
        \mathcal{T}\!\left(\mu + k\_B T \ln\frac{1+x\_k}{1-x\_k}\right),$$
:   with $w\_k$ and $x\_k$ the weights and abcissae of the Gauss-Legendre quadrature rule.

## Related tags and articles

* Transport calculations
* ELPH\_RUN
* ELPH\_TRANSPORT
* TRANSPORT\_NEDOS
* ELPH\_TRANSPORT\_DFERMI\_TOL
* ELPH\_TRANSPORT\_EMIN
* ELPH\_TRANSPORT\_EMAX
