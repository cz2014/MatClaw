# LSPECTRALGW

Categories: INCAR tag, Many-body perturbation theory, GW

LSPECTRALGW = .FALSE. | .TRUE.  
 Default: **LSPECTRALGW** = .FALSE.

Description: LSPECTRALGW specifies to use the spectral method for calculating the self-energy.

---

If LSPECTRALGW = .TRUE. is set, the imaginary part of the self-energy $\Sigma(\omega)= G W$ is calculated from the imaginary part of screened potential $W(\omega)$ by shifting the poles of
$W$ by $\pm \epsilon$, where $\epsilon$ are the poles of the Green's function $G$.
Generally, LSPECTRALGW affects the compute time very little. QP energies also hardly
change when LSPECTRALGW is modified.
However, LSPECTRALGW = .TRUE. is usually slightly more robust,
and should be selected for molecules and other systems with flat dispersion-less bands.
One the other hand, LSPECTRALGW = .TRUE. seems to converge slightly slower,
as the complex shift CSHIFT is decreased. Set this flag, if the QP energies
show erratic behavior, for instance, if QP energies or Z-factors are not in the expected
range of values (0.5<Z<0.9).

## Related tags and articles

LSPECTRAL

Examples that use this tag

---
