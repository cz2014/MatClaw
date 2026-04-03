# Berry phases and finite electric fields

Categories: Linear response, Dielectric properties, Berry phases, Theory

## Modern Theory of Polarization

### Berry phase expression for the macroscopic polarization

Calculating the change in dipole moment per unit cell under PBC's, is a nontrivial task. In general one *cannot* define it as the first moment of the induced change in charge density δ(**r**), through

:   $$\Delta \mathbf{P}= \frac{1}{\Omega\_{0}} \int\_{\Omega\_{0}} \mathbf{r} \delta
    \left(
    \mathbf{r} \right) d^{3}r$$

without introducing a dependency on the shape of Ω0, the chosen unit cell.

Recently King-Smith and Vanderbilt, building on the work of Resta, showed that the electronic contribution to the difference in polarization Δ**P**e, due to a finite adiabatic change in the Hamiltonian of a system, can be identified as a *geometric quantum phase* or *Berry phase* of the valence wave functions. We will briefly summarize the essential results (for a review of geometric quantum phases in polarization theory see the papers of Resta).

Central to the modern theory of polarization is the proposition of Resta to write the electronic contribution to the change in polarization due to a finite adiabatic change in the Kohn-Sham Hamiltonian of the crystalline solid, as

:   $$\Delta \mathbf{P}\_{e}= \int^{\lambda\_{2}}\_{\lambda\_{1}}{\partial \mathbf{P}\_{e}
    \over
    \partial \lambda} d\lambda$$

with

:   $${\partial \mathbf{P}\_{e} \over \partial \lambda}= {i |e| \hbar \over N \Omega\_{0} m\_{e}} \sum\_{\mathbf{k}} \sum^{M}\_{n=1} \sum^{\infty}\_{m=M+1} {\langle \psi^{\left(\lambda\right)}\_{n\mathbf{k}} | \mathbf{\hat{p}} | \psi^{\left(\lambda\right)}\_{m\mathbf{k}}\rangle \langle \psi^{\left(\lambda\right)}\_{m\mathbf{k}} | \partial V^{\left(\lambda\right)}/\partial \lambda | \psi^{\left(\lambda\right)}\_{n\mathbf{k}}\rangle \over \left( \epsilon^{\left(\lambda\right)}\_{n\mathbf{k}}- \epsilon^{\left(\lambda\right)}\_{m\mathbf{k}} \right)^{2}}+ \mathrm{c.c.}$$

where *me* and *e* are the electronic mass and charge, *N* is the number of unit cells in the crystal, Ω0 is the unit cell volume, *M* is the number of occupied bands, **p** is the momentum operator, and the functions ψ(λ)n**k** are the usual Bloch solutions to the crystalline Hamiltonian. Within Kohn-Sham density-functional theory, the potential V(λ) is to be interpreted as the Kohn-Sham potential V(λ)KS, where λ parameterizes some change in this potential, for instance due to the displacement of an atom in the unit cell.

King-Smith and Vanderbilt have cast this expression in a form in which the conduction band states ψ(λ)m**k** no longer explicitly appear, and they show that the change in polarization along an arbitrary path, can be found from only a knowledge of the system at the end points

:   $$\Delta \mathbf{P}\_{e}= \mathbf{P}^{\left(\lambda\_{2} \right)}\_{e} - \mathbf{P}^{\left(\lambda\_{1}\right)}\_{e}$$

with

:   $$\mathbf{P}^{\left(\lambda\right)}\_{e}=-{if|e|\over 8\pi^{3}} \sum^{M}\_{n=1}\int\_{BZ} d^{3}k \langle u^{\left(\lambda\right)}\_{n\mathbf{k}} | \nabla\_{\mathbf{k}} | u^{\left(\lambda\right)}\_{n\mathbf{k}} \rangle$$

where *f* is the occupation number of the states in the valence bands, u(λ)n**k** is the cell-periodic part of the Bloch function ψ(λ)n**k**, and the sum *n* runs over all *M* occupied bands.

The physics behind the equation above becomes more transparent when this expression is written in terms of the Wannier functions of the occupied bands,

:   $$\mathbf{P}^{\left(\lambda\right)}\_{e}=-{f |e| \over \Omega\_{0}} \sum^{M}\_{n=1}
    \langle W^{\left(\lambda\right)}\_{n} | \mathbf{r} |W^{\left(\lambda\right)}\_{n}
    \rangle$$

