# LIBMBD_N_OMEGA_GRID

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_N\_OMEGA\_GRID = [integer]  
 Default: **LIBMBD\_N\_OMEGA\_GRID** = 15 (default in libMBD)

Description: LIBMBD\_N\_OMEGA\_GRID sets the number of points on the grid of imaginary frequencies used in the library libMBD of many-body dispersion methods.

---

LIBMBD\_N\_OMEGA\_GRID allows to choose the number of points on the grid of imaginary frequencies used in the library libMBD of many-body dispersion methods. The value is internally passed to the libMBD input **n\_omega\_grid** described at the page .

> **Important:** This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_METHOD

Examples that use this tag

## References

---
