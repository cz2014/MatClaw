# KSPACING

Categories: INCAR tag, Crystal momentum

KSPACING = [real]  
 Default: **KSPACING** = 0.5

Description: The tag KSPACING determines the number of k points if the KPOINTS file
is not present.

---

KSPACING is the smallest allowed spacing between k points in units of $\AA^{-1}$. The number of k points increases when the spacing is decreased.
The number of k points in the direction of the first, second and third reciprocal lattice vector is determined by $N\_i= \mathrm{max}(1, \mathrm{ceiling}( | \mathbf{b}\_i| 2\pi / \mathrm{KSPACING} ))$
with $\mathrm{ceiling}( x )$ being the ceiling function which returns the least integer that is equal or larger than $x$. In this equation, $\mathbf{b}\_i$ are the reciprocal lattice vectors $\mathbf{b}\_i \mathbf{a}\_j = \delta\_{ij}$.
The generated grid is centered at the $\Gamma$ point if KGAMMA=True (default), i.e., includes the $\Gamma$ point. For KGAMMA=False, the grid is shifted away from the $\Gamma$ point as done for Monkhorst-Pack grids.

> **Mind:** This implementation is not entirely identical with the deprecated automatic k-point generation used in the KPOINTS file.

If the k points are generated using the automatic mode in the KPOINTS file, $N\_i$ is calculated as
$N\_i= \mathrm{int}(\mathrm{max}(1, R\_k| \mathbf{b}\_i| + 0.5))$ with $R\_k=2\pi/\mathrm{KSPACING}$
and rounding it to the nearest integer. We recommend using the KSPACING tag in the INCAR file
and avoiding the automatic mode via the KPOINTS file.

## Related tags and articles

KGAMMA, KPOINTS

Examples that use this tag

---
