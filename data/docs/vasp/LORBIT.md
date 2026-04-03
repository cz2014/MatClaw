# LORBIT

Categories: INCAR tag, Electronic ground-state properties, Density of states, Band structure

LORBIT = 0 | 1 | 2 | 5 | 10 | 11 | 12  
 Default: **LORBIT** = 0

Description: Selects a projection method onto local quantum numbers ($lm$) and writes PROCAR/PROOUT file.

---

When LORBIT is set, VASP performs a post-processing step of the Kohn-Sham (KS) orbitals to decompose the KS orbitals into local quantum numbers ($lm$) and obtain local properties, e.g., the on-site charge density or on-site magnetic moments due to the spin degrees of freedom. The decomposition is achieved by means of one of several projection methods selected by LORBIT. All these projections rely on the fact that most of the charge density is close to the ion center, and interstitial regions separate them well. This is merely a qualitative approach in contrast to performing a wannierization in order to obtain a localized basis, but often it serves as a good estimate.

> **Tip:** As this is a post-processing step, LORBIT can be added/changed when restarting a converged calculation. To this end, set ALGO=None and the desired LORBIT, and restart from WAVECAR.

For VASP version < 6 with LORBIT >= 11 and ISYM = 2, see known issues.

## Projection methods

See the table for an overview:

:   |  |  |  |
    | --- | --- | --- |
    | LORBIT | RWIGS tag | files written |
    | 0 | required | DOSCAR and PROCAR |
    | 1 | required | DOSCAR and *lm*-decomposed PROCAR |
    | 2 | required | DOSCAR and *lm*-decomposed PROCAR + phase factors |
    | 5 | required | DOSCAR and PROOUT |
    | 10 | ignored | DOSCAR and PROCAR |
    | 11 | ignored | DOSCAR and *lm*-decomposed PROCAR |
    | 12 | ignored | DOSCAR and *lm*-decomposed PROCAR + phase factors (not recommended) |
    | 13 | ignored | DOSCAR and *lm*-decomposed PROCAR + phase factors, choose best projector for each band (not recommended) |
    | 14 | ignored | DOSCAR and *lm*-decomposed PROCAR + phase factors, choose single projector for interval EMIN,EMAX |

### For LORBIT < 10

The projection is onto spherical harmonics at each ionic site within a sphere defined by RWIGS. The radius must be specified for each atomic species, and there is some uncertainty introduced depending on the size of the sphere.

### For LORBIT >= 10

The projection uses the projector functions that are provided by the PAW method. This is, of course, still a qualitative approach because also, for the PAW projectors, the radius was somehow defined, and it is not guaranteed to be the best choice for that particular system as it depends on the chemical composition and crystal or molecular structure.

### Phase factors

For LORBIT>=12:
The **phase factors** written by VASP can usually only be used as a qualitative measure of the projection of the orbitals into the atomic sphere. The main issue is that most VASP POTCAR files have two or three projectors per $l$-quantum number, and projecting an orbital onto two projectors will yield two complex numbers. VASP combines these two numbers into a single number. The precise algorithms differ in different versions of VASP, and we recommend that you inspect the source code for more details. From vasp.6 onward, an improved scheme has been implemented and can be selected using LORBIT=14. In this case, VASP first selects a single projector for each $l$-quantum number by linearly combining all projectors with the same $l$-quantum number. This is done in such a way that the new projector is optimally chosen to represent the calculated orbitals in the energy interval specified by EMAX and EMIN. In the second step, VASP projects onto these optimized projectors, yielding a single complex number for each orbital, site and $l$-quantum number, which is written to the PROCAR file. For details we also refer to .
LORBIT=12 should no longer be used except for qualitative calculations. LORBIT=13 chooses the projectors also automatically, but allows for different optimal linear combinations for each orbital.
Note that this is generally not desirable, since the resultant projection is not compatible with the required properties of a projection operator (a projection operator needs to use energy and orbital independent projectors).
Hence, do not use LORBIT=13 for anything but a qualitative analysis.

LORBIT=13 and LORBIT=14 are only supported by version >=5.4.4.

