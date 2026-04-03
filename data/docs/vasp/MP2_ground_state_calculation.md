# MP2 ground state calculation - Tutorial

Categories: Many-body perturbation theory, MP2, Tutorials

Overview > MP2 > LTMP2 > stochastic LTMP2  > High energy contributions using stochastic LTMP2 > List of tutorials

This tutorial introduces how to calculate the ground state energy using second order Møller-Plesset perturbation theory (MP2) with VASP. Currently there are three implementations available:

* **MP2**: this implementation is recommended for very small unit cells, very few k-points and very low plane-wave cuttofs. The system size scaling of this algorithm is N⁵.
* **LTMP2**: for all larger systems this Laplace transformed MP2 (LTMP) implementation is recommended. Larger cutoffs and denser k-point meshes can be used. It possesses a lower system size scaling (N⁴) and a more efficient k-point sampling.
* **stochastic LTMP2**: even faster calculations at the price of statistical noise can be achieved with the stochastic MP2 algorithm. It is an optimal choice for very large systems where only relative errors per valence electron are relevant. Keeping the absolute error fixed, the algorithm exhibits a cubic scaling with the system size, N³, whereas for a fixed relative error, a linear scaling, N¹, can be achieved. Note that there is no k-point sampling and no spin polarization implemented for this algorithm.

**NOTE:** *If you use one of these algorithms, please cite the corresponding reference in your publication in addition to the standard VASP reference.*

Both LTMP2 as well as stochastic LTMP2 are high performance algorithms that can parallelize the MP2 calculation over thousands of CPUs.

At first, one should select the best algorithm according to the considered system size. In the following, a step by step instruction for each algorithm is presented.

## Preparation: the Hartree-Fock ground state

In order to calculate the Hartree-Fock ground state, use the following INCAR file

```
ISMEAR = 0 ; SIGMA = 0.01
ALGO = A
LHFCALC = .TRUE. ; AEXX = 1.0
EDIFF = 1E-6
ENCUT = # 10-20% larger than ENMAX in the POTCAR file
LORBITALREAL = .TRUE. # only necessary for LTMP2 and stochastic LTMP2
```

Keep the OUTCAR file to read-out the Hartree-Fock ground state energy later.

## Calculating the unoccupied Hartree-Fock orbitals

We also need the unoccupied/virtual Hartree-Fock orbitals to perform MP2 calculations. The number of necessary orbitals should be equal to the number of plane-waves, that can be found via

```
nplw=`awk '/number of plane-waves:/ {print $5} ' < OUTCAR_HARTREE_FOCK_GROUND_STATE
```

For the Gamma-only version of VASP, twice the number of plane-waves have to be used.

Set the INCAR file to

```
ISMEAR = 0 ; SIGMA = 0.01
ALGO = Exact
LHFCALC = .TRUE. ; AEXX = 1.0
NELM = 1
NBANDS = # number of plane-waves (favorably a multiple of the used mpi-ranks)
ENCUT = # same value as in the Hartree-Fock step
LORBITALREAL = .TRUE. # only necessary for LTMP2 and stochastic LTMP2
```

Make sure that VASP reads the WAVECAR file from the previous Hartree-Fock step.

## Actual MP2 calculations

Depending on your choice, please switch to the corresponding page.

1. MP2
2. LTMP2
3. stochastic LTMP2

## References

---
