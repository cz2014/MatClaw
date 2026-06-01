# Projector-augmented-wave formalism

Categories: Electronic minimization, Projector-augmented-wave method, Theory

## Basics of the PAW formalism

The PAW formalism is a generalization of ideas of both Vanderbilt-type
ultrasoft-pseudopotentials (USPP) and the
linearized augmented-plane-wave (LAPW) method. The method was first
proposed and implemented by Blöchl. The formal relationship between Vanderbilt-type
ultrasoft pseudopotentials and the PAW method has been derived by Kresse and
Joubert, and the generalization of the PAW method to noncollinear
magnetism has been
discussed by Hobbs, Kresse and Hafner.
We briefly summarize the basics of the PAW method below (following Refs.
and ).

In the PAW method the one electron wavefunctions $\psi\_{n\mathbf{k}}$, in the following simply
called orbitals, are
derived from the pseudo orbitals $\widetilde{\psi}\_{n\mathbf{k}}$ by means of a
linear transformation:

:   :   $$|\psi\_{n\mathbf{k}} \rangle = |\widetilde{\psi}\_{n\mathbf{k}} \rangle +
        \sum\_{i}(|\phi\_{i} \rangle - |\widetilde{\phi}\_{i} \rangle)
        \langle \widetilde{p}\_{i} |\widetilde{\psi}\_{n\mathbf{k}} \rangle.$$

The pseudo orbitals
$\widetilde{\psi}\_{n\mathbf{k}}$, where $nk$ is the band index and k-point index, are the variational quantities
and expanded in plane waves (see below). In the interstitial region between the PAW spheres,
the orbitals $\widetilde{\psi}\_{n\mathbf{k}}$ are identical to the exact orbitals ${\psi}\_{n\mathbf{k}}$.
Inside the spheres, the pseudo-orbitals are however only a computational
tool and an inaccurate
approximation to the true orbitals, since even the
norm of the all-electron wave function is not reproduced.
The last equation is required to map the auxiliary quantities $\widetilde{\psi}\_{n\mathbf{k}}$
onto the corresponding exact orbitals.
The PAW method implemented in VASP exploits the frozen core (FC) approximation,
which is not an inherent characteristic of the PAW method, but has been made in all
implementations so far.
In the present case, the core electrons are also kept frozen in the configuration for
which the PAW dataset was generated.

The index $\alpha$ is a shorthand for the atomic site $\mathbf{R}\_\alpha$, the angular momentum
quantum numbers $l\_\alpha,m\_\alpha$ and an additional index $\varepsilon\_\alpha$ referring to
the reference
energy. The pseudo orbitals are expanded in the reciprocal space using plane waves

:   :   $$\langle \mathbf{r} | \widetilde{\psi}\_{n\mathbf{k}} \rangle =
        \frac{1}{\Omega^{1/2}} \sum\_{\mathbf{G}} C\_{n\mathbf{kG}}
        e^{i(\mathbf{G}+\mathbf{k})\cdot \mathbf{r}} = e^{i\mathbf{k}\cdot \mathbf{r}}\tilde u\_{n\mathbf k}(\mathbf r),$$

where $\Omega$ is the volume of the Wigner-Seitz cell and $\tilde u\_{n\mathbf k}(\mathbf r)$ is the cell periodic part of the pseudo orbital. The all-electron (AE)
partial waves
$\phi\_{\alpha}$ are solutions of the radial Schrödinger equation for a
non-spinpolarized reference atom
at a specific energy $\varepsilon\_\alpha$ and for a specific angular momentum $l\_\alpha$:

:   :   $$\langle \mathbf{r}|\phi\_{\alpha}\rangle = \frac{1}{|\mathbf{r}-\mathbf{R}\_\alpha|}
        u\_{\alpha}(|\mathbf{r}-\mathbf{R}\_\alpha|)Y\_{\alpha}(\widehat{\mathbf{r}-\mathbf{R}\_\alpha})
        = \frac{1}{|\mathbf{r}-\mathbf{R}\_\alpha|} u\_{l\_\alpha\varepsilon\_\alpha}(|\mathbf{r}-\mathbf{R}\_\alpha|)\,
        Y\_{l\_\alpha m\_\alpha}(\widehat{\mathbf{r}-\mathbf{R}\_\alpha}).$$

