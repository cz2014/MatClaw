# FOCKCORR

Categories: INCAR tag, Hybrid functionals

FOCKCORR = 1 | 2

|  |  |  |
| --- | --- | --- |
| Default: **FOCKCORR** | = 2 | if LMAXFOCKAE>0 |
|  | = 1 | else |

Description: The tag FOCKCORR determines how the Coulomb convergence corrections are applied.

---

The Coulomb potential in reciprocal space

:   $$V(G)=\frac{4\pi e^2}{G^2}$$

diverges for small G vectors.
To alleviate this issue and improve the convergence of the exact exchange integral with respect to supercell size (or k-point mesh density) different methods have been proposed: the auxiliary function methods, probe-charge Ewald (HFALPHA), and Coulomb truncation methods (HFRCUT).
These mostly involve modifying the Coulomb Kernel in a way that yields the same result as the unmodified kernel within the limit of large supercell sizes.

These corrections are implemented in VASP either by changing the $\mathbf{G}=0$ component of the Coulomb kernel when FOCKCORR=1

:   $$\Phi(\mathbf{G}) =
    \left\{
    \begin{array}{lr}
    \frac{4\pi e^2}{\Omega} \frac{1}{G^2} & \mathbf{G} \neq 0\\
    \chi & \mathbf{G} = 0
    \end{array}
    \right.$$

with $\chi$ being the value of the correction and depends on whether HFALPHA or HFRCUT are set,
or by including the original orbital scaled by the convergence correction when FOCKCORR=2

:   $$\langle \mathbf{k}+\mathbf{G}' | V^\text{HF}\_\text{x} | \mathbf{k}+\mathbf{G} \rangle =
    - \sum\_{m\mathbf{q}}f\_{m\mathbf{q}}\sum\_{\mathbf{G}''}
    C^\*\_{m\mathbf{q}}(\mathbf{G}'-\mathbf{G}'') \Phi(\mathbf{k}-\mathbf{q}+\mathbf{G}'') C\_{m\mathbf{q}}(\mathbf{G}-\mathbf{G}'')$$

:   $$\begin{aligned}
    \langle \mathbf{k}+\mathbf{G}' |\hat{V}^\text{HF}\_{\text{x}} | \psi\_{\mathbf{k}n} \rangle
    &=
    - \sum\_{m\mathbf{q}}f\_{m\mathbf{q}}\sum\_{\mathbf{G}''}
    C^\*\_{m\mathbf{q}}(\mathbf{G}'-\mathbf{G}'') \Phi(\mathbf{k}-\mathbf{q}+\mathbf{G}'') C\_{m\mathbf{q}}(\mathbf{G}-\mathbf{G}'')
    C\_{n\mathbf{k}}(\mathbf{G})\\
    &=
    - \chi\sum\_{m\mathbf{q}}f\_{m\mathbf{q}}
    C\_{m\mathbf{q}}(\mathbf{G})
    \end{aligned}$$

For Hartree-Fock or hybrid functional calculations, either FOCKCORR=1 or FOCKCORR=2 can be used and should yield the same results when LMAXFOCKAE=-1 and there are no aliasing errors in the exact exchange (see PRECFOCK for more details).
For post-DFT methods such as ACDFT, GW, and BSE the FOCKCORR=2 should be used because the overlap densities are reconstructed in the plane-wave grid (see LMAXFOCKAE tag).

Note that in the case FOCKCORR=2 the corrections are only applied to orbitals in the $\mathbf{q}$ regular grid used to describe the exact exchange potential so this method cannot be used to compute band structures where this potential is applied to orbitals $n\mathbf{k}$ not in the $m\mathbf{q}$ set.

> **Warning:** FOCKCORR=2 should **not** be used when computing the band structure along a path with the 0-weight scheme or KPOINTS\_OPT

In previous versions of VASP,
FOCKCORR=1 was used when ALGO=Normal; LFOCKACE=.FALSE. and
FOCKCORR=2 when ALGO=All or ALGO=Normal; LFOCKACE=.TRUE. .

> **Mind:** Only available as of VASP 6.3.1.

## Related tags and articles

HFRCUT,
HFALPHA

Examples that use this tag

---
