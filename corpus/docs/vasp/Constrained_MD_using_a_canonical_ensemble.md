# Constrained MD using a canonical ensemble

**Description**:
Compare adsoption of H2O on TiO2[110] using a simple model structure: the model surface consists of 2 layers TiO2, (1x1)

* The bottom layer of the slab will be kept frozen
* 2 setups will be tested:
  + Standard relaxation, minimizing the Hellmann-Feyman forces
  + Constrained MD, fixing the bond lengths and angle of H2O, the system is coupled to an ANDERSEN thermostat:
    - Microcanonical NVE ensemble (no collisions with the thermostat)
    - Canonical ensembe at T= 10K, to be close to the standard relaxation (0K)

To keep the computing time reasonable, the number of steps in the MD is limited to 100 (100 fs) which implies that the MD is NOT CONVERGED.

* INCAR for standard relaxation

```
SYSTEM = H2O_TiO2
ENMAX = 400
ISMEAR =  2
SIGMA = 0.05
EDIFF = 1e-6
EDIFFG = -0.05
IBRION = 2
POTIM = 0.5
NSW = 200
```

* INCAR for constrained MD using a microcanonical ensemble

```
SYSTEM = H2O_TiO2
ENMAX = 400
ISMEAR = 2
SIGMA = 0.05
ISMEAR = 0
EDIFF = 1e-6
EDIFFG = -0.05
IBRION = 0
POTIM = 1.
MDALGO = 1    # Andersen Thermostat
TEBEG = 10; TEEND = 10
NSW = 100
```

* ICONST for constrained MD using a microcanonical ensemble

```
R 7 8 0
R 7 9 0
A 8 7 9 0
```

* INCAR for constrained MD using a canonical ensemble

```
SYSTEM = H2O_TiO2
ENMAX = 400
ISMEAR = 2
SIGMA = 0.05
ISMEAR = 0
EDIFF = 1e-6
EDIFFG = -0.05
IBRION = 0
POTIM = 1.
MDALGO = 1    # Andersen Thermostat
ANDERSEN_PROB = 0.9
TEBEG = 10; TEEND = 10
NSW = 100
```

* ICONST for constrained MD using a canonical ensemble

```
R 7 8 0
R 7 9 0
A 8 7 9 0
```

* POSCAR

```
TiO2+H2O                                    
   1.00000000000000     
     4.61949   0.00000    0.00000
     0.00000   4.61949    0.00000
     0.00000   0.00000   14.7788
   Ti   O  H
     2     5     2
Selective
Direct
  0.00000  0.00000  0.00000    F F F
  0.50000  0.50000  0.10000    T T T
  0.30374  0.30374  0.00000    F F F
  0.69625  0.69625  0.00000    F F F
  0.19625  0.80374  0.10000    T T T
  0.80374  0.19625  0.10000    T T T
  0.50000  0.50000  0.31500    T T T
  0.37720  0.62280  0.35881    T T T
  0.62280  0.37720  0.35881    T T T
```

* KPOINTS

```
Automatically generated mesh
       0
Gamma
 5 5 1
```

## Download

h2o\_on\_tio2.tgz, sub-folder constrMD\_canonical

---

To the list of examples or to the main page
