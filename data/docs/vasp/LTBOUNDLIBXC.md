# LTBOUNDLIBXC

Categories: INCAR tag, Exchange-correlation functionals

LTBOUNDLIBXC = .TRUE. | .FALSE.  
 Default: **LTBOUNDLIBXC** = .FALSE.

Description: LTBOUNDLIBXC specifies whether or not the lower bound for the Kohn-Sham kinetic-energy density $\tau\_{\sigma}$ ($\tau\_{\sigma}^{\textrm{W}}\lt \tau\_{\sigma}$) is enforced before $\tau\_{\sigma}$ is used in a METAGGA functional from Libxc.

---

The Kohn-Sham kinetic-energy density

:   $$\tau\_{\sigma}=\frac{1}{2}\sum\_{i}\nabla\psi\_{i\sigma}^{\*}\cdot\nabla\psi\_{i\sigma}$$

should, in principle, be larger than the von Weizsäcker kinetic-energy density

:   $$\tau\_{\sigma}^{\textrm{W}}=\frac{\left\vert\nabla n\_{\sigma}\right\vert^{2}}{8 n\_{\sigma}}.$$

However, for numerical reasons $\tau\_{\sigma}^{\textrm{W}}\lt \tau\_{\sigma}$ may not be fulfilled, which can potentially lead to problems, in particular if the meta-GGA functional is not defined for negative values of $\tau\_{\sigma}-\tau\_{\sigma}^{\textrm{W}}$. If LTBOUNDLIBXC=.TRUE. in INCAR, then $\tau\_{\sigma}=\max(\tau\_{\sigma},\tau\_{\sigma}^{\mathrm{W}})$ is applied before $\tau\_{\sigma}$ is used in a meta-GGA functional from Libxc.

However, according to tests, for some of the most common meta-GGA functionals like SCAN, a violation of the lower bound is technically not a problem. Furthermore, it has been observed that applying $\tau\_{\sigma}=\max(\tau\_{\sigma},\tau\_{\sigma}^{\mathrm{W}})$ may possibly lead to very inaccurate forces and stress tensor. Therefore, by default LTBOUNDLIBXC=.FALSE. and Libxc should be compiled with the option `--disable-fhc` has explained here.

Thus, the recommendation is to set LTBOUNDLIBXC=.TRUE. only in the case convergence shows an erratic behavior. If this choice is made, then the forces and stress tensor should be carefully monitored if a geometry optimization is done.

## Related tags and articles

LIBXC1,
LIBXC2,
METAGGA

Examples that use this tag

## References

---
