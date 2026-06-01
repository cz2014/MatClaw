# LIBMBD_VDW_PARAMS_KIND

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_VDW\_PARAMS\_KIND = ts | tssurf

Default: LIBMBD\_VDW\_PARAMS\_KIND=ts (default in libMBD)

Description: LIBMBD\_VDW\_PARAMS\_KIND sets the type of free-atom van der Waals parameters that are used for the methods implemented in the library libMBD of many-body dispersion methods.

---

LIBMBD\_VDW\_PARAMS\_KIND allows to choose the set of van der Waals parameters from either the original Tkatchenko-Scheffler method (LIBMBD\_VDW\_PARAMS\_KIND=ts) or its variant that was designed to be more accurate for systems with surface (LIBMBD\_VDW\_PARAMS\_KIND=tssurf). The value is internally passed to the libMBD input **vdw\_params\_kind** described at the page . LIBMBD\_VDW\_PARAMS\_KIND is similar to the LTSSURF tag that is used for the VASP implementation of the Tkatchenko-Scheffler method.

> **Important:** This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_METHOD,
Tkatchenko-Scheffler method,
Many-body dispersion energy

Examples that use this tag

## References

---
