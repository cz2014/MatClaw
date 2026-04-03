# WRT_POTENTIAL

Categories: INCAR tag, Electrostatics, Electronic ground-state properties, Potential

WRT\_POTENTIAL = string  
 Default: **WRT\_POTENTIAL** = None

Description: Select which component of the local potential to be written as a post-processing step.

---

WRT\_POTENTIAL can select one or multiple local potentials on the real-space grid in the unit cell to be written, e.g.,

```
 WRT_POTENTIAL = total
```

or

```
 WRT_POTENTIAL = hartree ionic
```

The output is written to vaspout.h5 and can be accessed either by py4vasp or HDF5 command-line tools (h5ls, h5dump).

```
  import py4vasp as pv
  calc = pv.Calculation.from_path(".")
  pot_dict = calc.potential.read("total")
```

The above allows the creation of a Python dictionary with the potential data.

```
 h5ls -r vaspout.h5
```

The above shows the table of contents of vaspout.h5. Depending on the keywords specified with WRT\_POTENTIAL and the system it yields

```
 /results/potential       Group
 /results/potential/grid  Dataset {3}
 /results/potential/hartree Dataset {1, 24, 24, 24}
 /results/potential/ionic Dataset {1, 24, 24, 24}
 /results/potential/total Dataset {4, 24, 24, 24}
 /results/potential/xc    Dataset {4, 24, 24, 24}
```

The grid density can be increased by choosing a higher value for ENCUT or explicitly by NGXF, NGYF, NGZF.

The first dimension of the datasets in /results/potential is 1 for nonmagnetic calculation, 2 for spin-polarized calculation, and 4 for noncollinear calculations. In case the potential is scalar, i.e., has no B-field-like contribution that couples to the magnetization, only the 1st component exists. Hence, for *hartree* and *ionic*, the first dimension is 1. The components for the magnetic calculations correspond to the spinor representation with the scalar potential in the first component and the B-field in the second (ISPIN=2) or $B\_1$, $B\_2$ and $B\_3$ in the 2nd, 3rd and 4th component (LNONCOLLINEAR=T) in the basis of Pauli matrices $\{\sigma\_1$, $\sigma\_2$, $\mathbf{\sigma}\_3\}$ given by SAXIS.

> **Mind:** As a convention, the $\mathbf{G}{{=}}0$ component in reciprocal-space representations of both, the Hartree and ionic, potentials are set to zero. This implies that considering the sum of the Hartree and ionic potentials is more meaningful to visualize than either potential individually.

WRT\_POTENTIAL can be run as a post-processing step by restarting from a converged CHGCAR and setting ALGO=None. It is available for VASP >= 6.4.3.

## Options to select

### total

:   :   $$V\_{\text{total}}(\mathbf{r}) + B\_{\text{total}}(\mathbf{r}) =
        V\_{\text{ionic}}(\mathbf{r}) + V\_{\text{hartree}}(\mathbf{r})+
        V\_{\text{xc}}(\mathbf{r}) + B\_{\text{xc}}(\mathbf{r})$$

:   :   The output is written to `/results/potential/total`, as well as LOCPOT.

### hartree

:   :   $$V\_{\text{hartree}}(\mathbf{r}) = \int \frac{n(\mathbf{r'})}{|\mathbf{r}-\mathbf{r'}|}d\mathbf{r'}$$

:   :   The output is written to `/results/potential/hartree`.

### ionic

:   :   $V\_{\text{ionic}}(\mathbf{r})$ as mimicked by the pseudopotentials of the PAW method. The output is written to `/results/potential/ionic`.

### xc

:   :   $V\_{\text{xc}}(\mathbf{r}) + B\_{\text{xc}}(\mathbf{r})$ as defined by the selected exchange-correlation functional. The output is written to `/results/potential/xc`.

:   > **Mind:** This only corresponds to the (semi-)local functionals, i.e., LDA, GGA, non-local vdW-DF functionals, and does not account for either the potential $\mu$ associated with the kinetic energy density in METAGGA or the nonlocal Fock exchange considered in hybrid functionals.

## Related tags and articles

LVACPOTAV,
LVTOT,
LVHAR,
WRT\_POTENTIAL,
LDIPOL,
ENCUT, NGXF, NGYF, NGZF
