# LOPTICS

Categories: INCAR tag, Linear response, Dielectric properties

LOPTICS = .TRUE. | .FALSE.  
 Default: **LOPTICS** = .FALSE.

Description: LOPTICS=.TRUE. calculates the frequency dependent dielectric matrix after the electronic ground state has been determined.

---

The imaginary part is determined by a summation over empty states using the equation:

:   $$\epsilon^{(2)}\_{\alpha \beta}\left(\omega\right) = \frac{4\pi^2 e^2}{\Omega}
    \mathrm{lim}\_{q \rightarrow 0} \frac{1}{q^2} \sum\_{c,v,\mathbf{k}} 2 w\_\mathbf{k} \delta( \epsilon\_{c\mathbf{k}} - \epsilon\_{v\mathbf{k}} - \omega)
    \times \langle u\_{c\mathbf{k}+\mathbf{e}\_\alpha q} | u\_{v\mathbf{k}} \rangle
    \langle u\_{v\mathbf{k}} | u\_{c\mathbf{k}+\mathbf{e}\_\beta q} \rangle$$

here the indices *c* and *v* refer to conduction and valence band states respectively, and *u**c***k** is the cell periodic part of the orbitals at the k-point **k**. The real part of the dielectric tensor ε(1) is obtained by the usual Kramers-Kronig
transformation

:   $$\epsilon^{(1)}\_{\alpha \beta} (\omega) = 1 + \frac{2}{ \pi} P \int\_0^{\infty}
    \frac{ \epsilon^{(2)}\_{\alpha \beta} (\omega') \omega'}{ \omega'^2- \omega^2 + i \eta } d \omega'$$

where *P* denotes the principle value. The method is explained in detail in the paper by Gajdoš *et al.* (see Eqs. 15, 29, and 30). The complex shift η is determined by the parameter CSHIFT.

Note that local field effects, i.e. changes of the cell periodic part of the potential are neglected in this approximation. These can be evaluated using either the implemented density functional perturbation theory (LEPSILON=.TRUE.), or the GW routines.

The method selected using LOPTICS=.TRUE. requires an appreciable number of empty conduction band states. Reasonable results are usually only obtained, if the parameter NBANDS is roughly doubled or tripled in the INCAR file with respect to the VASP default.
Furthermore it is emphasized that the routine works properly even for HF and screened exchange type calculations and hybrid functionals. In this case, finite differences are used to determine the derivatives of the Hamiltonian with respect to **k**.

Note that the number of frequency grid points is determined by the parameter NEDOS. In many cases it is desirable to increase this parameter significantly from its default value. Values around NEDOS=2000 are strongly recommended.

VASP posses multiple other routines to calculate the frequency dependent dielectric function.
Specifically, one can use ALGO = TDHF (Casida/BSE calculations), ALGO = GW (GW calculations) and ALGO = TIMEEV (Time Evolution: apply a delta kick and follow the induced dipoles).
Compared to LOPTICS=.TRUE., all those routines have the advantage to include
effects beyond the independent particle approximation, however, they are usually
also much more expensive than LOPTICS=.TRUE.

### Spectral broadening

The dielectric function calculated with LOPTICS includes broadening due to the smearing method ISMEAR and the Lorentzian broadening due to the complex shift in the Kramers-Kronig transformation. For example, the combination of LOPTICS=.TRUE. and ISMEAR=0 produces the dielectric function broadened by a Gaussian with the width SIGMA and a Lorentzian with the width CSHIFT. To avoid using two different broadening methods simultaneously and only include the Lorentzian broadening, one should set SIGMA to a much smaller value than CSHIFT.

Note, that the imaginary part of the dielectric function is also broadened by the Lorentzian as long as CSHIFT is not too small, in which case a warning is printed. This means that first a Gaussian broadening is added directly when the imaginary part of the dielectric function is calculated, and successively afterwards a Loretzian broadening is applied. Mind, that this especially affects the life time, i.e. long tails of the transitions, and can influence the dielectric function significantly and produce artifacts if the cut-off frequency OMEGAMAX is chosen close to a large transition element.

> **Warning:** Note that LOPTICS = .TRUE. with ISMEAR = -2 is currently not supported.

> **Mind:** Furthermore the combination of LOPTICS = .TRUE. and ISMEAR selecting the tetrahedron method is only supported as of VASP 6.3.

## Related tags and articles

CSHIFT,
LNABLA,
LEPSILON,
Time Evolution,
WPLASMAI

See also: Examples that use this tag

## References

---
