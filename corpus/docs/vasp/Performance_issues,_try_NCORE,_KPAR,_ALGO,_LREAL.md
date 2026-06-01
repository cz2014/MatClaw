# Performance issues, try NCORE, KPAR, ALGO, LREAL

Categories: Common Pitfalls, Performance, Parallelization

Many user have difficulties to make good choices for various computational and technical parameters, resulting in suboptimal performance. Here is a very brief outline which tags can make a difference performance wise.

Nowadays computations are usually performed on multi-core machines. Two tags are relevant to optimize the performance on multi-core machines: KPAR and NCORE.

Using the tag KPAR, the k-points are distributed in a round-robin fashion onto
the compute cores. A group of *N*=(total number of cores/KPAR) cores jointly work on a group of **k**-points.
Within this group of *N* cores the usual parallelism over bands and/or plane wave coefficients can be used. KPAR is particularly efficient for small unit cells
and many k-points and it causes essentially no communication overhead. For small until cells and few atoms in the unit cell, one often achieves the best performance by setting

KPAR = total-number-of-cores.

NCORE determines how many cores share the work on an individual orbital. The current default is NCORE=1, meaning that one orbital is treated by one core.
NCORE=1 is the optimal setting only for small unit cells, and platforms with a small communication bandwidth. However, this mode requires a lot of memory for large systems, because the non-local projector functions must be stored on each core. In addition, substantial all-to-all communications are required to orthogonalize the bands.
On massively parallel systems and modern multi-core machines we, therefore, strongly recommend to set

```
NCORE = 2 up to number-of-cores-per-socket (or number-of-cores-per-node)
```

For large unit cells, this can improve the performance by up to a factor four compared to the default. Ideally, NCORE should be a factor of the number-of-cores-per-socket (or number-of-cores-per-node), since this reduces communication between the sockets or nodes. The best value NCORE depends somewhat on the number of atoms
in the unit cell. Values around 4 are usually ideal for 100 atoms in the unit cell. For very large unit cells (more than 400 atoms) values around 12-16 are often optimal. If you perform long and expensive simulations, please make your own tests.

For large unit cells (more than 50-100 atoms), it is usually expedient to use real space
projects LREAL and change to ALGO= Fast

```
ALGO  = Fast
LREAL = Auto
```

ALGO does not change the predicted energy, but uses a more efficient (but slightly less robust) algorithm for the optimization of the electronic degrees of freedom.
LREAL slightly changes the energy by up to 1 meV/atom, but can greatly improve the performance of VASP for large unit cells. Note, though that in order to calculate relative energies or adsorption energies on surface, one should stick to one and the same setting for
LREAL.

---
