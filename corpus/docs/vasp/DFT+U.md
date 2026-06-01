# Category:DFT+U

Categories: VASP, Exchange-correlation functionals

The LDA and semilocal GGA functionals often fail to describe systems with localized (strongly correlated) $d$ or $f$ electrons (this manifests itself primarily in the form of unrealistic one-electron energies or too small magnetic moments). In some cases this can be remedied by introducing on the $d$ or $f$ atom a strong intra-atomic interaction in a simplified (screened) Hartree-Fock like manner ($E^{\text{HF}}[\hat{n}]$), as an on-site replacement of the LDA/GGA functional:

:   $$E\_{\text{xc}}^{\text{DFT}+U}[n,\hat{n}] = E\_{\text{xc}}^{\text{DFT}}[n] + E^{\text{HF}}[\hat{n}] - E\_{\text{dc}}[\hat{n}]$$

where $E\_{\text{dc}}[\hat{n}]$ is the double-counting term and $\hat{n}$ is the on-site occupancy matrix of the $d$ or $f$ electrons. This approach is known as the DFT+U method (traditionally called LSDA+U).

The first VASP DFT+U calculations, including some additional technical details on the VASP implementation, can be found in Ref. (the original implementation was done by Olivier Bengone and Georg Kresse).

More detail about the formalism is provided below.

## Theory

DFT+U is a method that was proposed to improve the description of systems with strongly correlated $d$ or $f$ electrons, like antiferromagnetic NiO for instance, that are usually inaccurately described with the standard LDA and GGA functionals. Several variants of the DFT+U method exist (see Refs. for reviews) that differ for instance in the way the double counting term $E\_{\text{dc}}[\hat{n}]$ is calculated. Three variants of them are implemented in VASP, whose formalism is briefly summarized below.

* LDAUTYPE=1: The rotationally invariant DFT+U introduced by Liechtenstein *et al.*

:   This particular flavour of DFT+U is of the form

    :   $$E^{\rm HF}[{\hat n}]=\frac{1}{2} \sum\_{\{\gamma\}}
        (U\_{\gamma\_1\gamma\_3\gamma\_2\gamma\_4} -
        U\_{\gamma\_1\gamma\_3\gamma\_4\gamma\_2}){ \hat
        n}\_{\gamma\_1\gamma\_2}{\hat n}\_{\gamma\_3\gamma\_4}$$
:   and is determined by the PAW on-site occupancies

    :   $${\hat n}\_{\gamma\_1\gamma\_2} = \langle \Psi^{s\_2} \mid m\_2 \rangle
        \langle m\_1 \mid \Psi^{s\_1} \rangle$$
:   and the (unscreened) on-site electron-electron interaction

    :   $$U\_{\gamma\_1\gamma\_3\gamma\_2\gamma\_4}= \langle m\_1 m\_3 \mid
        \frac{1}{|\mathbf{r}-\mathbf{r}^\prime|} \mid m\_2 m\_4 \rangle
        \delta\_{s\_1 s\_2} \delta\_{s\_3 s\_4}$$
:   where $|m\rangle$ represents a real spherical harmonics of angular momentum $l$=LDAUL.

:   The unscreened electron-electron interaction $U\_{\gamma\_{1}\gamma\_{3}\gamma\_{2}\gamma\_{4}}$ can be written in terms of the Slater integrals $F^0$, $F^2$, $F^4$, and $F^6$ ($f$ electrons). Using values for the Slater integrals calculated from atomic orbitals, however, would lead to a large overestimation of the true electron-electron interaction, since in solids the Coulomb interaction is screened (especially $F^0$).

:   In practice these integrals are often treated as parameters, *i.e.*, adjusted to reach agreement with experiment for a property like for instance the equilibrium volume, the magnetic moment or the band gap. They are normally specified in terms of the effective on-site Coulomb- and exchange parameters, $U$ and $J$ (LDAUU and LDAUJ, respectively). $U$ and $J$ can also be extracted from constrained-DFT calculations.

