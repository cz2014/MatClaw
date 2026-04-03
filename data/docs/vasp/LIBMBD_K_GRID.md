# LIBMBD_K_GRID

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_K\_GRID = [array of three integers]  
 Default: **LIBMBD\_K\_GRID** = determined in libMBD according to the cell shape

Description: LIBMBD\_K\_GRID sets the k-mesh of the collective oscillations defined in the methods available in the library libMBD of many-body dispersion methods.

---

LIBMBD\_K\_GRID allows to choose the k-mesh of the collective oscillations defined in the methods available in the library libMBD of many-body dispersion methods. The three integers correspond to the number of k-points along the axes of the cell in the reciprocal space. The values are internally passed to the libMBD input **k\_grid** described at the page .

> **Important:** This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_METHOD,
LIBMBD\_K\_GRID\_SHIFT

Examples that use this tag

## References

---
