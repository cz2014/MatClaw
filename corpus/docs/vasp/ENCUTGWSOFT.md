# ENCUTGWSOFT

Categories: INCAR tag, Many-body perturbation theory, GW

ENCUTGWSOFT = [real]

|  |  |  |
| --- | --- | --- |
| Default: **ENCUTGWSOFT** | = ENCUTGW$\times 0.8$ | for ALGO=*ACFDT* |
|  | = ENCUTGW$\times 0.8$ | as of VASP.6.3 |
|  | = ENCUTGW | else |

> **Important:** For vasp.6.3 and later releases ENCUTGWSOFT always defaults to ENCUTGW$\times 0.8$.

Descprition: The flag ENCUTGWSOFT sets the energy cutoff for the response function, such that it allows to truncate the Coulomb kernel slowly between the energy
specified by ENCUTGWSOFT and ENCUTGW using a cosine window function.

---

RPA/ACFDT correlation energies converge very slowly with respect to $\mathbf{G}\_{\rm max }$.
Thus VASP automatically extrapolates to the infinite basis set limit using a linear regression to the equation:

$E\_{\mathrm{c}}({\mathbf{G}})=E\_{\mathrm{c}}(\infty)+\frac{A}{{\mathbf{G}}^3}$.

This usually leads to much smoother energy-volume curves in ACFDT calculations and MP2 calculations.
The modified Coulomb kernel is in this case:
$v\_{G} = \frac{4 \pi e^2} {G^2} \frac{1}{2} \left( 1 + \cos \left( \pi \, \frac{ \frac{\hbar^{2} G^2 }{2 m\_e} - \mathrm{ ENCUTGWSOFT} }{ \mathrm{ENCUTGW} - \mathrm{ENCUTGWSOFT}} \right) \right)
\qquad \mbox{for} \quad \frac{\hbar^2 G^2 }{2 m\_e} \gt \mathrm{ENCUTGWSOFT}$

If LSCK is set to .TRUE., the squeezed Coulomb kernel is used instead of the cosine window:

$v\_{G} = 4 \pi e^2 \frac{
(G\_{max}-G\_{min})(G\_{max}-G)
}{
(G\_{min}^2 - G(2G\_{min}-G\_{max}))^2
}
\qquad \mbox{for} \quad \mathrm{ENCUTGWSOFT}=\frac{\hbar^2G\_{min}^2}{2m\_e}\lt \frac{\hbar^2 G^2}{2m\_e}\lt \frac{\hbar^2G\_{max}^2}{2m\_e}=\mathrm{ENCUTGW}$

This kernel *squeezes* contributions from large wave vectors $G\gt G\_{max}$ into the window given by ENCUTGWSOFT.
For GW type calculations the squeezed Coulomb kernel was the default (when ENCUTGWSOFT was set in the INCAR file) before version vasp.6.3, but
in newer releases the code always defaults to a smoothed Coulomb kernel (both for GW and RPA type calculations). If one desires to recover the behavior
of vasp.6.2 and older versions, LSCK=.TRUE. must be set in the INCAR file for GW type calculations if ENCUTGWSOFT is set in the INCAR file.

> **Mind:** The infinite basis set limit extrapolation for RPA/ACFDT is described in more detail here.

## Related tags and articles

PRECFOCK,
ENCUT,
ENCUTGW,
GW calculations,
LSCK,
RPA/ACFDT basis set convergence,
Examples that use this tag

---
