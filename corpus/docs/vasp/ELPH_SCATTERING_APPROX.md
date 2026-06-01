# ELPH_SCATTERING_APPROX

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SCATTERING\_APPROX = [string]  
 Default: **ELPH\_SCATTERING\_APPROX** = SERTA MRTA\_LAMBDA

Description: Select which type of approximation is used to compute the electron scattering lifetimes due to electron-phonon coupling

> **Mind:** Available as of VASP 6.5.0

---

There are different approximations to compute the electronic lifetimes due to electron-phonon scattering.
Each of these can lead to significantly different transport coefficients.
It is possible to select more than one approximation in ELPH\_SCATTERING\_APPROX.
In this case, additional  electron-phonon accumulators are created for each scattering approximation.

## Options to select

`ELPH_SCATTERING_APPROX = CRTA` - Constant Relaxation-Time Approximation
:   The relaxation time is assumed constant. It needs to be specified via TRANSPORT\_RELAXATION\_TIME. In this case, the computation of electron-phonon matrix elements is skipped entirely, which is a huge performance boost compared to the other relaxation-time approximations.

> **Warning:** While the CRTA can be a reasonable approximation for metals, it will generally fail for insulators.

`ELPH_SCATTERING_APPROX = SERTA` - Self-Energy Relaxation-Time Approximation
:   Computes the relaxation time from the imaginary part of the Fan self-energy, evaluated on the electronic eigenenergy:
:   $$\frac{1}{\tau^{\mathrm{SERTA}}\_{n\mathbf{k}}} = \frac{2\pi}{\hbar} \sum\_{n'\nu\mathbf{k}'} w\_{n\mathbf{k},n'\mathbf{k}'} \, |g^{\nu}\_{n\mathbf{k},n'\mathbf{k}'}|^2 \left[ (n\_{\nu\mathbf{q}} + 1 - f\_{n'\mathbf{k}'}) \, \delta(\varepsilon\_{n\mathbf{k}} - \varepsilon\_{n'\mathbf{k}'} - \hbar\omega\_{\nu\mathbf{q}}) + (n\_{\nu\mathbf{q}} + f\_{n'\mathbf{k}'}) \, \delta(\varepsilon\_{n\mathbf{k}} - \varepsilon\_{n'\mathbf{k}'} + \hbar\omega\_{\nu\mathbf{q}}) \right]$$
:   where ${\tau^{\mathrm{SERTA}}\_{n\mathbf{k}}}$ is the relaxation time (or scattering time, or lifetime) for state $(n,\mathbf{k})$, $w\_{n\mathbf{k},n'\mathbf{k}'}$ is the scattering weight, $g^{\nu}\_{n\mathbf{k},n'\mathbf{k}'}$ is the electron-phonon coupling matrix element, $f\_{n\mathbf{k}}$ is the population of the electronic state (Fermi-Dirac distribution), $n\_{\nu\mathbf{q}}$ is the population of the phononic state (Bose-Einstein distribution), $\varepsilon\_{n\mathbf{k}}$ is the energy of an electron band, $\omega\_{\nu\mathbf{q}}$ is the phonon frequency, and $\delta$ is the Dirac delta function.

:   For SERTA, the scattering weight is:
:   $$w\_{n\mathbf{k},n'\mathbf{k}'} = 1$$

`ELPH_SCATTERING_APPROX = ERTA_LAMDBA` - Energy Relaxation-Time Approximation (mean-free path approximation)
:   Applies an energy-projected weight scaled by mean-free path (where $\mu$ is the chemical potential):
:   $$w\_{n\mathbf{k},n'\mathbf{k}'} = \left(1 - \frac{\mathbf{v}\_{n\mathbf{k}} \cdot \mathbf{v}\_{n'\mathbf{k}'}}{|\mathbf{v}\_{n\mathbf{k}}| |\mathbf{v}\_{n'\mathbf{k}'}|} \left| \frac{\varepsilon\_{n'\mathbf{k}'} - \mu}{\varepsilon\_{n\mathbf{k}} - \mu} \right|\right)$$

> **Warning:** The formula above is correct and used from the next release of VASP onwards. In VASP 6.5.0 and 6.5.1, the following formula is used:
>
> :   $$w\_{n\mathbf{k},n'\mathbf{k}'} = \left(1 - \frac{\mathbf{v}\_{n\mathbf{k}} \cdot \mathbf{v}\_{n'\mathbf{k}'}}{|\mathbf{v}\_{n\mathbf{k}}| |\mathbf{v}\_{n'\mathbf{k}'}|}\right) \left| \frac{\varepsilon\_{n'\mathbf{k}'} - \mu}{\varepsilon\_{n\mathbf{k}} - \mu} \right|$$

`ELPH_SCATTERING_APPROX = ERTA_TAU` - Energy Relaxation-Time Approximation (lifetime approximation)
:   $$w\_{n\mathbf{k},n'\mathbf{k}'} = \left(1 - \frac{\mathbf{v}\_{n\mathbf{k}} \cdot \mathbf{v}\_{n'\mathbf{k}'}}{|\mathbf{v}\_{n\mathbf{k}}|^2} \left| \frac{\varepsilon\_{n'\mathbf{k}'} - \mu}{\varepsilon\_{n\mathbf{k}} - \mu} \right|\right)$$

> **Warning:** The formula above is correct and used from the next release of VASP onwards. In VASP 6.5.0 and 6.5.1, the following formula is used:
>
> :   $$w\_{n\mathbf{k},n'\mathbf{k}'} = \left(1 - \frac{\mathbf{v}\_{n\mathbf{k}} \cdot \mathbf{v}\_{n'\mathbf{k}'}}{|\mathbf{v}\_{n\mathbf{k}}|^2}\right) \left| \frac{\varepsilon\_{n'\mathbf{k}'} - \mu}{\varepsilon\_{n\mathbf{k}} - \mu} \right|$$

`ELPH_SCATTERING_APPROX = MRTA_LAMDBA` - Momentum Relaxation-Time Approximation (mean-free path approximation)
:   $$w\_{n\mathbf{k},n'\mathbf{k}'} = \left(1 - \frac{\mathbf{v}\_{n\mathbf{k}} \cdot \mathbf{v}\_{n'\mathbf{k}'}}{|\mathbf{v}\_{n\mathbf{k}}| |\mathbf{v}\_{n'\mathbf{k}'}|}\right)$$

`ELPH_SCATTERING_APPROX = MRTA_TAU` - Momentum Relaxation-Time Approximation (lifetime approximation)
:   $$w\_{n\mathbf{k},n'\mathbf{k}'} = \left(1 - \frac{\mathbf{v}\_{n\mathbf{k}} \cdot \mathbf{v}\_{n'\mathbf{k}'}}{|\mathbf{v}\_{n\mathbf{k}}|^2}\right)$$

## Related tags and articles

* Transport calculations
* Electronic transport coefficients
* Electron-phonon accumulators
* ELPH\_RUN
* ELPH\_TRANSPORT
* ELPH\_TRANSPORT\_DRIVER
* TRANSPORT\_RELAXATION\_TIME
