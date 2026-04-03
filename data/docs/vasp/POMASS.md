# POMASS

Categories: INCAR tag, POTCAR tag, Pseudopotentials

POMASS = [real array]  
 Default: **POMASS** = values read from POTCAR

Description: Array of masses of the atoms in atomic units.

---

POMASS determines the atomic mass of each atomic species. For standard calculations this tag should be omitted since the atomic masses for each species are read from the POTCAR file (they are also called POMASS there). However if one needs to change the atomic mass of some species, e.g., the mass of Hydrogen atoms in molecular dynamics calculations, the atomic masses of all species need to be set with this tag in the order they appear on the POTCAR file. After setting POMASS to different values in the INCAR file than on the POTCAR file the following message will occur on stdout when running VASP, informing the user that the mass has changed:

`WARNING: mass on POTCAR and INCAR are incompatible.`

If any incompatibilities exist, e.g. the number of entries doesn't agree with that on the POTCAR, VASP will stop.

## Related tags and sections

ZVAL

Examples that use this tag
