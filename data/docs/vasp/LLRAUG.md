# LLRAUG

Categories: INCAR tag, NMR

LLRAUG = .TRUE. | .FALSE.  
 Default: **LLRAUG** = .FALSE.

Description: LLRAUG calculates the two-center contributions to the chemical shift tensor.

---

LLRAUG switches on two-center contributions to the NMR chemical shift tensor.
These are contributions due to the augmentation
currents in other PAW spheres than the sphere with the atom for which the shift tensor is calculated.
Typically these contributions are safely neglected.
It makes sense to include them for accurate calculations with hard potentials (\*\_h)
on systems containing also (non-hydrogen) atoms from the top rows of the periodic
table (B, C, N, O, F), typically with short bonds, e.g. C2H2, where
effects up to a few ppm are possible. Effects are most significant for the H shift. For such systems using standard potentials
typically introduces larger inaccuracies. The two-center contributions are calculated using
a multipole expansion of the current density that is represented on the plane wave grid; as in Sec. III.A.3 of. Ref. .
The relevance of LLRAUG to achieve basis-set completeness for shieldings is discussed in
Ref. that compares to basis-set converged quantum chemical calculations .

## Related tags and articles

LCHIMAG

## References
