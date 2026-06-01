# SPRING_V0

Categories: INCAR tag, Advanced molecular-dynamics sampling

SPRING\_V0 = [real (array)]

|  |  |  |
| --- | --- | --- |
| Default: **SPRING\_V0** | = 0 | for all coordinates with `status=8` in ICONST. |

Description: Rate at which the bias potential is shifted in $uc/fs$.

---

Consider the bias potential for a molecular-dynamics (MD) run of the form:

:   :   $$\tilde{V}(\xi\_1,\dots,\xi\_{M\_8}) = \sum\_{\mu=1}^{M\_8}\frac{1}{2}\kappa\_{\mu} (\xi\_{\mu}(q)-\xi\_{0\mu})^2, \;$$

where the sum runs over all ($M\_8$) coordinates the potential acts upon ($\xi\_{\mu}(q)$). The coordinates are defined in the ICONST file by setting the `status=8`.
Optionally, the position of minimum ($\xi\_{0\mu}$) can be shifted at a constant rate $\dot{\xi}\_{\mu}$ every MD step, i.e.,

:   :   $$\xi\_{0\mu}(t+\Delta t) = \xi\_{0\mu}(t) + \dot{\xi}\_{\mu}(q)\Delta t, \;$$

where $\Delta t$ is the time step used in MD (POTIM).
The rate $\dot{\xi}\_{\mu}$ can be defined via the parameter SPRING\_V0 and its units are $uc/fs$, where $uc$ corresponds to the units of the coordinate the potential acts upon (e.g., ${\AA}$ for coordinates with `flag` R, $rad.$ for coordinates with `flag` A, dimensionless for coordinates with `flag` W, etc...).
The number of items defined via SPRING\_V0 must be equal to $M\_8$, otherwise the calculation terminates with an error message.

## Related tags and articles

SPRING\_K,
SPRING\_R0,
ICONST,
Biased molecular dynamics

---
