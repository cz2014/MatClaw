# SYMPREC

Categories: INCAR tag, Symmetry

SYMPREC = [real]  
 Default: **SYMPREC** = $10^{-5}$

Description: SYMPREC determines to which accuracy the positions in the POSCAR file must be specified (as of VASP.4.4.4).

---

SYMPREC determines how accurately the positions in the POSCAR file must be specified.
The default, SYMPREC=10-5, is usually large enough, even if the POSCAR file has been generated with single precision accuracy.
Increasing SYMPREC means that the positions in the POSCAR file can be specified with less accuracy (increasing fuzziness). Please also have a look at this section.

## Related tags and articles

ISYM

Examples that use this tag
