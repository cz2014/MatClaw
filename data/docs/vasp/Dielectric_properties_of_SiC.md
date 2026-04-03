# Dielectric properties of SiC

Categories: Examples

Overview > dielectric properties of SiC > dielectric properties of Si  > Ionic contributions to the frequency dependent dielectric function of NaCl  > List of tutorials

## Task

Calculation of the static and frequency dependent dielectric properties of SiC.

## Static dielectric properties

### Density functional perturbation theory

Let us start with the calculation of the static dielectric properties.
The most convenient way to determine the Born effective charges, dielectric-,
piezoelectric tensors is by means of density functional perturbation theory
(LEPSILON=*.TRUE.*).

* INCAR (see INCAR.LEPSILON)

```
ISMEAR =  0
SIGMA  =  0.01
EDIFF  = 1.E-8
   
## to get the Born effective charges
## and the macroscopic dielectric tensor
LEPSILON = .TRUE.
    
#LRPA = .TRUE.
#LPEAD = .TRUE.
   
## to get the ionic contribution
## to the macroscopic dielectric tensor
#IBRION = 8
   
## As an alternative to LEPSILON = .TRUE.
## you might try the following:
#LCALCEPS = .TRUE.
   
## and:
#IBRION = 6
#NFREE = 2
```

* KPOINTS (see KPOINTS.8)

```
8x8x8
 0
G
 8 8 8
 0 0 0
```

* POSCAR

```
system SiC
4.35
0.5 0.5 0.0
0.0 0.5 0.5
0.5 0.0 0.5
1 1
cart
0.00 0.00 0.00 
0.25 0.25 0.25
```

* The LRPA-tag

By default the dielectric tensor is calculated in the independent-particle (IP) approximation,
you should see the following lines in the OUTCAR file:

```
HEAD OF MICROSCOPIC STATIC DIELECTRIC TENSOR (independent particle, excluding Hartree and local field effects)
```

and

```
MACROSCOPIC STATIC DIELECTRIC TENSOR (including local field effects in DFT)
```

which comes later in the OUTCAR file.

If one adds

```
LRPA=.TRUE.
```

to the INCAR above, the second instance will include local field effect
only with respect to the response in the Hartree part of the potential, i.e., in the
*random-phase-approximation* (RPA).
Search for

```
MACROSCOPIC STATIC DIELECTRIC TENSOR (including local field effects in RPA (Hartree))
```

in the OUTCAR.

* The Born effective charge tensors ($Z^{\*}\_{ij}$)

Roughly speaking, the Born effective tensors provide a measure of how much charge
effectively moves with an atom when you displace it.
For a definition see the article on Berry phases and finite electric fields.
For LEPSILON=.TRUE., the Born effective charge tensors are written near the end of the OUTCAR file.

Look for

```
BORN EFFECTIVE CHARGES (in e, cummulative output)
```

**Mind**: you will find this entry only if LRPA=.FALSE. (default), since the Born-effective charges in the RPA tend to be nonsensical.

* The LPEAD-tag

As an alternative to solving a linear Sternheimer equation (Eq. 32 of ), one may
compute $| \nabla\_{\mathbf{k}} \tilde{u}\_{n\mathbf{k}} \rangle$ from finite differences by specifying

```
LPEAD=.TRUE.
```

in the INCAR file.
The derivative of the cell-periodic part of the wave function w.r.t. the Bloch vector is then computed
by means of a fourth-order finite difference stencil, in the spirit of Eqs. 96 and 97 of .
The results of the calculation of static dielectric properties by means of LEPSILON=.TRUE.
tend to converge more rapidly w.r.t. **k**-point sampling with LPEAD=.TRUE.

Rerun the example with

```
ISMEAR =  0
SIGMA  =  0.01
EDIFF  = 1.E-8
   
## to get the Born effective charges
## and the macroscopic dielectric tensor
LEPSILON = .TRUE.
LPEAD = .TRUE.
```

This will allow for a clean comparison with the next topic.

### Response to finite electric fields

The second way one may compute the static dielectric properties is from self-consistent response of the system to a finite electric field.

* INCAR

```
ISMEAR =  0
SIGMA  =  0.01
EDIFF  = 1.E-8
    
LCALCEPS = .TRUE.
```

### Ionic contributions to the static dielectric properties

To obtain the ionic contributions to the static dielectric properties one needs to compute the force-constant matrices (Hessian of the total energy w.r.t. the ionic positions) and internal strain tensors (second derivative of the total energy w.r.t. strain fields and ionic postions).
These properties may be obtained from finite differences (IBRION=5 or 6) or from perturbation theory (IBRION=7 or 8).
Try the following

* INCAR

```
ISMEAR =  0
SIGMA  =  0.01
EDIFF  = 1.E-8
   
## to get the Born effective charges
## and the macroscopic dielectric tensor
LEPSILON = .TRUE.
LPEAD = .TRUE.
    
## to get the ionic contribution
## to the macroscopic dielectric tensor
IBRION = 8
```

and search for

```
MACROSCOPIC STATIC DIELECTRIC TENSOR IONIC CONTRIBUTION
```

