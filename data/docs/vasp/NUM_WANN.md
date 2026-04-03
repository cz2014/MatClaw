# NUM_WANN

Categories: INCAR tag, Wannier functions, Constrained-random-phase approximation

NUM\_WANN = [integer]  
 Default: **NUM\_WANN** = NBANDS

Description: Controls the number of Wannier orbitals to be constructed.

---

This tag is used to determine the number of Wannier orbitals to be constructed in the SCDM method.

Since VASP 6.2.0, NUM\_WANN also determines the number of Wannier orbitals to be used with wannier90.
Note that the `num_wann` value written to the `wannier90.win` file is always the value of NUM\_WANN known by vasp.

When using LOCPROJ for Wannierization, it is not necessary to set NUM\_WANN.
In this case, the number of Wannier orbitals is automatically set equal to the number of local functions.

## Related tags and articles

LWANNIER90,
LSCDM,
CUTOFF\_TYPE

---
