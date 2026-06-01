# LIBMBD_METHOD

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_METHOD = [string]  
 Default: **LIBMBD\_METHOD** = mbd-rsscs (default in libMBD)

Description: LIBMBD\_METHOD selects one of the methods available in the library libMBD of many-body dispersion methods. Only used when `IVDW = 14`.

---

LIBMBD\_METHOD can be set to a label (string) corresponding to one of the methods listed on the libMBD website (see **method** at the page ).

> **Mind:** Note that the use of the mbd-nl method is currently not possible, since the associated atomic polarizabilities and semilocal functional are currently not implemented in VASP.

> **Important:** This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_XC,
LIBMBD\_TS\_D,
LIBMBD\_TS\_SR,
LIBMBD\_MBD\_A,
LIBMBD\_MBD\_BETA,
LIBMBD\_VDW\_PARAMS\_KIND,
LIBMBD\_ALPHA,
LIBMBD\_C6AU,
LIBMBD\_R0AU,
LIBMBD\_N\_OMEGA\_GRID,
LIBMBD\_K\_GRID,
LIBMBD\_K\_GRID\_SHIFT,
LIBMBD\_PARALLEL\_MODE,
Tkatchenko-Scheffler method,
Many-body dispersion energy

Examples that use this tag

## References

---
