# LCHIMAG

Categories: INCAR tag, NMR

LCHIMAG = .TRUE. | .FALSE.  
 Default: **LCHIMAG** = .FALSE.

Description: Calculate the chemical shifts and magnetic susceptibility within linear response theory.

---

For `LCHIMAG = True`, the chemical shift tensors and magnetic susceptibility is computed. The implementation is based on linear response theory using the gauge-invariant PAW method of Yates, Pickard, and Mauri , that is an extension to the standard PAW method to account for the effects of a vector gauge field $A$. The NMR response currents are computed and the induced B field is calculated based on the Biot-Savart law.

Follow these guides for calculating the chemical shieldings and calculating the magnetic susceptibility.

## Definitions

The chemical shielding tensor is defined as:

:   $$\sigma\_{ij}(\mathbf{R}) = - \frac{ \partial B^{\mathrm{in}}\_i(\mathbf{R})}{ \partial B^{\mathrm{ext}}\_j}$$

Here $\mathbf{R}$ denotes the atomic nuclear site, $i$ and $j$ denote Cartesian indices, $\mathbf{B}^{\mathrm{ext}}$ an applied DC external magnetic field and $\mathbf{B}^{\mathrm{in}}(\mathbf{R})$ the induced magnetic field at the nucleus.

NMR experiments yield information on the shielding relative to a reference compound:

:   $$\delta\_{ij}(\mathbf{R}) = \sigma\_{ij}^{\mathrm{ref}} - \sigma\_{ij}(\mathbf{R})$$

Here, $\sigma\_{ij}^{\mathrm{ref}}$ is the isotropic shielding of the nucleus in the reference compound. $\delta\_{ij}(\mathbf{R})$ is the chemical shift tensor. In order to compare numerical results with the experimental data, one usually considers a series of compounds and references them to the experimental series.

VASP calculates chemical "shifts" for non-metallic crystalline systems using the linear response method of Yates, Pickard, and Mauri .

The isotropic chemical "shift" $\sigma\_{iso}$, span $\Omega$, and skew $\kappa$ are also reported, according to the following Herzfeld-Berger convention :

:   $$\sigma\_{iso} = (\sigma\_{11} + \sigma\_{22} + \sigma\_{33})/3$$

:   $$\Omega = \sigma\_{33} - \sigma\_{11}$$

:   $$\kappa = 3(\sigma\_{iso} - \sigma\_{22})/\Omega.$$

The orbital magnetic susceptibility $\chi$ is calculated according to a finite-differences approach:

:   $$\chi\_{\textrm{bare}} = \lim\_{q\to0} \frac{F(q) 2F(q) + F(-q)}{q^2}$$

where $F\_{ij}(q)=(2-\delta\_{ij})Q\_{ij}(q)$.

*Qij* is approximated in two ways. The so-called *pGv*-approximation is used by default , where *p* is momentum, *v* is velocity, and *G* is a Green's function. An alternative approach, the *vGv*-approximation is also used to calculate an alternative susceptibility since VASP 6.4.0 . *Q* is defined for the *pGv*-approximation as:

:   $$Q(q) = - \frac{1}{c^2 N\_k V\_c} \sum\_{i=x,y,z} \sum\_{o,\textbf{k}} \textrm{Re}[\langle \bar{u}^{(0)}\_{o,\textbf{k}} | \hat{\textbf{u}}\_i \times (-i \nabla + \textbf{k}) \times \mathcal{G}\_{\textbf{k} + \textbf{q}\_i}(\epsilon\_{o,\textbf{k}}) \hat{\textbf{u}}\_i \times \textbf{v}\_{\textbf{k} + \textbf{q}\_i, \textbf{k}}(\epsilon\_{o,\textbf{k}}) | \bar{u}^{(0)}\_{o,\textbf{k}} \rangle]$$

and for the *vGv*-approximation as:

:   $Q(q) = - \frac{1}{c^2 N\_k V\_c} \sum\_{i=x,y,z} \sum\_{o,\textbf{k}} \textrm{Re}[\langle \bar{u}^{(0)}\_{o,\textbf{k}} | \hat{\textbf{u}}\_i \times \textbf{v}\_{\textbf{k} + \textbf{q}\_i, \textbf{k}}(\epsilon\_{o,\textbf{k}}) \times \mathcal{G}\_{\textbf{k} + \textbf{q}\_i}(\epsilon\_{o,\textbf{k}}) \hat{\textbf{u}}\_i \times \textbf{v}\_{\textbf{k} + \textbf{q}\_i, \textbf{k}}(\epsilon\_{o,\textbf{k}}) | \bar{u}^{(0)}\_{o,\textbf{k}} \rangle]$.

## Output

The isotropic chemical shieldings are printed towards the end of the OUTCAR file, after the self-consistent calculation has finished. The chemical shift tensors both before and after space group symmetrization. These are the absolute tensors for the infinite lattice, excluding core contributions. They can be searched for under the `UNSYMMETRIZED TENSORS` and `SYMMETRIZED TENSORS` after `Absolute Chemical Shift tensors`. Additionally, the magnetic susceptibility is printed shortly after and found under `ORBITAL MAGNETIC SUSCEPTIBILITY`.

### Magnetic susceptibility

