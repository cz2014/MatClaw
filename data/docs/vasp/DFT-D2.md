# DFT-D2

Categories: Exchange-correlation functionals, Van der Waals functionals, Theory, Howto

In the DFT-D2 method of Grimme the correction term takes the form:

:   $$E\_{\mathrm{disp}} = -\frac{1}{2} \sum\_{i=1}^{N\_{at}} \sum\_{j=1}^{N\_{at}} \sum\_{\mathbf{L}} {}^{\prime} \frac{C\_{6ij}}{r\_{ij,L}^{6}} f\_{d,6}({r}\_{ij,\mathbf{L}})$$

where the first two summations are over all $N\_{at}$ atoms in the unit cell and the third summation is over all translations of the unit cell ${\mathbf{L}}=(l\_1,l\_2,l\_3)$ where the prime indicates that $i\not=j$ for ${\mathbf{L}}=0$. $C\_{6ij}$ denotes the dispersion coefficient for the atom pair $ij$, ${r}\_{ij,\mathbf{L}}$ is the distance between atom $i$ located in the reference cell $\mathbf{L}=0$ and atom $j$ in the cell $L$ and the term $f(r\_{ij})$ is a damping function whose role is to scale the force field such as to minimize the contributions from interactions within typical bonding distances. In practice, the terms in the equation for $E\_{\mathrm{disp}}$ corresponding to interactions over distances longer than a certain suitably chosen cutoff radius (VDW\_RADIUS, see below) contribute only negligibly to $E\_{\mathrm{disp}}$ and can be ignored. Parameters $C\_{6ij}$ and $R\_{0ij}$ are computed using the following combination rules:

:   $$C\_{6ij} = \sqrt{C\_{6ii} C\_{6jj}}$$

and

:   $$R\_{0ij} = R\_{0i}+ R\_{0j}.$$

The values for $C\_{6ii}$ and $R\_{0i}$ are tabulated for each element and are insensitive to the particular chemical situation (for instance, $C\_6$ for carbon in methane takes exactly the same value as that for C in benzene within this approximation). In the DFT-D2 method, a Fermi-type damping function is used:

:   $$f\_{d,6}(r\_{ij}) = \frac{s\_6}{1+e^{-d(r\_{ij}/(s\_R\,R\_{0ij})-1)}}$$

whereby the global scaling parameter $s\_6$ has been optimized for several different DFT functionals such as PBE ($s\_6=0.75$), BLYP ($s\_6=1.2$) or B3LYP ($s\_6=1.05$). The parameter $s\_R$ is usually fixed at 1.00.

The performance of PBE-D2 method in optimization of various crystalline systems has been tested systematically in reference .

> **Important:** It is recommended to use the more advanced and more accurate method DFT-D3.

## Usage

The DFT-D2 method is activated by setting IVDW=1 or 10 (or the obsolete LVDW=*.TRUE.*). Optionally, the damping function and the vdW parameters can be controlled using the following flags (the given values are the default ones):

* VDW\_RADIUS=50.0 : cutoff radius (in $\AA$) for pair interactions
* VDW\_S6=0.75 : global scaling factor $s\_6$ (available in VASP.5.3.4 and later)
* VDW\_SR=1.00 : scaling factor $s\_R$ (available in VASP.5.3.4 and later)
* VDW\_SCALING=0.75 : the same as VDW\_S6 (obsolete as of VASP.5.3.4)
* VDW\_D=20.0 : damping parameter $d$
* VDW\_C6=[real array] : $C\_6$ parameters ($\mathrm{Jnm}^{6}\mathrm{mol}^{-1}$) for each species defined in the POSCAR file
* VDW\_R0=[real array] : $R\_0$ parameters ($\AA$) for each species defined in the POSCAR file
* LVDW\_EWALD=*.FALSE.* : the lattice summation in $E\_{\mathrm{disp}}$ expression is computed by means of Ewald's summation (*.TRUE.* ) or via a real space summation over all atomic pairs within cutoff radius VDW\_RADIUS (*.FALSE.*). (available in VASP.5.3.4 and later)

> **Mind:**
>
> * The defaults for VDW\_C6 and VDW\_R0 are defined only for elements in the first five rows of the periodic table (i.e. H-Xe). If the system contains other elements the user has to define these parameters in INCAR.
> * The defaults for parameters controlling the damping function (VDW\_S6, VDW\_SR, VDW\_D) are available for the PBE (GGA=PE), BP, revPBE, PBE0, TPSS, and B3LYP functionals. If any other functional is used in a DFT-D2 calculation, the value of VDW\_S6 (or VDW\_SCALING in versions before VASP.5.3.4) has to be defined in INCAR.
> * As of VASP.5.3.4, the default value for VDW\_RADIUS has been increased from 30 to 50 $\AA$.
> * Ewald's summation in the calculation of $E\_{\mathrm{disp}}$ calculation (controlled via LVDW\_EWALD) is implemented according to reference and is available as of VASP.5.3.4.

## Related tags and articles

VDW\_RADIUS,
VDW\_S6,
VDW\_SR,
VDW\_SCALING,
VDW\_D,
VDW\_C6,
VDW\_R0,
LVDW\_EWALD,
IVDW,
DFT-ulg,
DFT-D3,
DFT-D4

## References

---
