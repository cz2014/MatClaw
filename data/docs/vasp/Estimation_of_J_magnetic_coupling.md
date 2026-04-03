# Estimation of J magnetic coupling

Categories: Examples

Description: Estimation of the J magnetic exchange coupling using the GGA+U method.

Switching off the symmetry (ISYM = 0) is often necessary to generate different magnetic configurations.

*Exercise :* Study the change of the 180° superexchange coupling J2 between the next nearest neighbors (dNi-Ni = 4.17 A) by varying the Ueff value. The following equation J2 = (EFM - EAFM) / 12 expresses the super exchange Ni-O-Ni coupling as a function of the energy difference of the ferromagnetic (FM) and antiferromagnetic (AFM) configurations. In this case, the superexchange coupling J1 between the nearest neighbors is neglected. The theoretical results can be compared to the experimental one : J2 = 19.01 meV (Hutchings M. T., Samuelsen E. J., *Phys. Rev. B 6*, 9, **1972**, 3447)

---

* INCAR

```
NiO GGA+U AFM
  SYSTEM    = "NiO"
    
Electronic minimization
  ENCUT     = 450
  EDIFF     = 1E-4
  LORBIT    = 11
  LREAL     = .False.
  ISTART    = 0
  ISYM      = 0
  NELMIN    = 6
    
DOS
  ISMEAR    = -5
    
Magnetism
  ISPIN     = 2
  MAGMOM    = 2.0 -2.0 2*0  # AFM conf.
  # MAGMOM    = 2*2.0 2*0  # FM conf.
```

```
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

---

Necessarely, the J magnetic coupling decreases with the increasing of the Ueff value. To assess the obtained value, similar calculations could be done using a hybrid functional.

## Download

nio\_Jcoupl.tgz

---
