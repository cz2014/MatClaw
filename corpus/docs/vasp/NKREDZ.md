# NKREDZ

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

NKREDZ = [integer]  
 Default: **NKREDZ** = 1

Description: NKREDZ specifies a reduction factor for the **q**-point grid representation of the exact exchange potential along reciprocal space direction **b**3.

---

One may restrict the sum over **q** in the Fock exchange potential (or one of its short range counterparts) to a subset, {**q****k**}, of the full (*N*1×*N*2×*N*3) **k**-point set, {**k**}, for which the following holds

:   $$\mathbf{q\_k} = \mathbf{b}\_1 \frac{n\_1 C\_1}{N\_1} + \mathbf{b}\_2 \frac{n\_2 C\_2}{N\_2}
    + \mathbf{b}\_3 \frac{n\_3 C\_3}{N\_3},\quad(n\_i=0,..,N\_i-1)$$

where **b**1,2,3 are the reciprocal lattice vectors of the primitive cell,
and *C*i is the integer grid reduction factor along reciprocal lattice direction
**b**i. This leads to a reduction in the computational workload by a factor:

:   $$\frac{1}{C\_1 C\_2 C\_3}$$

In case one sets NKRED, the grid reduction factors will be uniformly set to *C*1=*C*2=*C*3=NKRED. If one wants to specify separate grid reduction factors for *C*1, *C*2, and *C*3 one should use *C*1=NKREDX, *C*2=NKREDY, and *C*3=NKREDZ, respectively.

> **Warning:** there are circumstances under which **NKRED** and **NKREDX**,**Y**,**Z** should not be used!

## Related tags and articles

NKRED,
NKREDX,
NKREDY,
EVENONLY,
ODDONLY,
downsampling

Examples that use this tag

---
