# Category:Molecular dynamics

Categories: VASP

To get an idea about what basically molecular dynamics is and what the main contents are we refer the reader to references and . After understanding the theory behind molecular dynamics we refer the reader to Molecular dynamics calculations, which describes how to run standard molecular dynamics simulations. Every advanced molecular dynamics method builds on the knowledge in that tutorial and should be ideally only viewed after understanding the basics.

## Important files

The input files for standard molecular dynamics runs are the same as for other calculational methods. However additionally to the structural data the POSCAR file can contain the initial velocities as a separate block. It can also contain the input on which atomic positions should be constrained or not.

Constrained and bias molecular dynamics (Constrained molecular dynamics, Metadynamics and Biased molecular dynamics) also require an additional input file, the ICONST file. This file specifies the collective variables. The (ICONST) file is also required for the monitoring of geometric parameters (Monitoring geometric parameters).

Besides the main output files, OUTCAR and OSZICAR, the XDATCAR is an important output file. It contains the trajectory of the MD. Another important output file for molecular dynamics calculations is the REPORT file. It contains various important information and is especially important for calculations where the ICONST file was used.

## Theory

* Ensembles: Ensembles.
* Thermostats: Thermostats.
* Interface pinning: Interface pinning calculations.
* Constrained molecular dynamics: Constrained molecular dynamics.
* Metadynamics: Metadynamics.
* Biased molecular dynamics: Biased molecular dynamics.
* Slow-growth approach: Slow-growth approach.

## How to

* Basic molecular dynamics calculations: Molecular dynamics calculations.
* Ensembles: Ensembles.
* Thermostats: Thermostats.
* Interface pinning: Interface pinning calculations.
* Constrained molecular dynamics: Constrained molecular dynamics.
* Metadynamics: Metadynamics.
* Biased molecular dynamics: Biased molecular dynamics.
* Slow-growth approach: Slow-growth approach.
* Monitoring of geometric parameters: Monitoring geometric parameters.
* Thermodynamic integration: Thermodynamic integration
* Thermodynamic integration with harmonic reference: Thermodynamic integration with harmonic reference
* Thermal conductivity Müller-Plathe method

## Compilation

Many of the simulation methods described in this section are included in VASP as of version 5.2.12, and require VASP to be compiled with the preprocessor flag `-Dtbdyn`. This is usually the case because all makefile.include templates shipped with VASP since version 5.4.4 contain this flag by default.

## Tutorials

* Tutorial for MD calculations.
* Tutorial for training a machine learning force field using MD.
* Lecture for an introduction to MD.
* Lecture on advanced methods of MD.

## References

---
