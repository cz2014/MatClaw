# NGZ

Categories: INCAR tag, Projector-augmented-wave method

NGZ = [integer]  
 Default: **NGZ** = set in accordance with PREC and ENCUT

Description: NGZ sets the number of grid points in the FFT grid along the third lattice vector.

---

By default NGZ is set in accordance with the requested "precision" mode PREC and the plane wave kinetic energy cutoff ENCUT:

:   :   |  |  |
        | --- | --- |
        | PREC | NGZ |
        | Normal | 3/2×$G\_{\rm cut}$ |
        | Single (VASP.5) | 3/2×$G\_{\rm cut}$ |
        | Single (VASP.6) | 2×$G\_{\rm cut}$ |
        | SingleN (VASP.6) | 3/2×$G\_{\rm cut}$ |
        | Accurate | 2×$G\_{\rm cut}$ |
        | Low | 3/2×$G\_{\rm cut}$ |
        | Medium | 3/2×$G\_{\rm cut}$ |
        | High | 2×$G\_{\rm cut}$ |

where

:   $$E\_{\rm cut}=\frac{\hbar^2}{2m\_e}G\_{\rm cut}^2$$

with $E\_{\rm cut}$=ENCUT.

Alternatively, NGZ can be set to a specific value in the INCAR file.

## Related tags and articles

NGX,
NGY,
NGXF,
NGYF,
NGZF,
PREC,
ENCUT,
ENAUG

Examples that use this tag

---
