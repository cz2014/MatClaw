# LDOWNSAMPLE

Categories: INCAR tag, Wannier functions, Constrained-random-phase approximation, Many-body perturbation theory

LDOWNSAMPLE = [logical]  
 Default: **LDOWNSAMPLE** = .FALSE.

Description: LDOWNSAMPLE selects a sub-grid of k-points defined in KPOINTS from WAVECAR.

---

If LDOWNSAMPLE is present, VASP selects a sub-grid of k-points defined in KPOINTS and stored in the WAVECAR file.
This option is automatically selected for cRPA calculations, where it can be beneficial to perform the Wannier projection on a denser k-point grid than the actual cRPA calculation. For this purpose, the Wannier projection should be written to WANPROJ.

This tag is not restricted to cRPA jobs and can be used for any other task that start from a pre-calculated WAVECAR and/or WANPROJ file.

## Related tags and articles

LWANNIER90,
LWANNIER90\_RUN,
WANPROJ

Examples that use this tag

---
