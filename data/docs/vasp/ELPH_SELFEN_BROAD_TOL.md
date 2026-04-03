# ELPH_SELFEN_BROAD_TOL

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_BROAD\_TOL = [real]  
 Default: **ELPH\_SELFEN\_BROAD\_TOL** = 1e-6

Description: defines the fraction of the total weight of the broadening function (derived from the imaginary part of the electron self-energy) that is excluded when setting the energy window beyond which the delta function is considered zero.
Must be between 0 and 1. This tag is only used when ELPH\_SELFEN\_IMAG\_SKIP=.TRUE. and ELPH\_SELFEN\_DELTA>0.

> **Mind:** Available as of VASP 6.5.0

---

When evaluating delta-like quantities from the imaginary part of the electron self-energy, a finite broadening function $f(\epsilon)$ is used.
ELPH\_SELFEN\_BROAD\_TOL determines what fraction of the integral of this function is retained inside the energy window $[-y, y]$ around the chemical potential, such that the remaining tails are ignored.

For a Lorentzian broadening of the form

:   $$f(x) = \frac{\delta}{\delta^2 + x^2},$$

where $\delta \equiv$ ELPH\_SELFEN\_DELTA,
the integral between $-y$ and $y$ is

:   $$\int\_{-y}^{y} \frac{\delta}{\delta^2 + x^2} \, dx = 2 \arctan\!\left(\frac{y}{\delta}\right),$$

while the total integral over all energies ($y \to \infty$) is $\pi$.
We thus require

:   $$2 \arctan\!\left(\frac{y}{\delta}\right) = \pi (1 - \alpha),$$

where $\alpha \equiv$ ELPH\_SELFEN\_BROAD\_TOL.

Solving for $y$ gives the energy cutoff:

:   $$y = \delta \, \tan\!\left(\frac{\pi (1 - \alpha)}{2}\right).$$

Hence:

* A small value of ELPH\_SELFEN\_BROAD\_TOL (e.g. 1e-6) means that nearly the entire Lorentzian area is included — a wide energy window.
* A large value (e.g. 0.1) restricts the integration to a smaller region around the resonance.

This parameter ensures a consistent and physically meaningful truncation of the Lorentzian tails when transforming the imaginary part of the self-energy into an effective delta function.
The width parameter $\delta$ is directly controlled by ELPH\_SELFEN\_DELTA.

## Related tags and articles

* ELPH\_RUN
* ELPH\_SELFEN\_IMAG\_SKIP
* ELPH\_SELFEN\_DELTA
* ELPH\_TRANSPORT
