# PREC

Categories: INCAR tag, Projector-augmented-wave method, Memory

PREC = Normal | Single | SingleN | Accurate | Low | Medium | High

|  |  |  |
| --- | --- | --- |
| Default: **PREC** | = Medium | for VASP.4.X |
|  | = Normal | since VASP.5.X |

Description: PREC specifies the "precision" mode.

---

PREC sets default values for the energy cutoff ENCUT, the FFT grids (NGX,NGY,NGZ) and (NGXF,NGYF,NGZF), and the accuracy of the projectors in real space ROPT (used only when LREAL=.TRUE.). Details are given below in the table.

We recommend using PREC=Normal or PREC=Accurate. PREC=Normal can be used for most routine calculations. PREC=Accurate leads to a denser grid (NGX,NGY,NGZ). Thus, it reduces egg-box effects and strictly avoids any aliasing/wrap-around errors. PREC=Normal and PREC=Accurate use an augmentation fine grid (NGXF,NGYF,NGZF) that is twice larger than the grid (NGX,NGY,NGZ) used for the representation of the pseudo-orbitals. PREC=Accurate increases the memory requirements somewhat, but it should be used (in combination with an increased value for ENCUT) when a very good accuracy is required, e.g., for accurate forces, for phonons and stress tensor or in general when second derivatives are computed. The accuracy of forces can also be sometimes further improved by specifying ADDGRID=.TRUE., however, reports from users are somewhat contradictory about whether this really helps. More details can be found at Energy cutoff and FFT mesh.

> **Important:**
>
> * We strongly recommend specifying the energy cutoff ENCUT always manually in the INCAR file to ensure the same accuracy between calculations. Otherwise, the default ENCUT may differ among the different calculations (e.g., for the calculation of the cohesive energy), with the consequence that the total energies, for instance, can not be compared.
> * Setting PREC=Accurate does not necessarily mean that the results are converged. The convergence of the results with respect to the energy cutoff ENCUT has to be checked separately.
> * Setting ENAUG has an effect only if PREC is set to one of the deprecated settings (Low, Medium or High); otherwise, it is ignored.

> **Mind:**
>
> * The value of a parameter set by PREC (e.g., ENCUT) can be overridden by specifying explicitly the value of that parameter in the INCAR file.
> * PREC=Normal and PREC=Accurate are only available in VASP.4.5 and newer versions. The setting PREC=Single is only available as of VASP.5.1, and has been updated in VASP.6.

> **Deprecated:** The old settings PREC=Medium, High and Low are no longer recommended and are available only for backward compatibility. Essentially, PREC=High only increases the energy cutoff by 30 %, which can also be achieved by just manually increasing ENCUT.

## Default values set by PREC

Default values set by PREC for the parameters ENCUT, (NGX,NGY,NGZ), (NGXF,NGYF,NGZF) and ROPT:

:   :   |  |  |  |  |  |  |
        | --- | --- | --- | --- | --- | --- |
        | PREC | ENCUT | NGX,Y,Z | NGXF,YF,ZF | ROPT (LREAL=A) | ROPT (LREAL=O) |
        | Normal | max(ENMAX) | 3/2×$G\_{\rm cut}$ | 2×NGX | -5×10-4 | 1.0 |
        | Single (VASP.5) | max(ENMAX) | 3/2×$G\_{\rm cut}$ | NGX | -5×10-4 | 1.0 |
        | Single (VASP.6) | max(ENMAX) | 2×$G\_{\rm cut}$ | NGX | -5×10-4 | 1.0 |
        | SingleN (VASP.6) | max(ENMAX) | 3/2×$G\_{\rm cut}$ | NGX | -5×10-4 | 1.0 |
        | Accurate | max(ENMAX) | 2×$G\_{\rm cut}$ | 2×NGX | -2.5×10-4 | 1.0 |
        | **Deprecated settings:** | | | | | |
        | Low | max(ENMIN) | 3/2×$G\_{\rm cut}$ | 3×$G\_{\rm aug}$ | -1×10-2 | 2/3 |
        | Medium | max(ENMAX) | 3/2×$G\_{\rm cut}$ | 4×$G\_{\rm aug}$ | -2×10-3 | 1.0 |
        | High | 1.3×max(ENMAX) | 2×$G\_{\rm cut}$ | 16/3×$G\_{\rm aug}$ | -4×10-4 | 1.5 |

where max(ENMAX) and max(ENMIN) are the maxima of ENMAX and ENMIN found in the POTCAR file, and $G\_{\rm cut}$ and $G\_{\rm aug}$ are defined by

:   $$E\_{\rm cut}=\frac{\hbar^2}{2m\_e}G\_{\rm cut}^2 \qquad E\_{\rm aug}=\frac{\hbar^2}{2m\_e}G\_{\rm aug}^2$$

with $E\_{\rm cut}$=ENCUT and $E\_{\rm aug}$=ENAUG.

## Further remarks

* With PREC=Normal, Single, and Accurate the grid (NGXF,NGYF,NGZF) representing the augmentation charges, charge densities and potentials has either the same size (PREC=Single) or the double size (PREC=Normal or Accurate) as the grid (NGX,NGY,NGZ). With the deprecated (and no longer recommended) settings for PREC (Low, Medium and High), the grid (NGXF,NGYF,NGZF) is determined by some heuristic formula from ENAUG.

* PREC=Single uses the same grid (NGX,NGY,NGZ) as PREC=Normal in VASP.5, but the same grid as PREC=Accurate in VASP.6. However, the double grid technique is not used, i.e., (NGXF,NGYF,NGZF)=(NGX,NGY,NGZ). This is convenient if one needs to cut down on storage demands or if one wants to reduce the size of the files CHG and CHGCAR. Furthermore, PREC=Single avoids high-frequency oscillations caused by the double-grid technique and the resulting Fourier interpolation. It is often expedient for scanning tunneling simulations or other calculations where high-frequency wiggles of the charge density in the vacuum region are undesirable.

* PREC=High should guarantee that the absolute energies are converged to a few meV and the stress tensor converged within a few kBar.

## Related tags and articles

NGX,
NGY,
NGZ,
NGXF,
NGYF,
NGZF,
ENCUT,
ENAUG,
ENMIN,
ENMAX,
ROPT,
LREAL,
ADDGRID,
PRECFOCK,
Energy cutoff and FFT mesh,
Wrap-around errors

Examples that use this tag
