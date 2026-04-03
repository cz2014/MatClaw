# SPRING

Categories: INCAR tag, Transition states, Ionic minimization

SPRING = [integer]  
 Default: **SPRING** = -5

Description: SPRING gives the *spring constant* between the images as used in the elastic band method.

---

SPRING has to be set together with IMAGES if the elastic band method is used to calculate energy barriers between two ionic configurations of a system.

For SPRING = 0, each image is only allowed
to move into the direction perpendicular to the current
hyper-tangent, which is calculated as the normal vector
between two neighboring images.
This algorithm keeps the distance between the images
constant to *first order*. It is therefore possible to start
with a dense image spacing around the saddle point to obtain
a finer resolution around this point.

The nudged elastic band method
is applied when SPRING is set to a negative value e.g.

```
SPRING= -5
```

This is also the recommended setting.
Compared to the previous case, additional tangential springs
are introduced to keep the images equidistant
during the relaxation (remember the constraint is only
conserved to first order otherwise). Do not use too large values,
because this can slow down convergence. The default value
usually works quite reliably.

One problem of the nudged elastic band method is
that the constraint (i.e movements only
in the hyper-plane perpendicular to the current tangent) is
non linear. Therefore, the CG algorithm usually fails
to converge, and we recommended to use
the RMM-DIIS algorithm (IBRION=1) or the quick-min algorithm (IBRION=3).
Additionally,
the non-linear constraint (equidistant images) tends to be violated
significantly during the first few steps (it is only enforced to first order).
If this problem is
encountered, a very low dimensionality parameter (IBRION=1, NFREE=2)
should be applied in the first few steps, or a steepest
descent minimization without line optimization (IBRION=3, SMASS=2).
should be used, to pre-converge the images.

## Related tags and articles

IMAGES,
IBRION,
NFREE,
SMASS

Examples that use this tag

## References

---
