# Integrating over all orbitals

Categories: Electronic minimization, Electronic occupancy, Crystal momentum, Theory

Computing expectation values of observables *O* over all Kohn-Sham orbitals is an important concept relevant to most *ab initio* calculations.
Typically, we can evaluate these expectation values as integral over all orbitals

$\langle O \rangle = \sum\_n \frac{1}{\Omega\_{\mathrm{BZ}}} \int\_{\Omega\_{\mathrm{BZ}}}
O\_{n\mathbf{k}} \, \Theta(\epsilon\_{\mathrm{F}} - \epsilon\_{n\mathbf{k}}) \, d^{3}k,$

where ΩBZ is the volume of the Brillouin zone,
*O*n**k** is the expectation value of the observable with a single Kohn-Sham orbital,
and Θ is the Heaviside step function and limits the integral to orbitals with eigenvalues ϵn**k** below the Fermi energy ϵF.

When evaluating the integral above numerically, we need to address two concerns:
(i) We need to discretize the **k**-point integral since we do not know the analytic expression of the observable.
(ii) A sharp function cutoff like the Heaviside function is numerically unstable so we need robust smearing methods.

## Integrating over **k** points

Discretizing the **k**-point integral involves replacing the continuous integral over the Brillouin zone by a **k**-point mesh.

$\frac{1}{\Omega\_{\mathrm{BZ}}} \int\_{\Omega\_{\mathrm{BZ}}} \to \sum\_{\mathbf{k}} w\_{\mathbf{k}}.$

A **k**-point mesh consists of **k**-point coordinates and associated weights *w***k**.
In general, any mesh could be chosen but for periodic boundaries the optimal one are equidistant grids.
In VASP, we select this sampling by a KPOINTS file or the KSPACING tag.

We can improve the integrals further because the crystal exhibits certain symmetries.
Often we can deduce the value *O*n**k** from a different symmetry-equivalent **k** point.
VASP automatically analyzes the symmetry of the crystal and reduces the **k** point mesh to the irreducible Brillouin zone.
The weights of each irreducible **k** point measure how many equivalent **k** points exist in the reducible Brillouin zone.

## Integrating near the Fermi energy

Occupation of different smearing techniques near the Fermi energy ϵF. The energy is measured in units of the smearing σ (SIGMA). The Methfessel-Paxton method (cyan) is closer to the step function than the Gaussian distribution (blue) but also has nonmonotonous features. The smearing Fermi-Dirac distribution (purple) corresponds to a temperature but is much broader at the same value of σ.

We want to replace the Heaviside step function by a smooth equivalent to make the integral numerically stable.
Otherwise small changes in the energies would toggle the inclusion of a sample *O*n**k** close to the Fermi energy.

$\sum\_{n\mathbf{k}} \Theta(\epsilon\_{\mathrm{F}} - \epsilon\_{n\mathbf{k}}) \ldots \to \sum\_{n\mathbf{k}} f\_\sigma(\epsilon\_{n\mathbf{k}}) \ldots$

Here, the occupations *f*σ(ϵn**k**) approach 1 for energies far below the Fermi energy ϵF and 0 for energies far above it.
The parameter σ determines how wide the broadened step function is.

In the figure, we illustrate the different smearing methods implemented in VASP.
The Fermi-Dirac smearing (`ISMEAR = -1`) uses σ as the temperature in the Fermi-Dirac distribution

$f\_\sigma(\epsilon) = \Bigl[\exp(\frac{\epsilon-\epsilon\_{\mathrm{F}}}{\sigma})+1\Bigr]^{-1}~.$

One can also use the complementary error function (`ISMEAR = 0`) which results from integrating a Gaussian distribution as the occupation function.
This leads to a narrower edge than the Fermi-Dirac distribution for the same σ and a faster approach to the asymptotic behavior

$f\_\sigma(\epsilon) = \frac{1}{2} \text{erfc}\Bigl[\frac{\epsilon-\epsilon\_{\mathrm{F}}}{\sigma}\Bigr]~.$

Methfessel and Paxton developed higher order approximations to the step function (`ISMEAR > 0`).

$f\_\sigma(\epsilon) = \frac{1}{2} \text{erfc}\Bigl[\frac{\epsilon-\epsilon\_{\mathrm{F}}}{\sigma}\Bigr] + \exp\Bigl[-\bigl(\frac{\epsilon-\epsilon\_{\mathrm{F}}}{\sigma}\bigr)^2\Bigr] \sum\_{i=1}^{n} \frac{(-1)^i}{4^i i! \sqrt\pi} H\_{2i-1}\Bigl[\frac{\epsilon-\epsilon\_{\mathrm{F}}}{\sigma}\Bigr]~.$

