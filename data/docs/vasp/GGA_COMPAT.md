# GGA_COMPAT

Categories: INCAR tag, Exchange-correlation functionals, Symmetry

GGA\_COMPAT = .TRUE. | .FALSE.  
 Default: **GGA\_COMPAT** = .TRUE.

Description: If set to GGA\_COMPAT = .*FALSE*., this tag restores the full lattice symmetry for gradient-corrected functionals.

---

GGA and METAGGA functionals might break the symmetry of
the Bravais lattice slightly for cells that are not primitive cubic cells.
The origin of this problem is subtle and relates to the fact that the gradient field breaks the lattice symmetry for noncubic lattices. This can be fixed by setting

```
GGA_COMPAT = .FALSE.
```

to apply a spherical cutoff to the gradient field. In other words, the gradient field, as well as the charge density are set to zero for all reciprocal lattice vectors $\mathbf{G}$ that exceed a certain cutoff length
$\mathbf{G}\_{cut}$ before calculating the exchange-correlation energy and potential.
The cutoff $\mathbf{G}\_{cut}$ is determined automatically so that the cutoff sphere is fully inscribed in the parallelepiped defined by the FFT grid in reciprocal space.

:   > **Mind:** For compatibility reasons with older versions of VASP, the default is GGA\_COMPAT=*.TRUE.* However, setting the tag usually changes the energy only in the sub-meV energy range (0.1 meV), and for most results the setting of GGA\_COMPAT is insignificant. The most important exception is for the calculation of magnetic anisotropy, for which we strongly recommend GGA\_COMPAT=.*FALSE*.

## Related tags and articles

GGA,
METAGGA

Examples that use this tag

---
