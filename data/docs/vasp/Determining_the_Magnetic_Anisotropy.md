# Determining the Magnetic Anisotropy

Categories: Examples

Description: Magnetocrystalline Anisotropy Energy determined non-self-consistently

The Magnetocrystalline Anisotropy Energy is determined by rotating all spins according to different directions. First of all, an accurate (PREC = Accurate, LREAL = .False.) collinear calculation (using the vasp\_std version) in the ground state has to be done. Next, the spin-orbit coupling (LSORBIT = .True. using the vasp\_ncl version) is taken into account non-self-consistently (ICHARG = 11) for several spin orientations. In most cases, the changes in energies are very low (sometimes around micro-eV). The number of bands for the has to be doubled compared to the collinear run.

To modify the orientation of the spins in the crystal, we consider the second approach described here. For the MAGMOM-tag, the total local magnetic moment is written according to the z-direction (necessarily, the x and y-directions are equal to 0). The spin orientation $(u,v,w)$ is defined by the SAXIS-tag in the Cartesian frame. The Magnetocrystalline Anisotropy Energy is calculated by orientating the spins in different directions and the following equation

:   :   $$E\_{\text{MAE}} = E\_{(u,v,w)} - E\_0$$

with $E\_0$ the energy of the most stable spin orientation.
More details are available in the SAXIS and LSORBIT pages.

*Exercise :* Determine the Magnetocrystalline Anisotropy Energy of NiO in a non self-consistent approach by orientating the spins along the following path : (2,2,2) --> (2,2,1) --> (2,2,0) --> ... --> (2,2,-6). Compare to the self-consistent approach.

---

* INCAR

```
NiO MAE
  SYSTEM    = "NiO"
    
Electronic minimization
  PREC = Accurate
  ENCUT         = 450
  EDIFF         = 1E-7
  LORBIT        = 11
  LREAL         = .False.
  ISYM          = -1
  NELMIN        = 6
  #  ICHARG = 11
  #  LCHARG = .FALSE.
  #  LWAVE = .FALSE.
  #  NBANDS = 52
  #  GGA_COMPAT = .FALSE.
    
DOS
  ISMEAR    = -5
    
Magnetism
  ISPIN     = 2
  MAGMOM = 2.0 -2.0 2*0.0
  # MAGMOM    = 0 0 2 0 0 -2 6*0 # Including Spin-orbit
  # LSORBIT       = .True.
  # SAXIS = 1 0 0 # Quantization axis used to rotate all spins in a direction defined in the (O,x,y,z) Cartesian frame
    
Orbital mom.
  LORBMOM = T
    
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

nio\_noSOC.tgz

---