The notation $\widehat{\mathbf{r}-\mathbf{R}\_\alpha}$ is used to clarify that
the spherical harmonics $Y$ depends on the orientation but not on
the length of the vector $\mathbf{r}-\mathbf{R}\_\alpha$.
Note that the radial component of the partial wave $u\_{\alpha}$ is independent of
$m\_\alpha$, since the partial waves are calculated for a spherical atom. Also, do not confuse the radial functions, $u\_{\alpha}(|\mathbf r|)$, with the functions of the cell-periodic part, $\tilde u\_{n\mathbf k}(\mathbf r)$.
Furthermore, the spherical harmonics depend on the angular quantum numbers only
and not on the reference energy. The pseudo partial
waves $\widetilde{\phi}\_{\alpha}$ are equivalent to the AE partial waves outside a core
radius $r\_{c}$ and match continuously onto $\phi\_{\alpha}$ inside the core radius:

:   :   $$\langle \mathbf{r}|\widetilde{\phi}\_{\alpha}\rangle = \frac{1}{|\mathbf{r}-\mathbf{R}\_\alpha|}
        \widetilde{u}\_{\alpha}(|\mathbf{r}-\mathbf{R}\_\alpha|)
        Y\_{\alpha}(\widehat{\mathbf{r}-\mathbf{R}\_\alpha})
        = \frac{1}{|\mathbf{r}-\mathbf{R}\_\alpha|}
        \widetilde{u}\_{l\_\alpha\varepsilon\_\alpha}(|\mathbf{r}-\mathbf{R}\_\alpha|)\,
        Y\_{l\_\alpha m\_\alpha}(\widehat{\mathbf{r}-\mathbf{R}\_\alpha}).$$

The core radius $r\_{c}$ is usually chosen approximately around half the nearest
neighbor distance. The projector functions $\widetilde{p}\_{\alpha}$ are dual to the partial
waves:

:   :   $$\langle \widetilde{p}\_{i} | \widetilde{\phi}\_{j} \rangle = \delta\_{ij}.$$

## Charge and overlap densities

Starting from the completeness relations it is possible to show that, in the PAW
method, the total charge density (or more precisely the overlap density) related to two orbitals $\psi\_{n\mathbf{k}}$ and $\psi\_{m\mathbf{k}}$

:   :   $$n(\mathbf{r}) = \psi^{\ast}\_{n\mathbf{k}}(\mathbf{r})\,\psi\_{m\mathbf{k}}(\mathbf{r})$$

can be rewritten as (for details we refer to Ref. ):

:   :   $$n(\mathbf{r}) = \widetilde{n} (\mathbf{r}) -
        \widetilde{n}^{1}(\mathbf{r})+
        n^{1}(\mathbf{r}).$$

Here, the constituent charge densities are defined as:

:   :   $$\widetilde{n}(\mathbf{r}) = \langle \widetilde{\psi}\_{n\mathbf{k}}| \mathbf{r}\rangle\langle \mathbf{r}
        | \widetilde{\psi}\_{m\mathbf{k}} \rangle$$

:   :   $$\widetilde{n}^{1}(\mathbf{r}) = \sum\_{\alpha, \beta}
        \widetilde{\phi}^\ast\_\alpha(\mathbf{r})
        \widetilde{\phi}\_\beta (\mathbf{r})
        \langle\widetilde{\psi}\_{n\mathbf{k}}|\widetilde{p}\_\alpha\rangle
        \langle\widetilde{p}\_\beta| \widetilde{\psi}\_{m\mathbf{k}}\rangle$$

:   :   $$n^{1}(\mathbf{r}) = \sum\_{\alpha, \beta}
        \phi^\ast\_\alpha(\mathbf{r})
        \phi\_\beta (\mathbf{r})
        \langle\widetilde{\psi}\_{n\mathbf{k}}|\widetilde{p}\_\alpha\rangle
        \langle\widetilde{p}\_\beta| \widetilde{\psi}\_{m\mathbf{k}}\rangle.$$

The quantities with a superscript 1 are one-center quantities and
are usually only evaluated on radial grids. Furthermore, one can usually
drop the complex conjugation for the partial waves, since they are real-valued.
The indices $\alpha$ and $\beta$ are restricted to those pairs that correspond to one atom
$\mathbf{R}\_\alpha=\mathbf{R}\_\beta$.
For a complete set of projectors the one-centre pseudo
charge density $\widetilde{n}^{1}$ is exactly
identical to $\widetilde{n}$ within the augmentation spheres.
Furthermore, it is often necessary to define $\rho\_{\alpha\beta}$, the occupancies of each
augmentation channel $(\alpha,\beta)$ inside each PAW sphere. These are calculated from the pseudo orbitals
applying the projector functions and summing over all bands

