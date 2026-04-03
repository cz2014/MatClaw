# SCALEE

Categories: INCAR tag, Advanced molecular-dynamics sampling

SCALEE = [real]  
 Default: **SCALEE** = 1

Description: This tag specifies the coupling parameter of the energies and forces between a fully interacting system and a reference system.

---

The tag SCALEE sets the coupling parameter $\lambda$ and hence controls the Hamiltonian of the calculation.
By default SCALEE=1 and the scaling of the energies and forces via the coupling constant is internally skipped in the code. To enable the scaling SCALEE$\ne$1 has to be specified.

More information using this tag is given here.

## Related tags and articles

VCAIMAGES, IMAGES, NCORE IN IMAGE1, PHON\_NSTRUCT, IBRION

---
