# LIBMBD_MBD_BETA

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_MBD\_BETA = [real]  
 Default: **LIBMBD\_MBD\_BETA** = value that was determined for the exchange-correlation functional set with LIBMBD\_XC

Description: LIBMBD\_MBD\_BETA sets the value of the scaling factor $\beta$ (usually denoted $s\_R$) in the many-body methods as implemented in the library libMBD of many-body dispersion methods.

---

LIBMBD\_MBD\_BETA allows to choose the value of the damping parameter $\beta$ in the many-body methods as implemented in the library libMBD of many-body dispersion methods. The value is internally passed to the libMBD input **mbd\_beta** described at the page . LIBMBD\_MBD\_BETA is the same as the VDW\_SR tag that is used for the VASP implementation of the many-body methods.

> **Mind:** LIBMBD\_MBD\_BETA can be set only if LIBMBD\_XC=none.

> **Important:** This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_METHOD,
LIBMBD\_XC,
LIBMBD\_MBD\_A,
Many-body dispersion energy

Examples that use this tag

## References

---
