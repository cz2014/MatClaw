# INCAR

Categories: Files, Input files

The INCAR file is the central input file of VASP, which determines *what to do and how to do it*. The INCAR tags specified in the INCAR file select the algorithms and set the parameters that VASP uses during the calculation. VASP will use reasonable default values, which we recommend using when unsure. Yet, the settings in the INCAR file are the main source of errors and false results, so we suggest carefully checking the meaning of the set INCAR tags. Regarding the format, each statement consists of the name of a tag, the equal sign **=**, and the values assigned to the tag (tag = values). For instance, an INCAR file for a density-functional-theory calculation might read

```
  ALGO  = Normal # alorithm for electron optimization
  ISMEAR= -1     # Fermi smearing
  SIGMA = 0.05   # width of the smearing in eV
```

> **Tip:** VASP writes its interpretation of the data in the INCAR file to the OUTCAR file. Please verify that it agrees with the intended setup.

## Format

The INCAR file is a tagged format free-ASCII file. That is, each statement follows a *tag = values* syntax. Typically, each line contains a single statement, but it is possible to combine multiple statements on a single line, separating them by a semicolon **;**, e.g.,

```
  ISMEAR= -1 ;  SIGMA = 0.05
```

For better readability, long lines can be split with a backslash **\** . Avoid blanks after the backslash because some versions of VASP cannot parse those. For instance,

```
  MAGMOM  = 0 0 1.0 0 0 -1.0 \
            0 0 1.0 0 0 -1.0 \
            6*0
```

is the same as

```
  MAGMOM  = 0 0 1.0 0 0 -1.0 0 0 1.0 0 0 -1.0 0 0 0 0 0 0
```

Alternatively, enclose all the values in quotes **"** to ignore line breaks between the quotes, e.g.,

```
  WANNIER90_WIN = "
  Begin Projections
  Si:sp3
  End Projections
  "
```

For comments, VASP ignores any text after a hashtag **#** or exclamation mark **!**. Use this to add comments anywhere to the INCAR file. A comment prefix (#!) is often unnecessary because VASP ignores all text that does not fit the statement format (tag = values). In this case, do not use any syntax relevant character (=;") because it may break the parsing of the INCAR file. VASP generally ignores empty lines, but we have encountered issues due to lines with tabs for some compilers.

A typical (relatively complex) INCAR:

```
SYSTEM = Rhodium surface calculation

start parameters for this Run (automatic defaults, hence not often required)
  ISTART =      0    #  job   : 0-new  1- orbitals from WAVECAR
  ICHARG =      2    #  charge: 1-file 2-atom 10-const

electronic optimization
  ENCUT  = 300.00 eV # defaults from POTCAR, but wise to include
  ALGO  =  Normal    # alorithm for electron optimization, can be also FAST or ALL
  NELM   = 60        # of ELM steps, sometimes default is too small 
  EDIFF  = 1E-06     # stopping-criterion for ELM
! broadening and DOS related values; this works almost always
  SIGMA  =    0.05;  ISMEAR =  0   ! broadening in eV, -4-tet -1-fermi 0-gaus

ionic relaxation
  EDIFFG =  -1E-02   # stopping-criterion for IOM (all forces smaller 1E-2)
  NSW    =  20       # number of steps for IOM
  IBRION =  2        # CG for ions, often 1 (RMM-DISS) is faster
  POTIM  =  .5       # step for ionic-motion (for MD in fs)
performance optimization
  KPAR   =    4      # make 4 groups, each group working on one set of k-points 
  NCORE  =    4      # one orbital handled by 4 cores 
  LREAL  =    A      # real space projection; slightly less accurate but faster
```

## Related tags and articles

* A comprehensive list of all **INCAR** tags and related articles.
* Other important input files include KPOINTS, POSCAR, and POTCAR

---
