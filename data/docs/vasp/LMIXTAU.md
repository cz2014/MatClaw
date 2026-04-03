# LMIXTAU

Categories: INCAR tag, Exchange-correlation functionals, Density mixing

LMIXTAU = .TRUE. | .FALSE.  
 Default: **LMIXTAU** = .FALSE.

Description: send the kinetic-energy density through the density mixer as well.

---

In many cases, the density-mixing scheme works well enough without passing the kinetic-energy density through the mixer. Therefore VASP uses LMIXTAU=.FALSE. per default. However, when the self-consistency cycle fails to converge for one of the algorithms exploiting density mixing, e.g, IALGO=38 or 48, we recommend setting LMIXTAU=.TRUE..

## Related tags and articles

METAGGA,
LMAXTAU

Examples that use this tag

---
