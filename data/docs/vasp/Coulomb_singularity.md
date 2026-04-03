# Coulomb singularity

Categories: Exchange-correlation functionals, Hybrid functionals, Theory

The bare Coulomb operator

:   $$V(\vert\mathbf{r}-\mathbf{r}'\vert)=\frac{1}{\vert\mathbf{r}-\mathbf{r}'\vert}$$

in the unscreened HF exchange has a representation in the reciprocal space that is given by

:   $$V(q)=\frac{4\pi}{q^2}$$

It has an (integrable) singularity at $q=\vert\mathbf{k}'-\mathbf{k}+\mathbf{G}\vert=0$ that leads to a very slow convergence of the results with respect to the cell size or number of **k** points. In order to alleviate this issue different methods have been proposed: the auxiliary function , probe-charge Ewald (HFALPHA), and Coulomb truncation methods (selected with HFRCUT). These mostly involve modifying the Coulomb Kernel in a way that yields the same result as the unmodified kernel in the limit of large supercell sizes.
These methods can also be applied to the Thomas-Fermi and error function screened Coulomb operators given by

:   $$V(\vert\mathbf{r}-\mathbf{r}'\vert)=\frac{e^{-\lambda\left\vert\mathbf{r}-\mathbf{r}'\right\vert}}{\left\vert\mathbf{r}-\mathbf{r}'\right\vert}$$

and

:   $$V(\vert\mathbf{r}-\mathbf{r}'\vert)=\frac{\text{erfc}\left({-\lambda\left\vert\mathbf{r}-\mathbf{r}'\right\vert}\right)}{\left\vert\mathbf{r}-\mathbf{r}'\right\vert}$$

respectively, whose representations in the reciprocal space are given by

:   $$V(q)=\frac{4\pi}{q^{2}+\lambda^{2}}$$

and

:   $$V(q)=\frac{4\pi}{q^{2}}\left(1-e^{-q^{2}/\left(4\lambda^2\right)}\right)$$

respectively.

### Auxiliary function

In this approach an auxiliary periodic function $F(q)$ with the same $1/q^2$ divergence as the Coulomb potential in reciprocal space is subtracted in the **k** points used to integrate the Hartree-Fock energy, thus regularizing the integral. This function is chosen such that it has a closed analytical expression for its integral or the integral is evaluated numerically. This approach is currently not implemented in VASP, instead, the probe-charge Ewald method is used.

### Probe-charge Ewald

A similar approach to the auxiliary function method described above is the probe-charge Ewald method . In this case, the auxiliary function $F(q)$ is chosen to have the form of the Coulomb kernel times a Gaussian function $e^{-\alpha q^2}$ with a width $\alpha$ (HFALPHA) comparable to the Brillouin zone diameter.
This function is used to regularize the Coulomb integral that is evaluated in the regular **k** point grid with the divergent part being evaluated by analytical integration of the Coulomb kernel (see eq. 29 in ref. ).
The value of the integral of the bare Coulomb potential is (see eq. 31 in ref. )

:   $$\begin{aligned}
    \frac{1}{2\pi^2} \int \frac{4\pi}{\mathbf{|q|}^2} e^{-\alpha\mathbf{|q|}^2} d\mathbf{q}=
    \frac{2}{\pi} \int \frac{1}{q^2} e^{-\alpha q^2} q^2 dq =
    \frac{2}{\pi} \int e^{-\alpha q^2} dq= \frac{1}{\sqrt{\pi \alpha}}
    \end{aligned}$$

for the Thomas-Fermi and error function screened Coulomb kernels we have

:   $$\begin{aligned}
    \frac{1}{2\pi^2} \int \frac{4\pi}{\mathbf{|q|}^2+\lambda^2} e^{-\alpha\mathbf{|q|}^2} d\mathbf{q}=
    \frac{2} {\pi} \int \frac{q^2}{q^2+\lambda^2} e^{-\alpha q^2} q^2 dq =
    -\lambda e^{\alpha \lambda^2} \text{erfc}({\lambda \sqrt{\alpha}}) + \frac{1}{\sqrt{\pi \alpha}}
    \end{aligned}$$

and

:   $$\begin{aligned}
    \frac{1}{2\pi^2} \int \frac{4\pi}{\mathbf{q}^2}
    \left(
    1-e^{-\mathbf{|q|}^2/(4\lambda^2)}
    \right) e^{-
    \alpha\mathbf{|q|}^2} d\mathbf{q}=
    \frac{2}{\pi} \int \frac{1}{q^2}
    \left(
    1-e^{-q^2/(4\lambda^2)}
    \right) e^{-\alpha q^2} q^2 dq =
    \frac{1}{\sqrt{\pi \alpha}} -
    \frac{1}{\sqrt{\pi \left(\alpha+\frac{1}{4\lambda^2}\right)}}
    \end{aligned}$$

respectively.

### Spherical truncation

In this method the bare Coulomb operator $V(\vert\mathbf{r}-\mathbf{r}'\vert)$ is spherically truncated by multiplying it by the step function $\theta(R\_{\text{c}}-\left\vert\mathbf{r}-\mathbf{r}'\right\vert)$, and in the reciprocal this leads to

:   $$V(q)=\frac{4\pi}{q^{2}}\left(1-\cos(q R\_{\text{c}})\right)$$

whose value at $q=0$ is finite and is given by $V(q=0)=2\pi R\_{\text{c}}^{2}$, where the truncation radius $R\_{\text{c}}$ (HFRCUT) is by default chosen as $R\_{\text{c}}=\left(3/\left(4\pi\right)N\_{\mathbf{k}}\Omega\right)^{1/3}$ with $N\_{\mathbf{k}}$ being the number of $k$-points in the full Brillouin zone.

The screened potentials have no singularity at $q=0$. Nevertheless, it is still beneficial for accelerating the convergence with respect to the number of **k** points to multiply these screened operators by $\theta(R\_{\text{c}}-\left\vert\mathbf{r}-\mathbf{r}'\right\vert)$, which in the reciprocal space gives

:   $$V(q)=\frac{4\pi}{q^{2}+\lambda^{2}}
    \left(
    1-e^{-\lambda R\_{\text{c}}}\left(\frac{\lambda}{q}
    \sin\left(qR\_{\text{c}}\right) +
    \cos\left(qR\_{\text{c}}\right)\right)\right)$$

and

:   $$V(q)=\frac{4\pi}{q^{2}}
    \left(
    1-\cos(qR\_{\text{c}})\text{erfc}\left(\lambda R\_{\text{c}}\right) -
    e^{-q^{2}/\left(4\lambda^2\right)}
    \Re\left({\text{erf}\left(\lambda R\_{\text{c}} +
    \text{i}\frac{q}{2\lambda}\right)}\right)\right)$$

respectively, with the following values at $q=0$:

:   $$V(q=0)=\frac{4\pi}{\lambda^{2}}\left(1-e^{-\lambda R\_{\text{c}}}\left(\lambda R\_{\text{c}} + 1\right)\right)$$

and

:   $$V(q=0)=2\pi\left(R\_{\text{c}}^{2}\text{erfc}(\lambda R\_{\text{c}}) -
    \frac{R\_{\text{c}}e^{-\lambda^{2}R\_{\text{c}}^{2}}}{\sqrt{\pi}\lambda} +
    \frac{\text{erf}(\lambda R\_{\text{c}})}{2\lambda^{2}}\right)$$

Note that the spherical truncation method described above works very well in the case of 3D systems. However, it is not recommended for systems with a lower dimensionality. For such systems, the approach proposed in ref. (not implemented in VASP) is more adapted since the truncation is done according to the Wigner-Seitz cell and therefore more general.

## Related tags and articles

HFRCUT,
FOCKCORR,
Hybrid functionals: formalism,
Downsampling of the Hartree-Fock operator

## References

---
