# NiO GGA+U

Categories: Examples

Description: Antiferromagnetic (AFM) configuration for NiO in the GGA+Ueff (Dudarev's) approach ; PBE functional

In the Dudarev method, a Hubbard effective parameter Ueff = U - J is used. Concretely, the J value is considered equal to 0, and Ueff = U. For more details read the page on the LDAUTYPE-tag .

*Exercise :* Study the change of the magnetic moment of Ni atoms and the DOS by varying the Ueff value.

---

* INCAR

```
NiO GGA+U AFM
  SYSTEM    = "NiO"
    
Electronic minimization
  ENCUT     = 450
  EDIFF     = 1E-5
  LORBIT    = 11
  LREAL     = .False.
  ISTART    = 0
  NELMIN    = 6
    
DOS
  ISMEAR    = -5
    
Magnetism
  ISPIN     = 2
  MAGMOM    = 2.0 -2.0 2*0.0 
     
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

To check the results obtained with this approach, they can be compared to those determined with a hybrid approach. The magnetic moment for the Ni atoms and the Eg calculated using this approach are 1.67 μB and 3.97 eV respectively.

## Download

nio\_gga+u.tgz

---
