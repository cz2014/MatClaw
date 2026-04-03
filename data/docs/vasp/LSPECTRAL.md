# LSPECTRAL

Categories: INCAR tag, Many-body perturbation theory, GW

LSPECTRAL = .FALSE. | .TRUE.

|  |  |  |
| --- | --- | --- |
| Default: **LSPECTRAL** | = .TRUE. | if NOMEGA>2 |

Description: LSPECTRAL specifies to use the spectral method.

---

If LSPECTRAL = .TRUE. is set, the imaginary part of the independent particle polarizability $\chi\_{\mathbf{q}}^0 (\mathbf{G}, \mathbf{G}', \omega)$ is calculated first, and afterwards the full independent particle polarizability is determined using a Kramers-Kronig (or Hilbert) transform. This reduces the computational workload by almost a factor NOMEGA/2. The downside of the coin is that the response function must be kept in memory for all considered frequencies, which can cause excessive memory requirements. VASP, therefore, distributes the dielectric functions among the available compute nodes.

A similar trick is used when the QP-shifts are calculated. In general it is strongly recommended to set LSPECTRAL = .TRUE., except if memory requirements are too excessive.

## Related tags and articles

NOMEGA,
LSPECTRALGW

Examples that use this tag

---
