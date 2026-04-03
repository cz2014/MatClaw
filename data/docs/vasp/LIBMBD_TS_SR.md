# LIBMBD_TS_SR

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_TS\_SR = [real]  
 Default: **LIBMBD\_TS\_SR** = value that was determined for the exchange-correlation functional set with LIBMBD\_XC

Description: LIBMBD\_TS\_SR sets the value of the scaling factor $s\_R$ in the Tkatchenko-Scheffler method as implemented in the library libMBD of many-body dispersion methods.

---

LIBMBD\_TS\_SR allows to choose the value of the scaling factor $s\_R$ in the Tkatchenko-Scheffler method as implemented in the library libMBD of many-body dispersion methods. The value is internally passed to the libMBD input **ts\_sr** described at the page . LIBMBD\_TS\_SR is similar to the VDW\_SR tag that is used for the VASP implementation of the Tkatchenko-Scheffler method.

> **Mind:** LIBMBD\_TS\_SR can be set only if LIBMBD\_XC=none.

> **Important:** This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_METHOD,
LIBMBD\_XC,
LIBMBD\_TS\_D,
Tkatchenko-Scheffler method

Examples that use this tag

## References

---
