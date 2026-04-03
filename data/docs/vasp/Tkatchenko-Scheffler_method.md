# Tkatchenko-Scheffler method

Categories: Exchange-correlation functionals, Van der Waals functionals, Theory, Howto

The expression for the dispersion energy within the method of Tkatchenko and Scheffler is formally identical to that of the DFT-D2 method. The important difference is, however, that the dispersion coefficients and damping function are charge-density dependent. The Tkatchenko-Scheffler method is therefore able to take into account variations in vdW contributions of atoms due to their local chemical environment. In this method the polarizability, dispersion coefficients, and atomic radii of an atom in a molecule or a solid are computed from their free-atomic values using the following relations:

:   $$\alpha\_{i} = \nu\_{i}\, \alpha\_{i}^{free},$$

:   $$C\_{6ii} = \nu\_{i}^{2}\,C\_{6ii}^{free},$$

:   $$R\_{0i} = \left(\frac{\alpha\_{i}}{\alpha\_{i}^{free}} \right)^{\frac{1}{3}} R\_{0i}^{free}.$$

The free-atomic quantities $\alpha\_{i}^{free},C\_{6ii}^{free}$ and $R\_{0i}^{free}$ are tabulated for all elements from the first six rows of the periodic table except for lanthanides. If a Tkatchenko-Scheffler calculation is performed for the system containing an unsupported element, the user has to define the corresponding values using the tags VDW\_ALPHA, VDW\_C6 and VDW\_R0 (see below). The effective atomic volumes $\nu\_{i}$ are determined using the Hirshfeld partitioning of the all-electron density:

:   $$\nu\_{i} = \frac{\int r^3 \,w\_i({\mathbf{r}}) n({\mathbf{r}})\,d^3{\mathbf{r}}}{\int r^3\, n\_{i}^{free}({\mathbf{r}})\,d^3{\mathbf{r}}}$$

where $n({\mathbf{r}})$ is the total electron density and $n\_{i}^{free}({\mathbf{r}})$ is the spherically averaged electron density of the neutral free atomic species $i$. The Hirshfeld weight $w\_i({\mathbf{r}})$ is defined by free atomic densities as follows:

:   $$w\_i({\mathbf{r}}) = \frac{n\_{i}^{free}({\mathbf{r}})}{\sum\_{j=1}^{N\_{at}} n\_{j}^{free}({\mathbf{r}})}.$$

The combination rule to define the strength of the dipole-dipole dispersion interaction between unlike species is:

:   $$C\_{6ij} = \frac{2C\_{6ii}\,C\_{6jj}}{[\frac{\alpha\_{j}} {\alpha\_{i}}C\_{6ii}+\frac{\alpha\_{i}}{\alpha\_{j}}C\_{6jj}]}.$$

The parameter $R\_{0ij}$ used in the damping function of the DFT-D2 method is obtained from the atom-in-molecule vdW radii as follows:

:   $$R\_{0ij} = R\_{0i} + R\_{0j}.$$

The performance of the Tkatchenko-Scheffler method in optimization of various crystalline systems has been examined in reference .

## Usage

The Tkatchenko-Scheffler method is invoked by setting IVDW=2|20. The following parameters can be optionally defined in INCAR (the given values are the default ones):

* LVDWSCS=.FALSE. : activates the self-consistent screening in Tkatchenko-Scheffler method
* VDW\_RADIUS=50.0 : cutoff radius (in Å) for pair interactions
* VDW\_S6=1.00 : global scaling factor $s\_6$
* VDW\_SR=0.94 : scaling factor $s\_R$
* VDW\_D=20.0 : damping parameter $d$
* VDW\_ALPHA=[real array] : free-atomic polarizabilities (atomic units) for each species defined in the POSCAR file
* VDW\_C6AU=[real array] : free-atomic $C\_6$ parameters (atomic units) for each species defined in the POSCAR file
* VDW\_C6=[real array] : free-atomic $C\_6$ parameters ($\mathrm{Jnm}^{6}\mathrm{mol}^{-1}$) for each species defined in the POSCAR file (this parameter overrides VDW\_C6AU)
* VDW\_R0AU=[real array] : free-atomic $R\_0$ parameters (atomic units) for each species defined in the POSCAR file
* VDW\_R0=[real array] : $R\_0$ parameters (in Å) for each species defined in the POSCAR file (this parameter overrides VDW\_R0AU)
* LVDW\_EWALD=.FALSE. : the lattice summation in $E\_{\mathrm{disp}}$ expression is computed by means of Ewald's summation (*.TRUE.* ) or via a real space summation over all atomic pairs within cutoff radius VDW\_RADIUS (*.FALSE.*). (available in VASP.5.3.4 and later)
* LTSSURF=.FALSE.: if set to .TRUE., the standard parametrization of the Tkatchenko-Scheffler method is replaced by the one designed to enable reliable modeling of structure and stability for a broad class of organic molecules adsorbed on metal surfaces is activated

> **Mind:**
>
> * This method requires the use of POTCAR files from the PAW dataset version 52 or later.
> * The input reference data for non-interacting atoms is available only for elements of the first six rows of the periodic table except for lanthanides. If the system contains other elements, the user must provide the free-atomic parameters for all atoms in the system via VDW\_ALPHA, VDW\_C6, VDW\_R0 defined in the INCAR file.
> * The charge-density dependence of gradients is neglected.
> * The DFT-TS method is incompatible with the setting ADDGRID=*.TRUE.*.
> * It is essential that a sufficiently dense FFT grid (controlled via NGXF, NGYF and NGZF) is used in the DFT-TS calculation - we strongly recommend to use PREC=*Accurate* for this type of calculations (in any case, avoid using PREC=*Low*).
> * Defaults for the parameters controlling the damping function (VDW\_S6, VDW\_SR, VDW\_D) are available for the PBE, PBE0, HSE03, HSE06, TPSS, and M06L functionals. If any other functional is used, the value of VDW\_SR must be specified in the INCAR file.
> * Ewald's summation in the calculation of $E\_{disp}$ (controlled via LVDW\_EWALD) implemented according to reference is available as of VASP.5.3.4.
> * Parameters VDW\_C6AU and VDW\_R0AU are available as of VASP.5.3.4.
> * Hirshfeld charges for all configurations generated in a calculation are written out in the OUTCAR file. The corresponding table is introduced by the expression *Hirshfeld charges:*.

## Related tags and articles

VDW\_RADIUS,
VDW\_S6,
VDW\_SR,
VDW\_D,
VDW\_ALPHA,
VDW\_C6AU,
VDW\_C6,
VDW\_R0AU,
VDW\_R0,
LVDW\_EWALD,
IVDW,
Tkatchenko-Scheffler method with iterative Hirshfeld partitioning,
Self-consistent screening in Tkatchenko-Scheffler method,
Many-body dispersion energy,
Many-body dispersion energy with fractionally ionic model for polarizability

## References

---
