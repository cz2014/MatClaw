# ENMIN

Categories: POTCAR tag, Projector-augmented-wave method

ENMIN = [real]  
 Default: **ENMIN** = value read from POTCAR

Description: ENMIN describes the minimum viable plane-wave energy cutoff in eV for the pseudopotential it is read from.

---

For a multi-element POTCAR file, the maximum ENMIN determines the absolutely lowest cutoff energy for the plane-wave basis that should be used. If the deprecated PREC setting *Low* is used, this value is used by default. With all recommended PREC setting VASP will use the largest *recommended* cutoff energy ENMAX found in the POTCAR file instead. In all cases, the value can be overwritten by setting ENCUT in the INCAR file.

## Related tags and articles

POTCAR, pseudopotentials

---
