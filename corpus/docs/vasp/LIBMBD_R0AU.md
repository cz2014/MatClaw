# LIBMBD_R0AU

Categories: INCAR tag, Exchange-correlation functionals, Van der Waals functionals

LIBMBD\_R0AU = [real array]

Description: LIBMBD\_R0AU defines the free-atom $R\_0$ parameters (bohr) used in the Tkatchenko-Scheffler and Many-body dispersion energy methods as implemented in the library libMBD of many-body dispersion methods.

---

LIBMBD\_R0AU allows to set values for the free-atom $R\_0$ parameters (bohr) used in the Tkatchenko-Scheffler and Many-body dispersion energy methods as implemented in the library libMBD of many-body dispersion methods. For each atom listed in the POSCAR file, a value has to be provided. The values are internally passed to the third column of the libMBD input **free\_values** described at the page .

> **Important:** This feature is available from VASP.6.4.3 onwards that needs to be compiled with -DLIBMBD.

libMBD is a separate library package that has to be downloaded and compiled before VASP is compiled with the corresponding precompiler options and links to the libraries.

## Related tags and articles

LIBMBD\_METHOD,
LIBMBD\_ALPHA,
LIBMBD\_C6AU,
Tkatchenko-Scheffler,
Many-body dispersion energy

Examples that use this tag

## References

---
