# LKPOINTS_OPT

Categories: VASP, INCAR tag

LKPOINTS\_OPT = .TRUE.| .FALSE.

|  |  |  |
| --- | --- | --- |
| Default: **LKPOINTS\_OPT** | = .TRUE. | if KPOINTS\_OPT file is present. |

Description: LKPOINTS\_OPT controls whether VASP reads the KPOINTS\_OPT file.

---

To avoid reading the KPOINTS\_OPT file without removing it from the working directory, the LKPOINTS\_OPT tag can be set to `.FALSE.` in the INCAR file.

## Related tags and articles

KPOINTS\_OPT, PROCAR\_OPT

Examples that use this tag

---