## On-site partial charge densities and magnetization

The partial charge densities can be found in the OUTCAR

```
total charge     

# of ion       s       p       d       tot
------------------------------------------
    1        1.514   0.000   0.000   1.514
    2        0.123   0.345   0.000   0.468
```

Here, the first column corresponds to the ion index $\alpha$, the s, p, d,... columns correspond to the partial charges for $l=0,1,2,\cdots$ defined as

$\rho\_{\alpha l}=\frac{1}{N\_{\bf k}} \sum\_{n{\bf k}}f\_{n{\bf k}} \sum\_{m=-l}^{l}|\langle Y\_{lm}^{\alpha}|\phi\_{n\mathbf{k}}\rangle|^2$

The $\langle Y\_{lm}^{\alpha}|\phi\_{n\mathbf{k}}\rangle$ are obtained from the projection of the (occupied) KS orbitals $|\phi\_{n{\bf k}}\rangle$ onto spherical harmonics that are non zero within spheres of a radius RWIGS centered at ion $\alpha$ and the last column is the sum $\sum\_{l}\rho\_{\alpha l}$.

Note that depending on the system, an "f" column is written as well.

* In case of spin-polarized magnetic calculations (ISPIN=2), the partial magnetization densities are written to the OUTCAR

```
magnetization (x)
 
# of ion       s       p       d       tot
------------------------------------------
    1        0.000   0.000   0.000   0.000
    2        0.000   0.245   0.000   0.245
```

Here, the magnetization density is calculated from the difference in the up and down spin channel $m^{\alpha l}\_z = \rho\_{\alpha l}^{\uparrow}-\rho\_{\alpha l}^{\downarrow}$
Although the direction of the magnetization densities is meaningless in a spin-polarized calculation (no spin-orbit coupling, see LSORBIT), here the projection axis is the z-axis. This is consistent withe the behavior upon restarting a noncollinear calculation from a spin-polarized one with default SAXIS.

* In case of noncollinear calculations (LNONCOLLINEAR=.TRUE.), the lines after "total charge" correspond to the diagonal average

$\frac{\rho\_{\alpha l}^{\uparrow\uparrow} - \rho\_{\alpha l}^{\downarrow \downarrow}}{2}$
of the density tensor

:   :   $$\rho\_{\alpha l} = \left(\begin{matrix}
        \rho\_{\alpha l}^{\uparrow \uparrow } & \rho\_{\alpha l}^{\uparrow \downarrow} \\
        \rho\_{\alpha l}^{\downarrow \uparrow} & \rho\_{\alpha l}^{\downarrow \downarrow} \\
        \end{matrix}\right),$$

which is determined from the projected components

:   :   $$\rho^{\mu\nu}\_{\alpha l} = \frac{1}{N\_{\bf k}} \sum\_{n{\bf k}}f\_{n{\bf k}} \sum\_{m=-l}^{l}
        \langle \chi\_{n {\bf k}}^\mu | Y\_{lm}^\alpha \rangle
        \langle Y\_{lm}^\alpha | \chi\_{n {\bf k}}^\nu \rangle$$

of the spinor $|\Psi\_{n{\bf k}}\rangle=\left(\begin{matrix}\chi\_{n{\bf k}}^\uparrow \\\chi\_{n{\bf k}}^\downarrow \end{matrix}\right)$

Similarly, the lines after "magnetization (x)", "magnetization (y)", and "magnetization (z)"correspond to the partial magnetization density

:   :   $$m\_{\alpha l}^j = \frac{1}{2}\sum\_{\mu,\nu=1}^2 \sigma^j\_{\mu \nu} \rho\_{\alpha l}^{\mu \nu}.$$

projected onto Pauli matrices $\{\sigma\_1$, $\sigma\_2$, $\mathbf{\sigma}\_3\}$. By default, this corresponds to Cartesian directions $\sigma\_1=\hat x$, $\sigma\_2 =\hat y$, $\sigma\_3 = \hat z$, but the orientation can be changed using SAXIS.

## References

## Related tags and articles

RWIGS,
PROCAR,
PROOUT,
DOSCAR

Examples that use this tag
