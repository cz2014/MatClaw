# TS search using the NEB Method

Description: the Nudged Elastic Band Method generates an energy profile along a reaction path,
using equidistant IMAGES along the path. The input geometries of the IMAGES are interpolated between
the geometries of the initial and the final states, e.g. using the script interpolatePOSCAR, which
processes the con-catenated POSCAR files of the initial and the final state of the reaction (POSCAR\_if).
in the case of ammonia flipping the final state is a mirror of the initial state and need not be
calculated explicitely.
For each IMAGE, a separate sub-directory 00 ... (IMAGES+1) is needed, which contains all output of the
respective IMAGE. The number of cores on which VASP is run has to be an integer multiple of the number of IMAGES.

---

* INCAR

```
SYSTEM = Ammonia flipping
IMAGES = 6
SPRING = -5
IBRION = 2
NSW = 50
ALGO = N
POTIM = 1.0
EDIFF = 1e-6
```

* KPOINTS

```
k-points
 0
G
 1 1 1
```

* POSCAR\_if

```
ammonia flipping
  1.00000000000000
    6.000000    0.000000    0.000000
    0.000000    7.000000    0.000000
    0.000000    0.000000    8.000000
    3     1
Direct
 0.636428  0.567457  0.5491645
 0.500000  0.364985  0.5491330
 0.363572  0.567457  0.5491645
 0.500000  0.500000  0.5000000
ammonia flipping
  1.00000000000000
    6.000000    0.000000    0.000000
    0.000000    7.000000    0.000000
    0.000000    0.000000    8.000000
    3     1
Direct
 0.636428  0.567457  0.4508355
 0.500000  0.364985  0.4508670
 0.363572  0.567457  0.4508355
 0.500000  0.500000  0.5000000
```

## Download

ammonia\_flipping.tgz, sub-folder NEB

---

To the list of examples or to the main page