where Wn is the Wannier function corresponding to valence band *n*.

This shows the change in polarization of a solid, induced by an adiabatic change in the Hamiltonian, to be proportional to the displacement of the charge centers **r**n=⟨ W(λ)n|**r**| W(λ)n⟩, of the Wannier functions corresponding to the valence bands.

It is important to realize that the polarization in terms of Bloch or Wannier functions, and consequently the change in polarization, is only well-defined modulo *fe***R**/Ω0, where **R** is a lattice vector. This indeterminacy stems from the fact that the charge center of a Wannier function is only invariant modulo **R**, with respect to the choice of phase of the Bloch functions.

In practice one is usually interested in polarization changes |Δ**P**e| << |*fe***R**1/Ω0|, where **R**1 is the shortest nonzero lattice vector. An arbitrary term *fe***R**/Ω0 can therefore often be removed by simple inspection of the results. In cases where |Δ**P**e| is of the same order of magnitude as *fe***R**1/Ω0 any uncertainty can always be removed by dividing the total change in the Hamiltonian λ1→λ2 into a number of intervals.

### Computational aspects

In general, the direct evaluation of **P**e(λ) is useless, because there is no specific relationship between the phases of the eigenvectors u(λ)**k**n generated by a numerical diagonalization
routine. This problem is circumvented by dividing the Brillouin zone integration in two parts, a two-dimensional integral and a line integral, and by transforming the above into three equations, which separately provide the components of **P**e(λ) along the directions of three reciprocal lattice vectors **G**1, **G**2, and **G**3, which together span a unit cell of the reciprocal lattice. The component of **P**e(λ) along for instance **G**1 can be found from

:   $$\mathbf{G}\_{1} \cdot \mathbf{P}\_{e}^{\left(\lambda\right)}=-{if|e|\over 8\pi^{3}}
    \int\_{A} dk\_{2}dk\_{3} \sum^{M}\_{n=1} \int^{|\mathbf{G}\_{1}|}\_{0} dk\_{1} \langle
    u^{\left(\lambda\right)}\_{n\mathbf{k}} |\partial/\partial k\_{1} |
    u^{\left(\lambda\right)}\_{n\mathbf{k}} \rangle$$

where the two-dimensional integral is taken over the area *A*, spanned by **G**2 and **G**3, and the line integral runs over a line segment parallel to **G**1. Interchanging the indices *1*, *2* and *3* in  the equation above yields the expressions for two other components of **P**e(λ).

Thus the electronic part of the polarization **P**e(λ) is given (modulo *fe***R**/Ω0) by the sum

:   $$\sum^{3}\_{i=1}(\mathbf{P}\_{e}^{\left(\lambda\right)})\_{i}=\sum^{3}\_{i=1}
    \left(\mathbf{G}\_{i} \cdot \mathbf{P}\_{e}^{\left(\lambda\right)}\right)
    {\mathbf{R}\_{i}
    \over 2\pi}$$

where the lattice vectors **R**i obey the relationship **R**i·**G**j=2πδij.

The integration over *A* in the above, is straightforward and can be performed by sampling a 2D Monkhorst-Pack mesh of *k*-points, termed the *perpendicular mesh* or **k**⊥-mesh by King-Smith and Vanderbilt. However, to remove the influence of the random phase of the functions u(λ)n**k**, introduced by the diagonalization routine, King-Smith and Vanderbilt propose to replace the line integral alias integration in the *parallel* or **G**|| direction by,

:   $$\phi^{\left(\lambda\right)}\_{J}\left(\mathbf{k}\_{\perp}\right)=\mathrm{Im}
    \left\{\ln \prod^{J-1}\_{j=0} \mathrm{det} \left( \langle
    u^{\left(\lambda\right)}\_{m\mathbf{k}\_{j}} | u^{\left(\lambda\right)}\_{n\mathbf{k}\_{j+1}}\rangle \right)\right\}$$

