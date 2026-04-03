# Number of k points and method for smearing

Categories: Common Pitfalls

Please read and understand K-point integration before reading this section.

The number of k points needed for a calculation depends critically
on the necessary precision and on whether the system is metallic.
Metallic systems require an order of magnitude more k points than
semiconducting and insulating systems.
The number of k points also depends on the smearing method in
use; not all methods converge with similar speed. In addition, the error
is not transferable at all i.e. a $9\times 9\times 9$ leads
to a completely different error for fcc, bcc, and sc. Therefore
absolute convergence with respect to the number of k points
is necessary. The only exception is commensurable super cells.
If it is possible to use the same super cell for two calculations
it is definitely a good idea to use the same k point set for both calculations.
Finally, we note that the k point mesh and smearing are closely connected.

We repeat here the guidelines for ISMEAR:

* For semiconductors or insulators always use the tetrahedron method (ISMEAR=-5), if the cell is too large to use tetrahedron method use ISMEAR=0.
* For relaxations in metals always use ISMEAR=1 and an appropriate SIGMA value (so that the entropy term is less than 1 meV per atom). **Mind**: Avoid using ISMEAR>0 for semiconductors and insulators, it might result in problems.
* For the DOS and very accurate total energy calculations (no relaxation in metals) use the tetrahedron method (ISMEAR=-5).

Once again, if possible we recommend using the tetrahedron method
with Blöchl corrections (ISMEAR=-5),
this method is foolproof and does not require any empirical parameters
like the other methods.
Especially for bulk materials, we were able to get highly accurate
results using this
method.

Even with this scheme, the number of k points remains relatively
large. For insulators, 100 k points/per atom in the full Brillouin zone
are generally sufficient
to reduce the energy error to less than 10 meV.
Metals require approximately 1000 k points/per atom for the same accuracy.
For problematic cases (transition metals with a steep DOS at the
Fermi level) it might be necessary to increase the number of
k points up to 5000/per atom, which usually reduces the error
to less than 1 meV per atom.

**Mind**: The number of k points in the irreducible part of the Brillouin
zone (IRBZ) might be much smaller. For fcc/bcc and sc a
$11\times 11\times 11$ mesh containing 1331 k-points is
reduced to 56 k-points in the
IRBZ. This is a relatively modest value compared with the values
used in conjunction with LMTO packages using the linear tetrahedron method.

Not in all cases, it is possible to use the tetrahedron method, for
instance, if the number of k-points falls below 3,
or if accurate forces are required. In this case,
use the method of Methfessel-Paxton with N=1 for metals and N=0 for semiconductors. SIGMA should be as large as possible,
but the difference between the free energy and the total energy,
i.e. the term

```
entropy T*S
```

in the OUTCAR file must be small (i.e. < 1-2 meV/per atom).
In this case the free energy and the energy one is really interested in $E(\sigma \to 0)$
are almost the same. The forces are also consistent with $E(\sigma \to 0)$.

**Mind**: A good check whether the entropy term causes any problems
is to compare the entropy term for different
situations. The entropy must be the same for all situations.
One has a problem if the entropy is 100 meV per atom
at the surface but 10 meV per atom for the bulk.

## Comparing different k-point meshes

It is necessary to be careful comparing different k-point meshes.
Not always does the number of k points in the IRBZ increase continuously
with the mesh size. This is for instance the case for fcc,
where even grids centered not at the $\Gamma$ point
(e.g. Monkhorst Pack $8\times 8\times 8 \to 60$) result in a larger
number of k points than odd divisions (e.g. $9\times 9\times 9 \to 35$).
In fact, the difference can be traced back to whether or whether not
the $\Gamma$ point is included in the resulting k-point mesh.
Meshes centered at $\Gamma$ (option *G* in the KPOINTS file or odd divisions,
see also Automatic k-mesh generation) behave different than meshes
without $\Gamma$ (option *M* in the KPOINTS file and even divisions).
The precision of the mesh is usually directly proportional to the number
of k points in the IRBZ, but not to the number of divisions.
Some ambiguities can be avoided if even meshes (not centered at $\Gamma$)
are not compared
with odd meshes (meshes centered at $\Gamma$).

## Some other considerations

It is recommended to use even meshes (e.g. $8\times 8\times 8$) for
up to $n=8$. From there on odd meshes are more efficient (e.g. $11\times 11\times 11$).
However, we have already stressed that the number of divisions is often
totally unrelated to the total number of k points and to the
precision of the grid.
Therefore a $8\times 8\times 8$ might be more accurate then a
$9\times 9\times 9$ grid. For fcc a $8\times 8\times 8$ grid is
approximately as precise as a $8\times 8\times 8$ mesh.
Finally,
for hexagonal cells, the mesh should be shifted so that the $\Gamma$ point
is always included i.e. the KPOINTS file

```
automatic mesh 
0
Gamma
  8   8   8   
  0.  0.  0.
```

is much more efficient than a KPOINTS  file with
*Gamma* replaced by *Monkhorst* (see also Automatic k-mesh generation).

---
