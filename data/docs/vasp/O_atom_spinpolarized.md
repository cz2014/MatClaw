# O atom spinpolarized

Categories: Examples

Overview > O atom > O atom spinpolarized > O atom spinpolarized low symmetry > O dimer > CO > CO vibration > CO partial DOS > H2O >
H2O vibration > H2O molecular dynamics > Further things to try  > List of tutorials

## Task

Performing a spin polarized calculation for a single oxygen atom in a cubic box to get the correct magnetic moment of the atom.

## Input

### POSCAR

```
O atom in a box
 1.0          ! universal scaling parameters
 8.0 0.0 0.0  ! lattice vector  a(1)
 0.0 8.0 0.0  ! lattice vector  a(2)
 0.0 0.0 8.0  ! lattice vector  a(3)
1             ! number of atoms
cart          ! positions in cartesian coordinates
 0 0 0
```

### INCAR

```
SYSTEM = O atom in a box
ISMEAR = 0  ! Gaussian smearing
ISPIN =  2  ! spin polarized calculation
```

### KPOINTS

```
Gamma-point only
 0
Monkhorst Pack
 1 1 1
 0 0 0
```

## Calculation

* The O atom is an open shell system with 2 unpaired electrons.

* Starting from the previous chapter add ISPIN=2 to the INCAR file remove the WAVECAR file and restart VASP.

* The following example output is obtained (stdout):

```
running on    8 total cores
distrk:  each k-point on    8 cores,    1 groups
distr:  one band on    1 cores,    8 groups
using from now: INCAR     
vasp.5.4.1 05Feb16 (build Aug 22 2016 16:46:23) complex                        
POSCAR found :  1 types and       1 ions
scaLAPACK will be used
LDA part: xc-table for Pade appr. of Perdew
POSCAR, INCAR and KPOINTS ok, starting setup
WARNING: small aliasing (wrap around) errors must be expected
FFT: planning ...
WAVECAR not read
entering main loop
N       E                     dE             d eps       ncg     rms          rms(c)
DAV:   1     0.389725012498E+02    0.38973E+02   -0.10098E+03    32   0.259E+02
DAV:   2     0.317912429240E+01   -0.35793E+02   -0.35786E+02    64   0.438E+01
DAV:   3    -0.119085682530E+01   -0.43700E+01   -0.36686E+01    32   0.328E+01
DAV:   4    -0.126198272139E+01   -0.71126E-01   -0.69189E-01    32   0.508E+00
DAV:   5    -0.126284205021E+01   -0.85933E-03   -0.85925E-03    48   0.504E-01    0.653E+00
DAV:   6     0.164008071667E+00    0.14269E+01   -0.32208E+00    32   0.894E+00    0.151E+00
...    ...      ...                 
DAV:  13    -0.167302579657E+01   -0.25698E-03   -0.13177E-05    32   0.203E-02    0.956E-03
DAV:  14    -0.167302926747E+01   -0.34709E-05   -0.34771E-06    32   0.116E-02
1 F= -.16730293E+01 E0= -.15958981E+01  d E =-.154262E+00  mag=     1.9999
writing wavefunctions
E-fermi : -7.1152 XC(G=0): -0.7730 alpha+bet : -0.1463
```

* Eigenstates for spin up and spin down are calculated "separately". In LSDA they interact only via the effective local potential spin-up and spin-down potential.

* In the OUTCAR file one can see two spin components:

```
spin component 1
  
k-point     1 :       0.0000    0.0000    0.0000
 band No.  band energies     occupation
     1     -25.0878      1.00000
     2     -10.0830      1.00000
     3     -10.0830      1.00000
     4     -10.0830      1.00000
     5      -0.4932      0.00000
     6       1.8213      0.00000
     7       1.8303      0.00000
     8       1.8303      0.00000
```

```
spin component 2
  
k-point     1 :       0.0000    0.0000    0.0000
 band No.  band energies     occupation
     1     -21.8396      1.00000
     2      -7.0543      0.33333
     3      -7.0543      0.33333
     4      -7.0543      0.33333
     5      -0.3594      0.00000
     6       1.9830      0.00000
     7       1.9830      0.00000
     8       1.9830      0.00000
```

The spin component 1 has two more electrons corresponding to a magnetization of $2\mu\_{B}$.

## Download

Oatomspin.tgz

Overview > O atom > O atom spinpolarized > O atom spinpolarized low symmetry > O dimer > CO > CO vibration > CO partial DOS > H2O >
H2O vibration > H2O molecular dynamics > Further things to try  > List of tutorials
