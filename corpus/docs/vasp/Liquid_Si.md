# Liquid Si - Freezing

Categories: Examples

Overview >Liquid Si - Standard MD > Liquid Si - Freezing > Nucleophile Substitution CH3Cl - Standard MD > Nuclephile Substitution CH3Cl - mMD1 > Nuclephile Substitution CH3Cl - mMD2 > Nuclephile Substitution CH3Cl - mMD3 > Nuclephile Substitution CH3Cl - SG > Nuclephile Substitution CH3Cl - BM > List of tutorials

## Task

In this example, the goal is to simulate the freezing of liquid Si.

## Input

### POSCAR

```
Si
15.12409564534287297131
     0.5000000000000000    0.5000000000000000    0.0000000000000000
     0.0000000000000000    0.5000000000000000    0.5000000000000000
     0.5000000000000000    0.0000000000000000    0.5000000000000000
  48
Direct
  0.8550657259653851  0.3204575801875221  0.6180363868822553
  0.6045454476433229  0.0546379652195404  0.1629680405553871
  0.4803889256776521  0.2999635319377835  0.0131251454718051
  0.8413504226620471  0.7598095803296524  0.1917781560970181
  0.9754163118144437  0.6134171268457649  0.7421364242876367
... [43 more coordinate lines truncated] ...
```

### INCAR

```
SYSTEM =  Si
# electronic degrees                                                            
LREAL = A                      # real space projection
PREC  = Normal                 # chose Low only after tests
EDIFF = 1E-5                   # do not use default (too large drift)
ISMEAR = -1 ; SIGMA = 0.130    # Fermi smearing: 1500 K 0.086 10-3
ALGO = Very Fast               # recommended for MD (fall back ALGO = Fast)
MAXMIX = 40                    # reuse mixer from one MD step to next
ISYM = 0                       # no symmetry                                    
NELMIN = 4                     # minimum 4 steps per time step, avoid breaking after 2 steps
# MD (do little writing to save disc space)
IBRION = 0                     # main molecular dynamics tag
NSW = 400                      # number of MD steps
POTIM = 3                      # time step of MD
NWRITE = 0                     # controls output
NBLOCK = 10                    # after ten steps pair correlation function is written out
LCHARG = .FALSE.               # no charge density written out
LWAVE = .FALSE.                # no wave function coefficients written out
TEBEG = $i                     # starting temperature for MD
TEEND = $i                     # end temperature for MD
# canonic (Nosé) MD with XDATCAR updated every 10 steps
MDALGO = 2                     ä switch to select thermostat
SMASS =  3                     # Nosé mass
ISIF = 2                       # this tag selects the ensemble in combination with the thermostat
```

* Most of the tags here are very similar to the tags used in the previous example (Liquid Si - Standard MD).
* A stepwise cooling will be applied in this example via a script where $i for TEBEG and TEEND will be replaced in each calculation (see below).

### KPOINTS

```
Si-freezing
0 0 0
Gamma
 1 1 1
 0 0 0
```

* A single k-point is sufficient in this example.

## Calculation

We will execute the cooling stepwise so several calculations at different temperatures are required in this calculation. The INCAR is created with a script for each temperature and run separately. After each step the important files are saved to file.$i, where $i are the temperatures ranging from 2000 to 800 K in steps of 100 K. The script running the calculations looks like the following:

```
for i in 2000 1900 1800 1700 1600 1500 1400 1300 1200 1100 1000 900 800
do
cat >INCAR <<!
SYSTEM =  Si
# electronic degrees                                                            
LREAL = A                      # real space projection
PREC  = Normal                 # chose Low only after tests
EDIFF = 1E-5                   # do not use default (too large drift)
ISMEAR = -1 ; SIGMA = 0.130    # Fermi smearing: 1500 K 0.086 10-3
ALGO = Very Fast               # recommended for MD (fall back ALGO = Fast)
MAXMIX = 40                    # reuse mixer from one MD step to next
ISYM = 0                       # no symmetry                                    
NELMIN = 4                     # minimum 4 steps per time step, avoid breaking after 2 steps
# MD (do little writing to save disc space)
IBRION = 0                     # main molecular dynamics tag
NSW = 400                      # number of MD steps
POTIM = 3                      # time step of MD
NWRITE = 0                     # controls output
NBLOCK = 10                    # after ten steps pair correlation function is written out
LCHARG = .FALSE.               # no charge density written out
LWAVE = .FALSE.                # no wave function coefficients written out
TEBEG = $i                     # starting temperature for MD
TEEND = $i                     # end temperature for MD
# canonic (Nosé) MD with XDATCAR updated every 10 steps
MDALGO = 2                     # switch to select thermostat
SMASS =  3                     # Nosé mass
ISIF = 2                       # this tag selects the ensemble in combination with the thermostat
!
mpirun -np 2 /path/to/your/vasp/executable
cp XDATCAR XDATCAR.$i
cp OUTCAR OUTCAR.$i
cp PCDAT PCDAT.$i
cp CONTCAR CONTCAR.$i
cp POSCAR POSCAR.$i
cp OSZICAR OSZICAR.$i
cp CONTCAR POSCAR
done
```

