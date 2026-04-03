# Relaxed geometry

Description: calculate the relaxed geometry of NH3: the total energy is the energy of the initial state of the flipping reaction

---

* INCAR

```
SYSTEM = Ammonia flipping
IBRION = 2
NSW = 10
ALGO = N
POTIM = 0.5
EDIFF = 1e-6
EDIFFG = -0.01
NELMIN = 5
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
  3    1
Selective dynamics
Direct
0.636429  0.567446  0.549205   T   T   T
0.500000  0.364896  0.549205   T   T   T
0.363571  0.567446  0.549205   T   T   T
0.500000  0.500000  0.500000   F   F   F
```

## Download

ammonia\_flipping.tgz, sub-folder scf

---

To the list of examples or to the main page
