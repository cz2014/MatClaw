# KPOINTS

Categories: VASP, Files, Input files, Band structure, Symmetry, Crystal momentum

The KPOINTS file specifies the Bloch vectors (**k** points) used to sample the Brillouin zone.
Converging this sampling is one of the essential tasks in many calculations concerning the electronic minimization.
A regular mesh is the most common choice to select **k** points:

```
Regular 4 x 4 x 4 mesh centered at Gamma 
0
Gamma
4 4 4
```

> **Tip:** Choose the number of points along each direction approximately inversely proportional to the corresponding length of the unit cell.

A  band structure is often visualized along high-symmetry paths.
Some external tools help to identify these points for materials of any symmetry.
Use the template below to setup band-structure calculations.
Alternatively, use a KPOINTS\_OPT file to get the band structure as a postprocessing step after the regular calculation.

```
k points along high symmetry lines
 40              ! number of points per line
line mode
fractional
  0    0    0    Γ
  0.5  0.5  0    X

  0.5  0.5  0    X
  0.5  0.75 0.25 W

  0.5  0.75 0.25 W
  0    0    0    Γ
```

> **Tip:** If the KPOINTS file is not present, the tag KSPACING determines the **k**-point sampling. Use that option for a quick first run but prefer generating a regular mesh for production calculations.

## Coordinate system

When specifying coordinates in the KPOINTS file, use one of the following coordinate systems:

Fractional coordinate system
:   The **k** points are linear combinations of the reciprocal lattice vectors ${\mathbf b}\_{1\ldots3}$

    :   $${\mathbf k} = x\_1 {\mathbf b}\_1 + x\_2 {\mathbf b}\_2 + x\_3 {\mathbf b}\_3~.$$
:   Use the factors $x\_{1\ldots3}$ as the coordinates in KPOINTS.

Cartesian coordinate system
:   The coordinates $x\_{1\ldots3}$ directly correspond to the **k** point

    :   $${\mathbf k} =\frac{2 \pi}{a} (x\_1, x\_2 , x\_3)~.$$
:   up to the scaling factor $2\pi / a$. Here, $a$ is the scaling parameter specified on the second line of the POSCAR file.

**Example: face-centered-cubic (fcc) lattice**

The following lattice vectors $\mathbf a\_i$ span the unit cell:

:   :   $$\mathbf a\_1 = a \begin{pmatrix} 0 \\ 1/2 \\ 1/2\end{pmatrix}
        \qquad
        \mathbf a\_2 = a \begin{pmatrix} 1/2 \\ 0 \\ 1/2\end{pmatrix}
        \qquad
        \mathbf a\_3 = a \begin{pmatrix} 1/2 \\ 1/2 \\ 0\end{pmatrix}$$

The corresponding reciprocal lattice vectors $\mathbf b\_i$ are

:   :   $$\mathbf b\_1 = \frac{2 \pi}{a} \begin{pmatrix} -1 \\ 1 \\ 1 \end{pmatrix}
        \qquad
        \mathbf b\_2 = \frac{2 \pi}{a} \begin{pmatrix} 1 \\ -1 \\ 1 \end{pmatrix}
        \qquad
        \mathbf b\_3 = \frac{2 \pi}{a} \begin{pmatrix} 1 \\ 1 \\ -1 \end{pmatrix}~.$$

The following table shows several high-symmetry points of the fcc lattice expressed in Cartesian and fractional coordinates, respectively:

```
Point     Cartesian coordinates     Fractional coordinates
            (units of 2pi/a)         (units of b1,b2,b3)
----------------------------------------------------------
  Γ         (  0    0    0  )         (  0    0    0  )
  X         (  0    0    1  )         ( 1/2  1/2   0  )
  W         ( 1/2   0    1  )         ( 1/2  3/4  1/4 )
  K         ( 3/4  3/4   0  )         ( 3/8  3/8  3/4 )
  L         ( 1/2  1/2  1/2 )         ( 1/2  1/2  1/2 )
```

## Explicit **k**-point mesh

When an explicit **k**-point mesh is provided, VASP uses exactly the provided points.
The primary use case of this mode is to look at particular features in the band structure, e.g., for effective mass calculations.
For regular meshes and band structures, we recommend using the automatic generation to avoid mistakes.
Nevertheless, all other modes write the processed input in this format to the IBZKPT file, so understanding this format helps analyze mistakes in setting up the KPOINTS file.
A typical example has the following format:

