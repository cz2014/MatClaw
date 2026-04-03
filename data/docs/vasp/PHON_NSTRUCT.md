# PHON_NSTRUCT

Categories: INCAR tag, Electron-phonon interactions, Phonons

PHON\_NSTRUCT = [integer]  
 Default: **PHON\_NSTRUCT** = none

Description: Sets the number of structures for electron-phonon interactions from Monte-Carlo (MC) sampling.

---

For PHON\_NSTRUCT=-1 the eigenvalues and eigenvectors of the dynamic matrix are written to the file DYNMATFULL.

For PHON\_NSTRUCT=0 the ZG configuration (one-shot) method is executed.

For PHON\_NSTRUCT>0 that many MC structures are prepared.

For further usage of this tag see: Electron-phonon interactions from Monte-Carlo sampling.

> **Mind:** This feature is available for VASP >= 6.0.

## Related tags and articles

Electron-phonon interactions from Monte-Carlo sampling, PHON\_LMC, PHON\_LBOSE, PHON\_NTLIST, PHON\_TLIST, TEBEG

Examples that use this tag

## References

---
