# NATURALO

Categories: INCAR tag, Many-body perturbation theory, GW, ACFDT, Low-scaling GW and RPA

NATURALO = [integer]  
 Default: **NATURALO** = 0; for low scaling GW type calculations the default is 4

Description: calculate RPA natural orbitals.

---

This flag should be used in combination with ALGO = G0W0R or ALGO = scGW0R. The VASP code diagonalizes the RPA density
matrix and writes the final natural orbitals to the WAVECAR file.
The one-electron occupancies on the WAVECAR file can also be updated to the eigenvalues of the RPA density matrix. For ALGO = G0W0R, the interacting Green's function is approximated as

$G = G\_0 + G\_0 \Sigma G\_0$

whereas for ALGO = scGW0R the Dyson equation is solved

$G = G\_0 + G \Sigma G\_0.$

In both cases, the RPA density matrix is determined as $\gamma= \lim\_{\tau \to 0^-} G(\tau)$. More details on the use of RPA natural orbitals can be found in Ref. .

The following settings are currently supported

* NATURALO=0 calculate the density matrix, diagonalize the matrix and write the natural orbitals and eigenvalues of the density matrix to WAVECAR. The eigenvalues of the density matrix are stored in the occupancy entries of the WAVECAR file, whereas the one-electron DFT eigenvalues remain untouched. This setting is usually not particularly useful for practical calculations and should be used only by experts. Furthermore, LFINITE\_TEMPERATURE should not be combined with this setting.

* NATURALO=1 calculate the density matrix, diagonalize the matrix only in the sub-block of unoccupied states, and write the occupied Kohn Sham orbitals, as well as the natural orbitals corresponding to unoccupied states to the file WAVECAR. The unoccupied orbitals are ordered according to their occupancies in the RPA density matrix. The one-electron occupancies and KS-DFT eigenvalues are not updated from their KS values (the occupancies will remain 1 for occupied Kohn-Sham orbitals and 0 for natural orbitals representing the virtual manifold). This setting has been used in Ref. . See also Ref. for further information. Note that all orbitals- even those with a tiny fractional occupancy -are treated as occupied orbitals and not updated: the algorithm should hence even work for metallic systems.

* NATURALO<0. Similar to NATURALO=1 but additionally conserves ABS|NATURALO| unoccupied Kohn-Sham states. This is expedient, for subsequent GW and BSE calculations to conserve few unoccupied orbitals to their Kohn-Sham states.

* If 10 is added (e.g. NATURALO=10, NATURALO=11) the density matrix is diagonalizes using a perturbative Loewdin algorithm that attempts to keep the orbital order strictly conserved: E.g. the natural orbital matching closest to each Kohn-Sham orbital will be determined and stored. Use this tag for metals.

* NATURALO=2 (or 12) is similar to 0, but the one-electron occupancies are not updated. In rare cases this might lead to inconsistencies, if the orbital order changes between DFT and the RPA density matrix (i.e. a previously occupied DFT orbitals posses a smaller occupation in the RPA density matrix than some unoccupied Kohn-Sham orbitals and are moved into the unoccupied block). This problem can be reduced using NATURALO=12, as described above. This flag, in combination with ALGO = scGW0R, can be used to evaluate the GW-singles contribution to the correlation energy. One can deduct the HF singles and the GW singles energies from the energies after

```
    Energies after diagonalization of HF Hamiltonian (single shot)
    Hartree-Fock free energy of the ion-electron system (eV)
```

```
    Energies after update of density matrix
    Hartree-Fock free energy of the ion-electron system (eV)
```

Experience has shown that there is very little difference between the natural orbitals obtained using ALGO = G0W0R and ALGO = scGW0R. We strongly recommend to use the more efficient and better tested algorithm ALGO = G0W0R (with the exception of GW-singles) to determine natural orbitals. Furthermore, perform careful tests for NOMEGA: the RPA total energy converges much faster then the natural orbitals. Using a too small NOMEGA can yield natural orbitals that are non-optimal, leading to very slow convergence of correlated calculations with respect to the number of natural orbitals.
A crucial test is that the following line

```
correlated contrib. to density matrix         0.0000004037        0.0000000000
```

in the stdout and OUTCAR file shows values close to zero (for ALGO = G0W0R). The above value is perfectly acceptable and the value decreases as NOMEGA increases.

* NATURALO=4 preserves original (DFT) orbitals but updates the eigenvalues in the WAVECAR file to the QP energies. This mode is useful if only quasi-particle energies are corrected with the GW method, for instance when selecting ALGO=EVGW0R.

> **Mind:** available as of VASP.6.4:

## Related tags and articles

* ALGO for response functions and *RPA* calculations
* for an overview on total energies using the ACFDT/RPA formalism
* for a practical guide to GW calculations

## References

---
