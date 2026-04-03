# SMEARINGS

Categories: INCAR tag, Electronic occupancy

SMEARINGS = [real array of length (2 \* NSW)]  
 Default: **SMEARINGS** = not set

Description: SMEARINGS defines the smearing parameters for `ISMEAR = -3` in the calculation of the partial occupancies.

---

`ISMEAR = -3` performs a loop over smearing-parameters supplied in the INCAR file. With the tag SMEARINGS, you select which smearings are used

```
SMEARINGS = ismear1 sigma1  ismear2 sigma2  ...
```

> **Mind:** You must set NSW to the number of different smearings.

VASP will then read the provided smearings and conduct (NSW + 1) calculations with the different smearings.
For the first calculation, VASP uses tetrahedron smearing `ISMEAR = -5` to ensure that the tetrahedron information is present in case any of the selected smearings uses a tetrahedron method.
Since VASP uses the relaxation engine to loop over the different smearings you cannot combine SMEARINGS with other relaxation methods IBRION.

## Related tags and articles

ISMEAR,
SIGMA,
NSW,
IBRION,
Smearing technique

Examples that use this tag