which is evaluated by calculating the cell-periodic parts of the wave functions at a string of *J* *k*-points, **k**j= **k**⊥+j**G**||/*J* (with *j*=0,..,*J*-1), and where for sufficiently large *J* one has that

:   $$\phi^{\left(\lambda\right)}\_{J}\left(\mathbf{k}\_{\perp}\right)= -i\sum^{M}\_{n=1}
    \int^{|\mathbf{G}\_{\parallel}|}\_{0} dk\_{\parallel} \langle
    u^{\left(\lambda\right)}\_{n\mathbf{k}} | \partial/\partial k\_{\parallel} |
    u^{\left(\lambda\right)}\_{n\mathbf{k}} \rangle$$

**Note**: the determinant appearing in the equation above is the determinant of the *M*×*M* matrix formed by letting *n* and *m* run over all valence bands.

The crucial step, instrumental in removing the random phase, is that the functions u(λ)n**k**J are not obtained from an independent diagonalization, but found through their relationship with the functions u(λ)n**k**0,

:   $$u^{\left(\lambda\right)}\_{n\mathbf{k}\_{J}}(\mathbf{r})=
    e^{-i\mathbf{G}\_{\parallel}\cdot \mathbf{r}} u^{\left(\lambda\right)}\_{n\mathbf{k}\_{0}}(\mathbf{r})$$

This way the product φJ(λ) becomes cyclic, and contains both u(λ)n**k**j as well as its complex conjugate for every *k*-point in the string, thus removing the random phase.

In practice **G**||·**P**e(λ) is evaluated by way of the following summation over the **k**⊥-mesh,

:   $$(\mathbf{P}\_{e}^{\left(\lambda\right)})\_{i} = \frac{f|e|\mathbf{R}\_{i}}{2\pi\Omega\_{0}}
    \left(\frac{1}{N\_{k\_{\perp}}}\sum\_{\mathbf{k}\_{\perp}} \mathrm{Im}\ln \frac{D^{\left(\lambda\right)}\_{J}\left(\mathbf{k}\_{\perp}\right)}{\langle D \rangle}
    +\mathrm{Im}\ln \langle D \rangle\right)$$

where

:   $$D^{\left(\lambda\right)}\_{J}\left(\mathbf{k}\_{\perp}\right)=
    \prod^{J-1}\_{j=0} \mathrm{det} \left( \langle
    u^{\left(\lambda\right)}\_{m\mathbf{k}\_{j}} | u^{\left(\lambda\right)}\_{n\mathbf{k}\_{j+1}}\rangle \right)$$

with **k**j= **k**⊥+j**G**||/*J* (with *j*=0,..,*J*-1), and

:   $$\langle D \rangle = \frac{1}{N\_{k\_{\perp}}}\sum\_{\mathbf{k}\_{\perp}}
    D^{\left(\lambda\right)}\_{J}\left(\mathbf{k}\_{\perp}\right),$$

and where we used **R**i·**G**j=2πδij.

Assuming the *D*J(λ)(**k**⊥) are reasonably well-clustered around ⟨*D*⟩, all terms *D*J(λ)(**k**⊥)/⟨*D*⟩ will lie on the same branch of the logarithm.
This makes it less likely that (**P**e(λ))i will pick up a spurious contribution (of *n***R**i/*N***k**⊥).

## Self-consistent response to finite electric fields

As of version 5.2, VASP can calculate the ground state of an insulating system under the application of a finite homogeneous electric field. The VASP implementation closely follows the *PEAD* (Perturbation Expression After Discretization) approach of Nunes and Gonze and the work of Souza *et al.*.

In short: to determine the ground state of an insulating system under the application of a finite homogeneous electric field *ε*, VASP solves for the field-polarized Bloch functions {*ψ*(*ε*)} by minimizing the electric enthalpy functional:

:   $$E[\{\psi^{({\mathcal E})}\},{\mathcal E}]=
    E\_{0}[\{\psi^{({\mathcal E})}\}]-\Omega
    {\mathcal E} \cdot \mathbf{P}[\{\psi^{({\mathcal E})}\}],$$

where **P**[{*ψ*(*ε*)}] is the macroscopic polarization as defined in the modern theory of polarization:

:   $$\mathbf{P}[\{\psi^{({\mathcal E})}\}]=-\frac{2ie}{(2\pi)^3}\sum\_n
    \int\_{\mathrm{BZ}} d\mathbf{k} \langle u^{({\mathcal E})}\_{n\mathbf{k}}|
    \nabla\_{\mathbf{k}}| u^{({\mathcal E})}\_{n\mathbf{k}} \rangle$$

and u(*ε*)n**k** is the cell-periodic part of *ψ*(*ε*)n**k**.

The second term on the right-hand side of the electric enthalpy functional introduces a corresponding additional term to the Hamiltonian

:   $$H |\psi^{({\mathcal E})}\_{n\mathbf{k}}\rangle=H\_0 |\psi^{({\mathcal E})}\_{n\mathbf{k}}\rangle
    -\Omega {\mathcal E}\cdot \frac{\delta \mathbf{P}\left[\{\psi^{({\mathcal E})} \}\right]}{\delta \langle \psi^{({\mathcal E})}\_{n\mathbf{k}}|}.$$

Following the work of Nunes and Gonze we write,

:   $$\frac{\delta \mathbf{P}\left[\{\psi^{({\mathcal E})} \}\right]}{\delta \langle \psi^{({\mathcal E})}\_{n\mathbf{k}}|}=
    -\frac{ie}{2\Delta k} \sum^N\_{m=1}
    \left[ | u^{({\mathcal E})}\_{m\mathbf{k}\_{j+1}} \rangle S^{-1}\_{mn}(\mathbf{k}\_j,\mathbf{k}\_{j+1}) -
    | u^{({\mathcal E})}\_{m\mathbf{k}\_{j-1}} \rangle S^{-1}\_{mn}(\mathbf{k}\_j,\mathbf{k}\_{j-1})\right]$$

where *m* runs over the *N* occupied bands of the system, Δ*k*=|**k**j+1-**k**j|, and

:   $$S\_{nm}(\mathbf{k}\_j,\mathbf{k}\_{j+1})=
    \langle u^{({\mathcal E})}\_{n\mathbf{k}\_{j}}| u^{({\mathcal E})}\_{m\mathbf{k}\_{j+1}}\rangle .$$

This Hamiltonian allows one to solve for {*ψ*(*ε*)} by means of a direct optimization method.

**Note**: By analogy, it can be shown that

:   $$\frac{\partial |u\_{n\mathbf{k}\_j} \rangle}{\partial k}=
    \frac{ie}{2\Delta k} \sum^N\_{m=1}
    \left[ | u^{({\mathcal E})}\_{m\mathbf{k}\_{j+1}} \rangle S^{-1}\_{mn}(\mathbf{k}\_j,\mathbf{k}\_{j+1}) -
    | u^{({\mathcal E})}\_{m\mathbf{k}\_{j-1}} \rangle S^{-1}\_{mn}(\mathbf{k}\_j,\mathbf{k}\_{j-1})\right]$$

in the sense of a first-order finite difference scheme (higher-order stencils may be similarly defined).

**Note**: One should be aware that when the electric field is chosen to be too large, the electric enthalpy functional will lose its minima, and VASP will not be able to find a stationary solution for the field-polarized orbitals.
This is discussed in some detail by Souza *et al.*.
VASP will produce a warning if:

:   $$e|\mathcal{E}\cdot \mathbf{a}\_i|\gt \frac{1}{10}E\_{\mathrm{gap}}/N\_i,$$

where *E*gap is the bandgap, **a**i are the lattice vectors, and *N*i is the number of **k**-points along the reciprocal lattice vector *i*, in the regular (*N*1×*N*2×*N*3) **k**-mesh. The factor 1/10 is chosen to be on the safe side. If one does not include unoccupied bands, VASP is obviously not able to determine the bandgap and can not check whether the electric field might be too large. This will also produce a warning message.

### Response properties

The change in the macroscopic polarization due to the electric field *ε* defines the ion-clamped static dielectric tensor

:   $$\epsilon^\infty\_{ij}=\delta\_{ij}+
    \frac{4\pi}{\epsilon\_0}\frac{\partial P\_i}{\partial {\mathcal E}\_j},
    \qquad
    {i,j=x,y,z},$$

the change in the Hellmann-Feynman forces due to *ε*, the Born effective charge tensors

:   $$Z^\*\_{ij}=\frac{\Omega}{e}\frac{\partial P\_i}{\partial u\_j}
    =\frac{1}{e}\frac{\partial F\_j}{\partial \mathcal{E}\_i},
    \qquad
    {i,j=x,y,z},$$

and the ion-clamped piezoelectric tensor of the system

:   $$e^{(0)}\_{ij}=-\frac{\partial \sigma\_i}{\partial \mathcal{E}\_j},
    \qquad
    {i=xx, yy, zz, xy, yz, zx}\quad{j=x,y,z},$$

is found as the change in the stress tensor.

## Related Tags and Sections

LCALCPOL,
LCALCEPS,
EFIELD\_PEAD,
LPEAD,
IPEAD,
LBERRY,
IGPAR,
NPPSTR,
DIPOL

## References

---
