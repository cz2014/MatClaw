# Spin-orbit coupling in a Fe monolayer

Categories: Examples

Overview > fcc Ni (revisited) > NiO > NiO LSDA+U > Spin-orbit coupling in a Ni monolayer > Spin-orbit coupling in a Fe monolayer >constraining local magnetic moments   > List of tutorials

## Task

Spin-orbit coupling (SOC) in a freestanding Fe monolayer. This example is carried out in total analogy to Spin-orbit coupling in a Ni monolayer.

## Input

### POSCAR

```
fcc Fe 100 surface
 3.45
   .50000   .50000   .00000
  -.50000   .50000   .00000
   .00000   .00000  5.00000
  1
Cartesian
   .00000   .00000   .00000
```

### INCAR

```
SYSTEM        = Fe (100) monolayer
ISTART        = 0
ENCUT         = 270.00
LNONCOLLINEAR = .TRUE.
MAGMOM        = 0.0 0.0 3.0
VOSKOWN       = 1
LSORBIT       = .TRUE.
     
LMAXMIX       = 4
```

* For the second calculation, switch to in-plane magnetiztion by setting MAGMOM= 3.0 0.0 0.0.

### KPOINTS

```
k-points
 0
Monkhorst-Pack
9 9 1
0 0 0
```

## Calculation

* From the energy differences of the calculations using in plane and out of plane magnetization we see that the easy axis lies (in contrast to Ni) out of plane:

$E\_{\textrm{MAE}}=E(m\_{\perp})-E(m\_{\parallel})=-0.2 \, \textrm{meV}$

## Download

4\_4\_SOI\_Fe.tgz

Overview > fcc Ni (revisited) > NiO > NiO LSDA+U > Spin-orbit coupling in a Ni monolayer > Spin-orbit coupling in a Fe monolayer >constraining local magnetic moments   > List of tutorials
