# LWANNIER90_RUN

Categories: INCAR tag, Wannier functions, Constrained-random-phase approximation

LWANNIER90\_RUN = .TRUE. | .FALSE.  
 Default: **LWANNIER90\_RUN** = .FALSE.

Description: LWANNIER90\_RUN executes wannier\_setup (see LWANNIER90=.TRUE.) and subsequently runs WANNIER90 in library mode (wannier\_run).

---

For details on the execution of wannier\_setup in VASP, see the description of the LWANNIER90-tag.
For information on the many tags one may set in the wannier90.win file to control the execution of WANNIER90 (be it standalone or in library mode) we refer to the WANNIER90 manual.

**Mind**: when running WANNIER90 in library mode, the wannier90.mmn and wannier90.amn files are not written. The information these files normally contain is passed on to wannier\_run internally. If you want these files to be written anyway, for instance to be able to run WANNIER90 standalone later on, one should add

```
LWRITE_MMN_AMN=.TRUE.
```

to the INCAR file.

## Related tags and articles

LWANNIER90,
LWRITE\_MMN\_AMN,
LWRITE\_UNK,
NUM\_WANN,
LWRITE\_SPN,
WANNIER90\_WIN

Examples that use this tag

---
