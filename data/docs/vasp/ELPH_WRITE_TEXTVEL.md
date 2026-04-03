# ELPH_WRITE_TEXTVEL

Categories: INCAR tag, Electron-phonon interactions

ELPH\_WRITE\_TEXTVEL = [logical]  
 Default: **ELPH\_WRITE\_TEXTVEL** = .FALSE.

Description: If set, writes the electron group velocities to a velocity human-readable text file.

> **Mind:** Available as of VASP 6.5.0

---

The velocity file contains the following information:

```
# band kpoint spin direction energy(eV)  velocity
 1 1 1 1 e1 vel1
 2 1 1 1 e2 vel2
 ...
 8 1 1 1 e8 vel8
 ...
```

The group velocities are written in ev Å units in cartesian coordinates.
This tag can be used independently of ELPH\_WRITE\_HDF5VEL.
The number of bands is the one set by ELPH\_NBANDS which can in some cases be different from NBANDS.
If both are set, both outputs are written.

## Related tags and articles

* ELPH\_RUN
* ELPH\_WRITE\_HDF5VEL
