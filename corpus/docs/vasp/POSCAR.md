# POSCAR

Categories: Files, Input files, Symmetry

The POSCAR file is a mandatory VASP input file. It is a plain text file and contains at least the lattice geometry and the ionic positions. Optionally, also starting velocities for a molecular-dynamics simulation can be provided here. This file shares its format with VASP output file CONTCAR. That may contain an additional section with predictor-corrector coordinates necessary for restarting molecular-dynamics runs.

Creating a POSCAR file is often the starting point of VASP-supported research. It can be written manually or obtained from various online materials and crystallographic databases providing a download in the POSCAR file format. POSCAR files can be visualized using a variety of softwares, including VESTA, Jmol, OVITO, and the Atomic Simulation Environment (ASE).

## Basic introduction (minimal example)

In its simplest form the POSCAR file contains basic information about the lattice, per-species number of ions and their positions. This is sufficient in most situation where a VASP calculation is started from scratch. Have a look at this example for cubic boron nitride:

```
Cubic BN
3.57
0.0 0.5 0.5
0.5 0.0 0.5
0.5 0.5 0.0
B N
1 1
Direct
0.00 0.00 0.00 
0.25 0.25 0.25
```

As indicated by the text coloring there are four blocks corresponding to the following file contents:

**Comment line**

The first line is reserved for a free user comment, e.g. a system description.

**Scaling factor and lattice**

In this block the first line specifies a universal lattice scaling factor $s$. The next three lines define the lattice vectors. Each line holds the unscaled Cartesian components of one lattice vector. The actual lattice vectors ${\vec a}\_1, {\vec a}\_2$ and ${\vec a}\_3$ (in $\AA$) are the product of the given numbers with the lattice scaling factor. Set the universal scaling factor to 1 if you want to enter the lattice vectors directly and avoid any additional scaling.

**Ion species and numbers:**

This section defines how many ions of each species are present. The first line lists the species names, the second specifies the number of ions for each species. The given order should match the order of species appearing in the POTCAR file.

> **Warning:** If machine-learned force fields are used (ML\_LMLFF=.TRUE.), it is not possible to give the same name to different groups of atoms in the POSCAR file.

**Ion positions:**

Finally, the ion positions ${\vec R}$ (in $\AA$) are listed in this section. The first line selects one of the two possible modes how the coordinates $x\_1, x\_2$ and $x\_3$ given in the following lines are interpreted:

* "Direct" means the positions are provided in direct (fractional) coordinates:

  ${\vec R} = x\_1 {\vec a}\_1 + x\_2 {\vec a}\_2 + x\_3 {\vec a}\_3,$

  where ${\vec R}$ is the position vector of an ion.

* "Cartesian" specifies that positions are provided in a Cartesian coordinate system. However, the actual ion positions are also multiplied with the universal scaling factor, i.e.

  ${\vec R} = s \left( \begin{array}{c}x\_1 \\ x\_2 \\ x\_3\end{array} \right).$

The total number of lines with positions must match the total number of ions given in the previous section. The ion species are also derived from there, i.e. in the example above it is implied that the list of positions contains one boron ion, followed by one nitrogen nuclei.

## Full format specification

The POSCAR file format is constructed from multiple sections arranged in a predefined order. Some sections contain only a single line, others span over many lines, some may even be omitted. The following list defines the section order and their contents:

Layout of POSCAR file.

* **Comment** - *(1 line), mandatory*
  + The first line is reserved for a free user comment, e.g. a system description. The maximum line length is 40 characters, extra characters are truncated.
* **Scaling factor(s)** - *(1 line), mandatory*
  + This line may contain one or three numbers. If one number is provided it specifies a universal lattice scaling factor $s$. It is multiplied with the three vectors in the following section to obtain the lattice vectors of the unit cell. Also, the ion positions are scaled with this factor if the "Cartesian" mode is selected (see section "Ion positions"). If the number is negative, it is interpreted as the desired cell volume. Then, the scaling factor $s$ is computed automatically to obtain the desired volume. If three numbers are provided in this line they act as individual scaling factors for the x-,y- and z-Cartesian components for the lattice vectors (and "Cartesian" mode ion positions). In this case all three numbers must be positive.
* **Lattice** - *(3 lines), mandatory*
  + This sections contains three lines defining the lattice vectors. Each line holds the unscaled Cartesian components of one lattice vector. The actual lattice vectors ${\vec a}\_1, {\vec a}\_2$ and ${\vec a}\_3$ (in $\AA$) are the product of the given numbers with the lattice scaling factor `s`. Set the universal scaling factor to 1 if you want to enter the lattice vectors directly and avoid any additional scaling.
* **Species names** - *(1 line), optional*
  + This line lists the species of the present ions. The given order should match the order of species appearing in the POTCAR file. This line is optional, if omitted the species names are taken from the POTCAR file.

