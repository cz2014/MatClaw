# M CONSTR

Categories: INCAR tag, Magnetism

M\_CONSTR = [real array]  
 Default: **M\_CONSTR** = 3\*NIONS\*0.0

Description: M\_CONSTR specifies the desired local magnetic moment (size and/or direction) for the constrained local moments approach.

---

The M\_CONSTR tag sets the desired size and/or direction of the integrated local magnetic moments in cartesian coordinates.

For each ion 3 coordinates must be specified, i.e., for a system of *N* ions

```
M_CONSTR= M_1x M_1y M_1z  M_2x M_2y M_2z  ....  M_Nx M_Ny M_Nz
```

For I\_CONSTRAINED\_M=1 the norm of this vector is meaningless since only the direction will be constrained. For I\_CONSTRAINED\_M=2 both the norm as well as the direction of the moments specified by means of M\_CONSTR are subject to constraints.

Setting

```
M_CONSTR=  ... 0 0 0 ...
```

for a certain ion is equivalent to imposing no constraints on the integrated local magnetic moment at this ionic site.

For an explanation of the constrained local moments approach see the description of the I\_CONSTRAINED\_M tag.

## Related tags and articles

I\_CONSTRAINED\_M,
LAMBDA,
RWIGS,
LNONCOLLINEAR

Examples that use this tag

---
