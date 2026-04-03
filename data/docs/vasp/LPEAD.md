# LPEAD

Categories: INCAR tag, Linear response, Dielectric properties, Berry phases

LPEAD = .TRUE. | .FALSE  
 Default: **LPEAD** = .FALSE.

Description: for LPEAD=.TRUE., the derivative of the cell-periodic part of the orbitals w.r.t. **k**, |∇**k**un**k**⟩, is calculated using finite differences ("perturbation expansion after discretization" (PEAD)).

---

The derivative of the cell-periodic part of the orbitals w.r.t. **k**, **k**, |∇**k**un**k**⟩, may be written as:

:   $$|\mathbf{\nabla\_{k}} \tilde{u}\_{n\mathbf{k}} \rangle =
    \sum\_{n\neq n'}
    \frac{| \tilde{u}\_{n'\mathbf{k}} \rangle \langle \tilde{u}\_{n'\mathbf{k}} |
    \frac{\partial\left[H(\mathbf{k})-\epsilon\_{n\mathbf{k}}S(\mathbf{k})\right]}{\partial \mathbf{k}}
    | \tilde{u}\_{n\mathbf{k}} \rangle}{\epsilon\_{n\mathbf{k}}-\epsilon\_{n'\mathbf{k}}}$$

where H(**k**) and S(**k**) are the Hamiltonian and overlap operator for the cell-periodic part of the orbitals, and the sum over *n*´ must include a sufficiently large number of unoccupied states.

It may also be found as the solution to the following linear Sternheimer equation (see LEPSILON):

:   $$\left[H(\mathbf{k})-\epsilon\_{n\mathbf{k}}S(\mathbf{k})\right]
    |\mathbf{\nabla\_{k}} \tilde{u}\_{n\mathbf{k}} \rangle
    =-\frac{\partial\left[H(\mathbf{k})-\epsilon\_{n\mathbf{k}}S(\mathbf{k})\right]}
    {\partial \mathbf{k}}|\tilde{u}\_{n\mathbf{k}} \rangle$$

Alternatively one may compute $\nabla\_{\mathbf{k}} \tilde{u}\_{n\mathbf{k}}$ from finite differences (LPEAD=.TRUE.):

:   $$\frac{\partial | \tilde{u}\_{n\mathbf{k}\_j} \rangle}{\partial k}=
    \frac{ie}{2\Delta k} \sum^N\_{m=1}
    \left[ | \tilde{u}\_{m\mathbf{k}\_{j+1}} \rangle
    S^{-1}\_{mn}(\mathbf{k}\_j,\mathbf{k}\_{j+1})\rangle -
    | \tilde{u}\_{m\mathbf{k}\_{j-1}} \rangle
    S^{-1}\_{mn}(\mathbf{k}\_j,\mathbf{k}\_{j-1})\rangle\right]$$

where *m* runs over the *N* occupied bands of the system, Δ*k*=**k**j+1-**k**j, and

:   $S\_{nm}(\mathbf{k}\_j,\mathbf{k}\_{j+1})=
    \langle \tilde{u}\_{n\mathbf{k}\_{j}}| \tilde{u}\_{m\mathbf{k}\_{j+1}}\rangle$.

As mentioned in the context of the self-consistent response to finite electric fields one may derive analoguous expressions for |∇**k**un**k**⟩ using higher-order finite difference approximations.

When LPEAD=.TRUE., VASP will compute |∇**k**un**k**⟩ using the aforementioned finite difference scheme. The order of the finite difference approximation can be specified by means of the IPEAD-tag (default: IPEAD=4).

These tags may be used in combination with LOPTICS=.TRUE. and LEPSILON=.TRUE..

---

* N.B. Please note that LPEAD = .TRUE. **is not supported for metallic systems**.

## Related tags and articles

IPEAD,
LEPSILON,
LOPTICS,
LCALCEPS,
EFIELD\_PEAD,
Berry phases and finite electric fields

Examples that use this tag

## References

---

---
