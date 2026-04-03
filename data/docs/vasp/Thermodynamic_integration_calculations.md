# Thermodynamic integration calculations

Categories: Advanced molecular-dynamics sampling, Howto

Thermodynamic integration (TI) is an approach where two different calculations (e.g., different k-point meshes, machine learning force fields vs. ab-initio) are run in parallel with linear combination of the forces and stresses. This creates allows controlled integration between the two, from a *reference* system to and *interacting* system. The free energy of a fully interacting system can be written as the sum of the free energy a non-interacting reference system and the difference in the free energy of the fully interacting system and the non-interacting system

:   :   $F\_{1} = F\_{0} + \Delta F\_{0\rightarrow 1}$.

Using thermodynamic integration the free energy difference between the two systems is written as

$\Delta F\_{0\rightarrow 1} = \int\limits\_{0}^{1} d\lambda \langle U\_{1}(\lambda) - U\_{0}(\lambda) \rangle\_{\lambda}$.

Here $U\_{1}(\lambda)$ and $U\_{0}(\lambda)$ describe the potential energies of a fully-interacting and a non-interacting reference system, respectively. The coupling strength of the systems is controlled via the coupling parameter $\lambda$. It is neccessary that the connection of the two systems via the coupling constant is reversible. The notation $\langle \ldots \rangle\_{\lambda}$ denotes an ensemble average of a system driven by the following classical Hamiltonian

:   :   $H\_{\lambda}= \lambda H\_{1} + (1-\lambda) H\_{0}$.

VASP supports three approaches to  thermodynamic integration (TI):

* TI between any two states using VCAIMAGES.
* TI with a harmonic solid or ideal gas as a reference state using SCALEE.
* TI with a harmonic solid as a reference state using TILAMBDA.

Details on choosing the ensemble size and how to perform the integration are described in the main text and especially the supplementary information of reference .
**Caution:** the tag *ISPECIAL*=0 used in that reference is not valid anymore, instead the tag PHON\_NSTRUCT=-1 is used.

## TI using VCAIMAGES

**Main tags:**

* VCAIMAGES
* NCORE\_IN\_IMAGE1.

**Directory structure:**

* A parent directory with two subdirectories: *01* and *02* (these represent two images).
* All three directories must include the VCAIMAGES and NCORE\_IN\_IMAGE1 tags in their INCAR files, with identical values.
* Subdirectories must contain identical POSCAR and POTCAR files. Other files (e.g., KPOINTS) can differ, enabling TI between distinct calculation setups (e.g., different k-point meshes, machine learning force fields vs. ab-initio).
* The parent directory's files should match those in *01*, except for the INCAR, which only needs the VCAIMAGES and VCAIMAGES entries.
* Parameters controlling atomic motion (e.g., IBRION, ISIF, POTIM, MDALGO) must be identical in both subdirectories.
* Force calculation parameters may differ.

**How it works:**

* Similar to nudged elastic band calculations, multiple calculations are run (subdirectories *01* and *02*).
* The VCAIMAGES tag linearly combines the forces and stresses:
  + Weight for *01*: VCAIMAGES
  + Weight for *02*: 1 - VCAIMAGES
  + Thus, VCAIMAGES must be between 0 and 1.
* NCORE\_IN\_IMAGE1 sets the number of cores used for *01*; remaining cores are used for *02*.

> **Warning:** Both directories must contain the same positions after applying the forces and the thermostat contributions. So thermostats containing random numbers cannot be used (MDALGO must be 2).

## TI using SCALEE

**Main tags:**

* SCALEE: Sets the coupling parameter $\lambda$ and determines the Hamiltonian used in the calculation.

**Directory structure:**

* Thermodynamic integration (TI) with SCALEE is performed in a single directory.
* Optionally, the calculation can read the file DYNMATFULL if present (see details below).

**How it works:**

* The main control tag is SCALEE, which sets the coupling parameter $\lambda$ and determines the Hamiltonian used in the calculation.

### Available options for reference system

**Ideal gas:**
By default the thermodynamic integration is carried out from the ideal gas to the fully interacting case (in the case when no DYNMATFULL is present in the calculation folder). Usually the Stirling approximation is used for the free energy of the ideal gas written as

:   :   $$F = -\frac{1}{\beta} \mathrm{ln} \left[ \frac{V^{N}}{\Alpha^{3N} N!} \right]$$

where $V$ is the volume of the system, $N$ is the number of particles in the system and $\Alpha$ is the de Broglie wavelength. The Stirling approximation applies in principle only in the limes of infinitely many particles. In reference the exact ideal gas equation was used since it helped to speed up the convergence of the final free energy of liquid Si with respect to the system size.

**Harmonic solid:**
If the file DYNMATFULL exists in the calculation directory and SCALEE$\ne$1, the second order Hessian matrix is added to the force and thermodynamic integration from a harmonic model to a fully interacting system is carried out. The DYNMATFULL file stores the eigenmodes and eigenvalues from diagonalizing the dynamic matrix. This file is written by a previous calculation using the INCAR tags IBRION=6 and PHON\_NSTRUCT=-1.
This calculaion runs in a single folder.
It optionally reads in a DYNMATFULL file in the calculation directory (for more details see below).
The tag SCALEE sets the coupling parameter $\lambda$ and hence controls the Hamiltonian of the calculation.
By default SCALEE=1 and the scaling of the energies and forces via the coupling constant is internally skipped in the code. To enable the scaling SCALEE$\lt$1 has to be specified.

## TI using TILAMBDA

**Main tags:**

* TILAMBDA: Sets the value for the coupling parameter $\lambda$.

**Directory structure:**

* Thermodynamic integration (TI) with TILAMBDA is performed in a single directory.
* Internal coordinates for the TI calculation are defined in the ICONST file, with the status set to 3.
* The Hessian matrix in Cartesian coordinates, $\mathbf{\underline{H}}^\mathbf{x}$, must be provided in the HESSEMAT file. The calculation automatically transforms this matrix to internal coordinates, $\mathbf{\underline{H}}^\mathbf{q}$.

**How it works:**

* The potential energies for both systems (system 1 and system 0) are computed in the internal coordinate representation, $\mathbf{q}$.
* These values are used to evaluate the integrand $\langle V\_1 - V\_{0,\mathbf{q}} \rangle$ in the TI expression $\Delta F\_{0,\mathbf{q} \rightarrow 1}$.
* The TI calculations are performed in the NVT ensemble using any available thermostat.

**Output:**

* The required energies are written in the REPORT file. Look for lines beginning with the string `e_ti>`.

## References
