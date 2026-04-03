# TS search using the Improved Dimer Method

Description:

---

* INCAR

```
SYSTEM = Ammonia flipping
IBRION = 44
NSW = 100
EDIFF = 1e-6
EDIFFG = -0.01
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
 ! decay direction
 0.000004   -0.000001    0.511990
 0.000000   -0.000003    0.547859
-0.000004   -0.000001    0.511988
 0.000000    0.000000   -0.111986
```

## Download

ammonia\_flipping.tgz, sub-folder improved\_dimer

---

To the list of examples or to the main page
