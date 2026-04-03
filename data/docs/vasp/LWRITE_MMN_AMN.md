# LWRITE_MMN_AMN

Categories: INCAR tag, Wannier functions

LWRITE\_MMN\_AMN = .TRUE. | .FALSE.

|  |  |  |
| --- | --- | --- |
| Default: **LWRITE\_MMN\_AMN** | = .TRUE. | if LWANNIER90=.TRUE. |
|  | = .FALSE. | otherwise |

Description: LWRITE\_MMN\_AMN=.TRUE. tells the VASP2WANNIER90 interface to write the **wannier90.mmn** and **wannier90.amn** files.

---

When running WANNIER90 in library mode (LWANNIER90\_RUN=.TRUE.), the **wannier90.mmn** and **wannier90.amn** files are not written. The information these files normally contain is passed on to wannier\_run internally. If you want these files to be written anyway, for instance, to be able to run WANNIER90 standalone later on, set LWRITE\_MMN\_AMN=.TRUE. in the INCAR file.

## Related tags and articles

LWANNIER90,
LWANNIER90\_RUN

Examples that use this tag

---
