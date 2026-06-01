# ICORELEVEL

Categories: INCAR tag, Linear response, Dielectric properties, XAS

ICORELEVEL = 0 | 1 | 2  
 Default: **ICORELEVEL** = 0

Description: ICORELEVEL controls whether the core energies are explicitly calculated or not and how they are calculated.

---

The binding energy of core electrons $E\_{CL}$ is given as

:   $E\_{CL} = E(n\_{c}-1) - E(n\_{c})$.

Here, $E(n\_{c})$ is the energy from a standard density-functional calculation in which the number of core electrons corresponds to the unexcited ground state. $E(n\_{c}-1)$ is the energy of a calculation where one electron is removed from the core of one particular atom and added to the valence or conduction band.

The core-level binding energies can be calculated either in the initial-state approximation or the final-state approximation. In the initial-state approximation, a core electron is removed from the core states and added to the valence/conduction bands but no change of the potential (by e.g. relaxation of the valence electrons) is allowed. The core-level binding energy can then be directly calculated by the Kohn-Sham eigenvalues of the core level $\epsilon\_{c}$ and the Fermi energy $\epsilon\_{F}$

:   $E\_{CL}^{\mathrm{i}}=\epsilon\_{c} - \epsilon\_{F}$.

In the final-state approximation, the electrons (valence electrons in the frozen-core approximation) are allowed to relax, so that the local hole is screened. In other words, a fully self-consistent electronic calculation is carried out with a core hole and an additional electron in the valence/conduction bands.

The following options are available in VASP:

* ICORELEVEL=0: The core energies are not calculated (default).
* ICORELEVEL=1: The initial-state approximation is used. This just involves recalculating the KS eigenvalues of the core states

after a self-consistent calculation of the valence charge density. ICORELEVEL=1 is a little bit more involved than the calculations using
LVTOT=*.TRUE.*, since the Kohn-Sham energy of each core state is recalculated. This adds very little extra cost to the calculations. Usually,
the shifts correspond very closely to the change of the electrostatic potential at the lattice sites (calculated using LVTOT=*.TRUE.*).

* ICORELEVEL=2: The final-state approximation is used. Electrons are removed from the core and placed into the valence (effectively increasing NELECT). The VASP implementation excites all selected core electrons for

all atoms of one species. The species, as well as the selected electrons, are specified using

```
CLNT = species 
CLN =  main quantum number of excited core electron 
CLL =  l quantum number of excited core electron
CLZ =  electron count
```

The electron count CLZ specifies how many electrons are excited
from the core. Usually, 1 or 0.5 (Slater's transition state) are sensible choices.
CLNT selects for which species in the POTCAR file the electrons
are excited. Usually one would like to excite the electrons for
only one atom, this requires changing the POSCAR and POTCAR file,
such that the selected atom corresponds to one species in the POTCAR file.
i.e. if the calculation invokes a supercell with 64 atoms of one type,
the selected atom needs to be singled out, and the POSCAR file will
then contain 63 "standard" atoms as well as one special species,
at which the excited core hole will be placed
(the POTCAR file will hold two identical PAW datasets in this case).

Several caveats apply to this mode.
First, the excited electron is always spherical and multipole splittings
are not available. Second, the other core electrons are not allowed
to relax, which might cause a slight error in the calculated
energies.
Third, absolute energies are not meaningful, since VASP usually
reports valence energies only. Only relative
shifts of the core electron binding energies are relevant
(in some cases, the VASP total energies might become even positive).

## Super-cell core-hole method

ICORELEVEL=2 and its related tags are necessary for the calculation of X-ray absorption spectra (XAS) using the super-cell core-hole method.

A description of how to set up super-cell core-hole calculations is given in this article.

A tutorial for the calculation of XAS is given in this article.

## Bethe-Salpeter equation for XAS

ICORELEVEL=2 is required for the calculation of XAS using the Bethe-Salpeter equation.

A description of how to set up a BSE calculation for XAS is given in this article. There is also an accompanying theory page.

## Related tags and articles

CLNT, CLN, CLL, CLZ, CH\_LSPEC, CH\_SIGMA, CH\_NEDOS,
ALGO,
LADDER,
LHARTREE,
NBANDSV,
NBANDSO,
OMEGAMAX,
ANTIRES

Bethe-Salpeter equation for core excitations
Supercell core-hole calculations

Examples that use this tag

## References

---
