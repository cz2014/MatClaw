# NELMDL

Categories: INCAR tag, Electronic minimization

NELMDL = [integer]

|  |  |  |
| --- | --- | --- |
| Default: **NELMDL** | = -12 | if ISTART=0, INIWAV=1, and IALGO=48 or IALGO=50 |
|  | = 0 | if WAVECAR is present |
|  | = -5 | else |

Description: NELMDL specifies the number of non-self-consistent steps at the beginning.

---

If the orbitals are initialized using a random number generator (the default in VASP), the initial orbitals are usually unreasonable and the iterative matrix diagonalization will require 5-10 steps to obtain reasonable orbitals. The charge density corresponding to the initial orbitals is also, at best, erratic. It is hence advisable to perform a few electronic steps while keeping the initial Hamiltonian fixed. This initial Hamiltonian is usually determined from a superposition of atomic charge densities (see ICHARG).

Such a 'delay' is absolutely necessary if the SCF-convergence is slow and problematic (e.g. for surfaces or metallic clusters, low dimensional system). Without a delay, VASP will most likely not converge, or at least the convergence speed is slowed significantly.

NELMDL might be set to a positive or negative value. A negative value means that the delay is only performed in the first ionic step (usually the recommended option). A positive number means that a delay is employed after each ionic movement. This can improve the convergence speed in VASP.6 (see below) but is not recommended in VASP.5.

For calculations using a direct minimization of the Hamiltonian (ALGO=ALL or ALGO=DAMPED), the Davidson algorithm is used during the delay phase and the Hamiltonian is kept fixed during these steps.

Special considerations for VASP.6:

* For calculations using a direct minimization of the Hamiltonian (ALGO=ALL or ALGO=DAMPED): if NELMDL is set, the Davidson algorithm is used in the first NELMDL steps as described above. Using a positive NELMDL (i.e. delay in every ionic step) does not work reliably in VASP.5, due to issues in the orbital and charge density prediction. In VASP.6, using NELMDL=1 (or NELMDL=2) and direct minimization often improves the stability and efficiency of molecular dynamics simulations or relaxations (ALGO=ALL or ALGO=DAMPED). Note, however, that this might require one to prepare a reasonable WAVECAR file since NELMDL =1/2 might not suffice to obtain a reasonable set of orbitals from the initial random numbers.

* For HF-type calculations, if NELMDL is larger or equal to 3, VASP will perform NELMDL non-selfconsistent steps using the Davidson algorithm, and a local Hamiltonian is calculated using the semi-local DFT functional corresponding to the chosen hybrid functional (i.e. PBE for HSE and PBE0). This is expedient if the ions move by a large distance between the ionic steps. Setting NELMDL =3 can thus improve the stability and performance during relaxations using HF-type Hamiltonians. Try to use ALGO=All and NELMDL=3 if you encounter convergence issues during relaxations using HF-type Hamiltonians.

## Related tags and articles

NELM,
NELMIN,
IALGO

Examples that use this tag

---
