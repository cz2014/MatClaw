# LTRIPLET

Categories: INCAR tag, Many-body perturbation theory, Bethe-Salpeter equations

LTRIPLET = .TRUE. | .FALSE.

|  |  |  |
| --- | --- | --- |
| Default: **LTRIPLET** | = .FALSE. |  |

Description: LTRIPLET selects a triplet ansatz for Bethe-Salpeter-equations (BSE) calculations. This is synonymous to LHARTREE = .FALSE.

---

For a usual BSE calculation (LHARTREE=.TRUE.; LTRIPLET = .FALSE.), the excited state corresponds to a singlet if the ground state is not spin-polarized (ISPIN=1) or anti-ferromagnetic (ISPIN=2, total magnetic moment 0). This is so because the ansatz for the BSE calculation involves a hole and an electron pair prepared within each spin channel. For instance, an electron with up spin is removed from the ground-state determinant and placed with the same spin into a previously unoccupied orbital. If there are no separate spin channels this ansatz results in a net spin-zero, which corresponds to a singlet state.

If LTRIPLET=.TRUE., VASP assumes that an *up* electron is removed from the ground-state determinant and placed as a *down* electron into a previously unoccupied orbital (spin flip). This ansatz corresponds to a triplet state as it has a net spin of one. Without spin-orbit coupling (LSORBIT = .FALSE.), the transition probability from the singlet ground state to the triplet solutions will be exactly zero. These excitations correspond to dark, potentially long-lived triplet excitons. However, VASP calculates the transition probabilities incorrectly, by assuming that a spin-flip excitation has the same transition probabilities as a usual singlet excitation.
The reported transition probabilities ("optical transitions" in vasprun.xml) are hence incorrect; they should be all zero. Likewise, the contributions to the dielectric function are zero for triplet excitations,
and incorrectly reported in the vasprun.xml file.

If a non-magnetic material is calculated using ISPIN=2 for both the groundstate and BSE calculation, and a usual BSE calculation is performed (LHARTREE=.TRUE.; LTRIPLET = .FALSE.), all
singlet transitions as well as one set of the triplet excitations (those with $m\_S=0$ ) are calculated. All triplet transitions will have zero transition probabilities. If LTRIPLET = .TRUE. is set for the BSE calculation, the other two sets of triplet excitations (those with $m\_S=1$ and $m\_S=-1$) are determined. Note that as for ISPIN=1 for ISPIN=2 and LTRIPLET = .FALSE., incorrect non-zero transition probabilities are reported in the vasprun.xml file (they should be all exactly zero, since the underlying pair states fed into the BSE can not be excited by light).

To obtain meaningful transition probabilities for the singlet and triplet excitations, include spin-orbit coupling by setting LSORBIT = .TRUE. in the INCAR file throughout the calculation, i.e., for the ground-state and BSE calculation. In this case, the singlet and all three sets of triplet excitations are calculated simultaneously, and proper transition probabilities are assigned to each transition. Small transition probabilities might be observed even for triplet excitations as a result of spin-orbit coupling. LTRIPLET = .TRUE. should not be used for calculations including spin-orbit coupling.

> **Warning:** LTRIPLET=.TRUE. has not been extensively tested in combination with spin-polarized ground states (ISPIN=2).

> **Warning:** We are not sure whether the BSEFATBAND approach can be combined with the LTRIPLET tag.

## Related tags and articles

LHARTREE,
ISPIN,
LSORBIT,
BSE calculations

Examples that use this tag

## References

---
