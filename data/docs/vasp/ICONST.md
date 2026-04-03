# ICONST

Categories: Files, Input files, Symmetry, Molecular dynamics, Advanced molecular-dynamics sampling, Ensemble properties

In the ICONST file, geometric parameters are defined, which are then monitored or controlled in a molecular-dynamics simulation. For instance, the distance between two sites can be constrained or affected by the action of a bias potential. Finally, VASP writes the output to the REPORT file.

## Overview

Two kinds of geometric parameters can be defined:
primitive parameters (e.g., bond lengths or angles), and complex parameters (i.e., linear combinations of primitive coordinates). Each line defines one coordinate, and the complex coordinates must be defined after all primitive ones.
The syntax reads as follows:

```
flag item(1) ... item(N) status
...
...
flag  c_1  ...  c_M  status
```

where `flag` specifies the type of primitive coordinate, `item(1) ... item(N)` is a space-separated list of integers that, e.g., specifies the ions enumerated in the order they appear in the POSCAR file (starting at 1), and `status` is an integer that sets the status, e.g., constrained or monitored. Here, the first line defines the syntax of a primitive coordinates $q\_i$. Assuming that $M$ primitive coordinates were specified on the first $M$ lines of the ICONST file, the last line defines a complex coordinate, where `c_1 ... c_M` is a space-separated list of the coefficients $c\_i$ for the primitive coordinate defined in line $i$.

For instance, the following ICONST file defines two primitive coordinates and one complex coordinate.

```
R 1 6 0
R 1 5 0
S 1 -1 0
```

The first two lines define the bonds between atom $1$ and atom $6$, and between atom $1$ and $5$. The complex coordinate is the difference between the two bond lengths, which is defined on the third line.

## Settings for `flag`

### In case of primitive coordinates

* `flag` = R: interatomic distance between atoms `item(1)` and `item(2)`.
* `flag` = A: angle defined by atoms `item(1)`, `item(2)` and `item(3)` (with the atom `item(2)` being the apex).
* `flag` = T: torsional angle defined by atoms `item(1)`, `item(2)`, `item(3)` and `item(4)`.
* `flag` = M: distance between atom `item(1)` and the center of bond between atoms `item(2)` and `item(3)`.
* `flag` = B: distance between the center of bond between atoms `item(1)` and `item(2)` and the center of bond between atoms `item(3)` and `item(4)`
* `flag` = P: ratio of length of the bond between atoms `item(1)` and `item(2)` and the length of the bond between atoms `item(3)` and `item(4)`
* `flag` = W: function $\frac{1-\left(R/c\right)^M}{1-\left(R/c\right)^{N}}$ with $R$ being the bond length (in $\AA$) between the atoms `item(1)` and `item(2)`, $c$ is the reference bond length specified as `item(3)`, and the exponents $M$ and $N$ are defined as `item(4)` and `item(5)`, respectively.
* `flag` = X, Y, and Z: fractional (direct) coordinates linked with the lattice vectors $a$, $b$, and $c$.
* `flag` = cX, cY, and cZ: Cartesian coordinates $x$, $y$, and $z$.
* `flag` = LR: length of lattice vector `item(1)`
* `flag` = LA: angle between lattice vectors `item(1)` and `item(2)`
* `flag` = LV: cell volume (no `item(i)` is defined in this case)

### In case of complex coordinates

* `flag` = S: simple linear combination of primitive coordinates, i.e., $\left ( \xi=\sum\_{i=1}^{M} c\_i\,q\_i \right)$.
* `flag` = C: norm of the vector of primitive coordinates, which reads $\left( \xi=\sqrt{\sum\_{i=1}^{M} \,(c\_i\,q\_i)^2} \right)$.
* `flag` = D: coordination number, i.e., $\left( \xi=\sum\_{i=1}^{M} \frac{1-\left(q\_{i}/c\_{i}\right)^9}{1-\left(q\_{i}/c\_{i}\right)^{14}} \right)$.
* `flag` = IS: path-based coordinate measuring progress along discretized path represented by $N$ points $\tilde{q}(j)$ predefined in file IRCCAR, i.e., $\xi=\frac{1}{N-1}\frac{\sum\_{i=1}^{N}(i-1)\exp\left(-\sum\_{j=1}^{M}c\_{j}(q\_{j}-\tilde{q}\_{j}(i))^2 \right) }{\sum\_{i=1}^{N} \exp\left(-\sum\_{j=1}^{M}c\_{j}(q\_{j}-\tilde{q}\_{j}(i))^2 \right)}$
* `flag` = IZ: path-based coordinate measuring orthogonal distance from the path $\tilde{q}$ predefined in file IRCCAR, i.e., $\xi=-\frac{1}{c\_1} \log \sum\_{i=1}^{N}\exp\left(-\sum\_{j=1}^{M}c\_{j}(q-\tilde{q}(i))^2 \right)$ with

$N$ as defined above
The complex coordinates are functions defined in the space spanned by the primitive coordinates.

> **Mind:** All complex coordinates must be defined after the last primitive coordinate. Whenever complex coordinates are defined, the primitive coordinates are only the basis for their definition, and their status is ignored.