```
Explicit k-point list
4
Cartesian
0.0  0.0  0.0   1
0.0  0.0  0.5   1
0.0  0.5  0.5   2
0.5  0.5  0.5   4
```

* The first line is treated as a comment line.
* Provide the number of **k** points on the second line.
* The first character on the third line specifies the coordinate system. Use *C*, *c*, *K*, or *k* to indicate Cartesian coordinates. Any other character is interpreted as fractional/reciprocal coordinates but we advise writing *fractional* or *reciprocal* to make this clear.
* Each following line contains the coordinates and weight of one **k** point. VASP takes care that weights are properly normalized so only relative weight is important. Typically the weights correspond to the symmetry degeneracy of a **k** point.

Use the explicit mode for

* a (small) number of **k** points not forming a regular mesh.
* the calculation of band structure when the line mode is not suitable (example: hybrid functionals).
* the irreducible part of the genereralized regular meshes generated for a particular target sampling density. Generate the corresponding KPOINTS files with KpLib or autoGR.

**Tetrahedron method**

:   When using the tetrahedron method (see ISMEAR), extend the list of **k** points by a list of all tetrahedra.

```
Explicit k-point list
4
Cartesian
0.0  0.0  0.0   1
0.0  0.0  0.5   1
0.0  0.5  0.5   2
0.5  0.5  0.5   4
Tetrahedra
1  0.183333333333333
6    1 2 3 4
```

:   The line following the list of **k** point coordinates and weights must start with 'T' or 't'. On the next line, enter the number of tetrahedra and the volume weight common to all the tetrahedra. The volume weight is simply the ratio between the volume of a tetrahedron and the volume of the first Brillouin zone.

:   Subsequently, list the symmetry-degeneration weight and the four corner points of each tetrahedron. The four integers represent the indices of the corners of the tetrahedron in the **k**-point list given above. Here, the counter starts at 1 and corresponds to the **k** point specified in the fourth line.

:   > **Warning:** VASP does not renormalize the weights of the tetrahedra. Make sure they are appropriately normalized.

> **Important:** Explicitly listing all the **k** points is not very convenient, especially in the context of the tetrahedron method. Keep in mind that the automatic modes generate the IBZKPT file in this format. For any nontrivial case, preferably modify an automatically-generated IBZKPT instead of building an explicit list from scratch.

## Regular **k**-point mesh

This mode will automatically generate a mesh where each lattice vector is subdivided into an explicitly defined number of subdivisions.
It offers sufficient flexibility and stability and should be preferred for most production calculations.
Choose the number of subdivisions $N\_1$, $N\_2$ and $N\_3$ in the KPOINTS file like this

```
Regular k-point mesh
0              ! 0 -> determine number of k points automatically
Gamma          ! generate a Gamma centered mesh
4  4  4        ! subdivisions N_1, N_2 and N_3 along the reciprocal lattice vectors
0  0  0        ! optional shift of the mesh (s_1, s_2, s_3)
```

* The first line is a comment line.
* In the second line, set the number of **k** points to 0 to indicate an automatic mesh generation.
* The first nonblank character of the third line determines the center of the mesh. The possible choice are Γ-centered (*G*, *g*) or the Monkhorst-Pack scheme (*M*, *m*).
* Specify the desired number of subdivisions $N\_1$, $N\_2$ and $N\_3$ in the fourth line.
* Optionally add a fifth line to shift the mesh by $(s\_1, s\_2, s\_3)$ with respect to the default.

