# LVDW_ONECELL

Categories: INCAR tag, Van der Waals functionals

LVDW\_ONECELL = [logical][logical][logical]  
 Default: **LVDW\_ONECELL** = .FALSE. .FALSE. .FALSE.

Description: LVDW\_ONECELL  can be used to disable vdW interaction with mirror image in X Y Z direction. This is advisable for molecular calculations in the gas phase. In all other cases, use the default.

Note: There is some confusing documentation on the ASE pages, which states that ".TRUE. .TRUE. .TRUE." enables the interaction with neighboring cells. However, the opposite is the case and *.TRUE.* disables the interaction (".FALSE. .FALSE. .FALSE." = interactions switched on, ".TRUE. .TRUE. .TRUE." = interactions switched off).

---

## Related tags and articles

IVDW,
Many-body dispersion energy,

Examples that use this tag

---
