# ELPH_DECOMPOSE

Categories: INCAR tag, Electron-phonon interactions

ELPH\_DECOMPOSE = [string]  
 Default: **ELPH\_DECOMPOSE** = VDPR

Description: Chooses which contributions to include in the computation of the electron-phonon matrix elements.

> **Mind:** Available as of VASP 6.5.0

---

The electron-phonon matrix element can be formulated in the projector-augmented-wave (PAW) method in terms of individual contributions.
Each contribution can be included by specifying the associated letter in ELPH\_DECOMPOSE.
We suggest two different combinations to define matrix elements:

`ELPH_DECOMPOSE = VDPR` - "All-electron" (AE) matrix element
:   This is the de-facto standard definition of the electron-phonon matrix element expressed in the language of the PAW method. The AE matrix element can be used in the framework of many-body perturbation theory without any further restrictions. It should also be used if one is not interested in the final observables, but in the values of the matrix elements themselves, for example, to study scattering channels.

`ELPH_DECOMPOSE = VDQ` - "Pseudo" (PS) matrix element
:   This matrix element arises naturally from the PAW formulation of the phonon-induced band-structure renormalization in the adiabatic Rayleigh-Schrödinger perturbation theory. It is only really well-defined in this particular context. However, when using this much smoother PS matrix element instead of the AE matrix element, the electron self-energy converges much faster with respect to the number of intermediate states. Despite its definition from an adiabatic theory, we recommend to use the PS matrix element also to compute the  non-adiabatic band-structure renormalization. In our experience, the PS matrix element is furthermore well suited to perform  transport calculations, since the difference between AE and PS matrix elements is small for scattering processes close to the Fermi edge. In any case, it is always recommended to compare observables computed with the PS matrix elements against the same observables computed with the AE matrix elements.

## Available contributions

V - Derivative of pseudopotential, $\tilde{v}$
:   $$g^{(\text{V})}\_{m \mathbf{k}', n \mathbf{k}, a}
    \equiv
    \langle
    \tilde{\psi}\_{m \mathbf{k}'} |
    \frac{\partial \tilde{v}}{\partial u\_{a}} |
    \tilde{\psi}\_{n \mathbf{k}}
    \rangle$$
:   This term is the pure plane-wave contribution to the total PAW matrix element. If the PAW augmentation region were vanishingly small, this would be the sole contribution.

D - Derivative of PAW strength parameters, $D\_{a, ij}$
:   $$g^{(\text{D})}\_{m \mathbf{k}', n \mathbf{k}, a}
    \equiv
    \sum\_{bij}
    \langle
    \tilde{\psi}\_{m \mathbf{k}'} |
    \tilde{p}\_{b i}
    \rangle
    \frac{\partial D\_{b, ij}}{\partial u\_{a}}
    \langle
    \tilde{p}\_{b j} |
    \tilde{\psi}\_{n \mathbf{k}}
    \rangle$$
:   This contribution stems from the PAW treatment of the electronic Hamiltonian. It is of the same nature as $g^{(\text{V})}$ but is treated in the local basis inside the augmentation region. For a detailed discussion of the PAW strength parameters, we refer to Ref. .

P - Derivative of PAW projectors, $|\tilde{p}\_{ai}\rangle$
:   $$\begin{split}
    g^{(\text{P})}\_{m \mathbf{k}', n \mathbf{k}, a}
    & \equiv
    \sum\_{ij}
    \langle
    \tilde{\psi}\_{m \mathbf{k}'} |
    \frac{\partial \tilde{p}\_{a i}}{\partial u\_{a}}
    \rangle
    (
    D\_{a, ij} - \varepsilon\_{n \mathbf{k}} Q\_{a, ij}
    )
    \langle
    \tilde{p}\_{a j} |
    \tilde{\psi}\_{n \mathbf{k}}
    \rangle
    \\ & +
    \sum\_{ij}
    \langle
    \tilde{\psi}\_{m \mathbf{k}'} |
    \tilde{p}\_{a i}
    \rangle
    (
    D\_{a, ij} - \varepsilon\_{m \mathbf{k}'} Q\_{a, ij}
    )
    \langle
    \frac{\partial \tilde{p}\_{a j}}{\partial u\_{a}} |
    \tilde{\psi}\_{n \mathbf{k}}
    \rangle
    \end{split}$$

R - Derivative of PAW partial waves, $|\phi\_{ai}\rangle$ and $|\tilde{\phi}\_{ai}\rangle$
:   $$g^{(\text{R})}\_{m \mathbf{k}', n \mathbf{k}, a}
    \equiv
    (\varepsilon\_{n \mathbf{k}} - \varepsilon\_{m \mathbf{k}'})
    \sum\_{ij}
    \langle
    \tilde{\psi}\_{m \mathbf{k}'} |
    \tilde{p}\_{a i}
    \rangle
    R\_{a, ij}
    \langle
    \tilde{p}\_{a j} |
    \tilde{\psi}\_{n \mathbf{k}}
    \rangle$$
:   with $R\_{a, ij}
    \equiv
    \langle
    \phi\_{a i} |
    \frac{\partial \phi\_{a j}}{\partial u\_{a}}
    \rangle -
    \langle
    \tilde{\phi}\_{a i} |
    \frac{\partial \tilde{\phi}\_{a j}}{\partial u\_{a}}
    \rangle$

Q - Derivative of PAW projectors, $|\tilde{p}\_{ai}\rangle$ (different eigenvalues)
:   $$\begin{split}
    g^{(\text{Q})}\_{m \mathbf{k}', n \mathbf{k}, a}
    & \equiv
    \sum\_{ij}
    \langle
    \tilde{\psi}\_{m \mathbf{k}'} |
    \frac{\partial \tilde{p}\_{a i}}{\partial u\_{a}}
    \rangle
    (
    D\_{a, ij} - \varepsilon\_{n \mathbf{k}} Q\_{a, ij}
    )
    \langle
    \tilde{p}\_{a j} |
    \tilde{\psi}\_{n \mathbf{k}}
    \rangle
    \\ & +
    \sum\_{ij}
    \langle
    \tilde{\psi}\_{m \mathbf{k}'} |
    \tilde{p}\_{a i}
    \rangle
    (
    D\_{a, ij} - \varepsilon\_{n \mathbf{k}} Q\_{a, ij}
    )
    \langle
    \frac{\partial \tilde{p}\_{a j}}{\partial u\_{a}} |
    \tilde{\psi}\_{n \mathbf{k}}
    \rangle
    \end{split}$$
:   This contribution is very similar to $g^{(\text{P})}$. The only difference is in the Kohn-Sham eigenvalues. While $g^{(\text{P})}$ uses the eigenvalues of both the initial and final state (so $\varepsilon\_{n \mathbf{k}}$ and $\varepsilon\_{m \mathbf{k}'}$), $g^{(\text{Q})}$ only uses the eigenvalues of the initial state ($\varepsilon\_{n \mathbf{k}}$).

## Related tags and articles

* Projector-augmented-wave formalism
* ELPH\_RUN
* ELPH\_SELFEN\_FAN
* ELPH\_SELFEN\_DW

## References
