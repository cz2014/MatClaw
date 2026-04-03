# PHON_LBOSE

Categories: INCAR tag, Electron-phonon interactions, Phonons

PHON\_LBOSE = [logical]  
 Default: **PHON\_LBOSE** = .TRUE.

Description: Determines whether structures in the sampling are created according to Bose-Einstein or Maxwell-Boltzmann statistics.

---

For PHON\_LBOSE=*.TRUE.* Bose-Einstein statistics is used.

For PHON\_LBOSE=*.FALSE.* Maxwell-Boltzmann statistics is used.

For further usage of this tag see: Electron-phonon interactions from Monte-Carlo sampling.

**Important**: This tag does not work together with PHON\_NSTRUCT=0.

> **Mind:** This feature is available for VASP >= 6.0.

## Related tags and articles

Electron-phonon interactions from Monte-Carlo sampling, PHON\_LMC, PHON\_NSTRUCT, PHON\_TLIST, PHON\_NTLIST, TEBEG

Examples that use this tag

---
