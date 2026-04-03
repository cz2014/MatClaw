# DFT-ulg

Categories: Exchange-correlation functionals, Van der Waals functionals, Theory, Howto

In the DFT-ulg method of Kim et al., the correction term takes the form:

:   $$E\_{\mathrm{disp}} = -\frac{1}{2} s\_{lg}\sum\_{i=1}^{N\_{at}} \sum\_{j=1}^{N\_{at}} \sum\_{\mathbf{L}} {}^{\prime} \frac{C\_{6ij}}{r\_{ij,L}^{6}+b\_{lg}(R\_{0}^{ij})^{6}}$$

where the first two summations are over all $N\_{at}$ atoms in the unit cell and the third summation is over all translations of the unit cell ${\mathbf{L}}=(l\_1,l\_2,l\_3)$ where the prime indicates that $i\not=j$ for ${\mathbf{L}}=0$. $C\_{6ij}$ denotes the dispersion coefficient for the atom pair $ij$, ${r}\_{ij,\mathbf{L}}$ is the distance between atom $i$ located in the reference cell $\mathbf{L}=0$ and atom $j$ in the cell $L$.

## Usage

The DFT-ulg method can be activated by setting IVDW=*3*. The parameters in the DFT-ulg method (see Ref. for details) that can be modified are listed below.

* VDW\_RADIUS=50.0 : cutoff radius (in $\AA$) for pair interactions
* VDW\_S6=0.7012 : global scaling parameter $s\_{lg}$
* VDW\_D=0.6966 : universal correction parameter $b\_{lg}$
* VDW\_C6=[real array] : $C\_6$ parameters ($\mathrm{Jnm}^{6}\mathrm{mol}^{-1}$) for each species defined in the POSCAR file
* VDW\_R0=[real array] : $R\_0$ parameters ($\AA$) for each species defined in the POSCAR file
* LVDW\_EWALD=*.FALSE.* : the lattice summation in $E\_{\mathrm{disp}}$ expression is computed by means of Ewald's summation (*.TRUE.* ) or via a real space summation over all atomic pairs within cutoff radius VDW\_RADIUS (*.FALSE.*). (available in VASP.5.3.5 and later)

> **Mind:** The default value of the parameter $s\_{lg}$ (0.7012) was determined in conjunction with the PBE GGA functional. Therefore, it is not recommended to use the DFT-ulg dispersion correction with a GGA functional other than PBE, unless $s\_{lg}$ is reoptimized.

## Related tags and articles

VDW\_RADIUS,
VDW\_S6,
VDW\_D,
VDW\_C6,
VDW\_R0,
LVDW\_EWALD,
IVDW,
DFT-D2

## References

---
