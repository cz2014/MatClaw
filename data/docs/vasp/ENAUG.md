# ENAUG

Categories: INCAR tag, Projector-augmented-wave method

ENAUG = [real]  
 Default: **ENAUG** = largest *EAUG* read from the POTCAR file

Description: Specifies the cutoff energy of the plane-wave representation of the augmentation charges in eV.

---

ENAUG determines NGXF, NGYF, and NGZF in accordance with the PREC tag.

> **Deprecated:** ENAUG is considered as deprecated and should not be used anymore.

> **Warning:** Setting ENAUG has an effect only if PREC is set to one of the old settings (Low, Medium or High), otherwise it is ignored.

## Related tags and articles

NGXF,
NGYF,
NGZF,
ENCUT,
PREC,
PRECFOCK

Examples that use this tag
