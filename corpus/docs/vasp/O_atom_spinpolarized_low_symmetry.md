# O atom spinpolarized low symmetry

Categories: Examples

Overview > O atom > O atom spinpolarized > O atom spinpolarized low symmetry > O dimer > CO > CO vibration > CO partial DOS > H2O >
H2O vibration > H2O molecular dynamics > Further things to try  > List of tutorials

## Task

Performing a spin-polarized low symmetry calculation of a single oxygen atom in a non cubic box to get the right energy minimum.

## Input

### POSCAR

```
O atom in a box
 1.0          ! universal scaling parameters
 7.0 0.0 0.0  ! lattice vector  a(1)
 0.0 7.5 0.0  ! lattice vector  a(2)
 0.0 0.0 8.0  ! lattice vector  a(3)
1             ! number of atoms
cart          ! positions in cartesian coordinates
 0 0 0
```

### INCAR

```
SYSTEM = O atom in a box
ISMEAR = 0  ! Gaussian smearing
SIGMA  = 0.01
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

* In the GGA most atoms are characterized by a symmetry broken solution. VASP, however, symmetrizes the charge density according to the determined symmetry of the cell. Check the OUTCAR file, to see what symmetry VASP is using.

* To lower the symmetry, simply change the lattice parameters to 7.0, 7.5 and 8.0 in the POSCAR file (see the example file above) and reduce SIGMA to SIGMA=0.01 in the INCAR file.

* By rerunning VASP one finds a much lower energy:

```
vasp.5.4.1 05Feb16 (build Aug 22 2016 16:46:23) complex
...   ...   . ..
DAV:  15    -0.189071145737E+01   -0.29321E-03   -0.39183E-05    48   0.478E-02    0.995E-03
DAV:  16    -0.189071145737E+01   -0.27775E-03   -0.39294E-05    40   0.290E-02    0.541E-03
DAV:  17    -0.189104076616E+01   -0.51555E-04   -0.34087E-06    48   0.132E-02    
   1 F= -.18910408E+01 E0= -.18910408E+01  d E =-.309633E-20  mag=     1.9998
```

## Further things to try

* How does the energy change when one decreases SIGMA to SIGMA=0.01 in the INCAR file? Why?

## Download

Oatomspinlowsym.tgz

Overview > O atom > O atom spinpolarized > O atom spinpolarized low symmetry > O dimer > CO > CO vibration > CO partial DOS > H2O >
H2O vibration > H2O molecular dynamics > Further things to try  > List of tutorials
