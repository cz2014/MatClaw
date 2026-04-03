# Ionic contributions to the frequency dependent dielectric function of NaCl

Categories: Examples

Overview > dielectric properties of SiC > dielectric properties of Si  > Ionic contributions to the frequency dependent dielectric function of NaCl  > List of tutorials

## Task

Calculation of the ionic contruibutions to the frequency dependent dielectric function of NaCl.

## Calculation

To get the full (electronic & ionic) frequency dependent dielectric function you will have to compute them separately.

Step 1. Do a standard DFT calculation

Step 2. Calculate the *electronic* contributions to the frequency dependent dielectric function.

Step 3. Calculate the *ionic* contributions to the frequency dependent dielectric function.

Step 4. Add the two dielectric functions together:

$\varepsilon(\omega)=\varepsilon\_{\rm elec}(\omega)+\varepsilon\_{\rm ion}(\omega)$

This approach can be used for semi-conductors and insulators, not for metals.

## Input

### POSCAR

```
NaCl FCC                               
  5.55596202    
    0.5000000000000000    0.5000000000000000    0.0000000000000000
    0.0000000000000000    0.5000000000000000    0.5000000000000000
    0.5000000000000000    0.0000000000000000    0.5000000000000000
  Na   Cl
    1     1
Direct
 0.0000000000000000  0.0000000000000000  0.0000000000000000
 0.5000000000000000  0.5000000000000000  0.5000000000000000
```

### KPOINTS

A smaller 4x4x4 or 8x8x8 would also suffice in case you are running interactively on one core.

```
Gamma-centred 11x11x11 Monkhorst-Pack grid
 0 
G
11 11 11
0 0 0
```

### INCAR

* INCAR file for the static calculation:

```
PREC = High
ISMEAR = 0 ; SIGMA = 0.01
EDIFF = 1.E-8
GGA = PS
```

* INCAR electronic contributions to the frequency dependent dielectric function

(see other tutorials for more advanced options: Dielectric\_properties\_of\_SiC. The same procedures for the electronic contributions apply to this example.)

```
PREC = High
ISMEAR = 0 ; SIGMA = 0.01
EDIFF = 1.E-8
GGA = PS
ALGO = Exact
LOPTICS = .TRUE.
```

* INCAR ionic contributions to the frequency dependent dielectric function:

```
PREC = High
ISMEAR = 0 ; SIGMA = 0.01
EDIFF = 1.E-8
GGA = PS
EDIFF = 1.E-8
#The ionic dielectric function can be calculated in two ways:################
#1# DFPT (faster), but does not allow for METAGGA use. ######################
IBRION = 8; LEPSILON=.TRUE.
#2# Finite differences (slower). ############################################
#IBRION = 6; LPEAD=.TRUE; LCALCEPS=.TRUE.
#NFREE = 2 ; POTIM = 0.015
#In both 1 and 2 the calculated dielectric function is in vasprun.xml #######
```

## Results

Download all necessary files and run doall.sh. An Awk script ("extract\_diel\_vasprun") is used to extract the dielectric function from the vasprun.xml file and write it into a easy to plot two-column format. If everything goes well you will obtain two files ("diel.electron.dat" and "diel.ion.dat"). The two dielectric functions have been plotted in the following figure:

*Note that the units on the frequency axes are different, eV and 2$\pi$THz!* The high frequency 'ion-clamped' dielectric constant ($\varepsilon\_{\infty}$) was obtained with the LOPTICS calculation. The static field ($\omega=0$) contribution of the ionic lattice to the dielectric constant ( $\varepsilon\_{\rm ion}$) can be calculated by DFPT or by the finite-difference method. In both cases the phonon frequencies (ie. eigenvalues of the dynamical matrix) and the Born effective charges are calculated and written to the OUTCAR file:

```
BORN EFFECTIVE CHARGES (including local field effects) (in e, cummulative output)
---------------------------------------------------------------------------------
ion    1
   1     1.07157     0.00000     0.00000
   2     0.00000     1.07157    -0.00000
   3    -0.00000    -0.00000     1.07157
ion    2
   1    -1.07157    -0.00000    -0.00000
   2    -0.00000    -1.07157     0.00000
   3     0.00000     0.00000    -1.07157
```

