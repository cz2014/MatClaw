# LSEPK

Categories: INCAR tag, Charge density

LSEPK = [logical]  
 Default: **LSEPK** = .FALSE.

Description: Specifies whether the partial charge density is summed up for all selected **k** points or separated and printed out in different files.

> **Mind:** If the **k** points are separated, each **k** point weight is set to 1. To get the correct results in this case it is necessary to turn off symmetry (ISYM = -1) for the initial ground state calculation and the post-processing partial charge calculation in most cases. However, the correct weight of each **k** point is determined from the KPOINTS file if all contributions are summed up.

---

If LPARD = .TRUE. the partial charge density is calculated for a subset of bands and **k** points depending on the setting of the tags IBAND, KPUSE, NBMOD, and EINT. If LSEPK is set to .TRUE., separate PARCHG.ALLB.nk or PARCHG.nb.nk files are created, dependent on the LSEPB tag. If LSEPK = .FALSE., the output is written to PARCHG or PARCHG.nb.ALLK, again depending on LSEPB.

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
LSEPB,
LPARDH5,
PARCHG,
vaspout.h5,
Band-decomposed charge densities

Examples that use this tag

---
