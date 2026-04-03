# CHG

Categories: Files, Output files

This file contains the lattice vectors, atomic coordinates and the total charge multiplied by the grid volume $n(r)\times V\_{\mathrm{grid}}$ on the fine FFT-grid (NG(X,Y,Z)F, with $V\_\mathrm{grid}$ = NGXF$\times$NGYF$\times$NGZF) at every tenth MD step i.e.

```
MOD(NSTEP,10)==1,
```

where NSTEP starts from 1. To save disc space less digits are written to the CHG file than to the CHGCAR. The file can be used to provide data for visualization programs, for instance IBM data explorer (for the IBM data explorer, a tool exists to convert the CHG file to a valid data explorer file). It is possible to avoid that the CHG file is written out by setting

```
LCHARG  =  .FALSE.
```

in the INCAR file. The data arrangement of the CHG file is similar to that of the CHGCAR file, with the exception of the PAW one centre occupancies, which are missing on the CHG file.

---
