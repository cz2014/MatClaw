# ADDGRID

Categories: INCAR tag, Projector-augmented-wave method

ADDGRID = .TRUE. | .FALSE.  
 Default: **ADDGRID** = .FALSE.

Description: ADDGRID determines whether an additional support grid is used for the evaluation of the augmentation charges.

---

When ADDGRID=.TRUE. VASP uses an additional support grid for the evaluation of the augmentation charges. This grid contains 8 times more points than the standard "fine" grid (NGXF×NGYF×NGZF). Whenever terms involving augmentation charges are evaluated, this additional grid is used. For instance: The augmentation charge is evaluated first in real space on this additional grid, FFT-transformed to reciprocal space, and then added to the total charge density on the standard "fine" grid (NGXF×NGYF×NGZF). The additional grid often helps to reduce the noise in the forces. In some cases, it even allows to perform calculations with NGXF=NGX.

Caveat:
If there is any contribution in the density or potential at the highest Fourier component $G$ of
the conventional fine grid (given by NGXF×NGYF×NGZF), then Fourier interpolation to twice the grid density leads to
oscillations in real space. These oscillations correspond to the largest wave vector $G\_{cut}$ i.e. $e^{i G\_{cut} r}$.
In real space, the charge density or potential will therefore alternate between positive and negative
values on the ultra-fine grid, in particular, in regions where the density or potential are small.
The terminus techniques is "termination wiggles".
Although this is a somewhat oversimplified presentation, it is fairly straightforward to derive more rigorous results in 1D.
The upshot is that Fourier-interpolation can lead to termination wiggles with oscillations $e^{i G\_{cut} r}$ in the interpolated potential (where $G\_{cut}$ corresponds to
the largest Fourier components on the fine grid). Fourier smoothing, which is in essence used for the augmentation densities, is generally less problematic, but it can also result in negative density in real space.
Therefore, we recommend performing careful tests, on whether ADDGRID works as desired; please do not use this tag as default in all your calculations!

## Related tags and articles

PREC,
NGX,
NGY,
NGZ,
NGXF,
NGYF,
NGZF,
ENCUT,
ENAUG,
ENMAX,
PRECFOCK

Examples that use this tag
