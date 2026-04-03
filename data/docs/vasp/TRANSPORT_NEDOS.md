# TRANSPORT_NEDOS

Categories: INCAR tag, Electron-phonon interactions

TRANSPORT\_NEDOS = [integer]  
 Default: **TRANSPORT\_NEDOS** = 501

Description: Choose the number of points in the Gauss-Legendre integration grid for the computation of the Onsager coefficients, which in turn are used to compute the transport coefficients.

> **Mind:** Available as of VASP 6.5.0

---

By a variable change in the integral of the transport function, it is possible to use Gauss-Legendre quadrature to evaluate the Onsager coefficients.
By increasing the number of points, one defines the energy window inside which we need to compute the electron group velocities and the electronic lifetimes due to electron-phonon coupling and the precision of the integral.

A convergence study is recommended since having a very large number of integration points can greatly increase the number of states for which the electronic lifetimes need to be computed, sometimes without a significant change in the final transport coefficients. Lower values of the number of integration points can significantly speed up the calculation, especially for very dense grids.

> **Mind:** **ELPH\_TRANSPORT\_NEDOS** is a valid alternative way of writing this tag.

## Related tags and articles

* Transport calculations
* ELPH\_RUN
* ELPH\_TRANSPORT
* ELPH\_TRANSPORT\_DRIVER
* ELPH\_FERMI\_NEDOS
