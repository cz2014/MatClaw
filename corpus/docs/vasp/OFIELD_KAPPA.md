# OFIELD_KAPPA

Categories: INCAR tag, Advanced molecular-dynamics sampling

OFIELD\_KAPPA = [real]

Description: The tag OFIELD\_KAPPA sets the strength of the bias potential in the Interface pinning method.

---

The bias potential in the Interface pinning method is written as

:   :   $U\_\text{bias}(\mathbf{R}) = \frac\kappa2 \left(Q\_6(\mathbf{R}) - A\right)^2$.

The tag OFIELD\_KAPPA method sets the strength of the bias potential $\kappa$. The unit of $\kappa$ is $\textrm{eV}/(\textrm{unit} \,\, \textrm{ of }\,\, Q)^2$.

## Related tags and articles

Interface pinning, OFIELD\_Q6\_NEAR, OFIELD\_Q6\_FAR, OFIELD\_A

Examples that use this tag

---
