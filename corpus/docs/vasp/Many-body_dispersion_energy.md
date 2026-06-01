# Many-body dispersion energy

Categories: Exchange-correlation functionals, Van der Waals functionals, Theory, Howto

The many-body dispersion energy method (MBD@rsSCS) of Tkatchenko et al., invoked by setting IVDW=202, is based on the random-phase expression for the correlation energy

:   $$E\_c = \int\_{0}^{\infty} \frac{d\omega}{2\pi} \mathrm{Tr}\left\{\mathrm{ln} (1-v\chi\_0(i\omega))+v\chi\_0(i\omega) \right\}$$

whereby the response function $\chi\_0$ is approximated by a sum of atomic contributions represented by quantum harmonic oscillators. The expression for the dispersion energy used in the VASP k-space implementation of the MBD@rsSCS method (see reference for details) is as follows:

:   $$E\_{\mathrm{disp}} = -\int\_{\mathrm{FBZ}}\frac{d{\mathbf{k}}}{v\_{\mathrm{FBZ}}} \int\_0^{\infty} {\frac{d\omega}{2\pi}} \, {\mathrm{Tr}}\left \{ \mathrm{ln} \left ({\mathbf{1}}-{\mathbf{A}}^{(0)}\_{LR}(\omega) {\mathbf{T}}\_{LR}({\mathbf{k}}) \right ) \right \}$$

where ${\mathbf{A}}\_{LR}$ is the frequency-dependent polarizability matrix and $\mathbf{T}\_{LR}$ is the long-range interaction tensor, which describes the interaction of the screened polarizabilities
embedded in the system in a given geometrical arrangement. The components of $\mathbf{A}\_{LR}$ are obtained using an atoms-in-molecule approach as employed in the pairwise Tkatchenko-Scheffler method (see
references for details).

Details of the implementation of the MBD@rsSCS method in VASP are presented in reference .

## Usage

The input reference data for non-interacting atoms can be optionally defined via the parameters VDW\_ALPHA, VDW\_C6, and VDW\_R0
(described by the Tkatchenko-Scheffler method). This method has one free parameter ($\beta$) that must be adjusted for each exchange-correlation functional. The default value of $\beta$=0.83 corresponds to the PBE functional (GGA=PE). If another functional is used, the value of $\beta$ must be specified via VDW\_SR in the INCAR file.

The following optional parameters can be user-defined (the given values are the default ones):

* VDW\_SR=0.83 : scaling parameter $\beta$
* LVDWEXPANSION=.FALSE. : writes the two- to six-body contributions to the MBD dispersion energy in the OUTCAR (LVDWEXPANSION=*.TRUE.*)
* LSCSGRAD=.TRUE. : compute gradients (or not)
* VDW\_ALPHA, VDW\_C6, VDW\_R0 : atomic reference (see also Tkatchenko-Scheffler method)
* ITIM=-1: if set to +1, apply eigenvalue remapping to avoid unphysical cases where the eigenvalues of the matrix

$\left(1-\mathbf{A}^{(0)}\_{LR}(\omega) {\mathbf{T}}\_{LR}({\mathbf{k}})\right)$are non-positive, see reference for details

> **Mind:**
>
> * This method requires the use of POTCAR files from the PAW dataset version 52 or later.
> * The input reference data for non-interacting atoms are available only for elements of the first six rows of the periodic table except of the lanthanides. If the system contains other elements, the user has to provide the free-atomic parameters for all atoms in the system via VDW\_ALPHA, VDW\_C6 and VDW\_R0 (described by the Tkatchenko-Scheffler method) defined in the INCAR file.
> * The charge-density dependence of gradients is neglected.
> * This method is incompatible with the setting ADDGRID=*.TRUE.*.
> * It is essential that a sufficiently dense FFT grid (controlled via NGXF, NGYF and NGZF ) is used in the Tkatchenko-Scheffler method calculation. We strongly recommend to use PREC=*Accurate* for this type of calculations (in any case, avoid using PREC=*Low*).
> * The method sometimes has numerical problems if highly polarizable atoms are located at short distances. In such a case the calculation terminates with an error message *Error(vdw\\_tsscs\\_range\\_separated\\_k): d\\_lr(pp)<=0*. Note that this problem is not caused by a bug, but rather it is due to a limitation of the underlying physical model.
> * Analytical gradients of the energy are implemented (fore details see reference ) and hence the atomic and lattice relaxations can be performed.
> * Due to the long-range nature of dispersion interactions, the convergence of energy with respect to the number of k-points should be carefully examined.
> * A default value for the free-parameter of this method is available only for the PBE (VDW\_SR=0.83), PBE0 (VDW\_SR=0.85), HSE06 (VDW\_SR=0.85), B3LYP (VDW\_SR=0.64), and SCAN (VDW\_SR=1.12) functionals. If any other functional is used, the value of VDW\_SR must be specified in the INCAR file.

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
Many-body dispersion energy with fractionally ionic model for polarizability

## References

---
