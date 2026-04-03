# NGZF

Categories: INCAR tag, Projector-augmented-wave method

NGZF = [integer]  
 Default: **NGZF** = set in accordance with PREC, NGZ, ENCUT and ENAUG

Description: NGZF sets the number of grid points in the "fine" FFT grid along the first lattice vector.

---

On this "fine" FFT mesh the localized augmentation charges are represented if ultrasoft pseudopotentials (USPPs) or the PAW method are used. In case USPPs are used, the local potentials (exchange-correlation, Hartree-potential, and ionic potentials) are also calculated on this "fine" FFT-mesh.

By default NGZF is set in accordance with the requested "precision" mode PREC, NGZ, and the plane wave kinetic energy cutoffs ENCUT and ENAUG:

:   :   |  |  |  |
        | --- | --- | --- |
        | PREC | NGZ | NGZF |
        | Normal | 3/2×$G\_{\rm cut}$ | 2×NGZ |
        | Single (VASP.5) | 3/2×$G\_{\rm cut}$ | NGZ |
        | Single (VASP.6) | 2×$G\_{\rm cut}$ | NGZ |
        | SingleN (VASP.6) | 3/2×$G\_{\rm cut}$ | NGZ |
        | Accurate | 2×$G\_{\rm cut}$ | 2×NGZ |
        | Low | 3/2×$G\_{\rm cut}$ | 3×$G\_{\rm aug}$ |
        | Medium | 3/2×$G\_{\rm cut}$ | 4×$G\_{\rm aug}$ |
        | High | 2×$G\_{\rm cut}$ | 16/3×$G\_{\rm aug}$ |

where

:   $$E\_{\rm cut}=\frac{\hbar^2}{2m\_e}G\_{\rm cut}^2 \qquad E\_{\rm aug}=\frac{\hbar^2}{2m\_e}G\_{\rm aug}^2$$

with $E\_{\rm cut}$=ENCUT and $E\_{\rm aug}$=ENAUG.

Alternatively, NGZF can be set to a specific value in the INCAR file.

## Related tags and articles

NGX,
NGY,
NGZ,
NGXF,
NGYF,
PREC,
ENCUT,
ENAUG

Examples that use this tag
