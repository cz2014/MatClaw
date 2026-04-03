# FBIAS_R0

Categories: INCAR tag, Advanced molecular-dynamics sampling

FBIAS\_R0 = [real (array)]

Description: Defines the half-step position for the bias potential.

---

FBIAS\_R0 defines the half-step position ($\xi\_{0\mu}$) for the Fermi-like step-shaped bias potential of the following form:

:   :   $$\tilde{V}(\xi\_1,\dots,\xi\_{M\_4}) = \sum\_{\mu=1}^{M\_4}\frac{A\_{\mu}}{1+\text{exp}\left [-D\_{\mu}(\frac{\xi(q)}{\xi\_{0\mu}} -1) \right ]}, \;$$

where the sum runs over all ($M\_4$) coordinates the potential acts upon, which are defined in the ICONST file by setting the `status` to 4.
The units of $\xi\_{0\mu}$ correspond to units of the coordinate the potential acts upon (e.g., ${\AA}$ for coordinates with `flag` R, $rad.$ for coordinates with `flag` A, dimensionless for coordinates with `flag` W, etc...).
The number of items defined via FBIAS\_R0 must be equal to $M\_4$. Otherwise, the calculation terminates with an error message.

## Related tags and articles

FBIAS\_A,
FBIAS\_D,
ICONST

---