:   :   $$\rho\_{\alpha\beta} = \sum\_{n\mathbf{k}}
        f\_{n\mathbf{k}} \langle \widetilde{\psi}\_{n\mathbf{k}} | \widetilde{p}\_{\alpha} \rangle
        \langle \widetilde{p}\_{\beta} | \widetilde{\psi}\_{n\mathbf{k}} \rangle,$$

where the occupancy $f\_{n\mathbf{k}}$ is one for occupied orbitals
and zero for unoccupied one electron orbitals.

## The compensation or augmentation density

The PAW method would yield exact overlap densities on the plane wave grid
if the density were calculated as

:   :   $$n(\mathbf{r})= \langle \widetilde{\psi}\_{n\mathbf{k}}| \mathbf{r}\rangle\langle \mathbf{r}
        | \widetilde{\psi}\_{m\mathbf{k}} \rangle + \sum\_{\alpha, \beta}
        (
        \phi^\ast\_\alpha(\mathbf{r})
        \phi\_\beta (\mathbf{r})
        -
        \widetilde{\phi}^\ast\_\alpha(\mathbf{r})
        \widetilde{\phi}\_\beta (\mathbf{r})
        )
        \langle\widetilde{\psi}\_{n\mathbf{k}}|\widetilde{p}\_\alpha\rangle
        \langle\widetilde{p}\_\beta| \widetilde{\psi}\_{m\mathbf{k}}\rangle$$

In practice, the second term changes far too rapidly in real space
to be represented on a plane wave grid. Since even the norm
of the pseudo-orbitals does not agree with the norm of the all-electron orbitals, it does not suffice to calculate
Hartree or exchange energies from the pseudo densities only.

Hence, in order to treat the long-range electrostatic interactions in the Hartree and exchange term
an additional quantity, the compensation density $\widehat{n}$, is introduced.
Its purpose is to approximate

:   :   $$Q\_{\alpha,\beta}({\mathbf r}) = \phi^\ast\_\alpha(\mathbf{r})
        \phi\_\beta (\mathbf{r})
        -
        \widetilde{\phi}^\ast\_\alpha(\mathbf{r})
        \widetilde{\phi}\_\beta (\mathbf{r}).$$

This compensation density (sometimes also referred to as augmentation density) is chosen such that the sum of the pseudo charge density
and the compensation density
$\widetilde{n}^{1} + \widehat{n}$ has exactly the same moments as the exact
density $n^{1}$ within each augmentation sphere centered at the position
$\mathbf{R}\_\alpha$. This requires that

:   :   $$\int\_{\Omega\_{r}}[n^{1}(\mathbf{r}) -\widetilde{n}^{1}(\mathbf{r}) -
        \widehat{n}(\mathbf{r})]|\mathbf{r}-\mathbf{R}\_\alpha|^{L}
        Y\_{LM}^{\ast}(\widehat{\mathbf{r}-\mathbf{R}\_\alpha})\,d\mathbf{r} = 0
        \quad \forall \quad \mathbf{R}\_\alpha, L, M.$$

This implies that the electrostatic potential originating from $n^{1}$
is identical to that of $\widetilde{n}^{1}+\widehat{n}$ outside
the augmentation sphere.
Details on the construction of the compensation charge density in the VASP program
have been published elsewhere. The compensation charge density is written in the form
of a one-center multipole expansion

:   :   $$\widehat{n}(\mathbf{r}) = \sum\_{\alpha,\beta,LM} \widehat{Q}\_{\alpha,\beta}^{LM}(\mathbf{r})\,
        \langle \widetilde{\psi}\_{n\mathbf{k}} | \widetilde{p}\_{\alpha} \rangle
        \langle \widetilde{p}\_{\beta} | \widetilde{\psi}\_{m\mathbf{k}} \rangle,$$

where the functions $\widehat{Q}\_{\alpha\beta}^{LM}(\mathbf{r})$ are given by

:   :   $$\widehat{Q}\_{\alpha \beta}^{LM}(\mathbf{r}) = q\_{\alpha \beta}^{LM}\,g\_{L}(|\mathbf{r}-\mathbf{R}\_i|)
        Y\_{LM}(\widehat{\mathbf{r}-\mathbf{R}\_\alpha}).$$

The moment $L$ of the function $g\_L(r)$ is equal to 1. The quantity $q\_{\alpha\beta}^{LM}$
is defined in Eq. (25) of Ref. .

## References

---
