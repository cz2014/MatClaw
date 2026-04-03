# NGXF

Categories: INCAR tag, Projector-augmented-wave method

NGXF = [integer]  
 Default: **NGXF** = set in accordance with PREC, NGX, ENCUT and ENAUG

Description: NGXF sets the number of grid points in the "fine" FFT grid along the first lattice vector.

---

On this "fine" FFT mesh the localized augmentation charges are represented if ultrasoft pseudopotentials (USPPs) or the PAW method are used. In case USPPs are used, the local potentials (exchange-correlation, Hartree-potential and ionic potentials) are also calculated on this "fine" FFT-mesh.

By default NGXF is set in accordance with the requested "precision" mode PREC, NGX, and the plane wave kinetic energy cutoffs ENCUT and ENAUG:

:   :   |  |  |  |
        | --- | --- | --- |
        | PREC | NGX | NGXF |
        | Normal | 3/2×$G\_{\rm cut}$ | 2×NGX |
        | Single (VASP.5) | 3/2×$G\_{\rm cut}$ | NGX |
        | Single (VASP.6) | 2×$G\_{\rm cut}$ | NGX |
        | SingleN (VASP.6) | 3/2×$G\_{\rm cut}$ | NGX |
        | Accurate | 2×$G\_{\rm cut}$ | 2×NGX |
        | Low | 3/2×$G\_{\rm cut}$ | 3×$G\_{\rm aug}$ |
        | Medium | 3/2×$G\_{\rm cut}$ | 4×$G\_{\rm aug}$ |
        | High | 2×$G\_{\rm cut}$ | 16/3×$G\_{\rm aug}$ |

where

:   $$E\_{\rm cut}=\frac{\hbar^2}{2m\_e}G\_{\rm cut}^2 \qquad E\_{\rm aug}=\frac{\hbar^2}{2m\_e}G\_{\rm aug}^2$$

with $E\_{\rm cut}$=ENCUT and $E\_{\rm aug}$=ENAUG.

Alternatively, NGXF can be set to a specific value in the INCAR file.

## Related tags and articles

NGX,
NGY,
NGZ,
NGYF,
NGZF,
PREC,
ENCUT,
ENAUG

Examples that use this tag
