# LDMATRIX

Categories: INCAR tag, Electronic ground-state properties, Magnetism

LDMATRIX = .TRUE. | .FALSE.  
 Default: **LDMATRIX** = .FALSE.

Description: Computes the zero-field splitting (ZFS) matrix.

---

To compute the zero-field-splitting (ZFS) tensor due to spin-spin interactions in a collinear magnetic calculation (`ISPIN = 2`), set:

```
 LDMATRIX = True
 # sets default LHFCALC = True ; AEXX=0.0
```

The ZFS arises from spin-spin interactions between unpaired electrons in a high-spin state with a total spin $S \geq 1$. The ZFS matrix, also called D matrix, is measured in electron-spin resonance (ESR) experiments and provides insights into the local electronic environment of defect centers.

The implementation follows the formalism of Rayson and Briddon (2008), which efficiently evaluates the spin-spin interaction within periodic density-functional theory (DFT) using reciprocal space methods. This approach avoids expensive six-dimensional real-space integrations, leading to a stable and computationally efficient method. The expressions are similar to integrals used to evaluate the exact exchange energies for hybrid and HF-type calculation, hence VASP sets `LHFCALC = True`. This still allows for simple DFT calculations (`AEXX = 0.0` default), however mind that the default symmetrization is `ISYM = 3`. LDMATRIX should not be combined with `ISYM = 1`, or `2`.

## Output

The computed zero-field splitting is written in MHz to the stdout:

```
 Jij:    -0.0003356     0.0003475    -0.0000119   965.1231107   965.1238969   965.1238508
-Kij:    -0.0002748    -0.0000059     0.0002807    64.8471208    64.8472015    64.8471523
 D1c:    -0.0000541     0.0000275     0.0000267    11.1897131    11.1897125    11.1897272
```

and the OUTCAR file:

```
Spin-spin contribution to zero-field splitting tensor (MHz)
---------------------------------------------------------------
     D_xx      D_yy      D_zz      D_xy      D_xz      D_yz 
---------------------------------------------------------------
     0.001     0.000    -0.001  1042.316  1020.260  1041.130
---------------------------------------------------------------

after diagonalization
---------------------------------------------
    D_diag          eigenvector (x,y,z)
---------------------------------------------
 -1020.244      -0.697    -0.019     0.717
 -1048.926      -0.427     0.814    -0.393
  2069.171      -0.576    -0.580    -0.576
---------------------------------------------
```

## Advice

* Choice of PAW potentials: The ZFS tensor values can be sensitive to the specific PAW potential used, as different pseudopotentials include varying number of electrons in the valence. In particular, it is crucial that the states that give rise to the magnetic moment are included.
* NUPDOWN tag can be used to obtain a high-spin state.
* The LDMATRIX implementation is best tested for `vasp_std`. A bug for `vasp_gam` with `NCORE > 1` has been fixed, see D-matrix broken for vasp\_gam.

:   > **Warning:** LDMATRIX cannot be used with noncollinear magnetic calculations (LNONCOLLINEAR and/or LSORBIT).

* Spin-contamination corrections: Some users have modified the source code to include spin-contamination corrections, particularly for low-spin states ($S=0$). These modifications are *not* included in the default VASP version but can be implemented manually. See forum discussion: https://vasp.at/forum/viewtopic.php?p=29801p29801

## Related tags an articles

LHFCALC, NUPDOWN, ISPIN

## References
