# Category:Wannier functions

Categories: VASP

Wannier functions $|w\_{m\mathbf{R}}\rangle$ are constructed by a linear combination of Bloch states $|\psi\_{n\mathbf{k}}\rangle$, i.e., the computed Kohn-Sham (KS) orbitals, as follows:

:   :   $$|w\_{m\mathbf{R}}\rangle =
        \sum\_{n\mathbf{k}}
        e^{-i\mathbf{k}\cdot\mathbf{R}}
        U\_{mn\mathbf{k}}
        |\psi\_{n\mathbf{k}}\rangle.$$

Here, $U\_{mn\mathbf{k}}$ is a unitary matrix which can be generated using different approaches discussed below, $m$ is an index enumerating Wannier functions with position $\mathbf{R}$, $n$ is the band index, and $\mathbf{k}$ is the Bloch vector.
Generally, one starts with an initial guess for $U\_{mn\mathbf{k}}$ that is built from $A\_{mn\mathbf{k}}$. The latter can be built from projections onto some localized-orbital basis.

* Comprehensive instructions on how to construct Wannier orbitals.

## One-shot singular-value decomposition (SVD)

In one-shot SVD, $A\_{mn\mathbf{k}}$ is computed by projecting the KS orbitals onto localized orbitals basis $\phi\_{m\mathbf{k}}$ that is specified by the LOCPROJ tag:

:   :   $$A\_{mn\mathbf{k}} =
        \langle \psi\_{n\mathbf{k}} | S |\phi\_{m\mathbf{k}}\rangle,$$

where

:   :   $$\phi\_{i\mathbf{k}}(\mathbf{r}) = e^{\mathrm{i}\mathbf{k}\cdot\mathbf{r}} Y\_{lm}(\hat{r})R\_n(r).$$

Note that $i$ encodes the quantum numbers $n$, $l$, and $m$. Thus, in $A\_{mn\mathbf{k}}$, $m$ is not the magnetic quantum number.

Then, VASP performs one-shot SVD for each k point

:   :   $$A\_{mn\mathbf{k}} = [D \Sigma V^\*]\_{mn\mathbf{k}}$$

to obtain the unitary matrix

:   :   $$U\_{mn\mathbf{k}} = [DV^\*]\_{mn\mathbf{k}}.$$

## Selected columns of the density matrix (SCDM)

The SCDM method is switched on using LSCDM. It has the advantage that the specification of a local basis in terms of atomic quantum numbers is omitted.

## Maximally localized Wannier functions using Wannier90

The interface of VASP with the Wannier90 code is mainly controlled by LWANNIER90 and LWANNIER90\_RUN. First, the initial guess for $A\_{mn\mathbf{k}}$ can be created by providing the *projections block* in the **wannier90.win** file (also see WANNIER90\_WIN) and setting LWANNIER90=True.

In order to obtain maximally localized Wannier functions, $U\_{mn\mathbf{k}}$ is constructed in a second step. For this, $A\_{mn\mathbf{k}}$ could be created using any projection method in the first step, i.e., single-shot SVD method (LOCPROJ), SCDM method (LSCDM), or Wannier90 (LWANNIER90). Then, Wannier90 can be executed directly or through VASP with the LWANNIER90\_RUN tag.

## References
