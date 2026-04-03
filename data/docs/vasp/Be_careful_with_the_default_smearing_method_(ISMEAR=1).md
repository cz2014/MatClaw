# Be careful with the default smearing method (ISMEAR=1)

Categories: Common Pitfalls

The default for ISMEAR is 1 in VASP. This setting is not appropriate for
insulators and semiconductors, and can results in one-electron occupancies that
are larger than 1 (2 for non spinpolarized) systems, and conversely
some states being occupied by less than 1 electron close to the Fermi-level.
It is strongly recommended to set ISMEAR=0 in the INCAR file
and use a small width SIGMA=0.05 (do not make SIGMA too small,
values below 0.001 can also lead to undesirable symmetry breaking).

Read more on this in Number of k points and method for smearing!

---