```
ELASTIC MODULI IONIC CONTR (kBar)
```

```
PIEZOELECTRIC TENSOR IONIC CONTR  for field in x, y, z        (C/m^2)
```

in the OUTCAR file.

## Frequency dependent dielectric response

Frequency dependent dielectric functions may be computed at various levels of approximation:

1. In the independent-particle approximation.
2. Including local field effects in the random-phase-approximation.
3. Including local field effects in DFT.

Whatever we may choose to do afterwards in terms of dielectric response calculations,
we have to start with a standard DFT (or hybrid functional) calculation

* INCAR (see INCAR.DFT)

```
ISMEAR =  0
SIGMA  =  0.01
EDIFF  = 1.E-8
```

* KPOINTS (see KPOINTS.6)

```
6x6x6
 0
G
 6 6 6
 0 0 0
```

**Mind**: keep the WAVECAR file, you're going to need it in the following.

### The independent-particle picture

To compute the frequency dependent dielectric function in the independent-particle (IP) picture
we restart from the WAVECAR of the previous run, with the following INCAR

* INCAR (see INCAR.LOPTICS)

```
ALGO = Exact
NBANDS  = 64
LOPTICS = .TRUE. ; CSHIFT = 0.100
NEDOS = 2000
   
## and you might try with the following
#LPEAD = .TRUE.
   
ISMEAR =  0
SIGMA  =  0.01
EDIFF  = 1.E-8
```

The frequency dependent dielectric functions is written to the OUTCAR file.
Search for

```
 frequency dependent IMAGINARY DIELECTRIC FUNCTION (independent particle, no local field effects)
```

and

```
 frequency dependent      REAL DIELECTRIC FUNCTION (independent particle, no local field effects)
```

To visualize the real and imaginary parts of the frequency dependent dielectric function you may
use p4vasp

```
p4v vasprun.xml
```

or run the following bash-script (plotoptics2)

```
awk 'BEGIN{i=1} /imag/,\
                /\/imag/ \
                 {a[i]=$2 ; b[i]=$3 ; i=i+1} \
     END{for (j=12;j<i-3;j++) print a[j],b[j]}' vasprun.xml > imag.dat

awk 'BEGIN{i=1} /real/,\
                /\/real/ \
                 {a[i]=$2 ; b[i]=$3 ; i=i+1} \
     END{for (j=12;j<i-3;j++) print a[j],b[j]}' vasprun.xml > real.dat

cat >plotfile<<!
# set term postscript enhanced eps colour lw 2 "Helvetica" 20
# set output "optics.eps"
plot [0:25] "imag.dat" using (\$1):(\$2) w lp, "real.dat" using (\$1):(\$2) w lp
!

gnuplot -persist plotfile
```

* LPEAD-tag

As an alternative to the perturbative expression (Eq. 31 of ), one may
compute $| \nabla\_{\mathbf{k}} \tilde{u}\_{n\mathbf{k}} \rangle$ from finite differences by specifying

```
LPEAD=.TRUE.
```

in the INCAR file.
The derivative of the cell-periodic part of the wave function w.r.t. the Bloch vector is then computed
by means of a fourth-order finite difference stencil, in the spirit of Eqs. 96 and 97 of .

**Mind**: keep the WAVECAR and WAVEDER files, you're going to need them in the following.
You might also want to keep a copy of the vasprun.xml.

```
cp vasprun.xml vasprun_loptics.xml
```

### Including local field effects

To determine the frequency dependent dielectric function including local field effects one needs the WAVECAR and WAVEDER files from the previous calculation (ALGO=Exact and LOPTICS=.TRUE., and sufficient virtual orbitals), and

* INCAR (see INCAR.CHI)

```
# Frequency dependent dielectric tensor with and
# without local field effects in RPA
# N.B.: beware one first has to have done a
# calculation with ALGO=Exact, LOPTICS=.TRUE.
# and a reasonable number of virtual states (see above)
ALGO = CHI
       
# be sure to take the same number of bands as for
# the LOPTICS=.TRUE. calculation, otherwise the
# WAVEDER file is not read correctly
NBANDS = 64
   
ISMEAR =  0
SIGMA  =  0.01
EDIFF  = 1.E-8
     
LWAVE = .FALSE.
LCHARG= .FALSE.
```

Information concerning the dielectric function in the independent-particle picture is written after the line

```
HEAD OF MICROSCOPIC DIELECTRIC TENSOR (INDEPENDENT PARTICLE)
```

in the OUTCAR file.

Per default, for ALGO=*CHI*, local field effects are included at the level of the RPA (LRPA=*.TRUE.*), i.e., limited to Hartree contributions only.

See the information after

```
INVERSE MACROSCOPIC DIELECTRIC TENSOR (including local field effects in RPA (Hartree))
```

in the OUTCAR file.

To include local field effects beyond the RPA, i.e., contributions from DFT exchange and correlation, one has to specify

```
LRPA=.FALSE.
```

in the INCAR file.

In this case look at the output after

```
INVERSE MACROSCOPIC DIELECTRIC TENSOR (test charge-test charge, local field effects in DFT)
```