Γ-centered mesh
:   The following **k** points sample the Brillouin zone

    :   $${\mathbf k} = \sum\_{i = 1}^3 \frac{n\_i+s\_i}{N\_i} {\mathbf b}\_i \qquad \forall {n\_i \in [0, N\_i[}$$

Monkhorst-Pack mesh
:   The **k** point mesh results from this definition

    :   $${\mathbf k} = \sum\_{i = 1}^3 \frac{n\_i+s\_i+\frac{1-N\_i}{2}}{N\_i} {\mathbf b}\_i \qquad \forall {n\_i \in [0, N\_i[}$$

The spacing between the points is the same for both meshes.
The only difference is the shift $(1-N\_i)/2$ in the numerator of the Monkhorst-Pack mesh.
For an odd number of subdivisions, this term is an integer, and therefore the two meshes agree due to periodic boundaries.
When the number of subdivisions is even the Γ-centered mesh is shifted by $s\_i = 1/2$ compared to the Monkhorst-Pack one.

> **Important:** Monkhorst-Pack meshes may converge faster than the Γ-centered ones. However, carefully read the section on symmetry considerations to avoid breaking the symmetry with a Monkhorst-Pack mesh.

**Guidelines for the choice of the subdivisions**

As a rule of thumb, choose $N\_1$, $N\_2$, and $N\_3$ such that

:   :   $$N\_1 : N\_2 : N\_3 \approx |\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|~.$$

This guideline is also implemented for the automatic **k**-point generation using KSPACING.
Nevertheless, specifying the $N\_1$, $N\_2$, and $N\_3$ manually ensures that changes in the lattice vectors do not affect the **k**-point mesh.
When the primitive cell has (nearly) perpendicular axes (cubic, tetragonal, orthorhombic), this is equivalent to:

:   :   $$N\_1 : N\_2 : N\_3 \approx \frac{1}{|\mathbf a\_1|} : \frac{1}{|\mathbf a\_2|} : \frac{1}{|\mathbf a\_3|}~.$$

Of course, this only provides a guide for the ratios between the subsections. The actual density of the **k** point mesh has to be increased until some relevant output quantity of the calculation is converged.

## Symmetry reduction of the mesh

VASP determines the symmetry of the system.
For ISYM $\ge$ 0, the automatically generated **k**-point meshes are reduced to the irreducible subset.
Every **k** point acquires a weight following their symmetry multiplicity.
This can significantly reduce the total number of **k** points.

> **Important:** To enable an efficient symmetry reduction, the (shifted) regular mesh of **k** points should conserve the point-group symmetry of the reciprocal lattice. Specifically, the generating lattice ($\mathbf g\_i = \mathbf k\_i / N\_i$) should belong to the same class of Bravais lattice as the reciprocal lattice.

Consequently, refrain from using a shifted regular mesh for some Bravais lattices, see table.
Importantly, this includes the default Monkhorst-Pack mesh for even numbers of subdivisions.
Furthermore, the reciprocal lattice vectors do not in general align with lattice vectors.
There is typically a difference in the subdivisions obtained from the inverse of the lattice vectors or the reciprocal lattice vectors.

:   :   $$\frac{1}{|\mathbf a\_1|} : \frac{1}{|\mathbf a\_2|} : \frac{1}{|\mathbf a\_3|} \neq |\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3| \qquad \text{in general}$$

In some special cases, the two options are equal, e.g., when the length of all vectors is the same, or they are mutually perpendicular.
Unfortunately, either choice yields incompatible **k** point meshes for some of the Bravais lattices.
Consult the table below to make an informed choice depending on the symmetry of the system.

| Bravais lattice | variant | mesh choices | subsection choices |
| --- | --- | --- | --- |
| triclinic | primitive | $\Gamma$-centered, Monkhorst Pack | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| monoclinic | primitive | $\Gamma$-centered, Monkhorst Pack | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| base-centered | $\Gamma$-centered, Monkhorst Pack | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| orthorhombic | primitive | $\Gamma$-centered, Monkhorst Pack | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| base-centered | $\Gamma$-centered, Monkhorst Pack | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| body-centered | $\Gamma$-centered, Monkhorst Pack | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$ |
| face-centered | $\Gamma$-centered | $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| tetragonal | primitive | $\Gamma$-centered, Monkhorst Pack | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| body-centered | $\Gamma$-centered, Monkhorst Pack | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$ |
| hexagonal | rhombohedral | $\Gamma$-centered | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| hexagonal | $\Gamma$-centered | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| cubic | primitive | $\Gamma$-centered, Monkhorst Pack | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| body-centered | $\Gamma$-centered, Monkhorst Pack | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |
| face-centered | $\Gamma$-centered | $|\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$, $|\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$ |

> **Tip:** VASP issues an error when it detects an incompatible **k**-point mesh. The specific error message depends on the particular setup but includes the name of the routine *IBZKPT*, some warning about the *generating k-lattice*, and some suggestions to overcome the problem.

Summarizing the information in the table above

* Use **only** $\Gamma$-centered meshes for face-centered cubic (fcc), hexagonal, and fcc-orthorhombic crystalline lattices.
* Choose the ratios of the subdivisions $N\_1 : N\_2 : N\_3 = |\mathbf a\_1|^{-1} : |\mathbf a\_2|^{-1} : |\mathbf a\_3|^{-1}$ for *body-centered tetragonal* and *body-centered orthorhombic* lattices. Keep in mind that the KSPACING uses the reciprocal lattice vectors so may not be suitable for these symmetries.
* For *face-centered orthorhombic* crystal structures, choose subdivisions according to $N\_1 : N\_2 : N\_3 = |\mathbf b\_1| : |\mathbf b\_2| : |\mathbf b\_3|$.
* For any other symmetry, all combinations should work but a change to other subdivisions or meshes may overcome possible issues.

Solve problems with the primitive cells of the body-centered tetragonal and body/face-centered orthorhombic Bravais lattices with one of these options:

1. Choose $N\_1=N\_2=N\_3$. For $N \times N \times N$ Monkhorst-Pack meshes the reciprocal lattice is always of the same Bravais lattice as the generating lattice. For body-centered tetragonal and face-centered orthorhombic primitive cells, the reciprocal lattices are body-centered tetragonal and body-centered orthorhombic, respectively. Therefore, choosing equal subdivisions is justified because the length of all reciprocal lattice vectors is the same $|\mathbf b\_1|=|\mathbf b\_2|=|\mathbf b\_3|$.
2. A simple but computationally-expensive option is to change to the conventional cell of the structure. For the body-centered tetragonal/orthorhombic structure, the conventional cell is two times bigger than the primitive cell.
3. Alternatively, define the **k**-point mesh for the conventional cell. This approach requires a generalized regular mesh introduced in the next section and is demonstrated for the example of a body-centered orthorhombic lattice.

## Generalized regular meshes

When more control about the generated mesh is desired, one can specify the generating vectors explicitly.
A typical use case would be to generate the mesh for the *conventional* unit cell and apply it to the *primitive* one.
Build a KPOINTS file for this mode starting from this template

```
Automatic generation
0
Cartesian
0.25 0.00 0.00
0.00 0.25 0.00
0.00 0.00 0.25
0.00 0.00 0.00
```

The mode is activated by specifying the coordinate system with the first nonblank character in line 3.
A *C*, *c*, *K* or *k* character determines that the generating basis vectors are in Cartesian coordinates.
Use *r* or *R* to select the reciprocal coordinate system instead.
The latter is also the default used if VASP cannot interpret the provided character but we recommend not relying on this behavior.
Otherwise, the introduction of further automatic modes in the future versions of VASP may change the interpretation of the KPOINTS file.

VASP generates three vectors $\mathbf g\_1$, $\mathbf g\_2$, and $\mathbf g\_3$ from the coefficients $x\_i$ given in line 4–6.
Depending on the selected coordinate system these vectors are either multiples of the reciprocal lattice vectors
$\mathbf b\_i$ (reciprocal) or simply multiplying the coefficients by $2\pi/a$ (Cartesian).
Here $a$ is the scaling parameter you have specified on the second line of the POSCAR file.

> **Important:** The generating vectors $\mathbf g\_1$, $\mathbf g\_2$, and $\mathbf g\_3$ must be commensurate with the reciprocal lattice. This means $\mathbf b\_i = \textstyle \sum\_{j} M\_{ij} \mathbf g\_j$ where the matrix $M$ contains only integer entries. If this is not the case the code will exit in error.

Combined with the shift ($s\_1$, $s\_2$, $s\_3$) specified in the last line, VASP uses the generating vectors $\mathbf g\_i$ to construct the **k**-point mesh

:   :   $${\mathbf k} = \sum\_i {\mathbf g}\_i (n\_i + s\_i) \qquad n\_i \in [0, N\_i[$$

where VASP chooses the $N\_i$ to include all possible points of the generating mesh in the first Brillouin zone.

The regular **k**-point meshes are a subset of the generalized regular meshes, for which

:   :   $$\mathbf g\_i = \mathbf b\_i / N\_i~.$$

Here, the generating lattice vectors are integer subdivisions of the reciprocal lattice vectors according to the $N\_i$ defined in the KPOINTS file.

For instance, the generalized regular mesh given by

```
Automatic generation
0
Reciprocal
 0.25 0.00 0.00
 0.00 0.25 0.00
 0.00 0.00 0.25
 0.50 0.50 0.50
```

is equivalent to the Monkhorst-Pack mesh specified by

```
Automatic generation
0
Monkhorst-pack
 4 4 4
 0 0 0
```

A typical use-case for generalized regular meshes is to generate a **k**-point mesh based on the *conventional* cell of a particular Bravais lattice to be used with the *primitive* cell of that lattice (see the subsection on symmetry considerations).
As an example, consider the primitive cell of a *body-centered orthorhombic* lattice:

:   :   $$A = a \left( \begin{array}{rrr}
        -1/2 & b/2a & c/2a \\
        1/2 & -b/2a & c/2a \\
        1/2 & b/2a & -c/2a \\
        \end{array} \right)$$

where the rows of $A$ represent the lattice vector of the primitive cell.
The corresponding conventional cell is given by

:   :   $$A = a \left( \begin{array}{rrr}
        1 & 0 & 0 \\
        0 & b/a & 0 \\
        0 & 0 & c/a \\
        \end{array} \right)$$

and its reciprocal lattice by

:   :   $$B = \frac{2\pi}{a} \left( \begin{array}{rrr}
        1 & 0 & 0 \\
        0 & a/b & 0 \\
        0 & 0 & a/c \\
        \end{array} \right)~.$$

Then the following generating lattice based on the reciprocal lattice of the conventional cell

:   :   $$G = \frac{2\pi}{a} \left( \begin{array}{rrr}
        1/N\_1 & 0 & 0 \\
        0 & a/bN\_2 & 0 \\
        0 & 0 & a/cN\_3 \\
        \end{array} \right)$$

yields a roughly uniform sampling of the Brillouin zone when $N\_1$, $N\_2$, and $N\_3$ are chosen such that:

:   :   $$N\_1 : N\_2 : N\_3 \approx 1 : \frac{a}{b} : \frac{a}{c}$$

For instance, for a body-centered orthorhombic primitive cell with $a=5, \; b/a=1.2 \; c/a=0.5$, here given in POSCAR file format:

```
body-centered orthorhombic primitive cell
5.0
-0.500000  0.600000  0.250000
 0.500000 -0.600000  0.250000
 0.500000  0.600000 -0.250000
1
direct
0.000000 0.000000 0.000000
```

this following KPOINTS file

```
Generalized regular mesh
0
Cartesian
 0.50000000  0.00000000  0.00000000
 0.00000000  0.41666667  0.00000000
 0.00000000  0.00000000  0.50000000
 0.00000000  0.00000000  0.00000000
```

corresponds to the aforementioned generating lattice for $N\_1=2$, $N\_2=2$, and $N\_3=4$.

Furthermore, using generalized regular meshes potentially requires fewer **k** points compared to Monkhorst-Pack meshes to converge total energy calculations.
Specifically this statement applies to the number of **k** points in the irreducible part of the Brillouin zone after symmetry reduction.
For the moment, however, VASP does not automatically construct optimal generalized regular **k**-point meshes.
But external tools construct meshes with certain target sampling density in the spirit of the aforementioned publications.

## Band-structure calculations

When properties depend on the **k** vector, it is often convenient to visualize the property along high-symmetry lines.
The line mode generates **k** points between user-defined points in the Brillouin zone.
The most common use case is analyzing the electronic band structure.

> **Warning:** The mesh generated by this mode is not suitable for self-consistent calculations. Please set ICHARG = 11 to avoid updating the density.

> **Mind:** For meta-GGA and hybrid functionals, a regular mesh must always be provided. Refer to band-structure calculations using meta-GGA functionals *or* using hybrid functionals, respectively.

Build the KPOINTS based on this template

```
k points along high symmetry lines
 40              ! number of points per line
line mode
fractional
  0    0    0    Γ
  0.5  0.5  0    X

  0.5  0.5  0    X
  0.5  0.75 0.25 W

  0.5  0.75 0.25 W
  0    0    0    Γ
```

* The first line is a comment line.
* Specify the number of points per line segment on the second line.
* The line mode activates when the first nonblank character on the third line is an *L* or *l* (for *line mode*)
* The fourth line defines the coordinate system. Use Cartesian (*C*, *c*, *K*, or *k*) or fractional (any other character) coordinates.
* Afterwards, any pair of lines define one path through the Brillouin zone. The empty lines and the label of the high-symmetry points are not required but simplify understanding the KPOINTS file. py4vasp uses the labels for the band structure plots.

The generated **k**-point mesh depends on the selected coordinate system.
VASP produces equidistant **k** points for each segment such that the total of points including the endpoints equals the required number.
Specifically for the template above, 40 points from $\Gamma$ to X, 40 points from X to W, and 40 points from W to $\Gamma$.
Because the endpoints are included every time, this generates two X and W points.

Transforming the same template to Cartesian coordinates produces

```
k points along high symmetry lines
 40              ! number of points per line
line mode
Cartesian
  0   0   0   Γ
  0   0   1   X

  0   0   1   X
  0.5 0   1   W

  0.5 0   1   W
  0   0   1   Γ
```

External tools are useful to decide which paths in the Brillouin zone to include.
The tools provide the coordinates and the labels for a given structure.
Because these paths depend on the symmetry, take special care that the analysis is not tainted by finite precision or rounding.
Also, keep in mind that the primitive and the conventional unit cell have different reciprocal coordinate systems.

Here is an example of a hexagonal structure

```
k-points along high symmetry lines for hexagonal structure
 40
line
reciprocal
0.000    0.000    0.500  A
0.000    0.000    0.000  Gamma

0.000    0.000    0.000  Gamma 
0.500    0.000    0.000  M

0.500    0.000    0.000  M
0.333333 0.333333 0.000  K 

0.333333 0.333333 0.000  K
0.000    0.000    0.000  Gamma
```

> **Mind:** The primary use of this particular mode of **k**-point generation is the calculation of DFT band structures. Because the mesh does not yield a good electronic density, it should only be used on a converged density. Therefore, run a calculation using a regular **k**-point mesh first. Freeze this density by setting ICHARG = 11 and run a non-self-consistent calculation with the line-mode **k**-point mesh afterward.
>
> As of VASP.6.3, the KPOINTS\_OPT file runs these two steps in a single calculation. It uses the same format and its presence triggers the postprocessing step. Use it for band-structure calculations with hybrid functionals to avoid the more cumbersome manual specification.

## Automatic **k**-point mesh

> **Deprecated:** The KSPACING tag provides almost the same functionality. Preferably use that method instead.

The following KPOINTS file generates a regular $\Gamma$-centered **k**-point.
The subdivisions $N\_1$, $N\_2$, and $N\_3$ are along the reciprocal lattice vectors $\mathbf b\_1$, $\mathbf b\_2$, and $\mathbf b\_3$, respectively.

```
Fully automatic mesh
0              ! 0 -> automatic generation scheme 
Auto           ! fully automatic
  10           ! length (R_k)
```

* The first line is a comment line.
* Automatically determine the number of **k** points by setting '0' on the second line.
* The first nonblank character in the third line is *A* or *a* activating the fully-automatic mode.
* The fourth line defines a length ($R\_k$) that determines the subdivisions $N\_1$, $N\_2$, and $N\_3$.

For every lattice vector $\mathbf b\_i$ the number of subdivisions is calculated as

:   :   $$N\_i = \text{int}\left(\max(1, R\_k |{\mathbf b}\_i| + 0.5)\right)~.$$

Note that this similar to the KSPACING tag, when the length $R\_k = 2\pi/\text{KSPACING}$.
The generated mesh is centered at $\Gamma$

:   :   $${\mathbf k} = \sum\_{i=1}^3 {\mathbf b}\_i \frac{n\_i}{N\_i} \qquad \forall n\_i \in [0, N\_i[$$

Useful values for the length vary between $R\_k = 10$ (large gap insulators) and $R\_k = 100$ (*d* metals).
Please verify that changes to $R\_k$ do not affect the quantity of interest.
For production calculations, preferably specify the mesh dimensions explicitly to avoid discontinuities between different cell sizes.

## Related tags and sections

KSPACING, KPOINTS\_OPT, IBZKPT, Number of k points and method for smearing

## References
