# LBONE

Categories: INCAR tag, NMR

LBONE = .TRUE. | .FALSE.  
 Default: **LBONE** = .FALSE.

Description: LBONE adds the small *B*-component to the chemical shift tensor.

---

LBONE restores the small *B*-component of the wave function inside
the PAW spheres in the linear-response calculation of the NMR chemical shift
tensor. The POTCARs used in VASP are scalar-relativistic and the
AE-partial waves are solutions of the scalar-relativistic Kohn-Sham
equation for the spherical atom. These have a large (*A*) and a small (*B*) component.
The latter is not retained on the POTCAR, but approximately restored when LBONE=.TRUE. .
LBONE only affects the one-center valence contributions to the chemical shift. The contribution of the core electrons includes the *B*-component by default.

## Related tags and articless

LCHIMAG

## References
