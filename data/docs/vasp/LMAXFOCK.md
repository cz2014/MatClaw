# LMAXFOCK

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

LMAXFOCK = [integer]  
 Default: **LMAXFOCK** = 4

Description: LMAXFOCK sets the maximum angular momentum quantum number *L* for the augmentation of charge densities in Hartree-Fock type routines.

---

In the PAW method, the difference between the charge density of the all-electron partial waves $\phi\_\beta$ and
the pseudo partial waves $\tilde \phi\_\beta$

$Q\_{\alpha\beta}({\mathbf r})= \phi^\*\_\alpha({\mathbf r})\phi\_\beta({\mathbf r}) - \tilde \phi^\*\_\alpha({\mathbf r})\tilde \phi\_\beta({\mathbf r})$

is usually treated on spherical grids centered at each atom
(one-center terms inside the PAW spheres, see PAW method). To describe long range electrostatic effects, the *moments* of the differences of the all-electron and pseudo charge density
also need to be added on the plane wave grid (compensation density, see PAW method).
These compensation charges exactly restore the moments of the all-electron density on the plane wave
grid. For the charge densities used in the Hartree and DFT term,
the augmentation is done exactly up to the maximum *L* quantum number required by the POTCAR files,
whereas for the Fock exchange, for reasons of efficiency,
the augmentation on the plane wave grid is controlled by LMAXFOCK.

Specifically, when the exchange energy is evaluated

:   $$E\_{\mathrm{x}}= -\frac{e^2}{2}\sum\_{n\mathbf{k},m\mathbf{q}}
    f\_{n\mathbf{k}} f\_{m\mathbf{q}} \times
    \int\int d^3\mathbf{r} d^3\mathbf{r}'
    \frac{\psi\_{n\mathbf{k}}^{\*}(\mathbf{r})\psi\_{m\mathbf{q}}^{\*}(\mathbf{r}')
    \psi\_{n\mathbf{k}}(\mathbf{r}')\psi\_{m\mathbf{q}}(\mathbf{r})}
    {\vert \mathbf{r}-\mathbf{r}' \vert}$$

the overlap density $\psi\_{n\mathbf{k}}^{\*}(\mathbf{r})\psi\_{m\mathbf{q}}(\mathbf{r})$
between two Bloch orbitals needs to be calculated on the plane wave grid (see PAW method). The tag LMAXFOCK
controls up to which *L* quantum number, the compensation charge $\widehat{n}(\mathbf{r})$ is calculated on the plane wave grid (compared PAW method compensation charge):

$\widehat{n}(\mathbf{r}) = \sum\_{\alpha,\beta,LM} \widehat{Q}\_{\alpha,\beta}^{LM}(\mathbf{r})\,
\langle \widetilde{\psi}\_{nk} | \widetilde{p}\_{\alpha} \rangle
\langle \widetilde{p}\_{\beta} | \widetilde{\psi}\_{mk} \rangle.$

To accelerate convergence with respect to LMAXFOCK, VASP uses a small trick: the contributions from the Hartree-Fock one-center terms are evaluated for the pseudo orbitals also only up to *L*=LMAXFOCK, whereas the one-center terms for the exact all-electron orbitals are evaluated up to the maximum required *L* (twice the angular quantum number of the partial wave with the highest *l*). The default is LMAXFOCK=4, and it might be necessary to increase this parameter, if the system contains f-electrons. Since this increases the computational load considerably (about factor 2), it is recommended to perform tests, whether the results are already reasonably converged using the default LMAXFOCK=4.

To be compatible w.r.t. old releases, VASP also reads the flag HFLMAX to the same effect as LMAXFOCK.

## Related tags and articles

HFLMAX,
LMAXFOCKAE

Examples that use this tag

---