Here, *n* is the order of the expansion and *H*j is the j-th Hermite polynomial.
The first order Methfessel-Paxton smearing is shown in the figure.
This method leads to an even narrower distribution but introduces a nonmonotonous behavior that can lead to problems in semiconductors and insulators.

A consequence of these broadening techniques is that the total energy is no longer variational (or minimal).
It is necessary to replace the total energy by some generalized free energy

$F = E - \sum\_{n\mathbf{k}} w\_{\mathbf{k}} \sigma S[f\_\sigma(\epsilon\_{n\mathbf{k}})].$

For the Fermi-Dirac statistics, we might interpret this as the free energy of the electrons at some finite temperature σ = *k*B*T*.
There is no straightforward interpretation of the free energy in the case of Gaussian or Methfessel-Paxton smearing.
Despite this, it is possible to obtain an accurate extrapolation for σ → 0 from results at finite σ using the formula

$E\_0 = E(\sigma \to 0) = \frac{1}{2} (F + E)~.$

*E*0 is a meaningful physical quantity for the ground state energy of the system.
Importantly, the calculated forces are the derivatives of the free energy *F* and not of *E*0.
Nonetheless, the difference of the forces is generally small and acceptable it a suitable σ is used.

When we consider *E*0 as our target property, the smearing methods serve as a mathematical tool to obtain faster convergence with respect to the number of k-points.
Generally, the Gaussian broadening requires more careful tuning of the width σ compared to the Methfessel-Paxton method.
If σ is too large, the energy *E*(σ → 0) will converge to the wrong value even for an infinite **k**-point mesh.
If σ is too small, we require a much denser **k**-point mesh and a significantly larger computational cost.
With the Methfessel-Paxton method the sharper edge usually averts the necessity of tuning σ.
However, since the occupation function is nonmonotonous, it is **not** suitable to describe systems with a bandgap.

## Tetrahedron method

Four **k** points forming a single tetrahedron with ordered eigenvalues ϵ1, ϵ2, ϵ3, and ϵ4. The lines show the occupation of the orbitals with changing Fermi energy ϵF where the darkest line corresponds to the lowest and the brightest line to the highest eigenvalue. For the Gaussian smearing (blue) every **k** point is considered individually leading to half filling when the Fermi energy reaches the eigenvalue. The tetrahedron method (red) does not fill any orbital if the Fermi energy is outside of the bounds of the tetrahedron.

The tetrahedron method is an alternative approach to address the sharp edge of the Heaviside step function.
Instead of considering each **k** point individually, we triangulate the **k**-point mesh, i.e., we split it into as many tetrahedra as necessary to cover the whole Brillouin zone.
We use a linear interpolation of the band energies ϵn**k** within each tetrahedron the band energies.
Blöchl derived correction terms to cancel the linearization errors of the tetrahedron method.

With this interpolation, we can solve integral over the Brillouin zone analytically considering each tetrahedron individually.
It does not require a choice of a width σ like the broadening methods.
The figure illustrates the difference between broadening and interpolation method.
A broadening method like the Gaussian smearing considers every **k** point individually.
Therefore, it will start filling the orbital as soon as the Fermi energy reaches the width σ of the broadening.
In the tetrahedron method, the **k** points of the tetrahedron only get occupied once the Fermi energy exceeds the lowest eigenvalue.
Similarly, it is completely filled once the Fermi energy exceeds the maximum value.
As a consequence, the occupations of the different **k** points are much closer to each other.

Overall, the tetrahedron method yields very accurate occupations with minimal user input.
It is very well suited to obtain accurate integral (e.g. total energy) and band onsets (e.g. density of state).
The main drawback is that the Blöchel's correction of the linearization errors is not variational with respect to the partial occupancies.
Therefore the calculated forces might be wrong by a few percent.
If accurate forces are required we recommend a finite temperature method.

## Determining the Fermi energy

One important example of integrals over all orbitals is the calculation of the Fermi energy.
In this case, the observable is identity and the sum of all occupations should be equal to the number of electrons *N*e

$\sum\_{n\mathbf{k}} f\_\sigma(\epsilon\_{n\mathbf{k}}) = N\_{\mathrm{e}}~.$

This leads to a straightforward interval-bisection algorithm to compute the Fermi energy.
We guess bounds for the Fermi energy and then compute the sum of all occupations in the middle of the interval.
If this results in a number larger than the number of electrons, we replace the upper bound otherwise we replace the lower one.

Note that this algorithm is not deterministic for systems with a bandgap, where any Fermi energy in the gap would be fine.
VASP achieves more consistent results for these system by a good initial guess for the Fermi energy (see EFERMI).
This potentially leads to an early exit of the bisection algorithm so that only for metals many iterations of bisection are considered.

## Related tags and sections

KPOINTS,
ISMEAR,
SIGMA,
Smearing technique

## References

---
