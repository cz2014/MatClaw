# ALGO

Categories: INCAR tag, Electronic minimization, Many-body perturbation theory, GW, Bethe-Salpeter equations

ALGO = Normal | VeryFast | Fast | Conjugate | All | Damped | Subrot | Eigenval | Exact | None | Nothing | CHI | G0W0 | GW0 | GW | scGW0 | scGW | G0W0R | GW0R | GWR | scGW0R | scGWR | ACFDT | RPA | ACFDTR | RPAR | BSE | TDHF  
 Default: **ALGO** = Normal

Description: the ALGO tag is a convenient option to specify the electronic minimization algorithm (as of VASP.4.5) and/or to select the type of GW calculations.

---

* ALGO=Normal selects IALGO=38 (blocked-Davidson-iteration scheme).

* ALGO=VeryFast selects IALGO=48 (RMM-DIIS). This algorithm has been updated for vasp.6 to increase robustness. To select the version that was available in vasp.5, select "Old VeryFast". hybrid functionals are not supported for ALGO=VeryFast. The algorithm can be combined with LDIAG=.FALSE. to conserve the initial orbital order (when orbitals are read from the WAVECAR file).

* ALGO=Old VeryFast (or "ov" or "vo") selects IALGO=48 (RMM-DIIS). This option is available in vasp.6 and selects the version of the RMM-DIIS algorithm that was available in vasp.5.

* ALGO=Fast selects a fairly robust mixture of the blocked-Davidson and RMM-DIIS algorithms. In this case, blocked Davidson (IALGO=38) is used for the initial phase, and then VASP switches to RMM-DIIS (IALGO=48). Subsequently, for each ionic update, one IALGO=38 sweep is performed for each ionic step (except the first one). This algorithm has been updated for vasp.6 to increase robustness. To select the version that was available in vasp.5, select "Old Fast".

* ALGO=Old Fast (or "of" or "fo"). This option is available in vasp.6 and selects the ALGO=Fast algorithm that was available in vasp.5.

* ALGO=Conjugate or ALGO=All selects an "all band simultaneous update of orbitals" (IALGO=58, both tags are synonymous). Recommended to be used with the improved line-search algorithm (ISEARCH = 1).

* ALGO=Damped selects a damped velocity friction algorithm (IALGO=53). The algorithm can be combined with LDIAG=.FALSE. to conserve the initial orbital order (when orbitals are read from the WAVECAR file).

* ALGO=Exact performs an exact diagonalization (IALGO=90).

* ALGO=Subrot selects subspace rotation or diagonalization in the sub-space spanned by the orbitals (IALGO=4).

* ALGO=Eigenval allows to recalculate one-electron energies, the density of state and perform selected postprocessing using the current orbitals (IALGO=3) e.g. read from the WAVECAR file.

* ALGO=None or ALGO=Nothing allows to recalculate the density of states or perform selected postprocessing, using the current orbitals and one electron energies (IALGO=2) e.g. read from the WAVECAR file.

More details can be found under the documentation for the tag IALGO.

> **Tip:** Except for 'None', 'Nothing', 'Exact' and 'Eigenval' (which must be spelled out), the first letter determines the applied algorithm.

Conjugate, Subrot, Eigenval, None and Nothing are only supported by vasp.5.2.9 and newer versions.

> **Warning:** For fast convergence, LMAXMIX must be set appropriately. E.g. LMAXMIX=6 for systems including f electrons.

## ALGO for response functions and GW calculations and ACFDT/RPA calculations

The following tags are available as of VASP.5.X.

* ALGO=CHI calculates the response functions only.

* ALGO=TDHF selects TDHF (or  TDDFT) calculations using the VASP internal Cassida code see BSE calculations, (available as of VASP.5.2.12)

* ALGO=BSE selects BSE calculations using the VASP internal Cassida code see BSE calculations, (available as of VASP.5.4.1)

* ALGO=Timeev performs a delta-pulse in time and then performs timepropagation

* ALGO=ACFDT selects RPA total energy calculations see ACFDT/RPA calculations

* ALGO=RPA synonymous to ACFDT see ACFDT/RPA calculations (available as of VASP.5.3.1)

GW tags have been renamed in VASP as follows

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| < 5.2.12 | scGW | scGW0 | GW | GW0 | N/A | N/A |
| >= 5.2.12, < 6 | QPGW | QPGW0 | GW | GW0 | N/A | N/A |
| >= 6 | QPGW | QPGW0 | EVGW | EVGW0 | GWR | GW0R |

* ALGO=EVGW0 selects single-shot *G*0*W*0 calculations or partially self-consistent *GW* calculations. The orbitals (wavefunctions) of the previous groundstate calculations are maintained, and G0W0 calculations are performed. If NELM is set, several iterations are performed, and the QP energies are updated in the calculation of *G* (for details, see EVGW0 calculations).

* ALGO=EVGW selects single-shot *G*0*W*0 calculations or partially self-consistent *GW* calculations. The orbitals of the previous groundstate calculations are maintained, and G0W0 calculations are performed. If NELM is set, several iterations are performed, and the QP energies are updated in the calculation of *G* AND *W* (for details, see self-consistent EVGW and QPGW calculations).

* ALGO=QPGW0 selects self-consistent *GW* calculations including off-diagonal components of the selfenergy. A full update of the QP energies AND one-electron orbitals is performed in the calculation of *G* only (for details see QPGW0 calculations).

* ALGO=QPGW selects self-consistent *GW* calculations, including off-diagonal components of the selfenergy. A full update of the QP energies AND one-electron orbitals is performed in the calculations of *G* AND *W* (for details, see QPGW calculations).

Following tags are available as of VASP.6

* ALGO=RPAR selects low scaling RPA total energy calculations (for details see ACFDT/RPA calculations)

* ALGO=ACFDTR synonym for RPAR (for details see ACFDT/RPA calculations)

* ALGO=ACFDTRK in combination with LMP2LT = .TRUE. selects the low scaling MP2 total energy calculations (for details see the MP2 ground state Tutorial)

* ALGO=GW0R selects self-consistent GW0 calculations, where only the Green's function *G* is updated from the corresponding Dyson. The screened potential *W* remains unchanged after the first iteration. NELM iteration cycles are performed (see self-consistent GW calculations).

* ALGO=GWR selects self-consistent GW calculations, where both, *G* and *W* are updated from the corresponding Dyson equation. NELM iteration cycles are performed. (for details see self-consistent GW calculations).

* ALGO=G0W0R selects single-shot GW calculations, non-interacting *G* and *W* are determined from Kohn-Sham system and NELM tag is ignored. Use this tag for single-shot QP energies and first-order corrections to the density matrix (for details, see single-shot GW calculations).

> **Important:** Changes as of VASP.6.3:

* NELMGW replaces NELM in self-consistent GW calculations.

* ALGO=CRPA selects constrained RPA alculations.

> **Important:** available as of VASP.6.4:

* ALGO=EVGW0R selects the low-scaling analog of EVGW0, that is the low-scaling partially self-consistent GW calculations, where non-interacting *G* and *W* are determined from Kohn-Sham system and NELMGW specifies the number of self-consistent loops for *G*. *W* is kept on the Kohn-Sham level.

## Related tags and sections

IALGO,
LDIAG,
Electronic minimization

Examples that use this tag

---
