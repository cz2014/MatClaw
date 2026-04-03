# OMEGAMAX

Categories: INCAR tag, Many-body perturbation theory, GW

OMEGAMAX = [real]  
 Default: **OMEGAMAX** = outermost node in dielectric function $\epsilon(\omega)$/1.3

Description: OMEGAMAX specifies the maximum frequency for the dense part of the frequency grid for GW calculations (old GW code, does not apply to GWR).
For CRPA calculations, OMEGAMAX is the frequency point of the interaction.
For BSE calculations OMEGAMAX determines the maximum energy difference for excitation pairs to be included.
For calculations of the dielectric function via LOPTICS OMEGAMAX determines the maximum frequency of the calculated dielectric properties. Since the flag controls different aspects of the code, be careful when setting it (and remember to remove the tag, when you change the type of calculations).

---

GW type calculations:

For the frequency grid along the real and imaginary axis sophisticated schemes are used, which are based on simple model functions for the macroscopic dielectric function. The grid spacing is dense up to roughly 1.3\*OMEGAMAX and becomes coarser for larger frequencies. The default value for OMEGAMAX is either determined by the outermost node in the dielectric function (corresponding to a singularity in the inverse of the dielectric function) or the energy difference between the valence band minimum and the conduction band minimum. The larger of these two values is used. Except for pseudopotentials with deep lying core states, OMEGAMAX is usually determined by the node in the dielectric function.

For ACFDT calculations, only OMEGAMIN and OMEGATL determine the frequency grid (using a minimax algorithm).

The defaults have been carefully tested, and it is recommended to leave them unmodified, whenever possible. The grid should be solely controlled by NOMEGA. The only other value that can be modified is the complex shift CSHIFT. In principle, CSHIFT should NOT be chosen independently of NOMEGA and OMEGAMAX: e.g. for less dense grids (smaller NOMEGA) the complex shift must be accordingly increased. The default for CSHIFT has been chosen such that the calculations are converged to 10 meV with respect to NOMEGA: i.e. if CSHIFT is kept constant and NOMEGA is increased, the QP shifts should not change by more than 10 meV; at least for LSPECTRAL = .TRUE.. This was the case for the considered test materials. For LSPECTRAL = .FALSE. this does not apply. In this case it is recommended to set CSHIFT manually and to perform careful convergence tests.

For LSPECTRAL = .TRUE. independent convergence tests with respect to NOMEGA and CSHIFT are usually not required, and it should be sufficient to control the technical parameters via the single parameter NOMEGA. Also note that too large values for NOMEGA in combination with coarse k-point grids can cause a decrease in precision (see NOMEGA).

BSE and TD-DFT type calculations (see BSE calculations):

In this case, OMEGAMAX allows to reduce the number of conduction/ valence band pairs. Usually these are determined by NBANDSV and NBANDSO. The number of pairs is roughly proportional to the products of NBANDSV, NBANDSO, and the number of k-points in the full Brillouin zone. If OMEGAMAX is set, pairs for which the difference of the independent particle energy is larger than
OMEGAMAX will be removed from the basis set (and from the BSE calculations). This can improve performance, without significantly affecting the imaginary part of the dielectric function. The real part of the dielectric function is, however, rather sensitive to reducing OMEGAMAX, NBANDSV, NBANDSO.

Frequency dependent dielectric matrix calculations (see LOPTICS):

Here, OMEGAMAX sets the maximum frequency of the dielectric function calculated. The number of grid points is then defined via NEDOS. Note, that this parameter does not cut-off the number conduction/ valence band pairs considered in the dielectric function. Only the dielectric function itself is cut-off at this frequency. Hence, this does not affect computational effort significantly. It is advisable to choose OMEGAMAX high enough such that the excitation spectrum is well covered, to avoid artifacts at the cut off frequency due to the Gaussian and Lorentzian broadening (see section LOPTICS#Spectral broadening)

## Related tags and articles

OMEGATL,
CSHIFT,
NOMEGA,
OMEGAMIN

Examples that use this tag

---
