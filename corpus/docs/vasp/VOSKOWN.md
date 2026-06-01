# VOSKOWN

Categories: INCAR tag, Exchange-correlation functionals

VOSKOWN = 0 | 1  
 Default: **VOSKOWN** = 0

Description: Determines whether Vosko-Wilk-Nusair interpolation is used or not.

---

This flag is not relevant for most "modern" gradient corrected functionals, such as PBE or PBEsol.

For the LDA and some "older" gradient corrected functionals such as PW91, VASP interpolates the correlation energy from the non-spinpolarized to the fully spinpolarized case in the same way as the exchange energy (Barth-Hedin spin interpolation. If VOSKOWN is set to 1, the interpolation formula according to Vosko, Wilk and Nusair is used (this interpolation is based on the RPA correlation energy of partially spin polarized systems). The Vosko, Wilk and Nusair interpolation usually enhances the magnetic moments and the magnetic energies. Because the Vosko-Wilk-Nusair interpolation is the interpolation usually applied in the context of gradient corrected functionals, it is desirable to use this interpolation whenever the PW91 functional is applied. Setting this tag is not required for most modern functions, such as the PBE or PBEsol functional, since these functional strictly follow the original publications and disregard the setting of this flag entirely (this implicitly implies that the correlation energy is interpolated according to Vosko, Wilk and Nusair).

## References

Examples that use this tag

---
