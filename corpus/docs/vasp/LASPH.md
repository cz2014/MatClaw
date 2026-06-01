# LASPH

Categories: INCAR tag, Exchange-correlation functionals

LASPH = .TRUE. | .FALSE.  
 Default: **LASPH** = .FALSE.

Description: include non-spherical contributions related to the gradient of the density in the PAW spheres.

---

Usually VASP calculates only the spherical contribution to the gradient corrections inside the PAW spheres (non-spherical contributions for the LDA part of the potential and the Hartree potential are always included).

For LASPH = .TRUE., non-spherical contributions from the gradient corrections inside the PAW spheres will be included as well. For VASP.4.6, these contributions are only included in the total energy, after self-consistency has been reached disregarding the aspherical contributions in the gradient corrections.

For VASP.5.X the aspherical contributions are properly accounted for in the Kohn-Sham potential as well, if
LASPH = .TRUE. is set. This is essential for accurate total energies and band structure calculations for *f*-elements (e.g. ceria), all 3*d*-elements (transition metal oxides), and magnetic atoms in the 2nd row (B-F atom), in particular if DFT+U or hybrid functionals, meta-GGAs, or vdW-DFT are used, since these functionals often result in aspherical charge densities.

## Related tags and articles

LMAXPAW,
LMAXTAU,
LMIXTAU

Examples that use this tag

---
