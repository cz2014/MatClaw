# ELPH_WRITE_HDF5VEL

Categories: INCAR tag, Electron-phonon interactions

ELPH\_WRITE\_HDF5VEL = [logical]  
 Default: **ELPH\_WRITE\_HDF5VEL** = .FALSE.

Description: If set, writes the electron group velocities to the vaspout.h5 file.

> **Mind:** Available as of VASP 6.5.0

---

The dataset is stored in the vaspout.h5 file

```
 $ h5ls -r vaspout.h5 | grep velocity
 /results/electron_phonon/electrons/velocity Dataset {3, 1, 20, 8}
```

The group velocities are written in ev Å units in cartesian coordinates.
This tag can be used independently of ELPH\_WRITE\_TEXTVEL.
The number of bands is the one set by ELPH\_NBANDS which can in some cases be different from NBANDS.
If both are set, both outputs are written.

## Related tags and articles

* ELPH\_RUN
* ELPH\_WRITE\_TEXTVEL
