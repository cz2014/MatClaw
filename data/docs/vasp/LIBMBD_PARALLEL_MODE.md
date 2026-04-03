# LIBMBD_PARALLEL_MODE

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_PARALLEL\_MODE = auto | kpoints | atoms

Default: LIBMBD\_PARALLEL\_MODE=auto (default in libMBD)

Description: LIBMBD\_PARALLEL\_MODE selects the parallelization scheme used in the library libMBD of many-body dispersion methods.

---

LIBMBD\_PARALLEL\_MODE allows to choose the parallelization scheme used in the library libMBD of many-body dispersion methods. The value is internally passed to the libMBD input **parallel\_mode** described at the page .

> **Important:**
>
> * The LIBMBD\_PARALLEL\_MODE tag can be used only if libMBD was compiled with MPI parallelization enabled.
> * This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_METHOD

Examples that use this tag

## References

---
