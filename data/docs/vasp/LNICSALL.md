# LNICSALL

Categories: INCAR tag, NMR

LNICSALL = .TRUE. | .FALSE.  
 Default: **LNICSALL** = .FALSE.

Description: LNICSALL=.TRUE. calculates the NICS at the positions on the fine FFT grid NGXF x NGYF x NGZF.

---

```
   Warning: Not yet released!
```

This page contains information about a feature that will be available in a future
release of VASP. In other words, currently you cannot use it even with the latest version of VASP. The information may change significantly until it is released.

LNICSALL=.TRUE. ensures that the FFT grid NGXF x NGYF x NGZF is used to calculate the NICS (nucleus-independent chemical shift) points. These chemical shieldings will be printed to NICS.

> **Mind:** If `LNICSALL = True` is set, and POSNICS is also present, LNICSALL will take precedent.

## Related tags and articles

LCHIMAG,
NUCIND,
NICS
