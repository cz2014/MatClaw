# Input

Overview > Input > Preparing a Super Cell >Output > List of tutorials

VASP basically needs 4 input files for standard production runs:

## INCAR

The INCAR file holds the input parameters which "steer" the calculation.

* The default values set by VASP itself are a clever choice to do standard calculations.
* These standard settings can be modified to specify:
  + What do you want to do? (SCF calculation, DOS, dielectric properties ...)
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

The POTCAR file contains the relevant information concerning the pseudopotentials that are necessary to run the calculation:

* Data that was required for generating the pseudopotentials.
* Number of valence electrons.
* Atomic mass.
* Energy cut-off.

If the cell contains different atomic species, the corresponding POTCAR files have to be concatenated, in the same order as the atomic species are given in the POSCAR file.

**N.B.**: Different XC-types must not be mixed.

Overview > Input > Preparing a Super Cell >Output > List of tutorials

Back to the main page.
