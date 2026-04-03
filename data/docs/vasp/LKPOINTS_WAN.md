# LKPOINTS WAN

Categories: INCAR tag, Wannier functions

LKPOINTS\_WAN = .TRUE.| .FALSE.

|  |  |  |
| --- | --- | --- |
| Default: **LKPOINTS\_WAN** | = .TRUE. | if KPOINTS\_WAN file is present. |

Description: LKPOINTS\_WAN controlls whether VASP reads the KPOINTS\_WAN file.

---

To avoid reading the KPOINTS\_WAN file without removing it from the working directory, the LKPOINTS\_WAN tag can be set to `.FALSE.` in the INCAR file.

## Related tags and articles

KPOINTS\_WAN

Examples that use this tag

---
