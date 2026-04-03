# LWANNIER90

Categories: INCAR tag, Wannier functions, Constrained-random-phase approximation

LWANNIER90 = .TRUE. | .FALSE.  
 Default: **LWANNIER90** = .FALSE.

Description: LWANNIER90=.TRUE. switches on the interface between VASP and WANNIER90.

**N.B.**: This feature is only present if VASP is compiled with -DVASP2WANNIER90 or -DVASP2WANNIER90v2.

---

For LWANNIER90=.TRUE., VASP will write the input files for a WANNIER90 run: **wannier90.win**, **wannier90.mmn**, **wannier90.eig**, **wannier90.amn**, and if LWRITE\_UNK=.TRUE. **wannier90.UNKp.s**. This is done by running wannier\_setup in library mode as described in Chapter 6 of the WANNIER90 manual. For documentation of these files and tags therein, please refer to the WANNIER90 manual.

The following cases may occur:

* If **wannier90.win** does not exist, VASP will write the following template

```
num_wann = NBANDS

begin unit_cell_cart
  ... ... ...
  ... ... ...
  ... ... ...
end unit_cell_cart

begin atoms_cart
   ... ... ...
   ... ... ...
   ... ... ...
   ... ... ...  
end atoms_cart

mp_grid = .. .. ..

begin kpoints
   ... ... ...
   ... ... ...
   ... ... ...
   ... ... ...
end kpoints
```

:   Here, the unit\_cell\_cart, atoms\_cart, and kpoints blocks, and mp\_grid array, will be set in accordance with the setup of the VASP calculation. This basically corresponds to the information given in the POSCAR and KPOINTS files.

* If the **wannier90.win** file already exists, VASP will only add the aforementioned information if it is not already present. This means that VASP will check, for instance, whether or not the **wannier90.win** file contains a kpoints block, and add one if not. **Mind**: If it finds a kpoints block, VASP will not check whether this block agrees with the k points used in the VASP calculation!

The user may create a **wannier90.win** file prior to running VASP with LWANNIER90=.TRUE., and specify any tag and/or block that is understood by wannier\_setup and/or wannier\_run. For instance, one can specify the projections block in the **wannier90.win** file that controls the initial guess for the maximally localized Wannier functions.
Then, VASP writes the projections of the Bloch functions onto the relevant projectors to the **wannier90.amn** file. See Chapter 3 of the WANNIER90 manual for more information.

## Related tags and articles

LWRITE\_UNK,
LWRITE\_MMN\_AMN,
LWRITE\_SPN,
LWANNIER90\_RUN,
NUM\_WANN,
WANNIER90\_WIN

Examples that use this tag

---
