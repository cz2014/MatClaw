# Wrap-around errors

Categories: Electronic minimization, Charge density, Theory

**Wrap-around errors** arise if the  Fast Fourier transformation (FFT) meshes are not
sufficiently large. It can be shown that no errors exist
if the FFT meshes contain all $\mathbf{G}$ vectors up to $2 G\_{\rm cut}$.

Fig. 1: Sphere intersections for $G\_{\mathrm{cut}}$

It can be shown that the charge density contains
components up to $2 G\_{\mathrm{cut}}$, where $2 G\_{\mathrm{cut}}$ is
the "longest" plane wave in the basis set:

The wavefunction is defined as

:   :   $$| \phi\_{n\mathbf{k}} \rangle = \sum\_\mathbf{G} C\_{\mathbf{G}n\mathbf{k}} | \mathbf{k}+\mathbf{G}\rangle,$$

and in real space it is given by

:   :   $$\langle \mathbf{r}| \phi\_{n\mathbf{k}} \rangle = \sum\_\mathbf{G} \langle \mathbf{r}| \mathbf{k}+\mathbf{G}\rangle \langle \mathbf{k}+\mathbf{G}|\phi\_{n\mathbf{k}} \rangle
        = \frac{1}{\Omega^{1/2}} \sum\_\mathbf{G} e^{i(\mathbf{k}+\mathbf{G})\mathbf{r}} C\_{\mathbf{G}n\mathbf{k}}.$$

Using FFTs one can define

:   :   $$C\_{\mathbf{r}n\mathbf{k}}= \sum\_{\mathbf{G}} C\_{\mathbf{G}n\mathbf{k}} e^{i\mathbf{G} \mathbf{r}} \qquad \qquad \qquad
        C\_{\mathbf{G}n\mathbf{k}}= \frac{1}{N\_{\mathrm{FFT}}} \sum\_{\mathbf{r}} C\_{\mathbf{r}n\mathbf{k}} e^{-i\mathbf{G} \mathbf{r}}.$$

Therefore the wavefunction can be written in real space as

:   :   $$\langle\mathbf{r}| \phi\_{n\mathbf{k}} \rangle = \phi\_{n\mathbf{k}}(r) = \frac{1}{\Omega^{1/2}} C\_{\mathbf{r}n\mathbf{k}} e^{i\mathbf{k}\mathbf{r}}.$$

The charge density is simply given by

:   :   $$\rho^{\mathrm{ps}}\_{\mathbf{r}} \equiv \langle \mathbf{r} |\rho^{\mathrm{ps}} | \mathbf{r} \rangle =
        \sum\_\mathbf{k} w\_{\mathbf{k}} \sum\_n f\_{n\mathbf{k}} \phi\_{n\mathbf{k}}(r) \phi^{\*}\_{n\mathbf{k}}(r) ,$$

and in the reciprocal mesh it can be written as

:   :   $$\rho^{\mathrm{ps}}\_\mathbf{G} \equiv
        \frac{1}{\Omega} \int \langle\mathbf{r} | \rho^{\mathrm{ps}}| \mathbf{r}\rangle e^{-i \mathbf{G}\mathbf{r}}\, d \mathbf{r} \to \frac{1}{N\_{\mathrm{FFT}}} \sum\_{\mathbf{r}} \rho^{\mathrm{ps}}\_{\mathbf{r}} e^{-i \mathbf{G}\mathbf{r}}.$$

Using the above equations for $\rho^{\mathrm{ps}}\_{\mathbf{r}}$ and $C\_{\mathbf{r}n\mathbf{k}}$ it
is very easy to show that $\rho^{\mathrm{ps}}\_{\mathbf{r}}$ contains Fourier-components up
to $2 G\_{\mathrm{cut}}$.

Generally it can be shown that
a the convolution $f\_r=f^1\_r f^2\_r$
of two functions $f^1\_r$ with Fourier-components
up to $G\_1$ and $f^2\_r$ with Fourier-components
up to $G\_2$ contains Fourier-components up to $G\_1+G\_2$.

The property of the convolution comes once again into play,
when the action of the Hamiltonian onto a wavefunction is
calculated. The action of the local-potential is given by

:   :   $$a\_{\mathbf{r}} = V\_{\mathbf{r}} C\_{\mathbf{r}n\mathbf{k}}.$$

Only the components $a\_{\mathbf{G}}$ with $|\mathbf{G}| \lt G\_{\mathrm{cut}}$ are taken into
account (see section ALGO: $a\_{\mathbf{G}}$ is added to the wavefunction
during the iterative refinement of the wavefunctions $C\_{\mathbf{G}n\mathbf{k}}$,
and $C\_{\mathbf{G}n\mathbf{k}}$ contains only components up to $G\_{\mathrm{cut}}$).
From the previous theorem we see that $a\_{\mathbf{r}}$ contains
components up to $3 G\_{\mathrm{cut}}$ ($V\_{\mathbf{r}}$ contains components up to
$2 G\_{\mathrm{cut}}$).

If the FFT mesh contains all components up to $2 G\_{\mathrm cut}$
the resulting wrap-around error is once again 0. This can
be easily seen in Fig. 1. Here we see that the small sphere contains all plane waves included in the basis set $G\lt G\_{\mathrm{cut}}$.
The charge density contains components up to $2 G\_{\mathrm{cut}}$ (second sphere), and
the acceleration $a$ components up to $3 G\_{\mathrm{cut}}$, which are reflected
in (third sphere) because of the finite size of the FFT mesh. Nevertheless
the components $a\_{\mathbf{G}}$ with $| \mathbf{G}| \lt G\_{\mathrm{cut}}$ are correct i.e.
the small sphere does not intersect with the third large sphere}

## Related tags and articles

PREC,
ENCUT,
NGX,
NGY,
NGZ

Energy cutoff and FFT meshes
