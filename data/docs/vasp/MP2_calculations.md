# MP2 calculations

Categories: Many-body perturbation theory, MP2, Howto

By specifying ALGO=*MP2* in the INCAR file VASP calculates MP2 correlation energies. It is strongly recommended to calculate all virtual states spanned by the basis set before calling the MP2 routines.

Thus any MP2 calculation should proceed in three steps:

* The first step is the determination of the occupied orbitals of the Hartree-Fock Hamiltonian. Note that MP2 requires to calculate the Hartree-Fock groundstate, and any LDA or GGA correlation should be switched off. Following specific INCAR tags have to be set:

```
LHFCALC = .TRUE.
AEXX = 1.0 ; ALDAC = 0.0 ; AGGAC = 0.0
ALGO = D ; EDIFF = 1E-7
```

* Next search for maximum number of plane-waves in the OUTCAR file and execute VASP again using the following INCAR tags:

```
NBANDS  =   maximum number of plane-waves
LHFCALC = .TRUE.
AEXX = 1.0 ; ALDAC = 0.0 ; AGGAC = 0.0
ALGO = Exact ; NELM = 1 ; LOPTICS = .TRUE.
```

* Finally calculate the MP2 correlation energy:

```
NBANDS  =   maximum number of plane-waves
LHFCALC = .TRUE. ;  AEXX = 1.0 ; ALDAC = 0.0
LMAXMP2 = 2
```

The flag LMAXMP2 specifies the maximum $l$ quantum number for the treatment of the one-center terms. This should be set to twice the maximum of the non local component in the pseudopotential. Alternatively LMAXFOCKAE can be set in the INCAR file. This is expected to be more efficient, but slightly less accurate. Combining LMAXFOCKAE and LMAXFOCKMP2 is in principle also allowed but hardly offers any advantage over using only LMAXFOCKAE or LMAXFOCKMP2.

---
