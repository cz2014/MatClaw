# Constraining the local magnetic moments

Categories: Examples

Description: Constraining the local magnetic moments on NiO.

To orient locally each spin, a penalty energy $E\_p$ is added, inversely proportional to the $\lambda$ (LAMBDA) parameter. Thus, the process has to begin with a low LAMBDA, which is increased step by step.

For additional information, go to the I\_CONSTRAINED\_M page.

*Exercise :* Verify the $E\_p=f(1/\lambda)$ relation by constraining the spin directions. Check the efficiency of the method by constraining only the direction, then the direction and the size of spins.

---

* INCAR

```
NiO GGA+U Constr.
  SYSTEM        = "NiO"
   
Electronic minimization
  ENCUT         = 450
  EDIFF         = 1E-5
  LORBIT        = 11
  LREAL         = .False.
  ISYM          = -1
  NELMIN        = 6
  LSORBIT       = .True.
  GGA_COMPAT    = .FALSE.
   
DOS
  ISMEAR    = -5
   
Magnetism
  ISPIN     = 2
  I_CONSTRAINED_M = 1  # direction
  # I_CONSTRAINED_M = 2  # size and direction
  M_CONSTR  = 2 0 0 0 -2 0 6*0
  LAMBDA    = 1
  RWIGS     = 1.30 0.70 
    
Orbital moment
  LORBMOM  = T
    
Mixer
  AMIX      = 0.2
  BMIX      = 0.00001
  AMIX_MAG  = 0.8
  BMIX_MAG  = 0.00001
    
GGA+U
  LDAU      = .TRUE.
  LDAUTYPE  = 2
  LDAUL     = 2 -1
  LDAUU     = 5.00 0.00
  LDAUJ     = 0.00 0.00
  LDAUPRINT = 1
  LMAXMIX   = 4
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

nio\_constr.tgz

---
