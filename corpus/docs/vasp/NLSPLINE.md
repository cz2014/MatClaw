# NLSPLINE

Categories: INCAR tag, Projector-augmented-wave method, Crystal momentum

NLSPLINE = .TRUE. | .FALSE.  
 Default: **NLSPLINE** = .FALSE.

Description: construct the PAW projectors in reciprocal space using spline interpolation so that they are *k*-differentiable.

---

For NLSPLINE=.TRUE., the PAW projectors in reciprocal space (LREAL=.FALSE.) are set up using a spline interpolation so that they are *k* differentiable. This improves the susceptibility contribution to the chemical shifts. It only slightly affects the other contributions to the chemical shifts.

It is advised to set NLSPLINE=.TRUE. if and only if PAW projectors are applied in reciprocal space and chemical shifts are calculated, i.e., if and only if LREAL=.FALSE. and LCHIMAG=.TRUE. As this option also gives slightly different total energies, it is advised to use the default NLSPLINE=.FALSE. in all other calculations for reasons of compatibility.

Real-space projectors are *k* differentiable by construction, hence do not require to set NLSPLINE=.TRUE.

## Related tags and articles

LCHIMAG,
DQ,
ICHIBARE,
LNMR\_SYM\_RED

Examples that use this tag

---
