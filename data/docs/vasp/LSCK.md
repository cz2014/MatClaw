# LSCK

Categories: INCAR tag, Many-body perturbation theory, GW, ACFDT

LSCK = [logical]  
 Default: **LSCK** = .FALSE.

> **Important:** Up to vasp.6.2, the default was LSCK= .TRUE.

---

Description: LSCK=.True. switches on the squeezed Coulomb kernel.

If LSCK is set to .TRUE., the squeezed Coulomb kernel is used instead of the cosine window :

$v\_{G} = 4 \pi e^2 \frac{
(G\_{max}-G\_{min})(G\_{max}-G)
}{
(G\_{min}^2 - G(2G\_{min}-G\_{max}))^2
}
\qquad \mbox{for} \quad \mathrm{ENCUTGWSOFT}=\frac{\hbar^2G\_{min}^2}{2m\_e}\lt \frac{\hbar^2 G^2}{2m\_e}\lt \frac{\hbar^2G\_{max}^2}{2m\_e}=\mathrm{ENCUTGW}$

This kernel 'squeezes' the contributions from large wave vectors $G\gt G\_{max}$ into the window given by ENCUTGWSOFT. Effectively, this extrapolates the random-phase-approximation–correlation energy to the ENCUTGW $\to \infty$ limit, assuming that the basis-set-incompleteness error falls off as $1/$ENCUTGW$^{3/2}$.

## Related tags and articles

ENCUTGW,
GW calculations
ACFDT/RPA calculations

Examples that use this tag

---
