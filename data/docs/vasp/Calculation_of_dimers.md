# Calculation of dimers

Categories: Atoms and Molecules, Howto

Reproducing accurate dimer distances is an important difficult benchmark for a potential. If a potential works accurately for dimers and bulk calculations, one can be quite confident that the potential possesses excellent transferability. For the simulation of the dimers, one can use the $\Gamma$ point and displace the second atom along the diagonal direction. Generally bonding length and vibrational frequency have to be compared with accurate reference data. It is recommended to perform these calculations using the constant velocity molecular dynamic mode (i.e. IBRION=2, SMASS=-2). This mode speeds up the calculation because the wave functions are extrapolated and predicted using information from previous steps. The INCAR file must contain additional lines to perform the constant velocity MD:

```
#ionic relaxation
NSW = 10     #number of steps for IOM
SMASS = -2   #constant velocity MD
POTIM = 1    #time-step for ionic-motion
```

In addition to the positions the POSCAR file must also contain velocities:

```
dimer
1
     10.00000    .00000    .00000
       .00000  10.00000    .00000
       .00000    .00000  10.00000
   2
cart
 0       0       0
 1.47802 1.47802 1.47802
cart
   0       0       0
 -.02309 -.02309 -.02309
```

For this POSCAR file the starting distance is 2.56 $\AA$, in each step the distance is reduced by 0.04 $\AA$, leading to a final distance of 2.20 $\AA$. The obtained energies can be fitted to a Morse potential.

Mind: In some rare cases like C2, the calculation of the dimer turns out to be problematic. For this case the LUMO (lowest unoccupied molecular orbital) and the HOMO (highest occupied molecular orbital) cross at a certain distance, and are actually degenerate, if the total energy is used as a variational quantity (i.e. $\sigma \to 0$). Within the finite temperature LDA these difficulties are avoided, but interpreting the results is not easy because of the finite entropy (for C2 see Ref. ).

## References

---
