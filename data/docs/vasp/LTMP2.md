# LTMP2 - Tutorial

Categories: Many-body perturbation theory, MP2, Tutorials

Overview > MP2 > LTMP2 > stochastic LTMP2  > High energy contributions using stochastic LTMP2 > List of tutorials

On this page, we explain how to perform a calculation using the **LTMP2** algorithm. Make sure you successfully completed the preparation steps Hartree-Fock ground state and Hartree-Fock virtuals.

**NOTE:** *If you use this algorithm, please cite reference in your publication in addition to the standard VASP reference.*

## The INCAR file

The LTMP2 calculation can simply be performed using the following INCAR file

```
ALGO = ACFDTRK 
LMP2LT = .TRUE.
NOMEGA = # number of tau points (see below)
NBANDS = # same value as in the Hartree-Fock unoccupied step ( = number of plane-waves)
ENCUT = # same value as in the Hartree-Fock step
LORBITALREAL = .TRUE.
PRECFOCK = Fast
KPAR = # parallelization (see below)
```

Make sure that VASP reads the WAVECAR file from the Hartree-Fock virtuals step. The setting for PRECFOCK is strongly recommended, since the code heavily relies on real space grid FFTs.

#### NOMEGA flag

The number of $\tau$-points is controlled by the NOMEGA flag. This is necessary to calculate the Laplace transformed energy denominator (see Ref for details),

$\frac{1}{\varepsilon\_i + \varepsilon\_j - \varepsilon\_a -\varepsilon\_b} = - \int\_0^\infty \textrm e^{-(\varepsilon\_i + \varepsilon\_j - \varepsilon\_a -\varepsilon\_b)\tau} \; \textrm d \tau \;.$

Usually it is sufficient to set NOMEGA=6. For materials with a small bandgap it is worth checking if the MP2 energy changes with increasing NOMEGA (e.g. 8 or 10). Note, that the MP2 energy diverges with 1/bandgap, independent of NOMEGA.

## Parallelization

The LTMP2 algorithm is a high-performance code and can easily be used on many CPUs. Both OpenMP and MPI is supported. We recommend to use MPI for parallelization since the code possesses an almost ideal parallelization efficiency. OpenMP should only be used to increase the shared memory, if necessary.

In order to activate the efficient MPI parallelization use the KPAR flag in the following way (note that the usual meaning of the KPAR flag becomes obsolete in the LTMP2 algorithm). KPAR specifies the number of plane-waves treated in parallel. Ideally, set KPAR to half of the used MPI ranks. If this results in memory issues, further decrease KPAR (such that KPAR is alway a divisor of the used MPI ranks) or increase the number of OpenMP threads.

#### Example for 512 CPUs

MPI ranks: 512   
OpenMP threads per rank: 1

```
KPAR = 256
```

To decrease the memory requirement you can alternatively set KPAR to 128 or 64 and so on. Or also try   
MPI ranks: 256   
OpenMP threads per rank: 2

```
KPAR = 128
```

## References

---