:   These translate into values for the Slater integrals in the following way (as implemented in VASP at the moment):

:   :   |  |  |  |  |  |
        | --- | --- | --- | --- | --- |
        | $L\;$ | $F^0\;$ | $F^2\;$ | $F^4\;$ | $F^6\;$ |
        | $1\;$ | $U\;$ | $5J\;$ | - | - |
        | $2\;$ | $U\;$ | $\frac{14}{1+0.625}J$ | $0.625 F^2\;$ | - |
        | $3\;$ | $U\;$ | $\frac{6435}{286+195 \cdot 0.668+250 \cdot 0.494}J$ | $0.668 F^2\;$ | $0.494 F^2\;$ |

:   The essence of the DFT+U method consists of the assumption that one may now write the total energy as:

:   :   $$E^{\mathrm{DFT}+U}[n,\hat n]=E^{\mathrm{DFT}}[n]+E^{\mathrm{HF}}[\hat n]-E\_{\mathrm{dc}}[\hat n]$$

:   where the Hartree-Fock-like interaction replaces the semilocal on-site due to the fact that one subtracts a double-counting energy $E\_{\mathrm{dc}}$, which supposedly equals the on-site semilocal contribution to the total energy,

:   :   $$E\_{\mathrm{dc}}[\hat n] = \frac{U}{2} {\hat n}\_{\mathrm{tot}}({\hat n}\_{\mathrm{tot}}-1) -
        \frac{J}{2} \sum\_\sigma {\hat n}^\sigma\_{\mathrm{tot}}({\hat n}^\sigma\_{\mathrm{tot}}-1).$$

* LDAUTYPE=2: The simplified (rotationally invariant) approach to the DFT+U, introduced by Dudarev *et al.*

:   This flavour of DFT+U is of the following form:

:   :   $$E^{\mathrm{DFT+U}}=E^{\mathrm{DFT}}+\frac{(U-J)}{2}\sum\_\sigma \left[
        \left(\sum\_{m\_1} n\_{m\_1,m\_1}^{\sigma}\right) - \left(\sum\_{m\_1,m\_2}
        \hat n\_{m\_1,m\_2}^{\sigma} \hat n\_{m\_2,m\_1}^{\sigma} \right) \right].$$

:   This can be understood as adding a penalty functional to the semilocal total energy expression that forces the on-site occupancy matrix in the direction of idempotency,

    :   $\hat n^{\sigma} = \hat n^{\sigma} \hat n^{\sigma}$.

:   Real matrices are only idempotent when their eigenvalues are either 1 or 0, which for an occupancy matrix translates to either fully occupied or fully unoccupied levels.

:   **Note**: in Dudarev's approach the parameters $U$ and $J$ do not enter seperately, only the difference $U-J$ is meaningful.

* LDAUTYPE=3: This option is for the calculation of the parameter $U$ using the linear response approach from Ref. . The steps to use this method are shown for the example of NiO.

* LDAUTYPE=4: same as LDAUTYPE=1, but without exchange splitting (i.e., the total spin-up plus spin-down occupancy matrix is used). The double-counting term is given by

:   :   $$E\_{\mathrm{dc}}[\hat n] = \frac{U}{2} {\hat n}\_{\mathrm{tot}}({\hat n}\_{\mathrm{tot}}-1) -
        \frac{J}{2} \sum\_\sigma {\hat n}^\sigma\_{\mathrm{tot}}({\hat n}^\sigma\_{\mathrm{tot}}-1).$$

## How to

DFT+U can be switched on with the LDAU tag, while the LDAUTYPE tag determines the DFT+U flavor that is used. LDAUL specifies the $l$-quantum number for which the on-site interaction is added, and the effective on-site Coulomb and exchange interactions are set (in eV) with the LDAUU and LDAUJ tags, respectively. Note that it is recommended to increase LMAXMIX to 4 for *d*-electrons or 6 for *f*-elements.

## Tutorials

* Lecture on the optical gap, introduces DFT+U towards the end of the lecture.

## References

---
