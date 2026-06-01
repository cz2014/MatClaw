# LHYPERFINE

Categories: INCAR tag, NMR

LHYPERFINE = .TRUE. | .FALSE.  
 Default: **LHYPERFINE** = .FALSE.

Description: compute the hyperfine tensors at the atomic sites (available as of vasp.5.3.2).

---

To have VASP compute the hyperfine tensors at the atomic sites, set

```
LHYPERFINE = .TRUE.
```

> **Mind:** Spin-polarized calclulations ISPIN = 2 **must** be used.

> **Warning:** Noncollinear calculations LNONCOLLINEAR = .TRUE. are not currently implemented for LHYPERFINE. There is not a warning message for this, which will be added in future releases, see  known issues.

The hyperfine tensor AI describes the interaction between a nuclear spin SI (located at site **R**I) and the electronic spin distribution Se (in most cases associated with a paramagnetic defect state) :

:   $$E=\sum\_{ij} S^e\_i A^I\_{ij} S^I\_j$$

In general it is written as the sum of an isotropic part, the so-called Fermi contact term, and an anisotropic (dipolar) part.

The Fermi contact term is given by

:   $$(A^I\_{\mathrm{iso}})\_{ij}= \frac{2}{3}\frac{\mu\_0\gamma\_e\gamma\_I}{\langle S\_z\rangle}\delta\_{ij}\int \delta\_T(\mathbf{r})\rho\_s(\mathbf{r}+\mathbf{R}\_I)d\mathbf{r}$$

where ρs is the spin density, μ0 is the magnetic susceptibility of free space,
γe the electron gyromagnetic ratio, γI the nuclear gyromagnetic ratio of the nucleus at **R**I, and $\langle S\_z \rangle$ the expectation value of the *z*-component of the total electronic spin.

δT(**r**) is a smeared out δ function, as described in
the Appendix of Ref. .

The dipolar contributions to the hyperfine tensor are given by

:   $$(A^I\_{\mathrm{ani}})\_{ij}=\frac{\mu\_0}{4\pi}\frac{\gamma\_e\gamma\_I}{\langle S\_z\rangle}
    \int \frac{\rho\_s(\mathbf{r}+\mathbf{R}\_I)}{r^3}\frac{3r\_ir\_j-\delta\_{ij}r^2}{r^2} d\mathbf{r}$$

In the equations above *r*=|**r**|, *r*i the i-th component of **r**, and **r** is
taken relative to the position of the nucleus **R**I.

The nuclear gyromagnetic ratios should be specified by means of the NGYROMAG-tag.

A guide for calculating the hyperfine coupling constant is available.

> **Mind:** The Zeroth Order Regular Approximation (ZORA) is used to account for the relativistic effects in the hyperfine tensor calculations.

## Output

As usual, all output is written to the OUTCAR file. VASP writes three blocks of data. The first is for the Fermi contact coupling parameter:

```
 Fermi contact (isotropic) hyperfine coupling parameter (MHz)
 -------------------------------------------------------------
  ion      A_pw      A_1PS     A_1AE     A_1c      A_tot
 -------------------------------------------------------------
   1       ...       ...       ...       ...       ...
  ..       ...       ...       ...       ...       ...

 -------------------------------------------------------------
```

with an entry for each ion on the POSCAR file.
Apw, A1PS, A1AE, and A1c are the plane wave, pseudo one-center, all-electron one-center, and one-center core contributions to the Fermi contact term, respectively.
The total Fermi contact term is given by Atot.

> **Important:** We have chosen **NOT** to include the core contributions A1c in Atot. These are important to add when comparing to experiment where they can contribute a significant proportion to the hyperfine coupling constant (up to ~50 % for 13C ). If you want them to be included, you should add them by hand to Atot:
>
> :   $$A\_{tot + 1c} = A\_{tot} + A\_{1c} = (A\_{pw} + A\_{PS} + A\_{AE}) + A\_{1c}$$
>
> Core electronic contributions to the Fermi contact term are calculated in the frozen valence approximation as proposed by Yazyev *et al.*.

The dipolar contributions are listed next:

```
 Dipolar hyperfine coupling parameters (MHz)
 ---------------------------------------------------------------------
  ion      A_xx      A_yy      A_zz      A_xy      A_xz      A_yz
 ---------------------------------------------------------------------
   1       ...       ...       ...       ...       ...       ...
  ..       ...       ...       ...       ...       ...       ...

 ---------------------------------------------------------------------
```

Again one line per ion in the POSCAR file.

The total hyperfine tensors are written as:

```
 Total hyperfine coupling parameters after diagonalization (MHz)
 (convention: |A_zz| > |A_xx| > |A_yy|)
 ----------------------------------------------------------------------
  ion      A_xx      A_yy      A_zz     asymmetry (A_yy - A_xx)/ A_zz
 ----------------------------------------------------------------------
   1       ...       ...       ...         ...
  ..       ...       ...       ...         ...

 ----------------------------------------------------------------------
```

i.e., the tensors have been diagonalized and rearranged.

> **Mind:** The Fermi contact term is strongly dominated by the all-electron one-center contribution A1AE.
>
> Unfortunately, this particular term is quite sensitive to the number and eigenenergy of the all-electron partial waves that
> make up the one-center basis set, *i.e.*, to the particulars of the PAW dataset you are using.
> As a result, the Fermi contact term may strongly depend on the choice of PAW dataset.

## Units

The Fermi contact term $A$ is measured in following units

$[A]=
\left[\mu\_0\right]\times
\left[g\_e \mu\_e\right]\times
\left[g\_j \mu\_j\right]\times
\left[|\psi(0)|^2\right] =
\frac{T^2m^3}{J}\times
\frac{J}{T}\times
\frac{MHz}{T}\times
\frac{1}{m^3} = MHz$

with $\mu\_0=4\pi\times 10^{-7} T^2 m^3 J^{-1}$, $g\_e\mu\_e=9.28476377\times 10^{-24} J T^{-1}, |\psi(0)|^2=10^{30}m^{-3}$.
NGYROMAG is given in units of MHz/T.

## Advice

It is possible that your system relaxes to a non-magnetic solution, causing the hyperfine splitting to disappear (i.e. all zeros). If you think your system should be magnetic, you can enforce it using NUPDOWN, which will return the hyperfine splitting, cf. forum post: https://vasp.at/forum/viewtopic.php?t=16921. NUPDOWN will change the `Total magnetic moment S=` at the start of the hyperfine coupling section in the OUTCAR.

> **Important:** For some cells, the total magnetic moment S can be very small (`grep " mag=" OSZICAR`), near zero. In the above equations, the isotropic and anisotropic components of the hyperfine coupling parameter (AIiso and AIani) are calculated by dividing through by S (cf. ⟨Sz⟩). To avoid division by zero, S is reset to 1 when S < 10-3. `Total magnetic moment S=` is changed, changing the hyperfine coupling constants, too. These hyperfine coupling constants are likely not meaningful. In future versions of the code, there will be a warning message stating that S has been reset and the correct total magnetic moment will be printed.

## Related tags and articles

NGYROMAG

Calculating the hyperfine coupling constant

Examples that use this tag

## References

---
