# BEXT

Categories: INCAR tag, Magnetism

BEXT = [real] ( [real] [real] )

|  |  |  |
| --- | --- | --- |
| Default: **BEXT** | = 0.0 | if ISPIN=2 |
|  | = 3\*0.0 | if LNONCOLLINEAR=.TRUE. |
|  | = N/A | else |

Description: Specifies an external magnetic field in eV.

---

BEXT tag sets an external magnetic field that acts on the electrons in a Zeeman-like manner.
An additional potential of the following form carries this interaction:

* For spin-polarized calculations (ISPIN = 2):

:   $$V^{\uparrow} = V^{\uparrow} + B\_{\rm ext}$$
:   $$V^{\downarrow} = V^{\downarrow} - B\_{\rm ext}$$
:   and $B\_{\rm ext}$ = BEXT (in eV).

* For noncollinear calculations (LNONCOLLINEAR = .TRUE.):

:   $$V\_{\alpha\beta} = V\_{\alpha\beta} + \mathbf{B}\_{\rm ext} \cdot \mathbf{\sigma}\_{\alpha \beta}$$

:   where $\mathbf{B}\_{\rm ext}=({B}^1\_{\rm ext}, {B}^2\_{\rm ext}, {B}^3\_{\rm ext})^T$ is given by

:   |  |
    | --- |
    | BEXT = B1 B2 B3 ! in eV |

:   and $\mathbf{\sigma}$ is the vector of Pauli matrices (SAXIS, default: $\sigma\_1=\hat x$, $\sigma\_2 =\hat y$, $\sigma\_3 = \hat z$).

The effect of the above is most easily understood for the collinear case (ISPIN=2):
The eigenenergies of spin-up states are raised by $B\_{\rm ext}$ eV, whereas the eigenenergies of spin-down states are lowered by the same amount. The total energy changes by:

:   :   $\Delta E = (n^{\uparrow} - n^{\downarrow}) B\_{\rm ext}$ eV

where $n^{\uparrow}$ and $n^{\downarrow}$ are the number of up- and down-spin electrons in the system.

BEXT is applied during the self-consistent electronic minimization and effectively shifts the eigenenergies of the spin-up and spin-down states w.r.t. each other at each step. Consequently, the electrons redistribute (changing the occupancies) *and* the density changes. The change in the density (,e.g., charge density and magnetization) also affects the scf potential and KS orbitals. For a rigid-band Zeeman splitting, converge the charge density with BEXT=0 and restart with BEXT$\neq$0 and fixed charge density (ICHARG=11).

## Units

For an applied magnetic field $B\_0$, the energy difference between two Zeeman-splitted electronic states is given by:

:   $$\hbar \omega = g\_e \mu\_B B\_0,$$

where $\mu\_B$ is the Bohr magneton and $g\_e$ is the electron spin *g*-factor.

For ISPIN=2, rigid-band Zeeman-splitted states imply:

:   $$V^{\uparrow} - V^{\downarrow} = 2 B\_{\rm ext}$$

This leads to the following relationship between our definition of $B\_{\rm ext}$ (in eV) and the magnetic field $B\_0$ (in T):

:   $$B\_0 = \frac{2 B\_{\rm ext}}{g\_e \mu\_B}$$

where $\mu\_B$= 5.788 381 8060 x 10-5 eV T-1, and $g\_e$= 2.002 319 304 362 56.

## Related tags and articles

ISPIN,
LNONCOLLINEAR,
SAXIS

---
