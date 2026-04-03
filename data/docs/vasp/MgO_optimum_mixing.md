# MgO optimum mixing

Categories: Examples

Overview > bandgap of Si using different DFT+HF methods > MgO optimum mixing > fcc Ni DOS with hybrid functional > Si bandstructure  > List of tutorials

## Task

Find optimum HSE mixing parameter for MgO.

## Input

### POSCAR

```
MgO
-18.79350000000000000000
0.5 0.5 0.0
0.0 0.5 0.5
0.5 0.0 0.5
1 1
cart
0.00 0.00 0.00
0.50 0.0 0.0
```

### INCAR

```
##############################################
## Optimum HSE mixing parameter (AEXX) for MgO
## Expt gap = 7.8 eV
## fit gap wrt. 0<AEXX<1
## Compute the bandgap using different value of AEXX 
## in the range (0,1) and find the value which leads 
## to the best agreement with the experimental gap. 
## hint: the gap grows lineraly with AEXX
## Better preconverge with PBE first!
##############################################
    
## Selects the HSE06 hybrid functional
#LHFCALC = .TRUE. ; HFSCREEN = 0.2 ; AEXX=0.25  
#ALGO = D ; TIME = 0.4 
     
## Leave this in
ISMEAR =  0
SIGMA  =  0.01
GGA    = PE
```

### KPOINTS

```
k-points
0
Gamma
  4  4  4
  0  0  0
```

## Calculation

* script to extract G-eigenvalues and calculate the bandgap

```
grep "      4     " OUTCAR | head -8 | \
awk 'BEGIN{i=1}{a[i]=$2 ; i=2} END{for (j=1;j<i;j++) print j,a[j]}' > vband.dat
grep "      5     " OUTCAR | head -8 | \
awk 'BEGIN{i=1}{a[i]=$2 ; i=2} END{for (j=1;j<i;j++) print j,a[j]}' > cband.dat
```

The bandgap is obainted by substracting the eigenvalues written in cband.dat (conduction band
minimum at Gamma) and vband.dat (valence band maximum at Gamma)

## Download

5\_2\_MgO\_mixing.tgz

Overview > bandgap of Si using different DFT+HF methods > MgO optimum mixing > fcc Ni DOS with hybrid functional > Si bandstructure  > List of tutorials
