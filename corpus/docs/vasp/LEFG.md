# LEFG

Categories: INCAR tag, NMR

LEFG = .TRUE. | .FALSE.  
 Default: **LEFG** = .FALSE.

Description: The LEFG computes the electric field gradient (EFG) at positions of the atomic nuclei.

---

For LEFG=.TRUE., the electric field gradient tensors at the positions of the atomic nuclei are calculated using the method of Petrilli *et al.* .

The EFG tensors are symmetric. The principal components *V*ii and asymmetry parameter η are printed for each atom. Following convention the principal components *V*ii are ordered such that:

:   $$|V\_{zz}| \gt |V\_{xx}| \gt |V\_{yy}|.$$

The asymmetry parameter is defined as $\eta = {(V\_{yy} - V\_{xx})}/ V\_{zz}$.
For so-called "quadrupolar nuclei", *i.e.*, nuclei with nuclear spin I>1/2, NMR experiments can
access *V*zz and η.

To convert the *V*zz values into the *C*q often encountered in NMR literature, one has to specify the nuclear quadrupole moment by means of the QUAD\_EFG-tag.

> **Mind:** Several definitions of $C\_q$ are used in the NMR community, ensure that you are comparing between the same definitions in calculation and experiment.

> **Important:** For heavy nuclei inaccuracies are to be expected because of an incomplete treatment of relativistic effects.

A guide for calculating the electric field gradient can be found in this article.

## Output

The EFG is listed atom-wise after the SCF cycle has been completed. First, the full 3x3 tensor is printed:

```
  Electric field gradients (V/A^2)
 ---------------------------------------------------------------------
  ion       V_xx      V_yy      V_zz      V_xy      V_xz      V_yz
 ---------------------------------------------------------------------
    1        -         -         -         -         -         -
```

The tensor is then diagonalized and reprinted:

```
  Electric field gradients after diagonalization (V/A^2)
  (convention: |V_zz| > |V_xx| > |V_yy|)
 ----------------------------------------------------------------------
  ion       V_xx      V_yy      V_zz     asymmetry (V_yy - V_xx)/ V_zz
 ----------------------------------------------------------------------
    1       -         -         -             -
```

The corresponding eigenvectors are printed atom-wise. Finally, the quadrupolar parameters are presented, which are commonly reported in NMR experiments.

```
            NMR quadrupolar parameters

  Cq : quadrupolar parameter    Cq=e*Q*V_zz/h
  eta: asymmetry parameters     (V_yy - V_xx)/ V_zz
  Q  : nuclear electric quadrupole moment in mb (millibarn)
 ----------------------------------------------------------------------
  ion       Cq(MHz)       eta       Q (mb)
 ----------------------------------------------------------------------
    1        -             -         -
```

## Related tags and articles

QUAD\_EFG

Calculating the electric field gradient

Examples that use this tag

## References
