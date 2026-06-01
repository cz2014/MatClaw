# ELPH_FERMI_NEDOS

Categories: INCAR tag, Electron–phonon coupling, Electronic occupancy

ELPH\_FERMI\_NEDOS = [integer]  
 Default: **ELPH\_FERMI\_NEDOS** = 501

Description: Number of Gauss–Legendre integration points used to evaluate the Fermi–Dirac distribution and determine the electronic Fermi level at finite temperature in the context of electron–phonon (el–ph) coupling calculations.

> **Mind:** Available as of VASP 6.5.0

---

**ELPH\_FERMI\_NEDOS** plays the same role as EFERMI\_NEDOS, but specifically in the context of electron-phonon coupling calculations.
It defines the number of points in the Gauss–Legendre grid used when integrating the Fermi–Dirac distribution to determine the Fermi level within the el–ph workflow.

Larger values yield more accurate Fermi–Dirac occupations and energy derivatives, particularly at low temperatures or when evaluating sharp features in the electronic density of states near the Fermi energy.
A short convergence test is recommended for systems with narrow bands or strong temperature dependence in el–ph properties.

For details of the numerical integration scheme, see EFERMI\_NEDOS.

## Related tags and articles

* EFERMI\_NEDOS
* TRANSPORT\_NEDOS
* ISMEAR
* Transport coefficients including electron-phonon scattering
* Smearing technique