```
Eigenvectors and eigenvalues of the dynamical matrix
----------------------------------------------------
  1 f  =    5.130373 THz   32.235082 2PiTHz  171.130804 cm-1    21.217523 meV
            X         Y         Z           dx          dy          dz
     0.000000  0.000000  0.000000     0.000000   -0.000000    0.779560
     2.777981  2.777981  2.777981     0.000000   -0.000000   -0.626328
  2 f  =    5.130373 THz    32.235082 2PiTHz  171.130804 cm-1    21.217523 meV
            X         Y         Z           dx          dy          dz
     0.000000  0.000000  0.000000    -0.697237   -0.348675    0.000000
     2.777981  2.777981  2.777981     0.560186    0.280139    0.000000
  3 f  =    5.130373 THz    32.235082 2PiTHz  171.130804 cm-1    21.217523 meV
            X         Y         Z           dx          dy          dz
     0.000000  0.000000  0.000000    -0.348675    0.697237    0.000000
     2.777981  2.777981  2.777981     0.280139   -0.560186    0.000000
```

We see that the Born charge on the Na and Cl ion have an opposite sign. If a phonon mode is 'dipole-active', meaning that the dipole moment of all ions involved in the mode changes in size during one period, it will appear in the frequency dependent dielectric function. This is the case here as we can see in the eigenvectors of the dynamical matrix.

The total static dielectric constant is then the sum of the two contributions: $\varepsilon\_{0}=\varepsilon\_{\infty}+\varepsilon\_{\rm ion}$

### Further study on the three imaginary phonon modes

Besides the three dipole-active modes, there are thee imaginary (f/i) phonon modes. Here these modes do not indicate that our structure is dynamically unstable. The finite plane-wave basisset that we have used can give slightly different answers for the total energy depending on where in the cell we place the center of mass of all ions combined.

```
   4 f/i=    0.005715 THz     0.035910 2PiTHz    0.190642 cm-1     0.023637 meV
            X         Y         Z           dx          dy          dz
     0.000000  0.000000  0.000000     0.366245    0.491651   -0.128181
     2.777981  2.777981  2.777981     0.455847    0.611934   -0.159541
  5 f/i=    0.005715 THz     0.035910 2PiTHz    0.190642 cm-1     0.023637 meV
            X         Y         Z           dx          dy          dz
     0.000000  0.000000  0.000000    -0.395455    0.176626   -0.452443
     2.777981  2.777981  2.777981    -0.492204    0.219838   -0.563134
  6 f/i=    0.005715 THz     0.035910 2PiTHz    0.190642 cm-1     0.023637 meV
            X         Y         Z           dx          dy          dz
     0.000000  0.000000  0.000000     0.319009   -0.345498   -0.413704
     2.777981  2.777981  2.777981     0.397055   -0.430024   -0.514918
```

* Are the vectors for the Na and Cl in modes 4, 5 and 6 parallel?

The two vectors do not have the same lenght. In this case that is the result of mass-weighting of the eigenvectors.

* Calculate $\sqrt{m\_{\rm Na}/m\_{\rm Cl}}$. The masses you can get by

```
grep POMASS POTCAR
```

* Is the calculated mass ratio similar as the ratio between the two displacement vectors? ($-0.128181/\sqrt{m\_{\rm Na}} =? -0.159541/\sqrt{m\_{\rm Cl}}$)

## Plotting

Use xmgrace or your other favourite plotting tool to plot the two collumn files (diel.electron.dat and diel.electron.dat):

```
xmgrace -nxy diel.electron.dat &
xmgrace -nxy diel.ion.dat
```

## References

## Download

NaCl\_dielectric.tgz

Overview > dielectric properties of SiC > dielectric properties of Si  > Ionic contributions to the frequency dependent dielectric function of NaCl  > List of tutorials
