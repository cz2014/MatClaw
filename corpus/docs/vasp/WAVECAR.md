# WAVECAR

Categories: Files, Input files, Output files

The WAVECAR file is a binary file containing the following data:

```
     NBAND       number of bands
     ENCUTI      'initial' cut-off energy
     AX          'initial' basis vectors defining the supercell
     CELEN       ('initial') eigenvalues
     FERWE       ('initial') Fermi-weights
     CPTWFP      ('initial') wavefunctions
```

Usually WAVECAR provides excellent starting wavefunctions for a continuation job. For dynamic simulation (IBRION=0) the wavefunctions in the file are usually those predicted for the next step: i.e. the file is compatible with CONTCAR. The WAVECAR, CHGCAR and the CONTCAR file can be used consistently for a molecular dynamics continuation job. For static calculations and relaxations (IBRION=-1,1,2) the written wavefunctions are the solution of the KS-equations for the last step. It is possible to avoid, that the WAVECAR is written out by setting

```
LWAVE  =  .FALSE.
```

in the INCAR file.

Mind: For dynamic simulations (IBRION=0) the WAVECAR file contains predicted wavefunctions compatible with CONTCAR. If you want to use the wavefunctions for additional calculations, first copy CONTCAR to POSCAR and make another static (ISTART=1; NSW=0) continuation run with ICHARG=1.

---
