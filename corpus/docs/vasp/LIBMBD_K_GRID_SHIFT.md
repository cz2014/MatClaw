# LIBMBD_K_GRID_SHIFT

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_K\_GRID\_SHIFT = [real]  
 Default: **LIBMBD\_K\_GRID\_SHIFT** = 0.5 (default in libMBD)

Description: LIBMBD\_K\_GRID\_SHIFT sets the shift for the k-mesh of the collective oscillations defined in the methods available in the library libMBD of many-body dispersion methods.

---

LIBMBD\_K\_GRID\_SHIFT allows to choose a shift for the k-mesh of the collective oscillations defined in the methods available in the library libMBD of many-body dispersion methods. The value is internally passed to the libMBD input **k\_grid\_shift** described at the page .

> **Important:** This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_METHOD,
LIBMBD\_K\_GRID

Examples that use this tag

## References

---
