# Category:Hybrid functionals

Categories: VASP, Exchange-correlation functionals

**Hybrid functionals** mix the Hartree-Fock (HF) and Kohn-Sham theories and can be more accurate than semilocal methods, e.g., GGA, in particular for nonmetallic systems. They are for instance suited for band-gap calculations. Several hybrid functionals are available in VASP.

## Theoretical background

In hybrid functionals the exchange part consists of a linear combination of HF and semilocal (e.g., GGA) exchange:

:   $$E\_{\mathrm{xc}}^{\mathrm{hybrid}}=a E\_{\mathrm{x}}^{\mathrm{HF}} + (1-a)E\_{\mathrm{x}}^{\mathrm{GGA}} + E\_{\mathrm{c}}^{\mathrm{GGA}}$$

where $a$ determines the relative amount of HF and semilocal exchange. The hybrid functionals can be divided into families according to the interelectronic range at which the HF exchange is applied: at full range (unscreened hybrids) or either at short or long range (called screened or range-separated hybrids). From the practical point of view, the short-range hybrid functionals like HSE06 are preferable for periodic solids, since leading to faster convergence with respect to the number of k-points (or size of the unit cell).

Note that as in most other codes, hybrid functionals are implemented in VASP within the generalized KS scheme, which means that the total energy is minimized with respect to the orbitals (instead of the electron density) as in the Hartree-Fock theory.

It is important to mention that hybrid functionals are computationally more expensive than semilocal methods.

Read more about formalism of the HF method and hybrids.

The unscreened Coulomb potential used to evaluate the exchange integral in Hartree-Fock has an integrable singularity that leads to slow convergence with respect to supercell size (or equivalently **k** point sampling).
To make the computations feasible requires special treatment of the Coulomb singularity.

## How to

* List of available hybrid functionals and how to specify them in the INCAR file.
* Downsampling of the Hartree-Fock operator to reduce the computational cost.
* band-structure calculation using hybrid functionals.

## Tutorials

* Tutorial for hybrid calculations.
* Lecture for hybrid functionals.

## Further reading

* A comprehensive study of the performance of the HSE03/HSE06 functional compared to the PBE and PBE0 functionals.
* The B3LYP functional applied to solid state systems.
* Applications of hybrid functionals to selected materials: Ceria, lead chalcogenides, CO adsorption on metals, defects in ZnO, excitonic properties, SrTiO and BaTiO.

## References

---
