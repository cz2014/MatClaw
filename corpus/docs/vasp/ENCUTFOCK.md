# ENCUTFOCK

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

ENCUTFOCK = [real]

Default: none

Description: The ENCUTFOCK tag sets the energy cutoff that determines the FFT grids used by the Hartree-Fock routines.

---

The flag ENCUTFOCK is no longer supported in VASP.5.2.4 and newer versions.
Please use PRECFOCK instead.

The only sensible value for ENCUTFOCK is ENCUTFOCK=0.
This implies that the smallest possible FFT grid, which just encloses the cutoff sphere
corresponding to the plane wave cutoff, is used.
This accelerates the calculations by roughly a factor two to three,
but causes slight changes in the total energies and some noise in the calculated forces.
The FFT grid used internally in the exact exchange (Hartree-Fock) routines
is written to the OUTCAR file. Simply search for lines starting with

```
FFT grid for exact exchange (Hartree Fock)
```

In many cases, a sensible approach is to determine the electronic and ionic groundstate
using ENCUTFOCK=0, and to make one final total energy calculation
without the flag ENCUTFOCK.

## Related tags and articles

PRECFOCK,
PREC,
ENCUT,
List of hybrid functionals,
Hybrid functionals: formalism

Examples that use this tag

---
