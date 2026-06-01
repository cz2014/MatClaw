# NBANDS

Categories: INCAR tag, Electronic minimization, Dielectric properties, Parallelization

NBANDS = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NBANDS** | = $\max \left( \frac{1}{2}\operatorname{nint} \left(N\_{\mathrm{elect}} + 2\right) + \max\left(\frac{1}{2}N\_{\mathrm{ions}}, 3\right), \operatorname{int}\left(\frac{3}{5} N\_{\mathrm{elect}}\right) \right)$ |  |

$N\_{\mathrm{elect}}$ is NELECT and $N\_{\mathrm{ions}}$ is the number of ions (NIONS in OUTCAR).

Description: NBANDS specifies the total number of KS or QP orbitals in the calculation.

---

The right choice of NBANDS strongly depends on the type of the performed calculation and the system. As a minimum, VASP requires all occupied states + one empty band, otherwise, a warning is given.

#### Electronic minimization

In the electronic minimization calculations, empty states do not contribute to the total energy, however, empty states are required to achieve a better convergence.
In iterative matrix-diagonalization algorithms (see ALGO) eigenvectors close to the top of the calculated number of states converge much slower than the lowest eigenstates, thus it is important to choose a sufficiently large NBANDS. Therefore, we recommend using the default settings for NBANDS, i.e., *NELECT/2 + NIONS/2*, which is a safe choice in most cases. In some cases, it is also possible to decrease it to *NELECT/2+NIONS/4*, however, in some transition metals with open *f* shells a much larger number of empty bands might be required (up to *NELECT/2+2\*NIONS*). To check this parameter perform several calculations for a fixed potential (ICHARG=12) with an increasing number of bands (e.g. starting from *NELECT/2 + NIONS/2*). An accuracy of $10^{-6}$ should be obtained in 10-15 iterations.

> **Tip:** Note that the RMM-DIIS scheme (ALGO=Fast) is more sensitive to the number of bands than the default Davidson algorithm (ALGO=Normal) and can require more bands for fast convergence.

#### Many-body perturbation theory calculations

In the Many-Body Perturbation Theory calculations (*GW*,RPA, and BSE), a large number of empty orbitals is usually required, which can be much higher than the number of occupied states. The convergence of the calculations with a large number of empty states can be very slow. In such cases, we recommend performing an exact diagonalization (ALGO=Exact) of the Hamiltonian with empty bands starting from a converged charge density.

#### Parallelization

When executed on multiple CPUs, VASP automatically increases the number of bands, so that NBANDS is divisible by the number of CPU cores. If NCORE > 1, NBANDS is increased until it is divisible by the number of cores in a group (NCORE). If KPAR > 1, NBANDS is increased until it is divisible by the number of cores in a group.

#### Spin-polarized calculation

In the case of spin-polarized calculations, the default value for NBANDS is increased to account for the initial magnetic moments.

#### Noncollinear calculation

In noncollinear calculations, the default NBANDS value is doubled to account for the spinors components.

## Related tags and article

NCORE, NBANDS, NBANDSGW, NBANDSV, NBANDSO, NPAR,KPAR

---
