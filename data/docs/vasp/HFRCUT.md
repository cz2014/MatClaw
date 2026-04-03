# HFRCUT

Categories: INCAR tag, Exchange-correlation functionals, Hybrid functionals

HFRCUT = [real]  
 Default: **HFRCUT** = 0

Description: HFRCUT specifies how the Coulomb kernel is approximated at G=0 when the Fock energy and the exchange potential are evaluated.

---

In systems with periodic boundary conditions, the Coulomb energy and the Coulomb potential are usually evaluated under the assumption of a compensating background by introducing a compensation charge density. This is well-justified for the Hartree energy, where the compensation charge density stems from the ions. Yet, this assumption is not valid for the Fock exchange, which causes an error. For the Fock exchange potential and energy, one can correct the resulting error by assuming that the density matrix is local. The leading order correction is given by the difference between the electrostatic energy of a localized model charge density in a homogeneous background periodically repeated and the same model charge density in isolation. For details we refer to J. Paier *et al.,* Section II. D. 4.

* HFRCUT = 0: Ewald summation *or* method of Massida, Posternak, and Baldereschi depending on k-mesh

:   If a regular automatic k-mesh and the standard 1/r Coulomb kernel are used, the correction is computed using Ewald summations. If the k-mesh is *not* regular (e.g., if the k-points are explicitly listed in the KPOINTS file) or if kernels different from the bare Coulomb kernel are used (e.g., HSE functional), the method of Massida, Posternak, and Baldereschi is used. This approach assumes that the model charge density is an error-function-like charge distribution in real space in order to handle the long-range nature of the potential in reciprocal space. It requires setting a decay constant for the error function, see HFALPHA. Both methods, the Ewald summation and the method of Massida, Posternak, and Baldereschi, are strictly equivalent for regular k-mesh.

* HFRCUT = -1: Automated cutoff radius

:   An alternative recipe is to replace the 1/r Coulomb kernel with a truncated Coulomb kernel that is strictly zero beyond a certain cutoff radius. If HFRCUT is set to -1, the radial cutoff is chosen to be equivalent to the radius of the sphere with a volume of the unit cell times the total number of k-points in the full Brillouin zone. For instance, for a 4x4x4 k-point grid, that yields 64 times the volume of the unit cell.

* HFRCUT = [cutoff radius]: Manually set cutoff radius in Ångström.

In the limit of many k-points, both methods (HFRCUT=-1 and HFRCUT=0) should yield identical results. In our experience, the HFRCUT=-1 converges more rapidly for systems with a gap, as well as molecules and atoms, whereas HFRCUT=0 converges faster for metallic systems. It is expedient to first converge the energies with respect to the number of k-points for both methods and then select for subsequent calculations the method that converges more rapidly. A detailed comparison of the convergence of the different methods for metallic and gapped materials was made by Sundararaman and Arias.

## Related tags and articles

AEXX,
AGGAX,
AGGAC,
ALDAC,
HFALPHA,
LTHOMAS,
List of hybrid functionals,
Hybrid functionals: formalism,
Coulomb singularity

Examples that use this tag

## References

---
