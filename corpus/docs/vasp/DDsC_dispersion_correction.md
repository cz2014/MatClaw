# DDsC dispersion correction

Categories: Exchange-correlation functionals, Van der Waals functionals, Theory, Howto

The expression for the density-dependent energy correction dDsC is very similar to that of the DFT-D2 method (see the equation for $E\_{disp}$ for the DFT-D2 method). The important difference is, however, that the dispersion coefficients and damping function are charge-density dependent. The dDsC method is therefore able to take into account variations in the vdW contributions of atoms due to their local chemical environment. In this method, polarizability, dispersion coefficients, charge and charge-overlap of an atom in a molecule or solid are computed in the basis of a simplified exchange-hole dipole moment formalism pioneered by Becke and Johnson.

The dDsC dispersion energy is expressed as follows:

:   $${{E}\_{\mathrm{disp}}}=-\sum\limits\_{i=2}^{{{N}\_\mathrm{at}}}{\sum\limits\_{j=1}^{i-1}\sum\limits\_{n=3}^{n=5}{{{f}\_{2n}}(b{{R}\_{ij}})\frac{C\_{2n}^{ij}}{R\_{ij}^{2n}}}}
    {{E}\_{\mathrm{disp}}}=-\sum\limits\_{i=2}^{{{N}\_{\mathrm{at}}}}{\sum\limits\_{j=1}^{i-1}
    {{{f}\_{6}}(b{{R}\_{ij}})\frac{C\_{6,ij}}{R\_{ij}^{6}}}}$$

where $N\_{\mathrm{at}}$ is the number of atoms in the system and $b$ is the Tang and Toennies (TT) damping factor. The damping function $f\_{6}(bR\_{ij})$ is defined as follows:

:   $$f\_{6}(x)=1-\exp(-x)\sum^{6}\_{k=0}\frac{x^k}{k!}$$

and its role is to attenuate the correction at short internuclear distances. A key component of the dDsC method is the damping factor $b$:

:   $$b(x)=\frac{2 b\_{ij,\mathrm{asym}}}{{{e}^{{{a}\_{0}}\cdot x}}+1}$$

where the fitted parameter $a\_{0}$ controls the short-range behaviour and $x$ is the damping argument for the TT-damping factor associated with two separated atoms ($b\_{ij,\mathrm{asym}}$).
The term $b\_{ij,\mathrm{asym}}$ is computed according to the combination rule:

:   $$b\_{ij,\mathrm{asym}}=2\frac{b\_{ii,\mathrm{asym}}\cdot b\_{jj,\mathrm{asym}}}{b\_{ii,\mathrm{asym}} + b\_{jj,\mathrm{asym}}}$$

with $b\_{ii,\mathrm{asym}}$ being estimated from effective atomic polarizabilities:

:   $${b}\_{ii,\mathrm{asym}}={b}\_{0}\cdot \sqrt[3]{\frac{1}{\alpha\_{i}}}$$

The effective atom-in-molecule polarizabilities $\alpha\_{i}$ are computed from the tabulated free-atomic polarizabilities (available for the elements of the first six rows of the periodic table except of lanthanides) in the same way as in the Tkatchenko-Scheffler method and Tkatchenko-Scheffler method with iterative Hirshfeld partitioning, but the Hirshfeld-dominant instead of the conventional Hirshfeld partitioning is used.
The last element of the correction is the damping argument $x$:

:   $$x=\left( 2{{q}\_{ij}}+\frac{|({{Z}\_{i}}-N\_{i}^{D})\cdot ({{Z}\_{j}}-N\_{j}^{D})|}{{{r}\_{ij}}} \right)\frac{N\_{i}^{D}+N\_{j}^{D}}{N\_{i}^{D}\cdot N\_{j}^{D}}$$

where $Z\_i$ and $N\_i^D$ are the nuclear charge and Hirshfeld dominant population of atom $i$, respectively.
The term $2q\_{ij} = q\_{ij} + q\_{ji}$ is a covalent bond index based on the overlap of conventional Hirshfeld populations $q\_{ij}=\int w\_i({\mathbf{r}})w\_j({\mathbf{r}})n({\mathbf{r}})d{\mathbf{r}}$, and the fractional term in the parentheses is a distance-dependent ionic bond index.

The Performance of PBE-dDsC in the description of the adsorption of hydrocarbons on Pt(111) has been examined in reference .

## Usage

The dDsC correction is invoked by setting IVDW=4. The default values for damping function parameters are available for the functionals PBE (GGA=*PE*}) and revPBE (GGA=*RE*). If another functional is used, the user has to define these parameters via corresponding tags in the INCAR file (parameters for common DFT functionals can be found in reference . The following parameters can be optionally defined in the INCAR file (the given values are the default ones):

* VDW\_RADIUS=50.0 : cutoff radius (in $\AA$) for pair interactions
* VDW\_S6=13.96 : scaling factor ${a}\_{0}$
* VDW\_SR=1.32 : scaling factor ${b}\_{0}$

> **Mind:**
>
> * The dDsC method has been implemented into VASP by Stephan N. Steinmann.
> * This method requires the use of POTCAR files from the PAW dataset version 52 or later.
> * The input reference polarizabilities for non-interacting atoms are available only for elements of the first six rows of periodic table except of the lanthanides.
> * It is essential that a sufficiently dense FFT grid (controlled via NGXF, NGYF and NGZF) is used when using dDsC, especially for accurate gradients. We strongly recommend to use PREC=*Accurate* for this type of calculations (in any case, avoid using PREC=*Low*).
> * The charge-density dependence of gradients is neglected. This approximation has been thoroughly investigated and validated in reference .

## Related tags and articles

VDW\_RADIUS,
VDW\_S6,
VDW\_SR,
IVDW

## References

---
