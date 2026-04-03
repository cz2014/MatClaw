# Category:Calculation setup

Categories: VASP

The Vienna ab-initio simulation package (VASP) is a computer program for atomic scale materials modeling from first principles. To get a license, please refer to the registration form on the VASP website. You will get access to the VASP source and compile it directly on your hardware to achieve optimal performance.

For **instructions of a basic calculation** read how to perform an electronic minimization.

In a nutshell, after the installation, VASP can be executed from the command line of a Terminal. Navigate to a working directory. In the working directory, VASP looks for input files that determine what calculation is performed. The most important input files are

* the POSCAR file: Defines the structure of the material, i.e., lattice vectors, ionic positions, etc.
* the INCAR file: General selection of the algorithm, setting parameters, etc.
* the POTCAR file: Contains the pseudopotentials and other information relevant for the PAW method
* the KPOINTS file: Defines the Bloch vectors **k** in reciprocal space.

The central way to control the calculation is by setting INCAR tags in the INCAR file. Depending on the VASP calculation, there are other input files to provide settings for the calculation, e.g., the ICONST file.

> **Tip:** To learn how to set up a calculation, we recommend following some of our tutorials.

Finally, VASP will write output files to the working directory.

> **Tip:** For postprocessing, py4vasp is a convenient Python package to read and visualize the produced data.

This category contains all pages and topics relevant to the **computational setup**. For instance, installation, files, performance, etc.
