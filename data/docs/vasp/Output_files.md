# Category:Output files

Categories: VASP, Files, Calculation setup

The main output file of VASP is the OUTCAR. The vasprun.xml contains similar information but in an xml format.
The OSZICAR file contains the total energies of the electronic and ionic SCF steps, and it is useful for the monitoring of the calculation.

When HDF5 support is enabled, a vaspout.h5 file is produced containing the main results of the VASP calculation.

Here is a comprehensive list of all important output files:

:   |  |  |
    | --- | --- |
    | BSEFATBAND | BSE eigenvalues used for "fatband" plots. |
    | CHG | Contains charge density, lattice vectors and atomic coordinates. Should be used for visualization. |
    | CHGCAR | Same as CHG but it contains also one-center occupancies. Should be used to restart VASP from existing charge density. |
    | CONTCAR | Is the updated POSCAR file after each calculation, whether ionic movement was performed or not. |
    | DOSCAR | Contains DOS and integrated DOS. |
    | EIGENVAL | Contains Kohn-Sham eigenvalues for each k point after the end of the calculation. |
    | ELFCAR | Contains electron localization function. |
    | IBZKPT | Contains k-point coordinates and weights. |
    | LOCPOT | Contains total local potential in eV. |
    | OSZICAR | Information on each electronic and ionic SCF step. |
    | OUTCAR | Main output file. |
    | PARCHG | Contains partial charge densities. |
    | PCDAT | Contains the pair correlation function. |
    | PROCAR | Contains spd and site-projected wave function character. |
    | PROOUT | Contains projection of wavefunction onto spherical harmonics. |
    | REPORT | Contains output of various molecular dynamics caculations (umbrella integration, etc.). |
    | TMPCAR | Contains wavefunction and ionic positions of previous ionic step. |
    | vasprun.xml | Main output file in xml format. |
    | vaspout.h5 | Main output file in hdf5 format. Required for the postprocessing with py4vasp. |
    | vaspwave.h5 | Contains charge density and wave functions when output is directed to hdf5. |
    | Wxxxx.tmp | Contains diagonal elements of screened exchange in BSE calculations. |
    | WAVECAR | Binary file containing information such as wave function coefficients, eigenvalues, Fermi weights, etc. |
    | WAVEDER | Contains derivative of wave functions with respect to k point. |
    | WFULLxxxx.tmp | Store full screened exchange in BSE calculations. |
    | XDATCAR | Contains ionic configuration for each output step of molecular dynamics simulations. |
