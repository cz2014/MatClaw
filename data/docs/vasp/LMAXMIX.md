# LMAXMIX

Categories: INCAR tag, Density mixing

LMAXMIX = [integer]  
 Default: **LMAXMIX** = 2

Description: LMAXMIX controls up to which *l*-quantum number the one-center PAW charge densities are passed through the charge density mixer and written to the CHGCAR file.

---

Higher *l*-quantum numbers (*l*>LMAXMIX) are not handled by the density mixer (these components of the one-center charge density are set to the value corresponding to the present orbitals). Usually, it is not necessary to increase LMAXMIX, but the following cases are exceptions:

* DFT+U calculations require, in many cases, an increase of LMAXMIX to 4 for *d*-electrons (or 6 for *f*-elements) to obtain fast convergence to the ground state.

* The CHGCAR file will contain the one-center PAW occupancy matrices up to LMAXMIX. When the CHGCAR file is read and kept fixed in the course of the calculations (ICHARG=11), the results will not necessarily be identical to a self-consistent run. The deviations will be large for DFT+U calculations. For the calculation of band structures within the DFT+U approach, it is strictly required to increase LMAXMIX to 4 for *d*-elements and to 6 for *f*-elements.

* SDFT calculations that consider noncollinear magnetism often require slow mixing of the spin density up to 4 for *d*-elements and up to 6 for *f*-elements to obtain fast convergence to the ground state.

## Related tags and articles

IMIX,
INIMIX,
MAXMIX,
BMIX,
AMIX\_MAG,
BMIX\_MAG,
AMIN,
MIXPRE,
WC

Examples that use this tag
