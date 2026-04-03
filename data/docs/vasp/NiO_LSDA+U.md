# NiO LSDA+U

Categories: Examples

Overview > fcc Ni (revisited) > NiO > NiO LSDA+U > Spin-orbit coupling in a Ni monolayer > Spin-orbit coupling in a Fe monolayer >constraining local magnetic moments   > List of tutorials

## Task

Calculation of antiferromagnetic NiO in the DFT+U (Dudarev's approach).

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

### INCAR

```
SYSTEM   = NiO
    
ISTART   = 0
    
ISPIN    = 2
MAGMOM   = 2.0 -2.0 2*0
    
ENMAX    = 250.0
EDIFF    = 1E-3
    
ISMEAR   = -5
    
AMIX     = 0.2
BMIX     = 0.00001
AMIX_MAG = 0.8
BMIX_MAG = 0.00001
    
LORBIT   = 11
    
LDAU      = .TRUE.
LDAUTYPE  = 2
LDAUL     = 2 -1
LDAUU     = 8.00 0.00
LDAUJ     = 0.95 0.00
LDAUPRINT = 1
    
LMAXMIX   = 4          ! Important: mix paw occupancies up to L=4
```

* Switching on DFT+U using Dudarev's approach (LDAUTYPE=2).
* LDAUL selects the l quantum number for which on site interaction is added (-1 = no on site interaction).
* The U and J parameters have to be specified.
* Print occupation matrices in the OUTCAR file (LDAUPRINT=2.
* L, U, and J must be specified for all atomic types!

### KPOINTS

```
k-points
 0
gamma
 4  4  4 
 0  0  0
```

## Calculation

### On site occupancies

* The sample output for the on site occupancies in the OUTCAR file should look like the following (the meaning of the columns after the second equality sign is given below):

```
atom =    1  type =  1  1 = 2
  
  
 onsite density matrix
...
...
 occupancies and eigenvectors
  
  
o = 0.1696 v =  0.0000  0.0000  0.0000  0.0000  0.0000  0.0013 -0.0006 -0.9999 -0.0007 -0.0104
o = 0.1696 v =  0.0000  0.0000  0.0000  0.0000  0.0000  0.0000 -0.0011 -0.0104  0.0011  0.9999
o = 0.9770 v =  0.0000  0.0000  0.0000  0.0000  0.0000  0.7787 -0.1766  0.0015 -0.6020  0.0005
o = 0.9770 v =  0.0000  0.0000  0.0000  0.0000  0.0000  0.2456 -0.7972  0.0005  0.5516 -0.0015
o = 0.9770 v =  0.0000  0.0000  0.0000  0.0000  0.0000  0.5774  0.5774  0.0000  0.5774  0.0000
o = 0.9803 v = -0.0193  0.7166  0.0001 -0.6972 -0.0039  0.0000  0.0000  0.0000  0.0000  0.0000
o = 0.9803 v =  0.8163 -0.3914 -0.0039 -0.4249 -0.0001  0.0000  0.0000  0.0000  0.0000  0.0000
o = 0.9803 v =  0.5774  0.5774  0.0000  0.5774  0.0000  0.0000  0.0000  0.0000  0.0000  0.0000
o = 1.0248 v = -0.0032  0.0016 -1.0000  0.0016  0.0000  0.0000  0.0000  0.0000  0.0000  0.0000
o = 1.0248 v =  0.0000  0.0027  0.0000 -0.0027  1.0000  0.0000  0.0000  0.0000  0.0000  0.0000
```

$\qquad \qquad \qquad \qquad \qquad \qquad d\_{xy}^{\uparrow} \qquad d\_{yz}^{\uparrow} \qquad \quad d\_{z^{2}-r^{2}}^{\uparrow} \qquad d\_{xz}^{\uparrow} \qquad d\_{z^{2}-y^{2}}^{\uparrow} \qquad d\_{xy}^{\downarrow} \qquad \quad d\_{yz}^{\downarrow} \qquad \quad d\_{z^{2}-r^{2}}^{\downarrow} \qquad d\_{xz}^{\downarrow} \qquad d\_{z^{2}-y^{2}}^{\downarrow}$

* Just for comparison when U=0 and J=0 (i.e. just LSDA) the on site occupancies are as follows:

```
o = 0.3462 v =  0.0000  0.0000  0.0000  0.0000  0.0000 -0.0048  0.0028  0.9951  0.0020 -0.0986
o = 0.3462 v =  0.0000  0.0000  0.0000  0.0000  0.0000  0.0005  0.0039 -0.0986 -0.0044 -0.9951
o = 0.9491 v =  0.0000  0.0000  0.0000  0.0000  0.0000  0.5774  0.5774  0.0000  0.5774  0.0000
o = 0.9495 v =  0.0000  0.0000  0.0000  0.0000  0.0000 -0.0588  0.7347 -0.0004 -0.6759  0.0059
o = 0.9495 v =  0.0000  0.0000  0.0000  0.0000  0.0000  0.8144 -0.3563  0.0059 -0.4581  0.0004
o = 0.9527 v =  0.0477 -0.0256  0.9974 -0.0221 -0.0420  0.0000  0.0000  0.0000  0.0000  0.0000
o = 0.9527 v =  0.0020  0.0403  0.0420 -0.0423  0.9974  0.0000  0.0000  0.0000  0.0000  0.0000
o = 0.9598 v =  0.5774  0.5774  0.0000  0.5774  0.0000  0.0000  0.0000  0.0000  0.0000  0.0000
o = 0.9599 v = -0.1186  0.7577  0.0085 -0.6391 -0.0579  0.0000  0.0000  0.0000  0.0000  0.0000
o = 0.9599 v =  0.8064 -0.3005 -0.0570 -0.5059 -0.0085  0.0000  0.0000  0.0000  0.0000  0.0000
```

$\qquad \qquad \qquad \qquad \qquad \qquad d\_{xy}^{\uparrow} \qquad d\_{yz}^{\uparrow} \qquad \quad d\_{z^{2}-r^{2}}^{\uparrow} \qquad d\_{xz}^{\uparrow} \qquad d\_{z^{2}-y^{2}}^{\uparrow} \qquad d\_{xy}^{\downarrow} \qquad \quad d\_{yz}^{\downarrow} \qquad \quad d\_{z^{2}-r^{2}}^{\downarrow} \qquad d\_{xz}^{\downarrow} \qquad d\_{z^{2}-y^{2}}^{\downarrow}$

### Magnetic moments

* The sample output for the l dependent local magnetic moments is given in the OUTCAR file:

```
 magnetization (x)
  
  
# of ion     s       p       d       tot
----------------------------------------
  1       -0.003  -0.006   1.721   1.711
  2        0.003   0.006  -1.719  -1.710
  3        0.000  -0.001   0.000  -0.001
  4        0.000  -0.001   0.000  -0.001
------------------------------------------------
tot        0.000  -0.002   0.002   0.000
```

### DOS

* The Ni lm decomposed DOS for the d states should look like the following:

### Total energy

* The on site occupany matrix is not idempotent, hence the total energy contains a penalty contribution.
* The sample output for the total energy in the OSZICAR file should look like the following:

```
...
DAV:  15    -0.229633055256E+02   -0.11057E-03   -0.50020E-05   520   0.104E-01    0.118E-02
DAV:  16    -0.229633263321E+02   -0.20806E-04   -0.16650E-05   520   0.492E-02
   1 F= -.22963326E+02 E0= -.22963326E+02  d E =0.000000E+00  mag=     0.0000
```

* The sample output for a calculation using just LSDA is given below:

```
...
DAV:  13    -0.267936242334E+02    0.12794E-03   -0.12638E-04   552   0.298E-01    0.169E-02
DAV:  14    -0.267936352231E+02   -0.10990E-04   -0.21775E-05   520   0.107E-01
   1 F= -.26793635E+02 E0= -.26793635E+02  d E =0.000000E+00  mag=     0.0000
```

* The total energy for (U-J)>0 is always higher than for (U-J)=0.
* Comparing the total energies from calculations with different (U-J) is meaningless!

## Download

4\_3\_NiO\_LSDA+U.tgz

Overview > fcc Ni (revisited) > NiO > NiO LSDA+U > Spin-orbit coupling in a Ni monolayer > Spin-orbit coupling in a Fe monolayer >constraining local magnetic moments   > List of tutorials

Back to the main page.
