# Harris-Foulkes functional

Categories: Theory, Exchange-correlation functionals

The **Harris-Foulkes** (HF) **functional** is a non-self-consistent functional.
The potential is constructed for some "input" charge density, then the band-structure term is calculated for this fixed non-self-consistent potential. Double counting corrections are calculated from the input charge density. The functional can be written as

:   :   $$E\_{\mathrm{HF}} [\rho\_{\mathrm{in}} ,\rho] = \mathrm{ bandstructure} \mathrm{ for } (V^H\_{\mathrm{in}} + V^{xc}\_{\mathrm{in}}) + \mathrm{Tr}[(-V^{H}\_{\mathrm{in}}/2 -V^{xc}\_{\mathrm{in}}) \rho\_{\mathrm{in}} ] + E^{xc}[\rho\_{\mathrm{in}}+\rho\_{c}].$$

In our experience, the functional gives a good description of the binding energies, equilibrium-lattice constants, and bulk-modulus even for covalently bonded systems like Ge. In a test calculation, we have found that the pair-correlation function of l-Sb calculated with the HF functional and the full Kohn-Sham functional differs only slightly. Nevertheless, we must point out that the computational gain in comparison to a self-consistent calculation is in many cases very small (for Sb less than $20~\%$). The main reason why to use the HF functional is therefore to access and establish the accuracy of the HF functional. To our knowledge, VASP is one of the few pseudopotential codes, which can access the validity of the HF functional at a very basic level, i.e., without any additional restrictions like local basis-sets, etc.

The band-structure energy is exactly evaluated using the same plane-wave basis-set and the same accuracy used for the self-consistent calculation. The forces and the stress tensor are correct, insofar as they are an exact derivative of the Harris-Foulkes functional. During a molecular dynamics calculation or an ionic relaxation the charge density is updated at each ionic step to enforce the HF functional.

Ideas based on the Harris-Foulkes functional are applied when LCORR or ICHARG=12.

## Related tags and articles

LCORR,
ICHARG

Examples that use this tag