The magnetic susceptibility is found at the start of the `ORBITAL MAGNETIC SUSCEPTIBILITY, excluding core contribution`. The magnetic susceptibility is split into that obtained by the *pGv*-approximation and obtained by the *vGv*-approximation:

```
-------------------------------------------------------------
  ORBITAL MAGNETIC SUSCEPTIBILITY, excluding core contribution
 -------------------------------------------------------------
  Approximate magnetic susceptibility, pGv (10^-6 cm^3/mole)
     1        -70.928534         -0.000000          0.000000
     2         -0.000000        -70.928534          0.000000
     3          0.000000          0.000000        -70.928534
 -------------------------------------------------------------
  Approximate magnetic susceptibility, vGv (10^-6 cm^3/mole)
     1        -63.412095         -0.000000          0.000000
     2         -0.000000        -63.412095          0.000000
     3          0.000000          0.000000        -63.412095

         principal value                      axis
       (10^-6 cm^3/mole)           x,          y,          z
      --------------------------------------------------------
              -63.412095      0.1652     -0.9863      0.0000
              -63.412095     -0.9863     -0.1652      0.0000
              -63.412095      0.0000      0.0000      1.0000
 -------------------------------------------------------------
```

### Chemical shielding

To obtain the full absolute tensors requires adding both the $\mathbf{G=0}$ contribution (cf. `G=0 CONTRIBUTION TO CHEMICAL SHIFT`) and the contributions due to the core electrons. The latter consists of contributions for each chemical species separately (depending on POTCAR) and a global $\mathbf{G=0}$ susceptibility contribution.

The reference shift experienced by the core is given first:

```
  Core NMR properties

  typ  El   Core shift (ppm)
 ----------------------------
    1  C     -200.5098801
 ----------------------------

  Core contribution to magnetic susceptibility:     -0.31  10^-6 cm^3/mole
 --------------------------------------------------------------------------
```

> **Important:** The isotropic chemical shift $\delta\_{\mathrm{iso}}\mathrm{[VASP]}$ (ISO\_SHIFT) is the negative of the isotropic shielding. To make it a *real shift* one should add the reference shielding.

Next, the tensor is processed and its chemical shielding anisotropy (CSA) characteristics are printed in the OUTCAR. The tensor is symmetrized ($\sigma\_{ij} = \sigma\_{ji}$ is enforced) and diagonalized. From the three diagonal values the isotropic chemical "shift" $\delta\_{\mathrm{iso}}\mathrm{[VASP]}$, span $\Omega$, and skew $\kappa$ are calculated and printed see Ref. for unambiguous definitions. Note that $\kappa$ is ill-defined if $\Omega = 0$. Units are ppm, except for the skew. A typical output is given below:

```
   ---------------------------------------------------------------------------------
    CSA tensor (J. Mason, Solid State Nucl. Magn. Reson. 2, 285 (1993))
   ---------------------------------------------------------------------------------
               EXCLUDING G=0 CONTRIBUTION             INCLUDING G=0 CONTRIBUTION
           -----------------------------------   -----------------------------------
    ATOM    ISO_SHIFT        SPAN        SKEW     ISO_SHIFT        SPAN        SKEW
   ---------------------------------------------------------------------------------
    (absolute, valence only)
       1    4598.8125      0.0000      0.0000     4589.9696      0.0000      0.0000
       2     291.5486      0.0000      0.0000      282.7058      0.0000      0.0000
       3     736.5979    344.8803      1.0000      727.7550    344.8803      1.0000
       4     736.5979    344.8803      1.0000      727.7550    344.8803      1.0000
       5     736.5979    344.8803      1.0000      727.7550    344.8803      1.0000
   ---------------------------------------------------------------------------------
    (absolute, valence and core)
       1   -6536.1417      0.0000      0.0000    -6547.9848      0.0000      0.0000
       2   -5706.3864      0.0000      0.0000    -5718.2296      0.0000      0.0000
       3   -2369.4015    344.8803      1.0000    -2381.2446    344.8803      1.0000
       4   -2369.4015    344.8803      1.0000    -2381.2446    344.8803      1.0000
       5   -2369.4015    344.8803      1.0000    -2381.2446    344.8803      1.0000
   ---------------------------------------------------------------------------------
    IF SPAN.EQ.0, THEN SKEW IS ILL-DEFINED
   ---------------------------------------------------------------------------------
```

The isotropic chemical shielding for each atom, excluding and including G=0 contributions, as well as the span and skew (descriptions of asymmetry), follow. Finally, core contributions are taken into account for the `ISO_SHIFT`, `SPAN`, and `SKEW`.

> **Important:**
>
> * The columns excluding the $\mathbf{G=0}$ contribution are useful for supercell calculations on molecules.
> * The columns including the $\mathbf{G=0}$ contribution are for crystals.
> * The upper block gives the shielding due to only the electrons included in the SCF calculation.
> * The lower block has the contributions due to the frozen PAW cores added. These core contributions are rigid . They depend on POTCAR and are isotropic, i.e. affect neither SPAN nor SKEW.

## Related tags and articles

DQ,
ICHIBARE,
LNMR\_SYM\_RED,
NLSPLINE,
LLRAUG,
LBONE,
LVGVCALC,
LVGVAPPL,
NUCIND

Calculating the chemical shieldings, Calculating the magnetic susceptibility

Examples that use this tag

## References
