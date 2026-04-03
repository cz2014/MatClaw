# FBIAS_D

Categories: INCAR tag, Advanced molecular-dynamics sampling

FBIAS\_D = [real (array)]

Description: Sets the slope of the bias potential.

---

FBIAS\_D defines the parameter $D\_{\mu}$, which controls the slope of the central part of the Fermi-like step-shaped bias potential of the following form:

:   :   $$\tilde{V}(\xi\_1,\dots,\xi\_{M\_4}) = \sum\_{\mu=1}^{M\_4}\frac{A\_{\mu}}{1+\text{exp}\left [-D\_{\mu}(\frac{\xi(q)}{\xi\_{0\mu}} -1) \right ]}, \;$$

where the sum runs over all ($M\_4$) coordinates the potential acts upon, which are defined in the ICONST-file by setting the `status` to 4.
The parameters $D\_{\mu}$ are dimensionless.
The number of items defined via FBIAS\_D must equal to $M\_4$, otherwise the calculation terminates with an error message.

## Related tags and articles

FBIAS\_R0,
FBIAS\_A,
ICONST,
Biased molecular dynamics

---
