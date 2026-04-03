# LSCDM

Categories: INCAR tag, Wannier functions

LSCDM = .TRUE. | .FALSE.

|  |  |  |
| --- | --- | --- |
| Default: **LSCDM** | = .FALSE. |  |

Description: LSCDM switches on the selected columns of the density matrix (SCDM) method.

---

The selected columns of the density matrix (SCDM) method works by fitting a unitary matrix $U\_{mn\mathbf{k}}$ that transforms
the basis from Bloch states $|\psi\_{n\mathbf{k}}\rangle$ obtained by VASP to a  Wannier basis $|w\_{m\mathbf{R}}\rangle$.

:   :   $$|w\_{m\mathbf{R}}\rangle =
        \sum\_{n\mathbf{k}}
        e^{-i\mathbf{k}\cdot\mathbf{R}}
        U\_{mn\mathbf{k}}
        |\psi\_{n\mathbf{k}}\rangle.$$

This is done using a  one-shot method  through a singular-value decomposition as proposed by A. Damle and L. Lin .

In order to obtain a good Wannierization, a certain level of freedom should be given to the localized orbitals to adequately accommodate the Bloch states. This is controlled by the cutoff function specified by the CUTOFF\_TYPE tag and related parameters
$\mu$ (CUTOFF\_MU) and
$\sigma$ (CUTOFF\_SIGMA).

## Related tags and articles

CUTOFF\_TYPE,
CUTOFF\_MU,
CUTOFF\_SIGMA

Examples that use this tag

## References
