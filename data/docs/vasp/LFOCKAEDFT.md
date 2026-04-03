# LFOCKAEDFT

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals, Many-body perturbation theory, GW

LFOCKAEDFT = [logical]  
 Default: **LFOCKAEDFT** = .FALSE.

Description: LFOCKAEDFT forces VASP to use the same charge augmentation
for the Hartree and DFT exchange correlation part as is used in the Fock exchange and
the many body beyond DFT methods, such as RPA, MP2 etc.

---

This flag should be set only in exceptional cases. The Hartree as well
as the DFT part are usually calculated very accurately using the one-centre
PAW spheres. Restoring the all-electron charge accurately on the plane
wave grid adds potentially noise, but should not change the results (relative energies,
forces etc.).
The flag, however, needs to be set for optimized potential methods, which
are supported by VASP but not documented yet.

## Related tags and articles

LMAXFOCKAE,
NMAXFOCKAE,
QMAXFOCKAE

Examples that use this tag

---
