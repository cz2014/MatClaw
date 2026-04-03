# DIPOL

Categories: INCAR tag, Molecules, Electrostatics

DIPOL = [real array]

Description: specifies the center of the cell in direct lattice coordinates with respect to which the total dipole-moment in the cell is calculated.

---

The center of the cell w.r.t. which the total dipole-moment in the cell is calculated is specified as

```
DIPOL=Rx Ry Rz
```

where **R**x, **R**y and **R**z are given in direct lattice coordinates.

Calculations using the dipole correction, i.e. using tags IDIPOL or LDIPOL, require a definition of the center of the cell. Results of the computed dipole moment might differ for different positions. The reason for this difference is that the definition of the dipole 'destroys' the translational symmetry, i.e., the dipole is defined as

:   $$\int ({\mathbf r}-{\mathbf R}\_{\rm center}) \rho\_{\rm ions+valence}({\mathbf r}) d^3 {\mathbf r}.$$

This measure will provide consistent values only if $\rho\_{\rm ions+valence}$ drops to zero at some distance from $\mathbf R\_{\rm center}$. If this is
not the case, the values are extremely sensitive with respect to changes in $\mathbf R\_{\rm center}$. In such cases, it might be beneficial to increase the size of the cell along the vacuum dimension (for surfaces) or for the entire cell (for isolated molecules). For practical purposes this means that for slab calculations or surfaces the position specified by DIPOL should roughly correspond to the center of mass of the atoms in the cell, so that there is enough vacuum for the field to dissipate. See the Electrostatic corrections page for an example.

> **Mind:** If the flag is not set, VASP determines where the charge density averaged over one plane drops to a minimum and calculates the center of the charge distribution by adding half of the lattice vector perpendicular to the plane where the charge density has a minimum (this is a rather reliable approach for orthorhombic cells)

> **Tip:** For calculations of isolated molecules and surfaces with the dipole correction, use DIPOL as the center of mass of the atoms in your cell. Additionally, note that for surfaces, only the component normal to the surface is meaningful.

## Related tags and articles

NELECT,
EPSILON,
IDIPOL,
LDIPOL,
LMONO,
EFIELD,
Monopole, Dipole and Quadrupole corrections,
Electrostatic corrections

Examples that use this tag

---
