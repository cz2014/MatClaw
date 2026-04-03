# LNONCOLLINEAR

Categories: INCAR tag, Magnetism, Noncollinear magnetism

LNONCOLLINEAR = .True. | .False.

|  |  |  |
| --- | --- | --- |
| Default: **LNONCOLLINEAR** | = .False. |  |
|  | = .True. | if spin-orbit coupling is included (LSORBIT=.True.) |

Description: Switch on noncollinear magnetic calculations.

---

For noncollinear magnetic calculations, set LNONCOLLINEAR = True in the INCAR file and use the `vasp_ncl` executable. The electronic minimization treats the full 2x2 spin density

:   $$n\_{\sigma\sigma'}(\mathbf{r}) = \sum\_{n=1}^N \psi\_{n\sigma}(\mathbf{r})\psi^\*\_{n\sigma'}(\mathbf{r}),$$

which is written to the CHGCAR file. In spinor space, the part of the spin density proportional to the 2x2 unit matrix corresponds to the charge density, and the part proportional to the vector of Pauli matrices is the magnetization density.
This enables the consideration of noncollinear magnetic structures within spin-density-functional theory. MAGMOM sets the initial magnetic moments. Write the final magnetic moments by setting LORBIT.

It is possible to **restart a noncollinear calculation** from a previous nonmagnetic calculation (ISPIN=1 and LNONCOLLINEAR=F) or spin-polarized calculation (ISPIN=2) by reading WAVECAR or CHGCAR files. The magnetization of the spin-polarized calculation is interpreted to point along SAXIS (default: Cartesian direction $\hat z$). It is not possible to rotate the magnetic moment locally on selected atoms when restarting with a magnetization density. The magnetic configuration can globally be rotated with respect to the lattice by restarting with a different SAXIS.

In practice, we recommend performing noncollinear calculations in two steps:

* First, calculate the nonmagnetic ground state and generate a WAVECAR and a CHGCAR file.
* Second, read the WAVECAR and CHGCAR file, and supply initial magnetic moments using the MAGMOM tag.

We recommend setting GGA\_COMPAT = False and LASPH= True for noncollinear calculations since this improves the numerical precision of calculations using the generalized-gradient approximation (GGA).

Consider setting AMIX\_MAG and BMIX\_MAG for better convergence when using density mixing.

The I\_CONSTRAINED\_M tag can constrain the on-site magnetic moments.

Supported as of VASP.4.5.

> **Important:** For noncollinear calculations ISPIN is ignored. In VASP 6.5.0, the calculation will exit with an error message if ISPIN=2 and MAGMOM is used in combination with the LNONCOLLINEAR=.TRUE.

## Related tags and articles

MAGMOM,
LSORBIT,
SAXIS,
GGA\_COMPAT,
LASPH,
AMIX\_MAG, BMIX\_MAG,

Examples that use this tag

---
