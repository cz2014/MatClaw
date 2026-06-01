# ELPH_SELFEN_KPTS

Categories: INCAR tag, Electron-phonon interactions

ELPH\_SELFEN\_KPTS = [real array]  
 Default: **ELPH\_SELFEN\_KPTS** = All k-points

Description: Computes the electron self-energy due to electron-phonon for a list of k-points specified by their fractional coordinates.

> **Mind:** Available as of VASP 6.5.0

---

For example, to select 4 different **k**-points we specify their coordinates in the INCAR file

```
ELPH_SELFEN_KPTS = \
  0.0  0.0  0.0 \
  0.5  0.5  0.0 \
  0.5  0.5  0.0 \
  0.5  0.75 0.25
```

The matching of the user input coordinates with the ones generated from the KPOINTS\_ELPH file in VASP is done by looking at the closest point in the full Brillouin zone, which is then mapped to the point in the irreducible Brillouin zone.
The user should always check whether the matching found and reported in the OUTCAR is correct.

This tag can be used in combination with ELPH\_SELFEN\_BAND\_START and ELPH\_SELFEN\_BAND\_STOP to select the calculation of the electron-phonon self-energy for a particular set of **k** points and bands.

Instead of specifying the reduced coordinates, one can specify the index of the **k** point appearing the in irreducible Brillouin zone list using ELPH\_SELFEN\_IKPT.

## Related tags and articles

* ELPH\_RUN
* KPOINTS\_ELPH
* ELPH\_SELFEN\_GAPS
* ELPH\_SELFEN\_BAND\_START
* ELPH\_SELFEN\_BAND\_STOP
* ELPH\_SELFEN\_IKPT