:   :   > **Warning:**
        >
        > * In a VASP calculation the POTCAR file together with the `Ions per species` section below defines the species of all ions provided in the POSCAR file! This `Species names` section should be considered only as a helpful comment to identify species when inspecting a POSCAR file independently. Switching species names here will not actually change the species of ions in a calculation if the POTCAR file stays the same!
        > * If machine-learned force fields are used (ML\_LMLFF=.TRUE.), it is not possible to give the same name to different groups of atoms in the POSCAR file.
        > * The number of characters a species name can have is only two. If more than two characters are given the code will run but will truncate the name species names after two characters. For example, "Si1" and "Si2" would both be treated as "Si" and "Si". In the case of ML\_LMLFF=.TRUE. the code would be terminated since twice the same name for different species is not allowed.

* **Ions per species** - *(1 line), mandatory*
  + This mandatory line lists how many ions of each species are present. The given order should match the order of species appearing in the POTCAR file.
* **Selective dynamics** - *(1 line), optional*
  + If the line after the "Ions per species" section contains `Selective dynamics` it enables the "selective dynamics" feature (actually only the first character is relevant and must be *S* or *s*). This allows to provide extra flags for each atom signaling whether the respective coordinate(s) of this atom will be allowed to change during the ionic relaxation (or MDs). This setting is useful if only certain shells around a defect or layers near a surface should relax. See also the structure optimization tips.
