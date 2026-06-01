# NGY

Categories: INCAR tag, Projector-augmented-wave method

NGY = [integer]  
 Default: **NGY** = set in accordance with PREC and ENCUT

Description: NGY sets the number of grid points in the FFT grid along the second lattice vector.

---

By default NGY is set in accordance with the requested "precision" mode PREC and the plane wave kinetic energy cutoff ENCUT:

:   :   |  |  |
        | --- | --- |
        | PREC | NGY |
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

Alternatively, NGY can be set to a specific value in the INCAR file.

## Related tags and articles

NGX,
NGZ,
NGXF,
NGYF,
NGZF,
PREC,
ENCUT,
ENAUG

Examples that use this tag
