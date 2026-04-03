# Input and Output - a short Intro

Categories: Files

# Input

VASP basically needs 4 input files for standard production runs:

## INCAR

The INCAR file holds the input parameters which "steer" the calculation.

* The default values set by VASP itself are a clever choice to do standard calculations.
* These standard settings can be modified to specify:
  + What do you want to do? (scf calculation, DOS, dielectric properties ...)
  + You can give parameters to fulfill your requirements concerning required precision, requested convergence, calculation time ...

## POSCAR

The POSCAR file contains the information on the structure.

* A simple POSCAR file may look like this:

```
fcc:  Ni
3.53
0.5 0.5 0.0
0.0 0.5 0.5
0.5 0.0 0.5
Ni
1
Selective Dyn
Cartesian
0 0 0  T T T
```

* The description of each line is given as follows:
  + 1: Header (comment).
  + 2: Overall scaling constant.
  + 3-6: Bravais matrix.
  + 4: Name(s) of the atom(s).
  + 5: Number of the atoms (of each atom type).
  + 6: (optional: selective dynamics).
  + 7: Specifies which coordinate system is used ("cartesian" or "direct").
  + 8-x: Positions of the atoms.

## KPOINTS

The KPOINTS file determines the sampling of the 1st Brillouin zone.

* A typical KPOINTS file:

```
Automatic mesh
0
G (M)
4 4 4
0.  0.  0.
```

* The description of each line is given as follows:
  + 1: Header (comment).
  + 2: Specifies the k mesh generation type. $N\_{\overrightarrow{k}} = 0$: automatic generation scheme.
  + 3: $\Gamma$-centered (Monkhorst-Pack) grid.
  + 4: Number of subdivisions in each direction.
  + 5: Optional shift of the mesh.

## POTCAR

The POTCAR file contains the relevant information concerning the pseudo potentials that are necessary to run the calculation:

* Data that was required for generating the pseudo potentials.
* Number of valence electrons.
* Atomic mass.
* Energy cutoff.

If the cell contains different atomic species, the corresponding POTCAR files have to be concatenated, in the same order as the atomic species are given in the POSCAR file.

**N.B.**: Different XC-types must not be mixed.

# Output

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

Back to the main page.
