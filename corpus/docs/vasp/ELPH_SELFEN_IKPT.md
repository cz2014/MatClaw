# ELPH_SELFEN_IKPT

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_IKPT = [real array]  
 Default: **ELPH\_SELFEN\_IKPT** = All k-points

Description: Compute the electron self-energy due to electron-phonon for a list of k-points specified by their index in the irreducible Brillouin zone generated from KPOINTS\_ELPH.

> **Mind:** Available as of VASP 6.5.0

---

For example, to select to compute for 4 different **k** points we specify their index in the INCAR file

```
ELPH_SELFEN_IKPT = 1 3 6 8
```

This tag can be used in combination with
ELPH\_SELFEN\_BAND\_START and ELPH\_SELFEN\_BAND\_STOP to select the calculation of the electron-phonon self-energy for a particular set of **k** points and bands.
Instead of specifying the indexes of the **k** points in the irreducible Brillouin zone, one can specify their reduced coordinates with ELPH\_SELFEN\_KPTS.

Instead of specifying the index of the **k** point appearing the in irreducible Brillouin zone, one can specify the reduced coordinates of the desired k-points using ELPH\_SELFEN\_KPTS.

## Related tags and articles

* ELPH\_RUN
* KPOINTS\_ELPH
* ELPH\_SELFEN\_GAPS
* ELPH\_SELFEN\_BAND\_START
* ELPH\_SELFEN\_BAND\_STOP
* ELPH\_SELFEN\_KPTS
