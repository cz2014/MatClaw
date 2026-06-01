# KPOINTS_OPT_MODE

Categories: INCAR tag, Electron-phonon interactions, Electronic minimization

KPOINTS\_OPT\_MODE = 0 | 1 | 2  
 Default: **KPOINTS\_OPT\_MODE** = 1

Description: Selects which diagonalization algorithm to use for the optional k-points driver

> **Mind:** Available as of VASP 6.5.0

---

Sometimes, the electronic Kohn-Sham orbitals are required on an alternative k-point mesh, for example via KPOINTS\_OPT or KPOINTS\_ELPH.
In this case, the tag KPOINTS\_OPT\_MODE selects which diagonalization algorithm should be used to obtain these eigenvalues.

## Tag options

`KPOINTS_OPT_MODE = 0`
:   The diagonalization of the Hamiltonian at the alternative k-points is skipped entirely

`KPOINTS_OPT_MODE = 1`
:   Uses the Blocked-Davidson algorithm (same as `ALGO = Normal`)

`KPOINTS_OPT_MODE = 2`
:   Performs an exact diagonalization (same as `ALGO = Exact`)

## Related tags and articles

* KPOINTS\_OPT
* KPOINTS\_ELPH
* ALGO
