# LMODELHF

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

LMODELHF = .TRUE. | .FALSE.  
 Default: **LMODELHF** = .FALSE.

Description: LMODELHF selects dielectric-dependent hybrid functionals with full exchange in the short-range, and AEXX in the long-range.

---

LMODELHF=.TRUE. selects the range separated hybrid functional suggested in Ref.
and Ref. under the name dielectric-dependent hybrid functionals (DDH) and doubly screened hybrid (DSH) functionals, respectively. These two hybrid functionals are both based on a common model for the dielectric function, but differ in the way how the range-separation parameters are obtained from first principles calculations. Their connection and performance have been discussed for instance in Ref. . In principle,
they can be considered to be a smartly constructed approximation to COH-SEX (local Coulomb hole plus screened exchange),
albeit fulfilling many important constraints that the exact exchange correlation functional must observe.

The corresponding functional has been available in VASP since VASP.5.2 released in 2009 (before the two publications), although the gradient contribution had been erroneously implemented in all VASP.5 releases and is only correct in VASP.6. The related bug fix has been made available by the authors of Ref. . The nonlocal exchange part of the functional has also been used and documented in Ref. and is covered in Improving the dielectric function.

Typically the user will need to set the following tags in the INCAR file:

```
LHFCALC = .TRUE.
LMODELHF = .TRUE.
HFSCREEN = 1.26
AEXX = 0.1
```

In this case, AEXX specifies the amount of exact exchange in the long range, that is for short wave vectors ($\mathbf{G} \to 0$). In the short range, that is for large wave vectors, always the full nonlocal exchange is used. The HFSCREEN determines how quickly the nonlocal exchange changes from AEXX to 1.

> **Mind:** If LMODELHF=.TRUE., then LHFCALC=.TRUE. is automatically set.

Specifically, in VASP, the Coulomb kernel $4 \pi e^2 / (\mathbf{q}+\mathbf{G})^2$ in the exact exchange is multiplied by a model for the dielectric function $\epsilon^{-1} (\mathbf{q}+\mathbf{G})$:

:   $\epsilon^{-1} (\mathbf{q}+\mathbf{G})=1-(1-{{\varepsilon}\_{\infty}^{-1}})\text{exp}(-\frac{|\mathbf{q+G}|^2}{4{\mu}^2})$.

where $\mu$ corresponds to HFSCREEN, and ${{\varepsilon}\_{\infty}^{-1}}$ is specified by AEXX. In real space this correspond to a Coulomb kernel

:   $V(r) =(1-(1-{{\varepsilon}\_{\infty}^{-1}})\text{erf}( {\mu} r)) \frac{e^2}{r}$.

The remaining part of the exchange is handled by an appropriate semi-local exchange correlation functional. For further detail we refer to the literature listed below.

Typical values for HFSCREEN are listed in the table below

```
AlP  1.24
AlAs 1.18
AlSb 1.13
BN   1.7
CdO  1.34
CdS  1.19
CdSe 1.18
CdTe 1.07
C    1.70
GaN  1.39
GaP  1.24
GaAs 1.18
GaSb 1.12
Ge   1.18
InP  1.14
InAs 1.09
InSb 1.05
LiF  1.47
MgO  1.39
SiC  1.47
Si   1.26
ZnO  1.34
ZnS  1.27
ZnSe 1.20
ZnTe 1.12
```

These values have been obtained from fits of the dielectric function using the Nanoquanta kernel and partially self-consistent GW calculations as used in Ref. . The values can be also estimated from simple dimensional scaling relations of the valence electron density. Furthermore band gap predictions are not very sensitive to the choice of HFSCREEN.

## Related tags and articles

LHFCALC,
HFSCREEN,
AEXX,
LRHFCALC,
LTHOMAS,
List of hybrid functionals,
Hybrid functionals: formalism,

## References
