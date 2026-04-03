# Output

Categories: Output files

Overview > Input > Preparing a Super Cell >Output > List of tutorials

VASP gives several different output files, depending on which task is performed. The most important files that are produced in (almost) every calculation are described in the following:

## OUTCAR

The OUTCAR file gives detailed output of a VASP run, including:

* A summary of the used input parameters.
* Information about the electronic steps: $E\_{\mathrm{Fermi}}$, KS-eigenvalues.
* Stress tensors.
* Forces on the atoms.
* Local charges and magnetic moments.
* Dielectric properties

The amount of output written onto the OUTCAR file can be chosen by modifying the NWRITE tag in the INCAR file.

## OSZICAR and stdout

The OSZICAR file gives a short summary of the results:

* Chosen SCF algorithm.
* Convergence of the total energy, charge- and spin densities.
* Free energies.
* Magnetic moments of the cell.

## CONTCAR

The CONTCAR file gives the updated geometry data at the end of a run:

* Lattice parameter.
* Bravais matrix.
* Ionic positions.
* (Optionally velocities).

The format of the CONTCAR file is the same as of the POSCAR file, hence it can be used directly for continuation runs after having been copied to the POSCAR file.

## XDATCAR

The XDATCAR file contains updated ionic positions of each ionic step.

## DOSCAR

The DOSCAR file contains the total and integrated DOS and optionally the local partial DOS.

## CHGCAR

The CHGCAR file contains the charges $\rho \* V$.

## WAVECAR

The WAVECAR file contains the wave function coefficients.
This file can be used to continue from a previous run.

Overview > Input > Preparing a Super Cell >Output > List of tutorials

Back to the main page.
