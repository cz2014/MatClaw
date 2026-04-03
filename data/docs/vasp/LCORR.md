# LCORR

Categories: INCAR tag, Ionic minimization, Forces

LCORR = [logical]  
 Default: **LCORR** = .TRUE.

Description: Controls whether Harris corrections are calculated or not.

---

Based on the ideas of the Harris-Foulkes functional it is possible to derive a correction to the forces for non fully self-consistent calculations, we call these corrections Harris corrections. For LCORR=*.TRUE.* these corrections are calculated and included in the stress-tensor and the forces. The contributions are explicitly written to the file OUTCAR and help to show how well forces and stress are converged. For surfaces, the correction term might be relatively large and testing has shown that the corrected forces converge much faster to the exact forces than uncorrected forces.

## Related tags and articles

Harris-Foulkes functional

Examples that use this tag

---
