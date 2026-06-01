# SPRING_R0

Categories: INCAR tag, Advanced molecular-dynamics sampling

SPRING\_R0 = [real (array)]

Description: Position of the minimum for a harmonic bias potential.

---

The parameter SPRING\_R0 defines the position of the minimum ($\xi\_{0\mu}$) for the harmonic bias potential of the following form:

:   :   $$\tilde{V}(\xi\_1,\dots,\xi\_{M\_8}) = \sum\_{\mu=1}^{M}\frac{1}{2}\kappa\_{\mu} (\xi\_{\mu}(q)-\xi\_{0\mu})^2, \;$$

where the sum runs over all ($M\_8$) coordinates the potential acts upon ($\xi\_{\mu}(q)$), which are defined in the ICONST file by setting the `status=8`.
The units of $\xi\_{0\mu}$ correspond to units of the coordinate the potential acts upon (e.g., ${\AA}$ for coordinates with `flag` R, $rad.$ for coordinates with `flag` A, dimensionless for coordinates with `flag` W, etc...).
The number of items defined via SPRING\_R0 must be equal to $M\_8$, otherwise the calculation terminates with an error message.

## Related tags and articles

SPRING\_K,
SPRING\_V0,
ICONST,
Biased molecular dynamics

---
