# LPARD

Categories: INCAR tag, Charge density

LPARD = [logical]  
 Default: **LPARD** = .FALSE.

Description: Determines whether partial (band and/or **k**-point-decomposed) charge densities are evaluated.

---

An LPARD run is a postprocessing step that requires a pre-converged calculation. It writes the partial density, or multiple partial charge densities, to one PARCHG file or several PARCHG.\*.\* files, depending on the setting of LSEPB and LSEPK.
If LPARDH5 = .TRUE., the output is redirected from PARCHG to vaspout.h5.

> **Warning:** The orbitals read from the WAVECAR file must be converged in a prior VASP run.

> **Warning:** LPARD is not supported for noncollinear calculations (LNONCOLLINEAR=true).

There are various ways to divide the partial charge density. You can pick the contributing bands either by index (refer to NBMOD and IBAND) or by energy range (refer to EINT), and select contributing **k** points through KPUSE.

> **Mind:** If only the LPARD tag is set, without any other tags to specify the separation of charge, then the NBMOD tag defaults to -1. The valence charge density (without the augmentation charges) is then written to the CHGCAR file, and no other partial charge output is generated.

## Related tags and articles

IBAND,
EINT,
NBMOD,
KPUSE,
LSEPB,
LSEPK,
LPARDH5,
PARCHG,
vaspout.h5,
Band-decomposed charge densities

Examples that use this tag

---
