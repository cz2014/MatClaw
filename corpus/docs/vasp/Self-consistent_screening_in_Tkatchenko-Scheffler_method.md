# Self-consistent screening in Tkatchenko-Scheffler method

Categories: Exchange-correlation functionals, Van der Waals functionals, Theory

A computationally efficient way to account for electrodynamic response effects, in particular the interaction of atoms with the dynamic electric field due to the surrounding polarizable atoms, was proposed by Tkatchenko et al. In this method, termed TS+SCS, the frequency-dependent screened polarizabilities $\alpha^{SCS}(\omega)$ are obtained by solving the self-consistent screening equation:

:   $$\alpha\_{i}^{SCS}(\omega) = \alpha\_{i}(\omega) - \alpha\_{i}(\omega)
    \sum\_{i \neq j} \tau\_{ij} \alpha\_{j}^{SCS}(\omega)$$

where $\tau\_{ij}$ is the dipole-dipole interaction tensor and $\alpha\_{i}(\omega)$ is the effective frequency-dependent polarizability, approximated by

:   $$\alpha\_{i}(\omega) = \frac{\alpha\_{i}}{1+\left (
    \omega / \omega\_i \right )^2}$$

with the characteristic mean excitation frequency $\omega\_i = \frac{4}{3} \frac{C\_{6ii}}{(\alpha\_{i})^2}$. The dispersion coefficients are computed from the Casimir-Polder integral:

:   $$C\_{6ii} = \frac{3}{\pi} \int\_0^{\infty} \alpha\_{i}^{SCS}(\omega)
    \alpha\_{i}^{SCS}(\omega) \,d\omega.$$

The van der Waals radii of atoms are obtained by rescaling the radii:

:   $$R\_{0i}^{SCS} = \left ( \frac{\alpha\_{i}^{SCS}}{\alpha\_{i}} \right )^{1/3} R\_{0i}.$$

The dispersion energy is computed using the same equation as in the original Tkatchenko-Scheffler method but with corrected parameters $C\_{6ii}^{SCS}$, $\alpha\_{i}^{SCS}$, and $R\_{0i}^{SCS}$.

Details of the implementation of the TS+SCS method in VASP and the performance tests made on various crystalline systems are presented in reference .

## Usage

The TS+SCS method is invoked by setting IVDW=2|20 and LVDWSCS=*.TRUE.*. In addition to parameters controlling the Tkatchenko-Scheffler method, the following optional parameters can set by the user:

* VDW\_SR=0.97 scaling factor $s\_{R}$
* SCSRAD=120 cutoff radius (in $\AA$) used in the calculation of $\tau\_{ij}$
* LSCSGRAD=.TRUE. decides whether to compute SCS contribution to gradients (LSCSGRAD=*.TRUE.*) or not
* LSCALER0=.TRUE. decides whether to use the equation above for $R\_{0i}^{SCS}$ to re-scale the parameter $R\_{0}$ (LSCALER0=*.TRUE.*) or not

> **Mind:**
>
> * This method requires the use of POTCAR files from the PAW dataset version 52 or later.
> * This method is incompatible with the setting ADDGRID=*.TRUE.*.
> * This type of calculation may be time-consuming for large systems. Note that the SCS contribution to gradients and stress tensor is only modest (but non-negligible) in many cases. In the initial stages of relaxation of large systems, or if only energy is of interest, the calculation can be accelerated by setting LSCSGRAD=*.FALSE.*.
> * The default value for the parameter VDW\_SR (which is, in general, different from that used in the unscreened Tkatchenko-Scheffler method method) is available only for the PBE functional. If a functional other than PBE is used, the value for VDW\_SR must be specified in the INCAR file.

## Related tags and articles

LVDWSCS,
VDW\_SR,
SCSRAD,
LSCSGRAD,
LSCALER0,
IVDW,
Tkatchenko-Scheffler method,
Tkatchenko-Scheffler method with iterative Hirshfeld partitioning,
Many-body dispersion energy,
Many-body dispersion energy with fractionally ionic model for polarizability

## References

---
