# EFERMI_NEDOS

Categories: INCAR tag, Electronic occupancy, Density of states

EFERMI\_NEDOS = [integer]  
 Default: **EFERMI\_NEDOS** = 21

Description: Number of Gauss–Legendre integration points used to evaluate the Fermi–Dirac distribution and determine the Fermi level at finite temperature using the tetrahedron method only with ISMEAR = −14 or -15 .

> **Mind:** Available as of VASP 6.5.0

---

**EFERMI\_NEDOS** sets the number of points in the Gauss–Legendre grid used to integrate the Fermi–Dirac distribution for determining the Fermi level within the  tetrahedron method when ISMEAR = −14 or -15 .
Larger values improve accuracy, especially at low temperatures or with sharp features in the electronic DOS, but also increase computational cost.
A brief convergence test is recommended in case very accurate occupancies are required, e.g., in the context of transport calculations.

## Implementation details

At $T=0$, the integrated and differential densities of states are
$$
n(\epsilon)=\sum\_{n\mathbf{k}}\theta(\epsilon-\epsilon\_{n\mathbf{k}}), \qquad
g(\epsilon)=\sum\_{n\mathbf{k}}\delta(\epsilon-\epsilon\_{n\mathbf{k}}).
$$

At finite temperature,
$$
N\_e(\epsilon\_F,T)=
\sum\_{n\mathbf{k}}f(\epsilon\_{n\mathbf{k}}-\epsilon\_F,T)
=\int g(\epsilon)f(\epsilon-\epsilon\_F,T)\,d\epsilon.
\tag{1}
$$

With the substitution $x = 1 - 2f(\epsilon-\epsilon\_F,T)$,
$$
\epsilon = k\_BT\ln\!\frac{1+x}{1-x}+\epsilon\_F, \qquad
d\epsilon = -k\_BT\,\frac{2}{x^2-1}\,dx,
$$
Eq. (1) becomes
$$
N\_e(\epsilon\_F,T)=
\frac{1}{2}\int\_{-1}^{1}
n\!\left(k\_BT\ln\!\frac{1+x}{1-x}+\epsilon\_F\right)\,dx.
$$

In practice, this integral is discretized as
$$
N\_e(\epsilon\_F,T)\simeq
\frac{1}{2}\sum\_{i=1}^{N}w\_i\,
n\!\left(k\_BT\ln\!\frac{1+x\_i}{1-x\_i}+\epsilon\_F\right),
$$
where $w\_i$ and $x\_i$ are Gauss–Legendre weights and abscissas.
The step functions \(\theta(\epsilon-\epsilon\_{n\mathbf{k}})\) entering \(n(\epsilon)\) are evaluated using the tetrahedron method, with the number of energy points $N$ given by EFERMI\_NEDOS.

## Related tags and articles

ISMEAR,
SIGMA,
Smearing technique,
K-point integration