* **Ion positions** - *(1 line + #atoms), mandatory*
  + Here, the ion positions ${\vec R}$ (in $\AA$) are listed. The first line selects one of the two possible modes how the coordinates $x\_1, x\_2$ and $x\_3$ given in the following lines are interpreted:
    - "Direct" means the positions are provided in direct (fractional) coordinates:

      ${\vec R} = x\_1 {\vec a}\_1 + x\_2 {\vec a}\_2 + x\_3 {\vec a}\_3,$

      where ${\vec R}$ is the position vector of an ion.
    - "Cartesian" specifies that positions are provided in a Cartesian coordinate system. However, the actual ion positions are also multiplied with the universal scaling factor, i.e.

      ${\vec R} = s \left( \begin{array}{c}x\_1 \\ x\_2 \\ x\_3\end{array} \right).$

:   :   Actually, only the first character on the line is significant and the only key characters recognized are `C`, `c`, `K` or `k` for switching to the "Cartesian" mode. Everything else will be interpreted as "Direct" mode.

:   :   The total number of lines with positions must match the total number of ions given in the "Ions per species" section. The ion species are also derived from there, e.g. if the "Ions per species" section lists `5 8`, then there must be five ion position lines for the first species, followed by eight ions of the second species. If your are not sure whether you have a correct input please check the OUTCAR file, which contains both the final Cartesian components of the vector ${\vec R}$ and the positions in direct (fractional) coordinates.

:   :   If the selective dynamics feature is enabled on each coordinate triplet is followed by three additional logical flags, i.e. each is either `T` or `F` for true and false, respectively. This determines whether to allow changes of the coordinates or not. If the line selective dynamics is removed from the POSCAR file this flag will be ignored (and internally set to `T`).

:   :   > **Mind:** The flags refer to the positions of the ions in direct coordinates, no matter whether the positions are entered in "Cartesian" or "Direct" coordinate modes.

:   :   For example, consider the following ion specification:

```
...
Selective dynamics
Cartesian
0.00 0.00 0.00 T F T
1.27 0.98 0.32 F T F
...
```

:   :   Here, the first atom is allowed to move into the direction of the first and third direct lattice vector. The second atom may only move in the second lattice vector direction.

:   :   If no initial velocities are provided, the file may end here.

* **Lattice velocities** - *(8 lines), optional - from CONTCAR only1*
  + Contains the lattice vectors ${\vec a}\_1, {\vec a}\_2$ and ${\vec a}\_3$ and their velocities. Lattice velocities occur when in molecular dynamics simulations, lattice vectors are treated as dynamic variables, i.e., are allowed to change over time (IBRION=0 together with ISIF=3), e.g., Nosé-Hoover thermostat. When written to the CONTCAR file the section starts with a line containing the string `Lattice velocities and vectors`. While reading in the POSCAR file upon restarting only the first character of the line is checked for `L` or `l`. The following line specifies the initialization state of the lattice velocities (usually just the integer 1). The next three lines contain the velocities corresponding to the three lattice vectors divided by the time step given via the POTIM tag. The remaining three lines repeat the actual lattice vectors ${\vec a}\_1, {\vec a}\_2$ and ${\vec a}\_3$ where multiplication with the scaling factor $s$ has already been taken into account.
* **Ion velocities** - *(1 line + #atoms), optional*
  + Here initial velocities for all ions can be provided. The input format is similar to the section "Ion positions" above. The first line determines the input mode which is either "Direct" or "Cartesian". In contrast to the reading of ion positions, there is no multiplication with the scaling factor $s$ applied in the "Cartesian" mode. Another minor difference is the interpretation of the contents of the first line in this section. In addition to `C`, `c`, `K` or `k` as the first character also an empty line switches on the "Cartesian" mode. Everything else enables the "Direct" mode instead. The velocity section written out to the CONTCAR file always starts with an empty line and velocities are given in "Cartesian" mode. The following lines contain the velocity vectors of each ion defined in the "Ion positions" section. Velocities must be provided in units "direct lattice vector/timestep" or $\AA$/fs for "Direct" or "Cartesian" mode, respectively.

:   :   > **Tip:** Entering velocities by hand is rarely done because a simple alternative to set initial velocities is provided via the TEBEG tag.

:   :   > **Mind:** Different rules for the input in this section apply for special VASP features:
        >
        > * IBRION=0 For molecular dynamics velocities are initialized randomly following the Maxwell-Boltzmann distribution, adjusted to the initial temperature set by TEBEG in the INCAR file. Alternatively, starting velocities can be provided either manually or from a previous VASP run.
        > * IBRION=0 and SMASS=-2: In this case the velocities are kept constant during the MD allowing to calculate the energy for a set of different linear dependent positions (for instance frozen phonons and dimers with varying bond-length). The actual steps taken are POTIM times read velocities. Hence, to avoid ambiguities, set POTIM to 1. Then, the velocities will are simply interpreted as vectors, along which the ions are moved. Therefore, for the "Direct" and "Cartesian" modes they are given in units of direct coordinates and $\AA$, respectively (again, no multiplication with the scaling factor).
        > * IBRION=44: The vectors in this section are interpreted as directions of the unstable mode in the context of the Improved Dimer Method.

* **MD extra** - *(variable line number), optional - from CONTCAR only1*
  + The predictor-corrector coordinates are only provided to continue a molecular dynamics run from a CONTCAR file of a previous run, they cannot be entered by hand. There is first a blank line after the ion velocities, the second line is the initialization state of the predictor-corrector coordinates, and the third line is the time step in MD POTIM. The fourth line is the Nosé-Hoover thermostat for the (*n*)th and (*n+1*)th iteration ($s\_{n+1}, \dot{s}\_{n+1}, \dot{s}\_{n}, s\_n$). Finally, the predictor-corrector coordinates are printed.

1 "from CONTCAR only": This section is usually not entered manually by the user. It appears in the CONTCAR file output at the end of VASP runs which involve ionic steps and is intended for restarting a previous calculation.

## Precision and symmetry

VASP determines the symmetry of the system from the POSCAR file.
It is a common mistake to enter the positions with insufficient precision
(too few digits). To make the best use of the symmetry routines in VASP, it is strongly
recommended to specify the positions (and lattice parameters) in the POSCAR file with at least 7 significant digits (but preferably more).
Internal tests for symmetry operations are done against a user-supplied
value for the precision, specified by SYMPREC (defaults to 10-5).
Hence, 5 significant digits are absolutely borderline and can cause
serious issues in the automatic symmetry determination, for instance, finding some
but not all generators for the symmetry group. Also, "noise" in the positions
might grow during relaxations, so that sometimes, upon reading the CONTCAR file,
some symmetry operations are not found. All these issues are best avoided by
making the initial POSCAR file as accurate as possible.

If you have a POSCAR file with the positions written with low precision and would like to reconstruct with higher precision, we recommend using a symmetry package, such as spglib, to find the symmetries given a certain precision, symmetrizing the lattice vectors and positions and writing the POSCAR file with a higher number of significant digits.
This can be done using pymatgen (which interfaces with spglib) to symmetrize the structure and write it to a POSCAR file, see example on github.

### Examples

```
Cubic BN
3.57
0.00000000 0.50000000 0.50000000
0.50000000 0.00000000 0.50000000
0.50000000 0.50000000 0.00000000
B N
1 1
Selective dynamics
Cartesian
0.00000000 0.00000000 0.00000000 T T F
0.25000000 0.25000000 0.25000000 F F F
Cartesian
0.01000000 0.01000000 0.01000000
0.00000000 0.00000000 0.00000000
optionally predictor-corrector coordinates 
   given on file CONTCAR of MD-run
  ....
  ....
```

```
fcc Si
3.9
 0.50000000 0.50000000 0.00000000
 0.00000000 0.50000000 0.50000000
 0.50000000 0.00000000 0.50000000
  1
cartesian
0.00000000 0.00000000 0.00000000
```

```
MgO Fm-3m (No. 225)
1.0
 2.606553 0.000000 1.504894
 0.868851 2.457482 1.504894
 0.000000 0.000000 3.009789
 Mg O
 1 1
direct
 0.000000 0.000000 0.000000 Mg
 0.500000 0.500000 0.500000 O
```

## Related tags and articles

structure optimization, SYMPREC, IBRION, CONTCAR, POTCAR

## References

---
