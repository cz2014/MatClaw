# DFT-D3

Categories: Exchange-correlation functionals, Van der Waals functionals, Theory, Howto

In the DFT-D3 method of Grimme et al., the following expression for the vdW dispersion energy-correction term is used:

:   $$E\_{\mathrm{disp}} = -\frac{1}{2} \sum\_{i=1}^{N\_{at}} \sum\_{j=1}^{N\_{at}} \sum\_{\mathbf{L}}{}^\prime \left ( f\_{d,6}(r\_{ij,L})\,\frac{C\_{6ij}}{r\_{ij,{L}}^6} +f\_{d,8}(r\_{ij,L})\,\frac{C\_{8ij}}{r\_{ij,L}^8} \right ).$$

Unlike in the method DFT-D2, the dispersion coefficients $C\_{6ij}$ are geometry-dependent as they are calculated on the basis of the local geometry (coordination number) around atoms $i$ and $j$. Two variants of DFT-D3, that differ in the damping functions $f\_{d,n}$, are available.

### DFT-D3(zero)

In the zero-damping variant of DFT-D3, invoked by setting IVDW=11, the damping function reads

:   $$f\_{d,n}(r\_{ij}) = \frac{s\_n}{1+6(r\_{ij}/(s\_{R,n}R\_{0ij}))^{-\alpha\_{n}}}$$

where $R\_{0ij} = \sqrt{\frac{C\_{8ij}}{C\_{6ij}}}$, the parameters $\alpha\_6$, $\alpha\_8$, $s\_{R,8}$ and $s\_{6}$ are fixed at values of 14, 16, 1, and 1, respectively, while $s\_{8}$ and $s\_{R,6}$ are adjustable parameters whose values depend on the choice of the exchange-correlation functional.

Optionally, the following parameters can be defined in the INCAR file (the given values are the default ones):

* VDW\_RADIUS=50.2 : cutoff radius (in $\AA$) for pair interactions considered in the equation of $E\_{\mathrm{disp}}$
* VDW\_CNRADIUS=20.0 : cutoff radius (in $\AA$) for the calculation of the coordination numbers
* VDW\_S8=[real] : damping function parameter $s\_8$
* VDW\_SR=[real] : damping function parameter $s\_{R,6}$

### DFT-D3(BJ)

In the Becke-Johnson (BJ) damping variant of DFT-D3,, invoked by setting IVDW=12, the damping function is given by

:   $$f\_{d,n}(r\_{ij}) = \frac{s\_n\,r\_{ij}^n}{r\_{ij}^n + (a\_1\,R\_{0ij}+a\_2)^n}$$

with $s\_6=1$ and $a\_1$, $a\_2$, and $s\_8$ being adjustable parameters. As before, the parameters VDW\_RADIUS and VDW\_CNRADIUS can be used to change the default values for the cutoff radii.

Optionally, the parameters of the damping function can be controlled using the following INCAR tags:

* VDW\_S8=[real]
* VDW\_A1=[real]
* VDW\_A2=[real]

> **Mind:**
>
> * The default values for the damping function parameters are available for several GGA (PBE, RPBE, revPBE and PBEsol), METAGGA (TPSS, M06L and SCAN) and hybrid (B3LYP and PBEh/PBE0) functionals, as well as Hartree-Fock. If another functional is used, the user has to define these parameters via the corresponding tags in the INCAR file. The up-to-date list of parametrized DFT functionals with recommended values of damping function parameters can be found on the webpage https://www.chemie.uni-bonn.de/grimme/de/software/dft-d3/ and follow the link "List of parametrized functionals".
> * The DFT-D3 method has been implemented in VASP by Jonas Moellmann based on the dftd3 program written by Stefan Grimme, Stephan Ehrlich and Helge Krieg. If you make use of the DFT-D3 method, please cite reference . When using DFT-D3(BJ) references and should also be cited. Also carefully check the more extensive list of references found on https://www.chemie.uni-bonn.de/grimme/de/software/dft-d3/.

## Related tags and articles

VDW\_RADIUS,
VDW\_CNRADIUS,
VDW\_S8,
VDW\_SR,
VDW\_A1,
VDW\_A2,
IVDW,
DFT-D2,
DFT-ulg,
DFT-D4

## References

---
