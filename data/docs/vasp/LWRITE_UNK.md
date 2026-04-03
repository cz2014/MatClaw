# LWRITE_UNK

Categories: INCAR tag, Wannier functions

LWRITE\_UNK = .TRUE. | .FALSE.  
 Default: **LWRITE\_UNK** = .FALSE.

Description: LWRITE\_UNK decides whether the cell-periodic part of the relevant Bloch functions is written.

---

For LWRITE\_UNK=True, VASP writes the cell-periodic part of the Kohn–Sham orbitals in spin channel s at k point p to the file **wannier90.UNKp.s**. This file can be used to plot Wannier orbitals with WANNIER90.

For details on the execution of wannier\_setup in VASP, see the description of the LWANNIER90 tag.
For information on the **wannier90.win** file and the execution of WANNIER90, we refer to the WANNIER90 manual.

## Related tags and articles

LWANNIER90,
LWRITE\_MMN\_AMN

Examples that use this tag

---
