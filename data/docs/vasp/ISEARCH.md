# ISEARCH

Categories: INCAR tag, Electronic minimization

ISEARCH = 0 | 1  
 Default: **ISEARCH** = 0

Description: Controls the line-search algorithm used during the direct minimization of the electronic structure (`ALGO = All`).

---

* `ISEARCH = 0`: Legacy line-search algorithm.
* `ISEARCH = 1`: Improved line-search algorithm.

The line search determines the optimal step size along the conjugate gradient search direction. `ISEARCH = 0` performs incremental steps along the search direction. It may lead to inconsistencies in total energy evaluations and slower convergence. `ISEARCH = 1` introduces a more robust and consistent method for determining the optimal step size, leading to improved convergence behavior and more reliable energy minimization.

> **Important:** We recommend `ISEARCH = 1` when performing electronic minimizations with `ALGO = All`, as it generally improves convergence stability and reduces the total number of required SCF steps.

> **Mind:** `ISEARCH = 0` should only be used for backward compatibility or benchmarking against legacy behavior.

## Improved line-search algorithm

The improved algorithm (`ISEARCH = 1`) introduces several enhancements over the legacy implementation:

* **Absolute reference** - each line search step starts from the origin of the search direction rather than progressing incrementally. This improves energy consistency.
* **Efficient slot system** - all trial steps are stored in slots, reducing redundant energy evaluations.
* **Minimum-acceptance criterion** - the final energy minimum of the line search is accepted only if its neighboring slots have also been evaluated (first principles energies are known), ensuring reliable interpolation.
* **Polynomial and spline fitting**
  + If ≤ 5 data points are available, an up to 4th-order polynomial fit is used to determine the minimum.
  + If > 5 data points are available, a spline interpolation is used instead, offering greater robustness than higher-order polynomials.
* **Gradient correction** - the line search typically relies on total energy evaluations only, which is faster than computing gradients. If the new gradient is not sufficiently orthogonal to the search direction from the previous step, a correction is applied using all available data points (via polynomial or spline fit).

## Related tags and articles

ALGO
