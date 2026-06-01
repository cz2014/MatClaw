# NiO HSE06

Categories: Examples

Description: Hybrid functional calculation using the HSE06 functional.

It is strongly recommended to start from a converged PBE calculation (ISTART = 1) before beginning with a DFT+HF method. For other hybrid functionals

*Exercise :* Check the values presented here.

---

* INCAR

```
NiO HSE06 AFM
  SYSTEM   = "NiO"
    
Electronic minimization
  ENCUT    = 450
  EDIFF    = 1E-5
  LORBIT   = 11
  LREAL    = .False.
  ISTART   = 0
  NELMIN   = 6
    
DOS
  ISMEAR   = -5
    
Magnetism
  ISPIN    = 2
  MAGMOM   = 2.0 -2.0 2*0.0
    
Mixer
  AMIX     = 0.2
  BMIX     = 0.00001
  AMIX_MAG = 0.8
  BMIX_MAG = 0.00001 
    
Hybrid functional
  #LHFCALC  = .TRUE.
  #HFSCREEN = 0.2 
  #ALGO     = D
  #TIME     = 0.4
```

* KPOINTS

```
k-points
 0
gamma
 4  4  4 
 0  0  0
```

* POSCAR

```
NiO
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

## Download

nio\_hse06.tgz

---
