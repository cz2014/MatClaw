# RWIGS

Categories: POTCAR tag, INCAR tag, Magnetism, Projector-augmented-wave method

RWIGS = [real array]  
 Default: **RWIGS** = -1

Description: RWIGS specifies the Wigner-Seitz radius (in $\AA$) for each atom type.

---

* RWIGS *has* to be supplied for each atom type if LORBIT is set to <10. In this case, the *spd*- and site projected wave function character of each band is evaluated, and the local partial DOS (see sections PROCAR and DOSCAR) and local magnetic moments are calculated.

* If LORBIT >= 10, RWIGS is ignored

* RWIGS *must* be set in calculations with constraining the local magnetic moments (see I\_CONSTRAINED\_M)

For **mono-atomic systems** RWIGS can be defined
unambiguously. The sum of the volume of the spheres around each atom should be
the same as the total volume of the cell (assuming that you do not have a
vacuum region within your cell). This is in the spirit of atomic sphere calculations.
VASP writes a line

```
Volume of Typ   1:     98.5 %
```

to the OUTCAR file. You should use a RWIGS value which yields a
volume of approximately 100%.

For systems consisting of **more than one atom type**, there is no unambiguous way to define RWIGS and
several choices are possible. In all cases, the sum of
the volume of the spheres should be close to the total
volume of the cell (i.e the sum of the values given by VASP should be
around 100%).

* One possible choice is to set RWIGS such that the overlap between the spheres is minimized.

* a more elaborate way is to apply a Bader-type charge analysis to estimate the radius of an atom in a specific compound.

* in most cases, it is simplest to choose the radius of each sphere such that they are close to the covalent radius as tabulated in most periodic tables. This simple criterion can be used in most cases, and it relies at least on some ``physical intuition*.*

Please keep in mind that results are **qualitative** i.e. there is no unambiguous way to determine the location of an electron
(and hence the local magnetic moments). With the current implementation, it is for instance
hardly possible to determine charge transfer. What can be derived from the partial DOS is the typical character of a peak in a DOS.
Quantitative results can be obtained only by careful comparison with a reference system (e.g. bulk versus surface).

## Related tags and articles

LORBIT,
I\_CONSTRAINED\_M,
Spin spirals

Examples that use this tag
