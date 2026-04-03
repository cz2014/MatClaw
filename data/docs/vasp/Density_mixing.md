# Category:Density mixing

Categories: VASP, Electronic minimization

**Density mixing** refers to the way of updating, e.g., the charge density with each iteration step in a self-consistent calculation within density-functional theory (DFT). In the case of magnetism and metaGGAs, VASP can also consider the spin-magnetization density and kinetic-energy density. Selecting the optimal procedure enhances the convergence of the electronic minimization and avoids charge sloshing. In many cases, VASP automatically selects suitable values, and it is unnecessary to set the tags related to density mixing manually.

## Theory

In each iteration of a DFT calculation, we start from a given charge density $\rho\_{in}$ and obtain the corresponding Kohn-Sham (KS) Hamiltonian and its eigenstates, i.e., KS orbitals. From the occupied KS orbitals, we can compute a new charge density $\rho\_{out}$. Thus, conceptionally VASP solves a multidimensional fixed-point problem. To solve this problem, VASP uses nonlinear solvers that work with the input vector $\rho\_{in}$ and the residual $R = \rho\_{out} - \rho\_{in}$. The optimal solution is obtained within the subspace spanned by the input vectors. The most efficient density-mixing schemes are the Broyden and the Pulay mixing (IMIX=4). In the Broyden mixing, an approximate of the Jacobian matrix is iteratively improved to find the optimal solution. In the Pulay mixing, the input vectors are combined assuming linearity to minimize the residual.

The implementation in VASP is based on the work of Johnson. Kresse and Furthmüller extended on it and demonstrated that the Broyden and Pulay schemes transform into each other for certain choices of weights for the previous iterations. They also introduced an efficient metric putting additional weight on the long-range components of the density (small $\mathbf G$ vectors), resulting in a more robust convergence. Furthermore, VASP uses a Kerker preconditioning to improve the choice of the input density for the next iteration.

## How to

### Improve the convergence

For most simple DFT calculations, the default choice of the convergence parameters is well suited to converge the calculation. As a first step, we suggest visualizing your structure or examining the output for warnings to check for very close atoms. That can happen during a structure relaxation if VASP performs a large ionic step. If the structure is correct, we recommend increasing the number of steps NELM and only if that doesn't work starting to tweak the parameters AMIX or BMIX; preferably the latter.

### Magnetic calculations

For magnetic materials, the charge density and the spin-magnetization density need to converge.

Hence, if you have problems to converge to a desired magnetic solution, try to calculate first the non-magnetic groundstate, and continue from the generated WAVECAR and CHGCAR file. For the continuation job, you need to set

```
ISPIN = 2
ICHARG = 1
```

in the INCAR file.

### MetaGGAs

For the density mixing schemes to work reliably, the charge density mixer must know all quantities that affect the total energy during the self-consistency cycle. For a standard DFT functional, this is solely the charge density. In the case of meta-GGAs, however, the total energy depends on the kinetic-energy density.

In many cases, the density-mixing scheme works well enough without passing the kinetic-energy density through the mixer, which is why LMIXTAU=.FALSE., per default. However, when the self-consistency cycle fails to converge for one of the algorithms exploiting density mixing, e.g., IALGO=38 or 48, one may set LMIXTAU=.TRUE. to have VASP pass the kinetic-energy density through the mixer as well.
It sometimes helps to cure convergence problems in the self-consistency cycle.

## References
