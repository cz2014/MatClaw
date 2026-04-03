# LSEPB

Categories: INCAR tag, Charge density

LSEPB = [logical]  
 Default: **LSEPB** = .FALSE.

Description: Specifies whether the partial charge density is summed up for all selected bands or separated and printed out in different files.

---

If LPARD = .TRUE. the partial charge density is calculated for a subset of bands selected via the IBAND, NBMOD, and EINT tags. If LSEPB is set to .TRUE., separate PARCHG.nb.ALLK or PARCHG.nb.nk files are created, dependent on the LSEPK tag. If LSEPB = .FALSE., the output is written to PARCHG or PARCHG.ALLB.nk, again depending on LSEPK.

Here are four examples to illustrate the interplay of LSEPB and LSEPK. in all cases, the following settings apply, selecting three specific bands and two **k** points `IBAND = 9 10 11`, `NBMOD = 3`, and `KPUSE = 1 34`:

* `LSEPB = .FALSE.`, `LSEPK = .FALSE.`

:   > **output files:** PARCHG

* `LSEPB = .TRUE.`, `LSEPK = .FALSE.`

:   > **output files:** PARCHG.0009.ALLK, PARCHG.0010.ALLK, PARCHG.0011.ALLK

* `LSEPB = .FALSE.`, `LSEPK = .TRUE.`

:   > **output files:** PARCHG.ALLB.0001, PARCHG.ALLB.0034

* `LSEPB = .TRUE.`, `LSEPK = .TRUE.`

:   > **output files:** PARCHG.0009.0001, PARCHG.0009.0034, PARCHG.0010.0001, PARCHG.0010.0034, PARCHG.0011.0001, PARCHG.0011.0034

> **Mind:** If VASP 6.5.0 or later is used, the code is compiled with HDF5 support, and LPARDH5 = .TRUE., all output will be redirected to the vaspout.h5 file, where it can be analyzed with py4vasp.

## Related tags and articles

LPARD,
IBAND,
EINT,
NBMOD,
KPUSE,
LSEPK,
LPARDH5,
PARCHG,
vaspout.h5,
Band-decomposed charge densities

Examples that use this tag

---
