# ICHARG

Categories: INCAR tag, Electronic minimization, Electronic ground-state properties, Charge density, Electronic occupancy

ICHARG = 0 | 1 | 2 | 4 | 5

|  |  |  |
| --- | --- | --- |
| Default: **ICHARG** | = 2 | if ISTART=0 |
|  | = 0 | else |

Description: ICHARG determines how VASP constructs the *initial* charge density.

---

* ICHARG=0

:   Calculate the charge density from initial wave functions.
:   If ISTART is *internally reset* due to an invalid WAVECAR file, ICHARG will be set to ICHARG=2.

:   > **Warning:** This may cause convergence problems for some systems.

* ICHARG=1

:   Read the charge density from CHGCAR file, and extrapolate from the old positions (on CHGCAR) to the new positions using a linear combination of atomic charge densities.
:   In the PAW method, there is, however, one important point to keep in mind: For the on-site densities (that is, the densities within the PAW sphere), only l-decomposed charge densities up to LMAXMIX are written. Upon restart, the energies might, therefore, differ slightly from the fully converged energies. The discrepancies can be large for the DFT+U method. In this case, one might need to increase LMAXMIX to 4 (d-elements) or even 6 (f-elements).

:   > **Tip:** To improve convergence and reduce the number of electronic steps, it is recommended to set ICHARG = 1 when starting calculations repeatedly with small changes in the input parameters.

* ICHARG=2

:   Take superposition of atomic charge densities.

* ICHARG=4

:   Read potential from file POT. The local potential on the file POT is written by the optimized-effective-potential methods (OEP), if the flag LVTOT=.TRUE. is supplied in the INCAR file. Supported as of VASP.5.1.

* ICHARG=5

:   External charge-density-update mode to read in and add an external correction to the Kohn-Sham (KS) occupations in every SCF step of the electronic minimization. The initialization of the charge density is done as in ICHARG=1, and after NELMDL steps VASP reads the occupations from a user-supplied text file GAMMA (or vaspgamma.h5 if compiled with HDF5 support) for each k point in each SCF step. The procedure described in Ref. Eq. (30)-(32) is then used to construct a new charge density from the combined occupations (KS occupations + GAMMA file), from which the next KS potential is constructed. The DFT workflow continues after a user-supplied vasp.lock file is read. Additionally, with ICHARG=5 after each SCF step VASP writes out all with LOCPROJ defined wave function projections. The ICHARG=5 mode can be used with an external code that modifies the occupations, and requires extra output after each SCF step. The TRIQS software package makes use of it to perform charge self-consistent DFT plus dynamical mean field theory (DMFT) calculations. See the DFT+DMFT howto page for a tutorial.

* ICHARG=10

:   non-selfconsistent calculations: Adding 10 to the value of ICHARG, e.g., ICHARG=11 or 12 (or the less convenient value 10) means that the charge density will be kept constant during the *entire electronic minimization*.

:   There are several reasons why to keep the charge density constant:

    * ICHARG=11

    :   To obtain the eigenvalues (for band-structure plots) or the density of states (DOS) of a given charge density read from CHGCAR. The self-consistent CHGCAR file must be determined beforehand by a fully self-consistent calculation with a k-point grid spanning the entire Brillouin zone.

:   * ICHARG=12

    :   Non-self-consistent calculations for a superposition of atomic charge densities. This is in the spirit of the non-self-consistent Harris-Foulkes functional. The stress and the forces calculated by VASP are correct, and it is possible to perform an ab-initio MD for the non-selfconsistent Harris-Foulkes functional.

:   > **Tip:** If ICHARG is set to 11 or 12, it is strongly recommended to set LMAXMIX to twice the maximum l-quantum number in the pseudopotentials. Thus, for s and p elements LMAXMIX should be set to 2, for d elements LMAXMIX should be set to 4, and for f elements LMAXMIX should be set to 6.

The initial charge density is of importance in the following cases:

* If ICHARG≥10 the charge density remains constant during the run.

* For all algorithms except IALGO=5X the initial charge density is used to set up the initial Hamiltonian that is used in the first few non-selfconsistent steps, c.f., NELMDL tag.

## Related tags and articles

CHGCAR, ISTART, LCHARG, LMAXMIX, NELMDL, INIWAV, GAMMA, vaspgamma.h5

Examples that use this tag

---
