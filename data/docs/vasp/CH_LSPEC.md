# CH_LSPEC

Categories: INCAR tag, Linear response, Dielectric properties, XAS

CH\_LSPEC = [logical]  
 Default: **CH\_LSPEC** = .FALSE.

Description: This flag controls whether the dielecectric function using the supercell core-hole method is calculated or not.

---

How to calculate X-ray absorption spectra from the supercell core-hole method are is explained here.

This tag should be used in combination with the following important tags for the core-hole approximation:

* ICORELEVEL: To enable core-hole calculations in the final-state approximation with self-consistent field cycles (SCF) one has to set ICORELEVEL=2. Core-hole calculations in the initial-state approximation (ICORELEVEL=1) are also available, but they are physically less relevant and should be only used if especially needed.
* CLNT: This tag selects the species holding the core hole. This number corresponds to the species defined in the POSCAR and POTCAR files.
* CLN: Specifies the $n$ quantum number of the excited electron.
* CLL: Specifies the $l$ quantum number of the excited electron.
* CLZ: Specifies how much of a faction of the chosen electron should be excited. Usually one always sets CLZ=1.0, but in some cases values lesser than 1 can lead to better agreement with experiment. However, this should be handled with caution since the physics behind is very dubious.

And following tags to control the calculation of the dieletric function:

* CH\_SIGMA: The broadening of the spectrum is by default of Gaussian form and the broadening width in eV is set by CH\_SIGMA. We recommend using a very small broadening CH\_SIGMA$\le$0.001 in the calculations and to broaden the spectrum in post-processing. Also, the spectrum can be recalculated with different parameters without the need to redo the electronic self-consistent field cycle. For that one can use the converged WAVECAR from the previous calculation and set ALGO=*None* together with the new parameters for the spectrum "CH\_\*" in the INCAR file.
* CH\_NEDOS: Sets the number of grid points on the energy axis of the spectrum.
* CH\_AMPLIFICATION: Scaling of the spectrum by the specified value. This tag is not important but can be useful sometimes if one needs to scale the spectrum a priori. Otherwise, it is recommended to scale the spectrum a posteriori.

> **Warning:** For XAS calculations it is strongly recommended to use the available GW PAW potentials for the POTCAR files, since many standard potentials don't have projectors with quantum numbers 2 or larger and the GW potentials are more exact for excited states than the standard potentials.

## Related tags and articles

CH\_SIGMA, CH\_NEDOS, CH\_AMPLIFICATION, ICORELEVEL, CLNT, CLN, CLL, CLZ, ISMEAR, CH\_AMPLIFICATION

Examples that use this tag

---
