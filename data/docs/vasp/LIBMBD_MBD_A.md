# LIBMBD_MBD_A

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_MBD\_A = [real]  
 Default: **LIBMBD\_MBD\_A** = 6.0

Description: LIBMBD\_MBD\_A sets the value of the damping parameter $a$ in the many-body methods as implemented in the library libMBD of many-body dispersion methods.

---

LIBMBD\_MBD\_A allows to choose the value of the damping parameter $a$ in the many-body methods as implemented in the library libMBD of many-body dispersion methods. The value is internally passed to the libMBD input **mbd\_a** described at the page .

> **Mind:** LIBMBD\_MBD\_A can be set only if LIBMBD\_XC=none.

> **Important:** This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_METHOD,
LIBMBD\_XC,
LIBMBD\_MBD\_BETA,
Many-body dispersion energy

Examples that use this tag

## References

---