## Settings for `item(i)`

It depends on the setting of `flag`. In most cases, `item(i)` is an integer specifying either the position of the atom or the lattice vector in the POSCAR file. Mind that two atoms are needed to define a bond length, three atoms are required for a bonding angle, etc. In the special case of the flag `W`, also some additional parameters, i.e., the reference bond length (generally a floating-point number) and exponents used in the definition (integers) are defined via `item(i)`. See the description of the corresponding `flag`.

## Settings for `status`

* `status` = 0: the coordinate is constrained.
* `status` = 4: the coordinate is affected by a Fermi-type step function
* `status` = 5: the coordinate defines the collective variable in metadynamics
* `status` = 7: the coordinate is monitored. Optionally, set the upper and/or lower limits for the coordinates by means of the VALUE\_MAX and VALUE\_MIN tags, respectively.
* `status` = 8: the coordinate is affected by a harmonic potential

## Use cases and examples

### Define two constraints

The following constrains the bond lengths between atoms 1 and 5, and between atoms 1 and 6.

```
 R 1 5 0
 R 1 6 0
```

### Use complex coordinates

Consider, for instance, the ICONST file with the following lines:

```
R 1 6 0
R 1 5 0
S 1 -1 0
```

The first two lines define two primitive coordinates - bonds between the atoms $1$ and $6$, and between the atoms $1$ and $5$. The complex coordinate is the difference between the two bond lengths which is defined on the third line. Mind that whenever complex coordinates are defined, the primitives are used only as a basis for their definition. Consequently, the two primitive coordinates are not constrained in the simulation (despite `status`=0). Thus, the only controlled parameter is the complex coordinate. Therefore, to fix the first bond length and the complex coordinate at the same time, the ICONST file should be modified as follows:

```
R 1 6 0
R 1 5 0
S 1 -1 0
S 1 0 0
```

Consider the same system as discussed above and assume that the reference distance for the bond between atoms 1 and 6 is 1.1 $\AA$, while that for the bond between 1 and 5 is 1.5 $\AA$.
The coordination number can be fixed in two equivalent ways.
The first definition makes use of the complex type D, in which case the corresponding ICONST would be written like this:

```
R 1 6 0
R 1 5 0
D 1.1 1.5 0
```

In this case, the exponents appearing in numerator and denominator of the defining formula for D (see above) are fixed at the values 9 and 14, respectively. Alternatively, one can fix the same coordination number using the W primitive and S complex coordinates. This can be accomplished as follows:

```
W 1 6 1.1 9 14 0
W 1 5 1.5 9 14 0
S 1 1 0
```

The advantage of this format is that the coefficients M and N (see above the definition of W) can be set for each distance separately. Moreover, this format allows for an easy and intuitive definition of scaled sums of (and/or differences between) multiple coordination numbers - simply via a suitable choice of coefficients linked with S, which can be positive, negative, or zero.

### Restrictions on the volume and/or shape of the simulation cell

In the context of a molecular dynamics simulation in NpT ensemble, the ICONST file can be used to impose restrictions on the volume and/or shape of the simulation cell. The following examples cover some of the most important scenarios:

1.) Simulation with a constant cell volume and variable shape.

```
LV 0
```

2.) Variable lengths of lattice vectors but fixed lattice angles.

```
LA 1 2 0
LA 1 3 0
LA 2 3 0
```

3.) A cubic cell with variable volume but fixed shape. Note that the S type constraints involving the lengths of the lattice vectors ($a\_i - a\_j = 0$) are chosen so as to preserve ratios $a\_1:a\_2:a\_3=1:1:1$, as required by the cubic shape.

```
LA 1 2 0
LA 1 3 0
LA 2 3 0
LR 1 0
LR 2 0
LR 3 0
S  1  0  0  0  0  0 0
S  0  1  0  0  0  0 0
S  0  0  1  0  0  0 0
S  0  0  0  1 -1  0 0
S  0  0  0  1  0 -1 0
S  0  0  0  0  1 -1 0
```

4.) An orthorhombic cell with variable volume but fixed shape. Here, in order to fix ratios between the lengths of the lattice vectors ($a\_1:a\_2:a\_3$),
we define the constraints of the form $c\_i\*a\_i + c\_j\*a\_j = 0$. For instance, if the cell vectors are such that the relative proportions of their lengths are $a\_1:a\_2:a\_3=1:1.5:2$, the following ICONST can be used:

```
LA 1 2 0
LA 1 3 0
LA 2 3 0
LR 1 0
LR 2 0
LR 3 0
S  1  0  0  0      0    0 0
S  0  1  0  0      0    0 0
S  0  0  1  0      0    0 0
S  0  0  0  1.5 -1.0  0.0 0
S  0  0  0  2.0  0.0 -1.0 0
S  0  0  0  0.0  4.0 -3.0 0
```

> **Mind:** Note that ICONST can only be used in molecular dynamics simulations `IBRION = 0`.

## Related tags and articles

SHAKETOL,
SHAKEMAXITER,
MDALGO, REPORT

---
