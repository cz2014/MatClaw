# NiO

Categories: Examples

Overview > fcc Ni (revisited) > NiO > NiO LSDA+U > Spin-orbit coupling in a Ni monolayer > Spin-orbit coupling in a Fe monolayer >constraining local magnetic moments   > List of tutorials

## Task

Calculation of NiO, an antiferromagnet.

## Input

### POSCAR

```
AFM  NiO
 4.17
 1.0 0.5 0.5
 0.5 1.0 0.5
 0.5 0.5 1.0
 2 2
Cartesian
 0.0 0.0 0.0
 1.0 1.0 1.0
 0.5 0.5 0.5
 1.5 1.5 1.5
```

* AFM coupling: 4 atoms in the basis (instead of 2).

### INCAR

```
SYSTEM = NiO    
 
ISTART = 0
 
ISPIN = 2
MAGMOM = 2.0 -2.0 2*0 
     
ENMAX = 250.0
EDIFF = 1E-3
    
ISMEAR = -5
    
AMIX = 0.2
BMIX = 0.00001
AMIX_MAG = 0.8
BMIX_MAG = 0.00001
    
LORBIT = 11
```

* Initial magnetic moments of 2μB (Ni) and 0μB (O).
* AMIX=0.2 and AMIX\_MAG=0.8 (default), BMIX and BMIX\_MAG practically zero, i.e. linear mixing.

### KPOINTS

```
k-points
 0
gamma
 4  4  4 
 0  0  0
```

## Calculation

* The total magnetic moment should be 0 in the OSZICAR file:

```
DAV:  13    -0.267936242334E+02    0.12794E-03   -0.12638E-04   552   0.298E-01    0.169E-02
DAV:  14    -0.267936352231E+02   -0.10990E-04   -0.21775E-05   520   0.107E-01
   1 F= -.26793635E+02 E0= -.26793635E+02  d E =0.000000E+00  mag=     0.0000
```

* The partial and integrated magnetic moments within the PAW spheres are given in the OUTCAR file:

```
 magnetization (x)
  
# of ion     s       p       d       tot
----------------------------------------
  1       -0.012  -0.014   1.245   1.219
  2        0.012   0.014  -1.242  -1.216
  3        0.000  -0.001   0.000  -0.001
  4        0.000  -0.001   0.000  -0.001
-----------------------------------------------
tot        0.000  -0.003   0.003   0.000
```

* The example total DOS and the partial l-decomposed DOS for the d orbitals of Ni should look like the following:

## Download

4\_2\_NiO.tgz

Overview > fcc Ni (revisited) > NiO > NiO LSDA+U > Spin-orbit coupling in a Ni monolayer > Spin-orbit coupling in a Fe monolayer >constraining local magnetic moments   > List of tutorials
