# ENCUTLR

Categories: INCAR tag, Electron-phonon interactions

ENCUTLR = [real]  
 Default: **ENCUTLR** = 50 eV

Description: Reciprocal space cutoff for the treatment of the long-range contribution.

> **Mind:** Available as of VASP 6.5.0

---

Similar to the treatment of the long-range part of the force-constants, the potential and the PAW strengths also require a special treatment in polar materials.
The correction scheme involves an Ewald summation over reciprocal lattice vectors that converges rapidly in reciprocal space.
ENCUTLR controls the number of G-vectors included in the Ewald sum in the same way as ENCUT controls the number of G-vectors (plane-wave components) of the electronic Kohn-Sham orbitals.

## Related tags and articles

* IFC\_LR
* ELPH\_LR
* PHON\_G\_CUTOFF

## References
