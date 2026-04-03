# KPOINT_BSE

Categories: INCAR tag, Many-body perturbation theory, Bethe-Salpeter equations

KPOINT\_BSE = [integer] (optionally [integer],[integer],[integer])

Description: KPOINT\_BSE specifies the k-point index at which VASP calculates the dielectric matrix.

---

In the simplest form, one can specify

```
  KPOINT_BSE = index_of_k-point
```

Select the desired k point from the list of k points in the OUTCAR file. Additionally, a shift by an arbitrary reciprocal lattice vector can be supplied by specifying three additional integer numbers:

```
 KPOINT_BSE = index_of_k-point  n1 n2 n3
```

This allows calculating the dielectric function at a k point outside of the first Brillouin zone corresponding to

:   $$\mathbf{k} + n\_{1} \mathbf{b}\_{1}+ n\_{2} \mathbf{b}\_{2} + n\_{3} \mathbf{b}\_{3}$$

where $\mathbf{b}\_{i}$ are the reciprocal-lattice vectors of the unit cell.

> **Warning:** We strongly recommend using ANTIRES=2 for the finite wavevector calculations. The Tamm-Dancoff approximation can lead to unphysical results for the dielectric function at a finite wavevector.

## Related tags and articles

BSE calculations

Examples that use this tag

---
