# Constraining local magnetic moments

Categories: Examples

Overview > fcc Ni (revisited) > NiO > NiO LSDA+U > Spin-orbit coupling in a Ni monolayer > Spin-orbit coupling in a Fe monolayer >constraining local magnetic moments   > List of tutorials

## Task

Constraining the local magnetic moments on an Fe dimer.

## Input

### POSCAR

```
Fe dimer                               
 1.00000000000000000
     8.0000000000000000    0.0000000000000000    0.0000000000000000
     0.0000000000000000    8.0000000000000000    0.0000000000000000
     0.0000000000000000    0.0000000000000000    8.0000000000000000
   2
Cartesian
 3.00  0.00  0.00
 5.00  0.00  0.00
```

### INCAR

```
SYSTEM        = Fe dimer
ISTART        = 0
ISYM          = 0
LNONCOLLINEAR = .TRUE.
MAGMOM        = 0 0 3   0 0 3
VOSKOWN       = 1
LORBIT        = 11
  
! mix slowly when increasing LAMBDA 
# AMIX          = 0.1
# BMIX          = 0.00001
# AMIX_MAG      = 0.2
# BMIX_MAG      = 0.00001
  
# I_CONSTRAINED_M = 1
# RWIGS           = 1.0
# LAMBDA         = 10
# M_CONSTR        = 0 0 1  0 0 1
```

* Symmetry is switched off (ISYM=0).
* Initially moments for ferromagnetic calculation are initialized.

### KPOINTS

```
k-points
0
Monkhorst Pack
  1   1   1
  0.  0.  0.
```

* A single k point in the calculation is sufficient.

## Calculation

* By using the initial ferromagnetic initialization of MAGMOM = 0 0 3 0 0 3 we get the following magnetic moments in the OSZICAR file:

```
...
DAV:  20    -0.929676054634E+01   -0.26101E-03   -0.16780E-03    60   0.102E-01    0.537E-02
DAV:  21    -0.929679955346E+01   -0.39007E-04   -0.30319E-04    60   0.590E-02
   1 F= -.92967996E+01 E0= -.93047629E+01  d E =0.238900E-01  mag= -0.0006 -0.0003  6.0537
```

* By using a different initial magnetization of MAGMOM = 0 0 3 0 2 2 the system converges to a ferromagnetic solution:

```
 magnetization (y)                          magnetization (z)
# of ion     s       p       d       tot   # of ion     s       p       d       tot
----------------------------------------   ----------------------------------------
  1        0.018  -0.001   1.071   1.087     1        0.045  -0.003   2.587   2.628
  2        0.019  -0.001   1.069   1.087     2        0.045  -0.003   2.588   2.629
----------------------------------------   ----------------------------------------
tot        0.037  -0.003   2.140   2.174   tot        0.089  -0.007   5.175   5.257
```

* A penalty functional is added to the system, driving the integrated local moments into the desired directions, when the following steps are modified in the input (beware the penalty functional contributes to the total energy):
  + Switching on constraints on magnetic moments (I\_CONSTRAINED\_M=1).
  + Setting integration radius to determine local moments (RWIGS=1.0).
  + Weight in penalty functional (LAMBDA=10).
  + Target directions for constraints on magnetic moments (M\_CONSTR= 0 0 1 0 1 1).

* The necessary information is found in the OSZICAR file:

```
 E_p =  0.35424E-02  lambda =  0.100E+02
 ion        MW_int                 M_int
  1  0.000  0.013  1.557    0.000  0.014  2.674
  2  0.000  1.092  1.110    0.000  1.880  1.901
DAV:  35    -0.905322335169E+01    0.58398E-04   -0.60872E-04    60   0.734E-02
   1 F= -.90532234E+01 E0= -.90355617E+01  d E =-.529849E-01  mag= -0.0005  2.1161  5.1088
```

* *E\_p* is the energy arising from the penalty function. It decreases with increasing LAMBDA.
* By increasing LAMBDA stepwise one can bring *E\_p* down (slowly so the solution remains stable from one run to another):

```
 E_p =  0.22591E-03  lambda =  0.500E+02
 ion        MW_int                 M_int
  1  0.000  0.002  1.545    0.001 -0.005  2.654
  2  0.000  1.086  1.087    0.001  1.871  1.862
DAV:  33    -0.907152551238E+01    0.48186E-04   -0.33125E-04    60   0.163E-01
   1 F= -.90715255E+01 E0= -.90541505E+01  d E =-.521251E-01  mag=  0.0042  2.0902  5.0659
```

* This way one approaches the LSDA total energy for a given magnetic configuration.

* What can one do when convergence is bad:
  + Start from charge density of non-spin-polarized calculation using ISTART=0 (or remove the WAVECAR file) and ICHARG=1.
  + Use linear mixing by setting BMIX=0.0001 and BMIX\_MAG=0.0001.
  + Mix slowly, i.e., reduce AMIX and AMIX\_MAG.
  + REDUCE MAXMIX, the number of steps stored in the Broyden mixer (default MAXMIX=45).
  + Restart from partially converged results (stop a calculation after say 20 steps and restart from the WAVECAR file).
  + Use constraints to stabilize the magnetic configuration.
  + Pray.

## Download

4\_5\_Fe\_dimer.tgz

Overview > fcc Ni (revisited) > NiO > NiO LSDA+U > Spin-orbit coupling in a Ni monolayer > Spin-orbit coupling in a Fe monolayer >constraining local magnetic moments   > List of tutorials

Back to the main page.
