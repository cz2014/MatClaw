# SPRING_K

Categories: INCAR tag, Advanced molecular-dynamics sampling

SPRING\_K = [real (array)]

Description: Force constant for harmonic bias potential.

---

The parameter SPRING\_K defines force constants ($\kappa\_{\mu}$) for the harmonic bias of the following form:

:   :   $$\tilde{V}(\xi\_1,\dots,\xi\_{M\_8}) = \sum\_{\mu=1}^{M}\frac{1}{2}\kappa\_{\mu} (\xi\_{\mu}(q)-\xi\_{0\mu})^2 \;$$

where the sum runs over all ($M\_8$) coordinates the potential acts upon ($\xi\_{\mu}(q)$), which are defined in the ICONST file by setting the `status` to 8.
The units of $\kappa\_{\mu}$ are $eV/uc$ where $uc$ units of coordinate the potential acts upon (e.g., ${\AA}$ for coordinates with `flag` R, $rad.$ for coordinates with `flag` A, dimensionless for coordinates with `flag` W, etc...)
The number of items defined via SPRING\_K must be equal to $M\_8$, otherwise the calculation terminates with an error message.

## Related tags and articles

SPRING\_R0,
SPRING\_V0,
ICONST,
Biased molecular dynamics

---
