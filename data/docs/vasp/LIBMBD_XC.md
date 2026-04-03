# LIBMBD_XC

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_XC = pbe | pbe0 | hse | blyp | b3lyp | revpbe | am05 | none

Default: The functional set by the GGA, METAGGA or XC tag

Description: LIBMBD\_XC sets the exchange-correlation functional for the setting of damping parameters used in the methods available in the library libMBD of many-body dispersion methods.

---

LIBMBD\_XC allows to choose the exchange-correlation functional that determines which set of damping parameters is used in the methods available in the library libMBD of many-body dispersion methods. The value is internally passed to the libMBD input **xc** described at the page .

The possible choices depend on the dispersion method selected with the LIBMBD\_METHOD tag and are listed in the file mbd\_damping.F90 of the libMBD source code. If LIBMBD\_XC=none is chosen, then no set of damping parameters is selected and either LIBMBD\_TS\_SR or LIBMBD\_MBD\_BETA has to be set.

> **Important:** This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_METHOD

Examples that use this tag

## References

---
