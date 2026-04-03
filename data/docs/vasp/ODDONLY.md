# ODDONLY

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals, Many-body perturbation theory, GW

ODDONLY = .TRUE. | .FALSE.  
 Default: **ODDONLY** = .FALSE.

Description: ODDONLY=.TRUE. selects a subset of **k**-points for the representation of the Fock exchange potential, with *C*1=*C*2=*C*3=1, and *n*1+*n*2+*n*3 odd.

---

One may restrict the sum over **q** in the Fock exchange potential (or one of its short range counterparts) to a subset, {**q****k**}, of the full (*N*1×*N*2×*N*3) **k**-point set, {**k**}, for which the following holds

:   $$\mathbf{q\_k} = \mathbf{b}\_1 \frac{n\_1 C\_1}{N\_1} + \mathbf{b}\_2 \frac{n\_2 C\_2}{N\_2}
    + \mathbf{b}\_3 \frac{n\_3 C\_3}{N\_3},\quad(n\_i=0,..,N\_i-1)$$

where **b**1,2,3 are the reciprocal lattice vectors of the primitive cell,
and *C*i is the integer grid reduction factor along reciprocal lattice direction
**b**i.

ODDONLY=.TRUE. selects a subset of **k**-points with *C*1=*C*2=*C*3=1, and *n*1+*n*2+*n*3 odd. It reduces the computational work load for HF type calculations by a factor two, but is only sensible for high symmetry cases (such as sc, fcc or bcc cells).

> **Warning:** there are circumstances under which **NKRED** and **NKREDX**,**Y**,**Z** should not be used!

## Related tags and articles

NKRED,
NKREDX,
NKREDY,
NKREDZ,
EVENONLY,
downsampling

Examples that use this tag

---
