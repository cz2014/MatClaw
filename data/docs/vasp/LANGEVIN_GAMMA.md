# LANGEVIN_GAMMA

Categories: INCAR tag, Molecular dynamics, Thermostats

LANGEVIN\_GAMMA = [Real array]  
 Default: **LANGEVIN\_GAMMA** = NTYP×0

Description: LANGEVIN\_GAMMA specifies the friction coefficients (in ps-1) for atomic degrees-of-freedom when using a Langevin thermostat (in case VASP was compiled with -Dtbdyn).

---

When using a Langevin thermostat (MDALGO=3), the friction coefficients γ for the atomic degrees-of-freedom are specified (in ps-1) using the LANGEVIN\_GAMMA-tag.

One has to specify a separate friction coefficient for each of the NTYP atomic species found on the POTCAR-file.

#### Practical example

Consider a system consisting of 16 hydrogen and 48 silicon atoms. Suppose that eight silicon atoms are considered to be Langevin atoms and the remaining 32 Si atoms are either fixed or Newtonian atoms. The Langevin and Newtonian (or fixed) atoms should be considered as different species, *i.e.*, the POSCAR-file should contain the line like this:

```
Si H Si
40 16 8
```

As only the final eight Si atoms are considered to be Langevin atoms, the INCAR-file should contain the following line defining the friction coefficients:

```
LANGEVIN_GAMMA = 0.0   0.0   10.0
```

*i.e.*, for all non-Langevin atoms, γ should be set to zero.

## Related tags and articles

LANGEVIN\_GAMMA\_L,
MDALGO

Examples that use this tag

## References

---
