# LSORBIT

Categories: INCAR tag, Magnetism, Spin-orbit coupling, Noncollinear magnetism

LSORBIT = .TRUE. | .FALSE.  
 Default: **LSORBIT** = .FALSE.

Description: Switch on spin-orbit coupling.

---

LSORBIT = True switches on spin-orbit coupling (SOC) and automatically sets LNONCOLLINEAR = True. It requires using `vasp_ncl`. SOC couples the spin degrees of freedom with the lattice degrees of freedom. We recommend carefully checking the symmetry and convergence of your results when using SOC; see below.

LSORBIT only works for PAW potentials and is not supported by ultrasoft pseudopotentials. It is supported as of VASP.4.5.

## Assumptions and output

* Switching on spin-orbit coupling (SOC) adds an additional term $H^{\alpha\beta}\_{soc}\propto\mathbf{\sigma}\cdot\mathbf{L}$ to the Hamiltonian that couples the Pauli-spin operator $\mathbf{\sigma}$ with the angular momentum operator $\mathbf{L}$. As a relativistic correction, SOC acts predominantly in the immediate vicinity of the nuclei. Therefore, it is assumed that contributions of $H\_{soc}$ outside the PAW spheres are negligible. Hence, VASP calculates the matrix elements of $H\_{soc}$ only for the all-electron one-center contributions

:   :   $$E\_{soc}^{ij} = \delta\_{{\bf R}\_i{\bf R}\_j}\delta\_{l\_il\_j} \sum\_{n \bf k} w\_{\bf k} f\_{n\bf k} \sum\_{\alpha\beta} \langle \tilde{\psi}^\alpha\_{n\bf k} |\tilde{p}\_i \rangle \langle \phi\_i | H^{\alpha\beta}\_{soc} | \phi\_j \rangle \langle \tilde{p}\_j | \tilde{\psi}^\beta\_{n\bf k} \rangle$$

:   where $\phi\_i({\bf r}) = R\_i(|{\bf r}-{\bf R}\_i|) Y\_{l\_im\_i}(\theta,\varphi)$ are the partial waves of an atom centered at ${\bf R}\_i$, $\tilde{\psi}^\alpha\_{n\bf k}$ is the spinor-component $\alpha=\uparrow,\downarrow$ of the pseudo-orbital with band-index *n* and Bloch vector **k**, and $f\_{n\bf k}$ and $w\_{\bf k}$ are the Fermi- and **k**-point weights, respectively.

* It is possible to write the partial magnetization by setting LORBIT, i.e., the site- and orbital-resolved expectation value of the Pauli-spin operator $\mathbf{\sigma}$. And the partial orbital angular momentum by setting LORBMOM, i.e., the site- and orbital-resolved expectation value of the orbital angular momentum operator $\mathbf{L}$.

:   > **Mind:** The orbital angular momentum (vector-like quantity) is written to the OUTCAR file in Cartesian coordinates, while the magnetic moments (spinor-like quantity) are read and written in the basis specified by SAXIS (spinor space).

:   The default orientation of spinor space is $\sigma\_1=\hat x$, $\sigma\_2 =\hat y$, $\sigma\_3 = \hat z$. Hence, the bases agree by default, and no transformation is required.

* After a successful calculation including SOC, VASP writes the following results to the OUTCAR file:

```
Spin-Orbit-Coupling matrix elements

Ion:    1  E_soc:     -0.0984080
l=   1
    0.0000000    -0.0134381    -0.0134381
   -0.0134381     0.0000000    -0.0134381
   -0.0134381    -0.0134381     0.0000000
l=   2
    0.0000000    -0.0005072     0.0000000    -0.0005072    -0.0024560
   -0.0005072     0.0000000    -0.0018420    -0.0005072    -0.0006140
    0.0000000    -0.0018420     0.0000000    -0.0018420     0.0000000
   -0.0005072    -0.0005072    -0.0018420     0.0000000    -0.0006140
   -0.0024560    -0.0006140     0.0000000    -0.0006140     0.0000000
l=   3
    0.0000000    -0.0000000     0.0000000     0.0000000     0.0000000    -0.0000000    -0.0000000
   -0.0000000     0.0000000    -0.0000000     0.0000000    -0.0000000    -0.0000000    -0.0000000
    0.0000000    -0.0000000     0.0000000    -0.0000000    -0.0000000    -0.0000000     0.0000000
    0.0000000     0.0000000    -0.0000000     0.0000000    -0.0000000     0.0000000     0.0000000
    0.0000000    -0.0000000    -0.0000000    -0.0000000     0.0000000    -0.0000000     0.0000000
   -0.0000000    -0.0000000    -0.0000000     0.0000000    -0.0000000     0.0000000    -0.0000000
   -0.0000000    -0.0000000     0.0000000     0.0000000     0.0000000    -0.0000000     0.0000000
```

:   Here, `1 E_soc` represents the accumulated energy contribution $E\_{soc}=\sum\_{ij} E\_{soc}^{ij}$ inside the augmentation sphere that is centered at ${\bf R}\_1$ (position of ion 1), while the following entries correspond to the matrix elements $E\_{soc}^{ij}$ for the angular momentum $l$. Rows and columns correspond to $m$ and $m'$ of the real spherical harmonics $Y\_{lm}$(see Angular functions for naming and ordering conventions).

## Symmetry and convergence

In any spin-polarized (ISPIN=2) or noncollinear (LNONCOLLINEAR=T) calculation, even without SOC, the total energy depends on the relative orientation of magnetic moments. For instance, two magnetic sites may couple ferromagnetically or antiferromagnetically. On the other hand, the total energy is independent of the orientation of the magnetic moments with respect to the lattice without SOC. For instance, in-plane and out-of-plane moments on a surface would yield the same energy in the absence of SOC.

Switching on SOC couples the spin degrees of freedom that live in spinor space and the lattice degrees of freedom that live in real space, see SAXIS. Therefore, the in-plane and out-of-plane magnetic moments on a surface would yield different energies, when including SOC. Similarly, the ferromagnetically or antiferromagnetically ordered magnetic moments may additionally align with, e.g., the third lattice vector by setting LSORBIT = True.

Generally, be extremely diligent when using SOC: The energy differences can be of the order of few $\mu$eV/atom, k-point convergence is tedious and slow, and the required compute time might be huge, even for small cells.

> **Warning:** When SOC is included, we recommend testing whether switching off symmetry (ISYM=-1) changes the results.

Often, the k-point set changes from one to the other spin orientation, thus worsening the transferability of the results. Note that the WAVECAR file cannot be reread properly if the number of k-points changes. Hence, restart the calculation without symmetry from a converged charge density by setting ICHARG=1! Also, consider the setting of LMAXMIX.

We recommend setting GGA\_COMPAT = False for noncollinear calculations since this improves the numerical precision of GGA calculations.

Please check the sections on LNONCOLLINEAR, SAXIS, LMAXMIX, and GGA\_COMPAT.

## Related tags and articles

LNONCOLLINEAR,
MAGMOM,
SAXIS,
LORBMOM,
LORBIT,
LMAXMIX,
GGA\_COMPAT

Examples that use this tag

## References

---
