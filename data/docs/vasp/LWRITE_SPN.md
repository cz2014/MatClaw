# LWRITE_SPN

Categories: INCAR tag, Wannier functions, Magnetism

LWRITE\_SPN = .TRUE. | .FALSE.  
 Default: **LWRITE\_SPN** = .FALSE.

Description: Write **wannier90.spn** file for noncollinear calculations.

---

For noncollinear calculations (LNONCOLLINEAR=T using vasp\_ncl) the **wannier90.spn** file is written when

```
 LWANNIER90=T ! switch on Wannier90 interface 
 LWRITE_SPN=T
```

The file is formatted, and the appropriate line (`spn_formatted = .true.`) is automatically added to the **wannier90.win** file.

> **Warning:** Only the default setting for SAXIS is supported.

> **Mind:** Available for VASP version > 6.4.2.

## Related tags and articles

LWANNIER90,
LWRITE\_UNK,
LWRITE\_MMN\_AMN,
LWANNIER90\_RUN,
NUM\_WANN

Examples that use this tag