* Before running the script one has to replace "'/path/to/your/vasp/executable'" by the path to his "'vasp\_gam'" executable. The script is then simply starte by typing the following command in the command line:

```
bash ./script
```

### Diffusion

The diffusion coefficient in 3 dimensions is given as

$D=\frac{\langle x^{2} \rangle} {6 t}$

where t defines time and $\langle x^{2} \rangle$. The 6 in the denominator contains a factor of 3 accounting for the 3 spatial dimensions (usually the diffusion coefficient is written with a 2 in the denominator in literature corresponding to only one dimension). In our case, we calculate the above equation as follows

$D=\frac{\langle \sum\_{i}^{N} [x\_{i}(t)-x\_{i}(0)]^{2} \rangle}{6 \Delta t}$.

Here the diffusion coefficient is calculated over an ensemble average to get better statistics. Our calculations were carried out for 1200 fs for each temperature. We will average in our case over the last 900 fs regarding the first 300 fs as equilibration of each temperature. The following python script (*diffusion\_coefficient.py*) calculates the diffusion coefficient at a given temperature:

**Click to show/*diffusion\_coefficient.py***

```
#!/usr/bin/python

import sys
import re
import math

#setting grid for histogram

potim = 3                               #timestep from INCAR file
readfile = open(sys.argv[1],"r")        #input XDATCAR file in format XDATCAR.TEMP
temp=re.sub("XDATCAR.",,sys.argv[1])  #extracts temperature from input file name
z=0                                     #counter
natoms=0                                #number of atoms in XDATCAR file
posion = []                             #atom positions in Cartesian coordinates
confcount = 0                           #number of structures in XDATCAR file
direct=[]                               #number of time steps for each structure in XDATCAR file
a=[]                                    #lattice parameter in 1st dimension
b=[]                                    #lattice parameter in 2nd dimension
c=[]                                    #lattice parameter in 3rd dimension
#read in XDATCAR file
line=readfile.readline()
while (line):
  z=z+1
  line.strip()
  line=re.sub('^',' ',line)
  y=line.split()
  if (z==2):
     scale=float(y[0])
  if (z==3):
     a.append(float(y[0]))
     a.append(float(y[1]))
     a.append(float(y[2]))
     a_len=(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])**0.5
  if (z==4):
     b.append(float(y[0]))
     b.append(float(y[1]))
     b.append(float(y[2]))
     b_len=(b[0]*b[0]+b[1]*b[1]+b[2]*b[2])**0.5
  if (z==5):
     c.append(float(y[0]))
     c.append(float(y[1]))
     c.append(float(y[2]))
     c_len=(c[0]*c[0]+c[1]*c[1]+c[2]*c[2])**0.5
  if (z==7):
     natoms=int(y[0])
  if (y[0]=="Direct"):
     direct.append(int(y[2]))
     posion.append([])
     for i in range(0,natoms):
        line=readfile.readline()
        line.strip()
        line=re.sub('^',' ',line)
        f=line.split()
        cartpos_x=a[0]*float(f[0])+a[1]*float(f[1])+a[2]*float(f[2])
        cartpos_y=b[0]*float(f[0])+b[1]*float(f[1])+b[2]*float(f[2])
        cartpos_z=c[0]*float(f[0])+c[1]*float(f[1])+c[2]*float(f[2])
        #positions of ions for each structure are obtained here
        posion[confcount].append([cartpos_x,cartpos_y,cartpos_z])
     confcount=confcount+1
  line=readfile.readline()
readfile.close

#calculate diffusion coefficient
#skip first 10 configurations corresponding to 300 fs
d=0.0
for i in range(10,confcount):
   for j in range(0,natoms):
      x_diff=posion[i][j][0]-posion[0][j][0]
      #if length is larger than 0.5 (in crystallographic coordinates) then we have to shift atom
      #due to periodic image to obtain the shortest distance.
      if (abs(x_diff)>(0.5*a_len)):
         if (x_diff<0):
            x_diff=x_diff+a_len
         elif (x_diff>0):
            x_diff=x_diff-a_len
      y_diff=posion[i][j][1]-posion[0][j][1]
      if (abs(y_diff)>(0.5*b_len)):
         if (y_diff<0):
            y_diff=y_diff+b_len
         elif (y_diff>0):
            y_diff=y_diff-b_len
      z_diff=posion[i][j][2]-posion[0][j][2]
      if (abs(z_diff)>(0.5*c_len)):
         if (z_diff<0):
            z_diff=z_diff+c_len
         elif (x_diff>0):
            z_diff=z_diff-c_len
      d=d+x_diff**2.0+y_diff**2.0+z_diff**2.0 

#print diffusion coefficient (in Ang^2/ps) vs temperature (in K)
d=d/(confcount-1-10)/natoms/6.0
time=(direct[confcount-1]-direct[10])*potim/10**3.0 #conversion to ps
print temp,d/time
```

Since the atoms can move such that the distance between old and new positions becomes larger than 0.5 (in crystallographic or fractional coordinates). Let us take for example the movement of atom 0 in the $x$ direction from 0 to -0.25, which would be output in the CONTCAR as 0.75. The distance corresponding to that would be then calculated as 0.75 which is wrong since we have periodic images and the real shortest distance would be 0.25. Hence all distances larger than 0.5 have to be shifted by -1.0. This is taken care of in the script.

We will use a short bash script (*dscript.sh*) to calculate the diffusion coefficient at different temperatures and plot them in a file (diff\_coeff.jpg):

```
#!/bin/bash

if test -f "diff_coeff.dat"; then
   rm diff_coeff.dat
fi

touch diff_coeff.dat

for i in 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000; do
   diffusion_coefficient.py XDATCAR.$i >>  diff_coeff.dat
done

gnuplot -e "set terminal jpeg; set key left; set xlabel 'temperature (K)'; set ylabel 'D (Ang^2/ps)'; set style data lines; plot 'diff_coeff.dat' " > diff_coeff.jpg
```

To execute it just type the following command:

```
bash ./dscript.sh
```

The data for the diffusion coefficient at each temperature is output to *diff\_coeff.dat* and plotted in *diff\_coeff.jpg* which should look like the following:

**Exercise**: Interpret Fig. 1 yourself!

**Click to show/Solution**

**Solution**:

For a given phase the diffusion coefficient depends directly on the temperature by

$D=\mu k\_{B} T$

where $k\_{B}$ is the Boltzmann constant and $\mu$ is the mobility of the particle. Evidently, this relation is approximately fulfilled in Fig. 1. At approximately 1400 K we see a peak. This temperature should correspond to the phase transition temperature.
Close to the phase transition point the scaling with respect to the reduced temperature $T\_{\mathrm{red}}$ becomes

$\langle x^{2} \rangle \propto T\_{\mathrm{red}}^{1-\alpha},\qquad \qquad \qquad T\_{\mathrm{red}}=\frac{T-T\_{c}}{T\_{c}}$

where $\alpha$ is an anomalous dimension (it may be positive or negative) and $T\_{c}$ is the critical temperature. For infinite large systems and infinite time, this would lead to a singularity in the plot, but since we are dealing with a finite-sized system it results in a finite peak at the phase transition point.

### Pair correlation function

The pair-correlation function provides information about the probability of finding two atoms at a given distance $r$.
The pair-correlation function is save for each temperature under *PCDAT.T*. The following script will plot the pair correlation functions at different temperatures in one figure:

```
#!/bin/bash

for i in 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000; do
   awk <PCDAT.$i >pair.$i ' NR==8 {pcskal=$1} NR==9 {pcfein=$1} NR>=10036 {line=line+1; print (line-0.5)*pcfein/pcskal,$1} '
done

gnuplot -e "set terminal jpeg; set key left; set xlabel 'r (Ang)'; set ylabel 'PCF'; set style data lines; plot 'pair.2000','pair.1400','pair.800' " > pair.jpg
```

To execute it type the following command:

```
bash ./pair.sh
```

The plot should look like the following:

**Exercise:** Interpret the figure yourself!

**Click to show/Solution**

**Solution**:

Crystalline structures usually have less diffuse pair correlation functions since the atoms are usually vibrating around high symmetry points. In liquids, the average positions are smeared out over a wider range of distances. With decreasing temperature, the pair correlation function in the plot gets more structured. This indicates that crystallization is happening.

## Download

Si\_Liquid\_Freezing.tgz

Overview >Liquid Si - Standard MD > Liquid Si - Freezing > Nucleophile Substitution CH3Cl - Standard MD > Nuclephile Substitution CH3Cl - mMD1 > Nuclephile Substitution CH3Cl - mMD2 > Nuclephile Substitution CH3Cl - mMD3 > Nuclephile Substitution CH3Cl - SG > Nuclephile Substitution CH3Cl - BM > List of tutorials
