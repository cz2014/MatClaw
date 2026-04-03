# LNOAUGXC

Categories: INCAR tag, Exchange-correlation functionals, Projector-augmented-wave method

LNOAUGXC = .TRUE. | .FALSE.  
 Default: **LNOAUGXC** = .FALSE.

Description: LNOAUGXC specifies if a METAGGA functional is evaluated with a density that is augmented or not.

---

The Kohn-Sham kinetic-energy density

:   $$\tau\_{\sigma}=\frac{1}{2}\sum\_{i}\nabla\psi\_{i\sigma}^{\*}\cdot\nabla\psi\_{i\sigma}$$

should, in principle, be larger than the von Weizsäcker kinetic-energy density

:   $$\tau\_{\sigma}^{\textrm{W}}=\frac{\left\vert\nabla n\_{\sigma}\right\vert^{2}}{8 n\_{\sigma}}.$$

However, this may not always be the case, particularly within the PAW spheres, when the pseudo density is augmented with the compensation charge. If LNOAUGXC=.TRUE. is set in the INCAR file, then the pseudo density is not augmented, which should alleviate the breaking of the condition $\tau\_{\sigma}^{\textrm{W}}\lt \tau\_{\sigma}$.

A violation of $\tau\_{\sigma}^{\textrm{W}}\lt \tau\_{\sigma}$ can make the calculations unstable, in particular with the TPSS family of functionals.

> **Mind:**
>
> * This tag is available since VASP.6.5.0 and is a replacement of the compiler option -DnoAugXCmeta that was available until VASP.6.4.3.
> * This option may negatively affect the results, therefore it should be used only for functionals, e.g., TPSS, for which the breaking of the condition $\tau\_{\sigma}^{\textrm{W}}\lt \tau\_{\sigma}$ may lead to numerical problems.

## Related tags and articles

METAGGA,
LTBOUNDLIBXC

Examples that use this tag

## References
