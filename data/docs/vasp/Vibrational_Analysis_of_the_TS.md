# Vibrational Analysis of the TS

Description: the Improved Dimer Method needs an educated guess of the decay path, which is extimated from the hardest vibration mode with imaginary frequency of the TS geometry
(which is a planar NH3 molecule):

---

* INCAR

```
SYSTEM = Ammonia flipping
IBRION = 5
NSW = 1
ALGO = F
POTIM = 0.015
EDIFF = 1e-8
EDIFFG = -0.01
NWRITE = 3
```

* KPOINTS

```
k-points
 0
G
 1 1 1
```

* POSCAR

```
ammonia flipping
  1.00000000000000
    6.000000    0.000000    0.000000
    0.000000    7.000000    0.000000
    0.000000    0.000000    8.000000
  H    N
    3     1
Direct
 0.6462   0.5736   0.5000
 0.5000   0.3547   0.5000
 0.3538   0.5736   0.5000
 0.5000   0.5000   0.5000
```

## Download

ammonia\_flipping.tgz, sub-folder TS\_vib

---

To the list of examples or to the main page
