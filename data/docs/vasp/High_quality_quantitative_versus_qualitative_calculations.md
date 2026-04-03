# High quality quantitative versus qualitative calculations

Categories: Common Pitfalls

Before going into further details, we want to distinguish between "high quality quantitative" (PREC should be *high*) and "qualitative" calculations (PREC can be *medium* or even *low*).

A "high quality quantitative" calculation is necessary if very small energy differences (less than 10 meV) between two competing "phases", which can not be described with the "same supercell", have to be calculated.

The term "same supercell" corresponds here to cells containing the same number of atoms and no dramatic changes in the cell-geometry (i.e. lattice vectors should be almost the same for both cells). For the calculation of energy-differences between two competing bulk-phases it is in many cases impossible to find a supercell, which meets this criterion. If one wants to calculate small energy-differences it is necessary to converge with respect to all parameters (k-points, FFT meshes, and sometimes energy cutoff). In most cases these three parameters are independent, so that convergence can be checked independently.

For surfaces, things are quite complicated. The calculation of the surface energy is clearly a "high quality quantitative" calculation. In this case you have to subtract from the energy of the slab the energy of the bulk phase. Both energies must be calculated with high accuracy. If the slab contains 20 atoms, an error of 5 meV per bulk atom will result in an error of 100 meV per surface atom. The situation is not as bad if one is interested in the adsorption energy of molecules. In this case accurate results (with errors of a few meV) can be obtained with PREC=*med*, if the reference energy of the slab, and the reference energy of the adsorbate are calculated in the same supercell as that one used to describe adsorbate and slab together.

Ab initio molecular dynamics clearly do not fall into the "high quality quantitative" category because the cell shape and the number of atoms remains constant during the calculation, and most ab initio MD's can be done with PREC=*Low*. We will give some exception to this general rule when the influence of the k-point mesh is discussed.

---