in the OUTCAR file.

The following bash-script (plotchi) uses *awk* to extract the frequency dependent dielectric constant, both
in the independent-particle picture as well as including local field effects (either in DFT or in the RPA) and plots the real and imaginary components using *gnuplot*:

```
awk 'BEGIN{i=1} /HEAD OF MICRO/,\
                /XI_LOCAL/ \
                 {if ($4=="dielectric") {a[i]=$1 ; b[i]=$2 ; c[i]=$3 ; i=i+1}} \
     END{for (j=1;j<i;j++) print a[j],b[j],c[j]}' OUTCAR > chi0.dat

awk 'BEGIN{i=1} /INVERSE MACRO/,\
                /XI_TO_W/ \
                 {if ($4=="dielectric") {a[i]=$1 ; b[i]=$2 ; c[i]=$3 ; i=i+1}} \
     END{for (j=1;j<i;j++) print a[j],b[j],c[j]}' OUTCAR > chi.dat
cat >plotfile<<!
# set term postscript enhanced eps colour lw 2 "Helvetica" 20
# set output "optics.eps"

plot "chi0.dat" using (\$1):(\$2)  w lp lt -1 lw 2 pt 4 title "chi0 real", \
     "chi0.dat" using (\$1):(-\$3) w lp lt  0 lw 2 pt 4 title "chi0 imag", \
     "chi.dat"  using (\$1):(\$2)  w lp lt  1 lw 2 pt 2 title "chi  real", \
     "chi.dat"  using (\$1):(-\$3) w lp lt  0 lw 2 pt 2 lc 1 title "chi  imag"
!

gnuplot -persist plotfile
```

If you have kept a copy of the vasprun.xml of the LOPTICS=*.TRUE.* run (e.g., vasprun\_loptics.xml), you might execute plotall to compare the dielectric functions computed with LOPTICS=*.TRUE.* and ALGO=*CHI*.

```
vasprun_LOPTICS=vasprun_loptics.xml
OUTCAR_CHI=OUTCAR

awk 'BEGIN{i=1} /imag/,\
                /\/imag/ \
                 {a[i]=$2 ; b[i]=$3 ; i=i+1} \
     END{for (j=12;j<i-3;j++) print a[j],b[j]}' $vasprun_LOPTICS > imag.dat

awk 'BEGIN{i=1} /real/,\
                /\/real/ \
                 {a[i]=$2 ; b[i]=$3 ; i=i+1} \
     END{for (j=12;j<i-3;j++) print a[j],b[j]}' $vasprun_LOPTICS > real.dat

awk 'BEGIN{i=1} /HEAD OF MICRO/,\
                /XI_LOCAL/ \
                 {if ($4=="dielectric") {a[i]=$1 ; b[i]=$2 ; c[i]=$3 ; i=i+1}} \
     END{for (j=1;j<i;j++) print a[j],b[j],c[j]}' $OUTCAR_CHI > chi0.dat

awk 'BEGIN{i=1} /INVERSE MACRO/,\
                /XI_TO_W/ \
                 {if ($4=="dielectric") {a[i]=$1 ; b[i]=$2 ; c[i]=$3 ; i=i+1}} \
     END{for (j=1;j<i;j++) print a[j],b[j],c[j]}' $OUTCAR_CHI > chi.dat

cat >plotfile<<!
# set term postscript enhanced eps colour lw 2 "Helvetica" 20
# set output "optics.eps"

plot "chi0.dat" using (\$1):(\$2)  w lp lt -1 lw 2 pt 4 title "chi0 real", \
     "chi0.dat" using (\$1):(-\$3) w lp lt  0 lw 2 pt 4 title "chi0 imag", \
     "chi.dat"  using (\$1):(\$2)  w lp lt  1 lw 2 pt 2 title "chi  real", \
     "chi.dat"  using (\$1):(-\$3) w lp lt  0 lw 2 pt 2 lc 1 title "chi  imag", \
     "real.dat"  using (\$1):(\$2) w l lt -1  title "optics  real", \
     "imag.dat"  using (\$1):(-\$2) w l lt  0 lc -1 title "optics  imag"
!

gnuplot -persist plotfile
```

Why are the dielectric functions in independent-particle picture from the LOPTICS=*.TRUE.* and the ALGO=*CHI* calculations different?

Hints:

* What CSHIFT is used in the ALGO=*CHI* calculation?

Try redoing the LOPTICS=*.TRUE.* calculation with the same CSHIFT as VASP chose for the ALGO=*CHI* calculation (see INCAR.LOPTICS2):

```
CSHIFT=0.466
```

* Redo the ALGO=*CHI* calculation with LSPECTRAL=*.FALSE.* in the ALGO=*CHI* calculation (see INCAR.CHI2).

and compare the dielectric functions again.

* The sample output (using a $6\times6\times6$ mesh for the k points) should look like the following:

## References

## Download

SiC\_dielectric.tgz

Overview > dielectric properties of SiC > dielectric properties of Si  > Ionic contributions to the frequency dependent dielectric function of NaCl  > List of tutorials
