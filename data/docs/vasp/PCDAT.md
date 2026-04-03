# PCDAT

Categories: Files, Output files, Ensemble properties, Symmetry

The PCDAT file contains the pair correlation function. For dynamic simulations (IBRION$\ge$0) an averaged pair correlation is written to the file (see also NBLOCK, KBLOCK, NPACO and APACO).

A sample output of the PCDAT file for a system containing two element types looks as follows:

```
  1   8   1   0  0.8163705E+01  0.1000000E+04
 CAR
 structure name
   0   0   0
   1   1
 350 350 350
 350
  0.1000000E-09
  0.2857143E-11
   1
  0.1000000E-14  0.4027100E-09  0.4027100E-09  0.4027100E-09
  0.2410163E+04  0.2410163E+04
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  0.000  0.000  0.000  0.000
  ...
  0.000  0.000  0.000  0.000
  0.165  0.000  0.331  0.000
  0.000  0.000  0.000  0.000
  0.152  0.000  0.304  0.000
  0.293  0.000  0.585  0.000
... [16 more coordinate lines truncated] ...
  ...
```

Here is the description of each line:

* Line 1: 1 (fixed output), number of ions, 1 (fixed output), 0 (fixed output), unit cell volume divided by number of atoms, temperature.
* Line 2: CAR (fixed output).
* Line 3: Header of INCAR file (the tag SYSTEM).
* Line 4: 0, 0, 0 (all fixed output).
* Line 5: 1 (fixed output), NBLOCK.
* Line 6: NPACO, NPACO, NPACO.
* Line 7: NPACO.
* Line 8: 0.1\*10-9 (fixed output).
* Line 9: APACO$\times$10-10/NPACO.
* Line 10: NSW/NBLOCK/KBLOCK.
* Line 11: POTIM$\times$10-15, norm of lattice vector 1 times 10-10, norm of lattice vector 2 times 10-10, norm of lattice vector 3 times 10-10.
* Line 12-(12+NPACO): Input mean temperature/(NBLOCK$\times$KBLOCK), actual mean temperature.
* Following that the next NPACO lines show the pair correlation function for each species combination.
* Optional (KBLOCK$\times$NBLOCK/NSW)$\times$NPACO+1 lines: The above is repeated KBLOCK$\times$NBLOCK/NSW times.

The order of species combinations (columns of the pair correlation function) follows column-wise the lower triangle of the species correlation matrix. That means for 3 species the order is the following:

```
total 1-1  1-2  1-3  2-2  2-3  3-3
```

The numbers listed above corresponds to the species as encountered in the POSCAR/POTCAR file. The first column (total) reports the total pair correlation function.

The PCDAT file contains no abscissa. To obtain the pair correlation functions with the corresponding abscissa the following 'bash/awk' script can be used:

**Click to show/*pair\_correlation\_xny.sh***

```
file=PCDAT
awk <$file >PCDAT.xy '
NR==8 { pcskal=$1}
NR==9 { pcfein=$1}
NR==7 { npaco=$1}
NR>=13 {  
  line=line+1
  if (line==1) s=s+1
  if (line==(npaco+1))  {
     print " "
     line=0
  }
  else  {
     a1[line]=  a1[line] + $1
     a2[line]=  a2[line] + $2
     a3[line]=  a3[line] + $3
     a4[line]=  a4[line] + $4
     print (line-0.5)*pcfein/pcskal,$1,$2, $3, $4, $5
  }
}
END {
 print "final sets=", s
 for (line=1 ; line<=npaco ; line++)
     print (line-0.5)*pcfein/pcskal,a1[line]/s,a2[line]/s,a3[line]/s,a4[line]/s
}
'
```

To use this script, in your folder with the PCDAT file, please copy the content to *pair\_correlation\_xny.sh* and type the following:

```
bash pair_correlation_xny.sh
```

The resulting pair correlation function is written to

```
PCDAT.xy
```

## Related tags and articles

IBRION, MDALGO, NBLOCK, KBLOCK, NSW, NPACO, APACO

---
