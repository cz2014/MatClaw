# Many-body dispersion energy with fractionally ionic model for polarizability

Categories: Exchange-correlation functionals, Van der Waals functionals, Theory, Howto

A variant of Many-body dispersion energy method based on fractionally ionic model for polarizability of Gould, hereafter dubbed MBD@rsSCS/FI, has been introduced in Ref.
Just like in the original MBD@rsSCS, dispersion energy in MBD@rsSCS/FI is computed using

:   $E\_{\mathrm{disp}} = -\int\_{\mathrm{FBZ}}\frac{d{\mathbf{k}}}{v\_{\mathrm{FBZ}}} \int\_0^{\infty} {\frac{d\omega}{2\pi}} \, {\mathrm{Tr}}\left \{ \mathrm{ln} \left ({\mathbf{1}}-{\mathbf{A}}^{(0)}\_{LR}(\omega) {\mathbf{T}}\_{LR}({\mathbf{k}}) \right ) \right \}$.

However, the two methods differ in the model used to approximate the atomic polarizabilities ($\alpha\_p^{\text{AIM}}$) needed to define tensor$\mathbf{A}^{(0)}(\omega)({\mathbf{k}})$. The MBD@rsSCS makes use of the pre-computed static polarizabilities of neutral atoms ($\alpha\_p^{\text{atom}}$)

:   $\alpha\_p^{\text{AIM}} = \alpha\_p^{\text{atom}}
    \frac{V^{\text{eff}}\_p}{V^{\text{atom}}\_p}$,

whereby the volume ratios between interacting and non-interacting atoms ($\frac{V^{\text{eff}}\_p}{V^{\text{atom}}\_p}$) is obtained using conventional Hirshfeld partitioning. Although the MBD@rsSCS/FI employs a similar scaling relation:

:   $\alpha\_p^{\text{AIM}}(\omega) = \alpha\_p^{\text{FI}}(\omega)
    \frac{V^{\text{eff}}\_p}{V^{\text{FI}}\_p}$,

it relies on Gould's model of frequency-dependent polarizabilities ($\alpha\_p^{\text{FI}}(\omega)$) and charge densities of non-interacting fractional ions combined with iterative Hirshfeld partitioning. Obviously, the MBD@rsSCS and the MBD@rsSCS/FI are equivalent for non-polar systems, such as graphite, but typically yield distinctly different results for polar and ionic materials.

## Usage

The MBD@rsSCS/FI method is invoked by setting IVDW=263. Optionally, the following parameters can be user-defined (the given values are the default ones):

* VDW\_SR=0.83 : scaling parameter $\beta$
* LVDWEXPANSION=.FALSE. : writes the two- to six- body contributions to the MBD dispersion energy in the OUTCAR (LVDWEXPANSION=*.TRUE.*)
* LSCSGRAD=.TRUE. : compute gradients (or not)
* VDW\_R0 : radii for atomic reference (see also Tkatchenko-Scheffler method)
* ITIM=1: if set to +1, apply eigenvalue remapping to avoid unphysical cases where the eigenvalues of the matrix $\left(1-\mathbf{A}^{(0)}\_{LR}(\omega) {\mathbf{T}}\_{LR}({\mathbf{k}})\right)$ are non-positive, see reference for details

> **Mind:**
>
> * This method requires the use of POTCAR files from the PAW dataset version 52 or later.
> * The parametrization of reference data is available only for elements of the first six rows of the periodic table except of the lanthanides.
> * The charge-density dependence of gradients is neglected.
> * This method is incompatible with the setting ADDGRID=*.TRUE.*.
> * It is essential that a sufficiently dense FFT grid (controlled via NGXF, NGYF and NGZF ) is used. We strongly recommend to use PREC=*Accurate* for this type of calculations (in any case, avoid using PREC=*Low*}).
> * The method has sometimes numerical problems if highly polarizable atoms are located at short distances. In such a case the calculation terminates with an error message *Error(vdw\\_tsscs\\_range\\_separated\\_k): d\\_lr(pp)<=0*. Note that this problem is not caused by a bug, but rather it is due to a limitation of the underlying physical model.
> * Analytical gradients of the energy are implemented (fore details see reference ) and hence the atomic and lattice relaxations can be performed.
> * Due to the long-range nature of dispersion interactions, the convergence of energy with respect to the number of k-points should be carefully examined.
> * A default value for the free-parameter of this method is available only for the PBE (VDW\_SR=0.83) and SCAN (VDW\_SR=1.12) functionals. If any other functional is used, the value of VDW\_SR must be specified in the INCAR file.

## Related tags and articles

VDW\_ALPHA,
VDW\_C6,
VDW\_R0,
VDW\_SR,
LVDWEXPANSION,
LSCSGRAD,
IVDW,
Tkatchenko-Scheffler method,
Self-consistent screening in Tkatchenko-Scheffler method,
Tkatchenko-Scheffler method with iterative Hirshfeld partitioning,
Many-body dispersion energy

## References

---
